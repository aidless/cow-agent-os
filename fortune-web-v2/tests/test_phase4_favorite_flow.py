"""
taixuan-web v2.0 Phase 4 - reading returns reading_id, can be favorited.

Key design: ALL THREE (users, favorites, readings) live in ONE DB.
This matches production where everything is in /var/www/taixuan/data.db.
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _setup_unified_db():
    """Create one DB file used by both user_system AND app.get_db."""
    fd, db_path = tempfile.mkstemp(suffix=".db", prefix="taixuan_phase4_")
    os.close(fd)
    os.unlink(db_path)
    os.environ["TAIXUAN_DB_PATH"] = db_path

    # Now import (env var is set, user_system.DB_PATH will pick it up)
    import user_system
    user_system.DB_PATH = db_path
    user_system.init_db()

    import app as app_module

    # Make app.get_db() return connections to the SAME unified DB
    def unified_get_db():
        import sqlite3
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    app_module.get_db = unified_get_db

    # Create readings table (so save_reading works)
    conn = unified_get_db()
    conn.executescript("""
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
    conn.commit()
    conn.close()

    return user_system, app_module, db_path


# Setup once at module load
user_system, app_module, db_path = _setup_unified_db()


def test_save_reading_returns_id():
    """save_reading returns int lastrowid on success."""
    rid = app_module.save_reading(
        liupai="bazi", client_ip="1.1.1.1",
        form_data={"question": "test"}, response_text="resp",
    )
    assert isinstance(rid, int), f"save_reading should return int, got {type(rid)}"
    assert rid > 0
    print(f"PASS: save_reading returns int lastrowid (got {rid})")


def test_favorite_button_flow():
    """End-to-end: register -> save reading -> POST /favorites -> verify DB."""
    client = app_module.app.test_client()

    r = client.post("/api/v2/auth/register", json={
        "email": "fav@test.com", "password": "goodpass1",
    })
    assert r.status_code == 200
    token = r.get_json()["access_token"]
    user_id = r.get_json()["user_id"]

    # Save a reading (user_id bound)
    reading_id = app_module.save_reading(
        liupai="bazi", client_ip="3.3.3.3",
        form_data={"question": "test fav"}, response_text="resp fav",
        user_id=user_id,
    )
    assert reading_id > 0
    print(f"PASS: saved reading_id={reading_id} for user_id={user_id}")

    # POST /favorites
    r = client.post("/api/v2/favorites", json={
        "reading_id": reading_id, "note": "test note",
    }, headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200, r.get_json()
    fav_id = r.get_json()["favorite_id"]
    assert fav_id > 0
    print(f"PASS: POST /favorites -> favorite_id={fav_id}")

    # Verify in DB
    import sqlite3
    conn_check = sqlite3.connect(db_path)
    row = conn_check.execute(
        "SELECT user_id, reading_id, note FROM favorites WHERE id = ?", (fav_id,)
    ).fetchone()
    conn_check.close()
    assert row[0] == user_id
    assert row[1] == reading_id
    assert row[2] == "test note"
    print(f"PASS: favorite row verified in DB (user={row[0]}, reading={row[1]})")


def test_favorite_without_token_rejected():
    """Anonymous POST /favorites returns 401."""
    client = app_module.app.test_client()
    reading_id = app_module.save_reading(
        liupai="bazi", client_ip="4.4.4.4",
        form_data={"question": "anon fav"}, response_text="resp",
    )
    r = client.post("/api/v2/favorites", json={"reading_id": reading_id})
    assert r.status_code == 401, r.get_json()
    print("PASS: anonymous POST /favorites returns 401")


def test_favorite_duplicate_rejected():
    """Same reading can't be favorited twice by same user."""
    client = app_module.app.test_client()
    r = client.post("/api/v2/auth/register", json={"email": "dup@test.com", "password": "goodpass1"})
    token = r.get_json()["access_token"]

    reading_id = app_module.save_reading(
        liupai="bazi", client_ip="5.5.5.5",
        form_data={"question": "dup fav"}, response_text="resp",
    )

    r1 = client.post("/api/v2/favorites", json={"reading_id": reading_id},
                     headers={"Authorization": f"Bearer {token}"})
    assert r1.status_code == 200

    r2 = client.post("/api/v2/favorites", json={"reading_id": reading_id},
                     headers={"Authorization": f"Bearer {token}"})
    assert r2.status_code == 400
    print("PASS: duplicate favorite returns 400")


def test_list_favorites_includes_reading_meta():
    """GET /favorites returns reading metadata (JOIN readings in same DB)."""
    client = app_module.app.test_client()
    r = client.post("/api/v2/auth/register", json={"email": "meta@test.com", "password": "goodpass1"})
    token = r.get_json()["access_token"]

    # Save a reading then favorite (now both in same DB)
    reading_id = app_module.save_reading(
        liupai="bazi", client_ip="6.6.6.6",
        form_data={"question": "meta test"}, response_text="resp",
    )
    r = client.post("/api/v2/favorites", json={"reading_id": reading_id, "note": "my note"},
                headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200

    # GET /favorites (JOIN reads from same unified DB)
    r = client.get("/api/v2/favorites", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    data = r.get_json()
    assert data["count"] == 1, f"expected 1 favorite, got {data}"
    item = data["items"][0]
    assert item["reading_id"] == reading_id
    assert item["liupai"] == "bazi"
    assert item["question"] == "meta test"
    assert item["note"] == "my note"
    print(f"PASS: GET /favorites returns item with reading meta (liupai={item['liupai']}, question={item['question']})")


def test_remove_favorite_flow():
    """DELETE /favorites/<id> removes favorite."""
    client = app_module.app.test_client()
    r = client.post("/api/v2/auth/register", json={"email": "del@test.com", "password": "goodpass1"})
    token = r.get_json()["access_token"]

    reading_id = app_module.save_reading(
        liupai="ziwei", client_ip="7.7.7.7",
        form_data={"question": "del test"}, response_text="resp",
    )
    fav_resp = client.post("/api/v2/favorites", json={"reading_id": reading_id},
                headers={"Authorization": f"Bearer {token}"})
    fav_id = fav_resp.get_json()["favorite_id"]

    # DELETE
    r = client.delete(f"/api/v2/favorites/{fav_id}",
                      headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200

    # Verify gone
    r = client.get("/api/v2/favorites", headers={"Authorization": f"Bearer {token}"})
    assert r.get_json()["count"] == 0
    print("PASS: DELETE favorite flow works")


if __name__ == "__main__":
    test_save_reading_returns_id()
    test_favorite_button_flow()
    test_favorite_without_token_rejected()
    test_favorite_duplicate_rejected()
    test_list_favorites_includes_reading_meta()
    test_remove_favorite_flow()
    print("\nAll Phase 4 favorite flow checks passed.")