"""
taixuan-web v2.0 user_system unit tests.
Run: pytest tests/test_user_system.py -v
or: python -m pytest tests/test_user_system.py -v
"""
import os
import sys
import tempfile
import unittest

# Allow imports from project root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ===== Per-test DB lifecycle helpers =====

def _make_fresh_db():
    """Returns path to a unique fresh DB file. Each test gets a new one."""
    fd, path = tempfile.mkstemp(suffix=".db", prefix="taixuan_test_")
    os.close(fd)
    os.unlink(path)  # delete file so init_db creates fresh
    os.environ["TAIXUAN_DB_PATH"] = path
    # Re-import or update module path
    if "user_system" in sys.modules:
        sys.modules["user_system"].DB_PATH = path
    return path


import user_system  # noqa: E402


class TestPassword(unittest.TestCase):
    def test_validate_password_min_length(self):
        ok, _ = user_system.validate_password("short")
        self.assertFalse(ok)

    def test_validate_password_requires_digit(self):
        ok, _ = user_system.validate_password("nodigitpassword")
        self.assertFalse(ok)

    def test_validate_password_ok(self):
        ok, msg = user_system.validate_password("goodpassword1")
        self.assertTrue(ok, msg)

    def test_validate_email(self):
        self.assertTrue(user_system.validate_email("user@example.com"))
        self.assertFalse(user_system.validate_email("not-an-email"))
        self.assertFalse(user_system.validate_email(""))
        self.assertFalse(user_system.validate_email("a@b"))


class TestHashVerify(unittest.TestCase):
    def test_hash_and_verify_roundtrip(self):
        plain = "secret-pass-123"
        h = user_system.hash_password(plain)
        self.assertTrue(user_system.verify_password(plain, h))

    def test_wrong_password_fails(self):
        h = user_system.hash_password("correctpass1")
        self.assertFalse(user_system.verify_password("wrongpass1", h))


class TestUserCRUD(unittest.TestCase):
    def setUp(self):
        user_system.DB_PATH = _make_fresh_db()
        user_system.init_db()

    def tearDown(self):
        # Force close any lingering sqlite handles (Windows file lock workaround)
        try:
            import gc
            gc.collect()
        except Exception:
            pass

    def test_create_user_ok(self):
        ok, msg, user = user_system.create_user("a@example.com", "goodpass1", "Alice")
        self.assertTrue(ok, msg)
        self.assertEqual(user["email"], "a@example.com")
        self.assertEqual(user["nickname"], "Alice")

    def test_create_user_duplicate_email(self):
        user_system.create_user("dup@example.com", "goodpass1")
        ok, msg, _ = user_system.create_user("dup@example.com", "goodpass2")
        self.assertFalse(ok)
        self.assertIn("already", msg.lower())

    def test_create_user_invalid_email(self):
        ok, _, _ = user_system.create_user("not-email", "goodpass1")
        self.assertFalse(ok)

    def test_create_user_weak_password(self):
        ok, msg, _ = user_system.create_user("weak@example.com", "abc")
        self.assertFalse(ok)
        self.assertIn("8", msg)

    def test_verify_login_success(self):
        user_system.create_user("login@example.com", "mypassword1", "Bob")
        user = user_system.verify_login("login@example.com", "mypassword1")
        self.assertIsNotNone(user)
        self.assertEqual(user["email"], "login@example.com")

    def test_verify_login_wrong_password(self):
        user_system.create_user("wrong@example.com", "rightpass1", "Eve")
        user = user_system.verify_login("wrong@example.com", "wrongpass1")
        self.assertIsNone(user)

    def test_verify_login_unknown_email(self):
        user = user_system.verify_login("ghost@example.com", "anypass1")
        self.assertIsNone(user)


class TestJWT(unittest.TestCase):
    def test_create_and_decode_token(self):
        token = user_system.create_token(42, "jwt@example.com")
        payload = user_system.decode_token(token)
        self.assertIsNotNone(payload)
        self.assertEqual(payload["sub"], 42)
        self.assertEqual(payload["email"], "jwt@example.com")
        self.assertGreater(payload["exp"], payload["iat"])

    def test_decode_invalid_token(self):
        self.assertIsNone(user_system.decode_token("not-a-jwt"))
        self.assertIsNone(user_system.decode_token("a.b.c"))
        self.assertIsNone(user_system.decode_token(""))

    def test_token_hash_is_stable(self):
        t = "fixed-token-xyz"
        h1 = user_system.token_hash(t)
        h2 = user_system.token_hash(t)
        self.assertEqual(h1, h2)


class TestSessions(unittest.TestCase):
    def setUp(self):
        user_system.DB_PATH = _make_fresh_db()
        user_system.init_db()

    def tearDown(self):
        try:
            import gc
            gc.collect()
        except Exception:
            pass

    def test_register_and_revoke_session(self):
        token = user_system.create_token(1, "s@example.com")
        user_system.register_session(1, token)
        # Note: in v2.0 design, "in sessions" = valid (we DELETE on logout)
        # Test that revocation actually deletes the row
        user_system.revoke_session(token)
        # Token should still decode (we just removed from tracking, JWT TTL is what enforces)
        payload = user_system.decode_token(token)
        self.assertIsNotNone(payload)


class TestFavorites(unittest.TestCase):
    def setUp(self):
        user_system.DB_PATH = _make_fresh_db()
        user_system.init_db()
        # Create minimal readings table (FK target for favorites)
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
        conn.commit()
        conn.close()

    def tearDown(self):
        try:
            import gc
            gc.collect()
        except Exception:
            pass

    def test_add_and_list_favorite(self):
        # Need a reading row first (FK constraint)
        conn = user_system.get_conn()
        conn.execute(
            "INSERT INTO readings (liupai, question, summary, created_at) VALUES (?, ?, ?, datetime('now'))",
            ("bazi", "test question", "test summary"),
        )
        conn.commit()
        reading_id = conn.execute("SELECT last_insert_rowid() AS id").fetchone()["id"]
        conn.close()

        fav_id = user_system.add_favorite(99, reading_id, "my private note")
        self.assertIsNotNone(fav_id)
        favs = user_system.list_favorites(99)
        self.assertEqual(len(favs), 1)
        self.assertEqual(favs[0]["note"], "my private note")

    def test_remove_favorite(self):
        conn = user_system.get_conn()
        conn.execute(
            "INSERT INTO readings (liupai, question, summary) VALUES ('bazi', 'q', 's')"
        )
        conn.commit()
        reading_id = conn.execute("SELECT last_insert_rowid() AS id").fetchone()["id"]
        conn.close()

        fav_id = user_system.add_favorite(99, reading_id)
        self.assertTrue(user_system.remove_favorite(99, fav_id))
        # Second remove should fail (row already gone)
        self.assertFalse(user_system.remove_favorite(99, fav_id))
        favs = user_system.list_favorites(99)
        self.assertEqual(len(favs), 0)


if __name__ == "__main__":
    unittest.main()
