"""
taixuan-web v2.0 Phase 7 - subscription flow (mock Stripe).
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _setup():
    fd, db_path = tempfile.mkstemp(suffix=".db", prefix="taixuan_phase7_")
    os.close(fd)
    os.unlink(db_path)
    os.environ["TAIXUAN_DB_PATH"] = db_path

    import user_system
    user_system.DB_PATH = db_path
    user_system.init_db()

    import stripe_mock
    stripe_mock.STRIPE_API_KEY = ""
    stripe_mock.USE_REAL_STRIPE = False

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

    return user_system, app_module, stripe_mock, db_path


user_system, app_module, stripe_mock, db_path = _setup()


def test_list_plans_public():
    """GET /api/v2/subscribe/plans is public (no auth needed)."""
    client = app_module.app.test_client()
    r = client.get("/api/v2/subscribe/plans")
    assert r.status_code == 200
    data = r.get_json()
    plans = [p["name"] for p in data["plans"]]
    assert "free" in plans
    assert "monthly" in plans
    assert "yearly" in plans
    assert data["mode"] == "mock"
    print(f"PASS: list_plans returns {plans} (mode={data['mode']})")


def test_checkout_requires_auth():
    """POST /api/v2/subscribe/checkout requires Bearer token."""
    client = app_module.app.test_client()
    r = client.post("/api/v2/subscribe/checkout", json={"plan": "monthly"})
    assert r.status_code == 401
    print("PASS: checkout without token: 401")


def test_checkout_invalid_plan():
    """Invalid plan returns 400."""
    client = app_module.app.test_client()
    # Register + get token
    r = client.post("/api/v2/auth/register", json={"email": "sub1@x.com", "password": "GoodPass1"})
    token = r.get_json()["access_token"]

    r = client.post("/api/v2/subscribe/checkout", json={"plan": "platinum"},
                    headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 400
    assert "platinum" in r.get_json()["error"].lower() or "unknown" in r.get_json()["error"].lower()
    print("PASS: invalid plan: 400")


def test_checkout_monthly_returns_mock_url():
    """Monthly plan returns mock checkout URL."""
    client = app_module.app.test_client()
    r = client.post("/api/v2/auth/register", json={"email": "sub2@x.com", "password": "GoodPass1"})
    token = r.get_json()["access_token"]

    r = client.post("/api/v2/subscribe/checkout", json={"plan": "monthly"},
                    headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200, r.get_json()
    data = r.get_json()
    assert data["mode"] == "mock"
    assert "mock_confirm" in data["url"]
    assert data["plan"] == "monthly"
    assert data["price_cents"] == 100
    print(f"PASS: checkout monthly returns mock URL: {data['url'][:60]}...")


def test_free_plan_immediate_downgrade():
    """Choosing free plan immediately deactivates current sub."""
    client = app_module.app.test_client()
    r = client.post("/api/v2/auth/register", json={"email": "sub3@x.com", "password": "GoodPass1"})
    token = r.get_json()["access_token"]
    user_id = r.get_json()["user_id"]

    # First subscribe to monthly
    r = client.post("/api/v2/subscribe/checkout", json={"plan": "monthly"},
                    headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    # Confirm mock payment
    mock_url = r.get_json()["url"]
    session_id = mock_url.split("session_id=")[1].split("&")[0]
    r = client.get(f"/api/v2/subscribe/mock_confirm?session_id={session_id}&plan=monthly",
                   headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200

    # Verify active
    r = client.get("/api/v2/subscribe/status", headers={"Authorization": f"Bearer {token}"})
    assert r.get_json()["is_premium"] is True

    # Downgrade to free
    r = client.post("/api/v2/subscribe/checkout", json={"plan": "free"},
                    headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert r.get_json()["subscription"]["plan"] == "free"

    # Verify inactive
    r = client.get("/api/v2/subscribe/status", headers={"Authorization": f"Bearer {token}"})
    assert r.get_json()["is_premium"] is False
    print("PASS: free plan immediately downgrades")


def test_full_subscription_flow():
    """End-to-end: register -> checkout -> mock_confirm -> status -> cancel."""
    client = app_module.app.test_client()
    r = client.post("/api/v2/auth/register", json={"email": "sub4@x.com", "password": "GoodPass1"})
    token = r.get_json()["access_token"]

    # 1. Initial status: free
    r = client.get("/api/v2/subscribe/status", headers={"Authorization": f"Bearer {token}"})
    assert r.get_json()["plan"] == "free"
    assert r.get_json()["is_premium"] is False

    # 2. Checkout yearly
    r = client.post("/api/v2/subscribe/checkout", json={"plan": "yearly"},
                    headers={"Authorization": f"Bearer {token}"})
    mock_url = r.get_json()["url"]
    session_id = mock_url.split("session_id=")[1].split("&")[0]

    # 3. Mock confirm
    r = client.get(f"/api/v2/subscribe/mock_confirm?session_id={session_id}&plan=yearly",
                   headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    sub = r.get_json()["subscription"]
    assert sub["plan"] == "yearly"
    assert sub["is_active"] == 1
    assert "expires_at" in sub

    # 4. Status now shows premium
    r = client.get("/api/v2/subscribe/status", headers={"Authorization": f"Bearer {token}"})
    status = r.get_json()
    assert status["plan"] == "yearly"
    assert status["is_premium"] is True
    assert status["days_remaining"] >= 360  # ~365 days

    # 5. Cancel
    r = client.post("/api/v2/subscribe/cancel", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert r.get_json()["ok"] is True

    # 6. Status: not premium anymore
    r = client.get("/api/v2/subscribe/status", headers={"Authorization": f"Bearer {token}"})
    assert r.get_json()["is_premium"] is False
    print("PASS: full subscription flow (free -> yearly -> cancel)")


def test_cancel_without_active_sub():
    """Cancel without active subscription returns 400."""
    client = app_module.app.test_client()
    r = client.post("/api/v2/auth/register", json={"email": "nocancel@x.com", "password": "GoodPass1"})
    token = r.get_json()["access_token"]

    r = client.post("/api/v2/subscribe/cancel", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 400
    assert "no active" in r.get_json()["error"].lower()
    print("PASS: cancel without active sub: 400")


def test_mock_confirm_in_real_mode():
    """mock_confirm endpoint rejects in real Stripe mode."""
    import importlib
    # Reimport stripe_mock with fake key
    stripe_mock.STRIPE_API_KEY = "sk_test_fake"
    stripe_mock.USE_REAL_STRIPE = True

    client = app_module.app.test_client()
    r = client.post("/api/v2/auth/register", json={"email": "real@x.com", "password": "GoodPass1"})
    token = r.get_json()["access_token"]

    r = client.get("/api/v2/subscribe/mock_confirm?session_id=xxx&plan=monthly",
                   headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 400
    assert "mock_disabled" in r.get_json()["error"]

    # Reset
    stripe_mock.STRIPE_API_KEY = ""
    stripe_mock.USE_REAL_STRIPE = False
    print("PASS: mock_confirm disabled in real Stripe mode")


if __name__ == "__main__":
    test_list_plans_public()
    test_checkout_requires_auth()
    test_checkout_invalid_plan()
    test_checkout_monthly_returns_mock_url()
    test_free_plan_immediate_downgrade()
    test_full_subscription_flow()
    test_cancel_without_active_sub()
    test_mock_confirm_in_real_mode()
    print("\nAll Phase 7 subscription checks passed.")