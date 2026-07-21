"""
taixuan-web v2.0 auth_routes + favorites_routes integration tests.
Uses Flask test_client, no live server required.

Run: pytest tests/test_auth_favorites_routes.py -v
"""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _make_fresh_db():
    fd, path = tempfile.mkstemp(suffix=".db", prefix="taixuan_test_routes_")
    os.close(fd)
    os.unlink(path)
    os.environ["TAIXUAN_DB_PATH"] = path
    if "user_system" in sys.modules:
        sys.modules["user_system"].DB_PATH = path
    return path


import user_system  # noqa: E402
from auth_routes import auth_bp  # noqa: E402
from favorites_routes import favorites_bp  # noqa: E402


def _build_app():
    """Create minimal Flask app with auth + favorites blueprints."""
    from flask import Flask
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.register_blueprint(auth_bp, url_prefix="/api/v2/auth")
    app.register_blueprint(favorites_bp, url_prefix="/api/v2/favorites")
    return app


class _BaseRouteTest(unittest.TestCase):
    def setUp(self):
        self.db_path = _make_fresh_db()
        user_system.init_db()
        # readings table for favorites FK
        conn = user_system.get_conn()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                liupai TEXT NOT NULL,
                question TEXT,
                summary TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Seed one reading for favorite tests
        conn.execute(
            "INSERT INTO readings (liupai, question, summary) VALUES ('bazi', 'seed q', 'seed s')"
        )
        conn.commit()
        conn.close()
        self.app = _build_app()
        self.client = self.app.test_client()

    def tearDown(self):
        try:
            import gc
            gc.collect()
        except Exception:
            pass


class TestRegister(_BaseRouteTest):
    def test_register_ok(self):
        resp = self.client.post("/api/v2/auth/register", json={
            "email": "alice@example.com",
            "password": "goodpass1",
            "nickname": "Alice",
        })
        self.assertEqual(resp.status_code, 200, resp.get_json())
        data = resp.get_json()
        self.assertIn("access_token", data)
        self.assertEqual(data["email"], "alice@example.com")
        self.assertEqual(data["nickname"], "Alice")

    def test_register_weak_password(self):
        resp = self.client.post("/api/v2/auth/register", json={
            "email": "weak@example.com",
            "password": "abc",
        })
        self.assertEqual(resp.status_code, 400)
        self.assertIn("error", resp.get_json())

    def test_register_invalid_email(self):
        resp = self.client.post("/api/v2/auth/register", json={
            "email": "not-email",
            "password": "goodpass1",
        })
        self.assertEqual(resp.status_code, 400)

    def test_register_duplicate(self):
        self.client.post("/api/v2/auth/register", json={
            "email": "dup@example.com",
            "password": "goodpass1",
        })
        resp = self.client.post("/api/v2/auth/register", json={
            "email": "dup@example.com",
            "password": "goodpass2",
        })
        self.assertEqual(resp.status_code, 400)
        self.assertIn("already", resp.get_json()["error"].lower())


class TestLogin(_BaseRouteTest):
    def setUp(self):
        super().setUp()
        # Pre-register a user
        self.client.post("/api/v2/auth/register", json={
            "email": "login@example.com",
            "password": "mypassword1",
            "nickname": "LoginUser",
        })

    def test_login_ok(self):
        resp = self.client.post("/api/v2/auth/login", json={
            "email": "login@example.com",
            "password": "mypassword1",
        })
        self.assertEqual(resp.status_code, 200, resp.get_json())
        self.assertIn("access_token", resp.get_json())

    def test_login_wrong_password(self):
        resp = self.client.post("/api/v2/auth/login", json={
            "email": "login@example.com",
            "password": "wrongpass1",
        })
        self.assertEqual(resp.status_code, 401)

    def test_login_unknown_email(self):
        resp = self.client.post("/api/v2/auth/login", json={
            "email": "ghost@example.com",
            "password": "anypass1",
        })
        self.assertEqual(resp.status_code, 401)


class TestMe(_BaseRouteTest):
    def _register_and_get_token(self):
        resp = self.client.post("/api/v2/auth/register", json={
            "email": "me@example.com",
            "password": "mypassword1",
            "nickname": "MeUser",
        })
        return resp.get_json()["access_token"]

    def test_me_ok(self):
        token = self._register_and_get_token()
        resp = self.client.get("/api/v2/auth/me", headers={
            "Authorization": f"Bearer {token}",
        })
        self.assertEqual(resp.status_code, 200, resp.get_json())
        data = resp.get_json()
        self.assertEqual(data["email"], "me@example.com")
        self.assertEqual(data["nickname"], "MeUser")

    def test_me_missing_token(self):
        resp = self.client.get("/api/v2/auth/me")
        self.assertEqual(resp.status_code, 401)

    def test_me_invalid_token(self):
        resp = self.client.get("/api/v2/auth/me", headers={
            "Authorization": "Bearer not-a-jwt",
        })
        self.assertEqual(resp.status_code, 401)


class TestFavorites(_BaseRouteTest):
    def _register_and_get_token(self):
        resp = self.client.post("/api/v2/auth/register", json={
            "email": "fav@example.com",
            "password": "mypassword1",
        })
        return resp.get_json()["access_token"]

    def test_add_favorite_ok(self):
        token = self._register_and_get_token()
        # reading_id=1 from seed
        resp = self.client.post("/api/v2/favorites", json={
            "reading_id": 1,
            "note": "good reading",
        }, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(resp.status_code, 200, resp.get_json())
        self.assertIn("favorite_id", resp.get_json())

    def test_add_favorite_no_token(self):
        resp = self.client.post("/api/v2/favorites", json={"reading_id": 1})
        self.assertEqual(resp.status_code, 401)

    def test_add_favorite_invalid_reading_id(self):
        token = self._register_and_get_token()
        resp = self.client.post("/api/v2/favorites", json={"reading_id": -1}, headers={
            "Authorization": f"Bearer {token}",
        })
        self.assertEqual(resp.status_code, 400)

    def test_list_favorites_ok(self):
        token = self._register_and_get_token()
        self.client.post("/api/v2/favorites", json={"reading_id": 1, "note": "n1"}, headers={
            "Authorization": f"Bearer {token}",
        })
        resp = self.client.get("/api/v2/favorites", headers={
            "Authorization": f"Bearer {token}",
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["items"][0]["note"], "n1")

    def test_remove_favorite_ok(self):
        token = self._register_and_get_token()
        add_resp = self.client.post("/api/v2/favorites", json={"reading_id": 1}, headers={
            "Authorization": f"Bearer {token}",
        })
        fav_id = add_resp.get_json()["favorite_id"]
        resp = self.client.delete(f"/api/v2/favorites/{fav_id}", headers={
            "Authorization": f"Bearer {token}",
        })
        self.assertEqual(resp.status_code, 200)
        # Second delete should 404
        resp2 = self.client.delete(f"/api/v2/favorites/{fav_id}", headers={
            "Authorization": f"Bearer {token}",
        })
        self.assertEqual(resp2.status_code, 404)


class TestLogout(_BaseRouteTest):
    def test_logout_ok(self):
        # Register
        reg = self.client.post("/api/v2/auth/register", json={
            "email": "logout@example.com",
            "password": "mypassword1",
        })
        token = reg.get_json()["access_token"]
        # Logout
        resp = self.client.post("/api/v2/auth/logout", headers={
            "Authorization": f"Bearer {token}",
        })
        self.assertEqual(resp.status_code, 200)


if __name__ == "__main__":
    unittest.main()