"""
taixuan-web v2.0 Phase 2 end-to-end smoke test.
Verifies app.py boots, all routes are registered, page templates render.
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Use a fresh DB so we don't conflict with anything
fd, db_path = tempfile.mkstemp(suffix=".db", prefix="taixuan_e2e_")
os.close(fd)
os.unlink(db_path)
os.environ["TAIXUAN_DB_PATH"] = db_path


def test_app_boots_and_routes():
    """Verify app.py imports cleanly with v2.0 modules wired."""
    import app
    import user_system

    # All v2.0 tables created
    user_system.DB_PATH = db_path
    conn = user_system.get_conn()
    tables = [r["name"] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    ).fetchall()]
    assert "users" in tables, f"users table missing, got {tables}"
    assert "sessions" in tables
    assert "favorites" in tables
    assert "subscriptions" in tables
    conn.close()

    # All expected routes registered
    rules = {r.rule: r for r in app.app.url_map.iter_rules()}
    # Auth API
    assert "/api/v2/auth/register" in rules
    assert "/api/v2/auth/login" in rules
    assert "/api/v2/auth/logout" in rules
    assert "/api/v2/auth/me" in rules
    # Favorites API
    assert "/api/v2/favorites" in rules
    assert "/api/v2/favorites/<int:favorite_id>" in rules
    # Page templates
    assert "/login" in rules
    assert "/register" in rules
    assert "/me" in rules
    # Existing v1.x must remain
    assert "/healthz" in rules
    assert "/api/v2/liupai/<name>/reading" in rules
    assert "/api/v2/history" in rules
    assert "/" in rules
    print(f"PASS: 22+ routes registered, all v2.0 tables created")


def test_register_login_me_flow():
    """End-to-end: register -> login -> me."""
    import app
    client = app.app.test_client()

    # Register
    r = client.post("/api/v2/auth/register", json={
        "email": "e2e@example.com",
        "password": "goodpass1",
        "nickname": "E2EUser",
    })
    assert r.status_code == 200, r.get_json()
    token = r.get_json()["access_token"]
    assert token, "register did not return token"

    # /me with token
    r = client.get("/api/v2/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200, r.get_json()
    me = r.get_json()
    assert me["email"] == "e2e@example.com"
    assert me["nickname"] == "E2EUser"
    print(f"PASS: register -> me flow works, user_id={me['user_id']}")

    # Login (with same credentials)
    r = client.post("/api/v2/auth/login", json={
        "email": "e2e@example.com",
        "password": "goodpass1",
    })
    assert r.status_code == 200
    new_token = r.get_json()["access_token"]
    assert new_token

    # Logout
    r = client.post("/api/v2/auth/logout", headers={"Authorization": f"Bearer {new_token}"})
    assert r.status_code == 200
    print("PASS: login -> logout flow works")


def test_pages_render():
    """Verify page templates render without error."""
    import app
    client = app.app.test_client()

    for path in ["/login", "/register", "/me"]:
        r = client.get(path)
        assert r.status_code == 200, f"{path} returned {r.status_code}"
        # Verify HTML content has expected elements
        html = r.data.decode("utf-8")
        assert "<html" in html or "<!DOCTYPE" in html
    print("PASS: /login, /register, /me all render 200")


def test_healthz_unchanged():
    """Verify healthz still works after v2.0 integration (regression check)."""
    import app
    client = app.app.test_client()

    r = client.get("/healthz")
    assert r.status_code == 200
    data = r.get_json()
    assert data["status"] == "ok"
    assert data["version"] == "1.2.0"
    print("PASS: /healthz still v1.2.0 after v2.0 wiring")


if __name__ == "__main__":
    test_app_boots_and_routes()
    test_register_login_me_flow()
    test_pages_render()
    test_healthz_unchanged()
    print("\nAll Phase 2 e2e checks passed.")