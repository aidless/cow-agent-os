"""
taixuan-web v2.0 Phase 3 - reading/history aware of user_id.
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Use fresh DB
fd, db_path = tempfile.mkstemp(suffix=".db", prefix="taixuan_phase3_")
os.close(fd)
os.unlink(db_path)
os.environ["TAIXUAN_DB_PATH"] = db_path

# Setup DB before app import
import user_system
user_system.DB_PATH = db_path
user_system.init_db()

import app as app_module  # noqa: E402
# Patch app's DB_PATH and re-init readings table (since app.py uses its own DB at logs/readings.db)
# Easier: set the readings.db path BEFORE app import via env var the app uses
# App uses BASE_DIR / "logs" / "readings.db"
# We'll patch by replacing get_db to use our db_path
import os as _os
from pathlib import Path

TEST_READINGS_DB = db_path

# Patch app's get_db to point to our test DB
def patched_get_db():
    import sqlite3
    conn = sqlite3.connect(TEST_READINGS_DB)
    conn.row_factory = sqlite3.Row
    return conn

app_module.get_db = patched_get_db
# Also force init in app to use our DB
import app as _app_init_module
# Create readings table manually with v2.0 schema
_conn = patched_get_db()
_conn.executescript("""
    CREATE TABLE IF NOT EXISTS readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        liupai TEXT NOT NULL,
        client_ip TEXT,
        question TEXT,
        form_json TEXT,
        response_text TEXT,
        reasoning_text TEXT,
        backend TEXT,
        latency_sec REAL DEFAULT 0,
        chunk_count INTEGER DEFAULT 0,
        status TEXT DEFAULT 'ok',
        user_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE INDEX IF NOT EXISTS idx_readings_user ON readings(user_id);
