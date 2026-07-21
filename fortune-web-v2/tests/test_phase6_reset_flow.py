"""
taixuan-web v2.0 Phase 6 - forgot/reset password flow.
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _setup():
    fd, db_path = tempfile.mkstemp(suffix=".db", prefix="taixuan_phase6_")
    os.close(fd)
    os.unlink(db_path)
    os.environ["TAIXUAN_DB_PATH"] = db_path

    import user_system
    user_system.DB_PATH = db_path
    user_system.init_db()

    import app as app_module

    def unified_get_db():
        import sqlite3
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    app_module.get_db = unified_get_db

    def _test_get_conn():
        import sqlite3
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    user_system.get_conn = _test_get_conn

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
        CREATE TABLE IF NOT EXISTS login_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_ip TEXT NOT NULL,
            email TEXT,
            success INTEGER DEFAULT 0,
            attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()

    return user_system, app_module, db_path


user_system, app_module, db_path = _setup()


def test_request_reset_for_existing_user():
    """Forgot for existing user returns reset_url (dev mode)."""
    client = app_module.app.test_client()
    client.post("/api/v2/auth/register", json={
        "email": "reset@test.com",
        "password": "GoodPass1",
    })

    r = client.post("/api/v2/auth/forgot", json={"email": "reset@test.com"})
    assert r.status_code == 200
    data = r.get_json()
    assert data["ok"] is True
    assert "reset_url" in data
    assert "token=" in data["reset_url"]
    assert data["expires_in_sec"] == 3600
    print(f"PASS: forgot returns reset_url for existing user")


def test_request_reset_for_nonexistent_user():
    """Forgot for non-existent user returns 200 OK but NO reset_url (anti-enumeration)."""
    client = app_module.app.test_client()
    r = client.post("/api/v2/auth/forgot", json={"email": "nobody@example.com"})
    assert r.status_code == 200, r.get_json()
    data = r.get_json()
    assert data["ok"] is True
    assert "reset_url" not in data  # No URL for unknown email
    print("PASS: forgot for unknown email: 200 OK but no reset_url (anti-enumeration)")


def test_request_reset_invalid_email():
    """Forgot with invalid email returns 400."""
    client = app_module.app.test_client()
    r = client.post("/api/v2/auth/forgot", json={"email": "not-an-email"})
    assert r.status_code == 400
    print("PASS: forgot with invalid email: 400")


def test_reset_with_valid_token():
    """Reset password with valid token succeeds and old password fails."""
    client = app_module.app.test_client()
    client.post("/api/v2/auth/register", json={
        "email": "validreset@test.com",
        "password": "OldPass1",
    })

    # Get reset token
    r = client.post("/api/v2/auth/forgot", json={"email": "validreset@test.com"})
    token = r.get_json()["reset_url"].split("token=")[1]

    # Reset to new password
    r = client.post("/api/v2/auth/reset", json={
        "token": token,
        "new_password": "NewPass1",
    })
    assert r.status_code == 200, r.get_json()
    assert r.get_json()["ok"] is True

    # Old password should fail
    r = client.post("/api/v2/auth/login", json={
        "email": "validreset@test.com",
        "password": "OldPass1",
    })
    assert r.status_code == 401

    # New password should work
    r = client.post("/api/v2/auth/login", json={
        "email": "validreset@test.com",
        "password": "NewPass1",
    })
    assert r.status_code == 200, r.get_json()
    print("PASS: full reset flow: forgot -> reset -> new password works, old fails")


def test_reset_with_used_token_rejected():
    """Used token can't be reused."""
    client = app_module.app.test_client()
    client.post("/api/v2/auth/register", json={
        "email": "used@test.com",
        "password": "OldPass1",
    })
    r = client.post("/api/v2/auth/forgot", json={"email": "used@test.com"})
    token = r.get_json()["reset_url"].split("token=")[1]

    # First use: success
    r = client.post("/api/v2/auth/reset", json={"token": token, "new_password": "NewPass1"})
    assert r.status_code == 200

    # Second use: reject
    r = client.post("/api/v2/auth/reset", json={"token": token, "new_password": "Other1"})
    assert r.status_code == 400
    assert "invalid" in r.get_json()["error"].lower() or "expired" in r.get_json()["error"].lower()
    print("PASS: reset token cannot be reused")


def test_reset_with_invalid_token():
    """Invalid token returns 400."""
    client = app_module.app.test_client()
    r = client.post("/api/v2/auth/reset", json={
        "token": "totally-fake-token-12345",
        "new_password": "NewPass1",
    })
    assert r.status_code == 400
    print("PASS: reset with invalid token: 400")


def test_reset_with_weak_new_password_rejected():
    """New password must meet complexity rules."""
    client = app_module.app.test_client()
    client.post("/api/v2/auth/register", json={
        "email": "weakreset@test.com",
        "password": "OldPass1",
    })
    r = client.post("/api/v2/auth/forgot", json={"email": "weakreset@test.com"})
    token = r.get_json()["reset_url"].split("token=")[1]

    r = client.post("/api/v2/auth/reset", json={
        "token": token,
        "new_password": "weakpassword",  # only lowercase
    })
    assert r.status_code == 400
    print(f"PASS: weak new password rejected: {r.get_json()['error']}")


def test_reset_invalidates_existing_sessions():
    """After password reset, old JWT tokens are invalidated."""
    client = app_module.app.test_client()
    # Register + get token
    r = client.post("/api/v2/auth/register", json={
        "email": "session@test.com",
        "password": "OldPass1",
    })
    old_token = r.get_json()["access_token"]

    # Verify old token works
    r = client.get("/api/v2/auth/me", headers={"Authorization": f"Bearer {old_token}"})
    assert r.status_code == 200

    # Reset password
    r = client.post("/api/v2/auth/forgot", json={"email": "session@test.com"})
    token = r.get_json()["reset_url"].split("token=")[1]
    r = client.post("/api/v2/auth/reset", json={"token": token, "new_password": "NewPass1"})
    assert r.status_code == 200

    # Old token should now fail (session invalidated)
    r = client.get("/api/v2/auth/me", headers={"Authorization": f"Bearer {old_token}"})
    assert r.status_code == 401, f"Old token should be invalid, got {r.status_code}"
    print("PASS: password reset invalidates existing sessions")


if __name__ == "__main__":
    test_request_reset_for_existing_user()
    test_request_reset_for_nonexistent_user()
    test_request_reset_invalid_email()
    test_reset_with_valid_token()
    test_reset_with_used_token_rejected()
    test_reset_with_invalid_token()
    test_reset_with_weak_new_password_rejected()
    test_reset_invalidates_existing_sessions()
    print("\nAll Phase 6 forgot/reset checks passed.")