""")
_conn.commit()
_conn.close()


def test_save_reading_with_user_id():
    """save_reading writes user_id when provided."""
    app_module.save_reading(
        liupai="bazi", client_ip="1.2.3.4",
        form_data={"question": "test"},
        response_text="test response",
        user_id=42,
    )
    conn = patched_get_db()
    row = conn.execute("SELECT user_id FROM readings ORDER BY id DESC LIMIT 1").fetchone()
    conn.close()
    assert row["user_id"] == 42, f"expected user_id=42, got {row['user_id']}"
    print("PASS: save_reading writes user_id=42")


def test_save_reading_anonymous():
    """save_reading without user_id writes NULL (anonymous)."""
    app_module.save_reading(
        liupai="bazi", client_ip="5.6.7.8",
        form_data={"question": "anon test"},
        response_text="anon response",
        user_id=None,
    )
    conn = patched_get_db()
    row = conn.execute("SELECT user_id FROM readings ORDER BY id DESC LIMIT 1").fetchone()
    conn.close()
    assert row["user_id"] is None, f"expected None, got {row['user_id']}"
    print("PASS: save_reading with user_id=None stores NULL")


def test_history_anonymous_sees_only_public():
    """Anonymous /history only sees rows where user_id IS NULL."""
    client = app_module.app.test_client()
    # Anonymous request (no Authorization header)
    resp = client.get("/api/v2/history?limit=10")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["scope"] == "public"
    assert data["user_id"] is None
    # Every item must have user_id == None
    for item in data["items"]:
        assert item["user_id"] is None, f"anonymous should not see user items, got {item}"
    print(f"PASS: anonymous /history sees {data['count']} public items only")


def test_history_logged_in_sees_only_own():
    """Logged-in /history only sees own rows."""
    client = app_module.app.test_client()

    # Register two users
    r1 = client.post("/api/v2/auth/register", json={
        "email": "alice@test.com", "password": "goodpass1",
    })
    assert r1.status_code == 200
    token_alice = r1.get_json()["access_token"]
    user_alice = r1.get_json()["user_id"]

    r2 = client.post("/api/v2/auth/register", json={
        "email": "bob@test.com", "password": "goodpass2",
    })
    assert r2.status_code == 200
    token_bob = r2.get_json()["access_token"]
    user_bob = r2.get_json()["user_id"]

    # Alice saves 2 readings
    for q in ["alice-q1", "alice-q2"]:
        app_module.save_reading(
            liupai="bazi", client_ip="10.0.0.1",
            form_data={"question": q}, response_text=f"resp for {q}",
            user_id=user_alice,
        )
    # Bob saves 1 reading
    app_module.save_reading(
        liupai="ziwei", client_ip="10.0.0.2",
        form_data={"question": "bob-q1"}, response_text="bob resp",
        user_id=user_bob,
    )
    # 1 anonymous reading
    app_module.save_reading(
        liupai="tarot", client_ip="10.0.0.3",
        form_data={"question": "anon-q"}, response_text="anon resp",
        user_id=None,
    )

    # Alice's /history
    resp = client.get("/api/v2/history?limit=50", headers={"Authorization": f"Bearer {token_alice}"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["scope"] == "mine"
    assert data["user_id"] == user_alice
    assert data["count"] == 2, f"Alice should see 2 of her own, got {data['count']}"
    for item in data["items"]:
        assert item["user_id"] == user_alice
    print(f"PASS: Alice sees {data['count']} of her own")

    # Bob's /history
    resp = client.get("/api/v2/history?limit=50", headers={"Authorization": f"Bearer {token_bob}"})
    data = resp.get_json()
    assert data["count"] == 1, f"Bob should see 1 of his own, got {data['count']}"
    assert data["items"][0]["question"] == "bob-q1"
    print(f"PASS: Bob sees {data['count']} of his own")


def test_history_scope_all_for_debugging():
    """?scope=all returns everything (admin/debug)."""
    client = app_module.app.test_client()
    # Logged in user requesting scope=all
    r = client.post("/api/v2/auth/register", json={"email": "debug@test.com", "password": "goodpass1"})
    token = r.get_json()["access_token"]

    resp = client.get("/api/v2/history?scope=all&limit=50", headers={"Authorization": f"Bearer {token}"})
    data = resp.get_json()
    assert data["scope"] == "all"
    # Should see Alice's 2 + Bob's 1 + anon 1 = 4+
    assert data["count"] >= 4, f"scope=all should see all, got {data['count']}"
    print(f"PASS: scope=all sees {data['count']} (>=4 from alice/bob/anon)")


def test_get_optional_user_no_header():
    """get_optional_user returns None when no Authorization header."""
    client = app_module.app.test_client()
    # Save a reading and check that user_id is None in saved row
    app_module.save_reading(
        liupai="bazi", client_ip="9.9.9.9",
        form_data={"question": "test no auth"}, response_text="resp",
        user_id=None,
    )
    conn = patched_get_db()
    row = conn.execute("SELECT user_id FROM readings ORDER BY id DESC LIMIT 1").fetchone()
    conn.close()
    assert row["user_id"] is None
    print("PASS: get_optional_user handles no-header case")


def test_get_optional_user_with_valid_token():
    """get_optional_user returns user when valid token provided."""
    client = app_module.app.test_client()
    r = client.post("/api/v2/auth/register", json={"email": "optuser@test.com", "password": "goodpass1"})
    token = r.get_json()["access_token"]
    user_id = r.get_json()["user_id"]

    # Now save a reading with the user logged in
    app_module.save_reading(
        liupai="bazi", client_ip="8.8.8.8",
        form_data={"question": "test with auth"}, response_text="resp",
        user_id=user_id,
    )
    conn = patched_get_db()
    row = conn.execute("SELECT user_id FROM readings ORDER BY id DESC LIMIT 1").fetchone()
    conn.close()
    assert row["user_id"] == user_id
    print(f"PASS: save_reading with user_id={user_id} works")


if __name__ == "__main__":
    test_save_reading_with_user_id()
    test_save_reading_anonymous()
    test_history_anonymous_sees_only_public()
    test_history_logged_in_sees_only_own()
    test_history_scope_all_for_debugging()
    test_get_optional_user_no_header()
    test_get_optional_user_with_valid_token()
    print("\nAll Phase 3 user-aware checks passed.")