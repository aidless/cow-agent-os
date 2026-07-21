#!/bin/bash
# taixuan-web v2.0 dependencies installer (ECS)
# Run on ECS: bash install_v20_deps.sh
#
# v2.0 only adds:
#   - bcrypt (password hashing)
#   - PyJWT (kept OPTIONAL - we use minimal HS256 implementation, no external dep)
#
# We deliberately do NOT add PyJWT to keep zero external auth deps.
# bcrypt is the only new dep.

set -e

echo "==== taixuan-web v2.0 deps install ===="

# Check Python and pip
PYTHON=$(which python3 || which python)
if [ -z "$PYTHON" ]; then
    echo "ERROR: python not found in PATH"
    exit 1
fi

echo "Python: $($PYTHON --version)"
echo "pip:    $($PYTHON -m pip --version)"

# Install bcrypt
echo ""
echo "[1/2] Installing bcrypt..."
$PYTHON -m pip install --upgrade bcrypt 2>&1 | tail -5

# Verify
echo ""
echo "[2/2] Verifying imports..."
$PYTHON -c "
import user_system
ok = user_system.BCRYPT_AVAILABLE
print('bcrypt available:', ok)
print('DB path:        ', user_system.DB_PATH)
print('JWT TTL (sec):  ', user_system.JWT_TTL_SEC)
print('JWT secret len: ', len(user_system.JWT_SECRET))
"

echo ""
echo "==== Done ===="
echo ""
echo "Notes:"
echo "  - bcrypt is the ONLY new runtime dep"
echo "  - JWT is self-implemented (HS256 + HMAC-SHA256, no PyJWT)"
echo "  - v20_schema.sql runs at app startup via user_system.init_db()"
echo ""
echo "Next steps:"
echo "  1. Add to app.py:"
echo "       import user_system"
echo "       from auth_routes import auth_bp"
echo "       from favorites_routes import favorites_bp"
echo "       user_system.init_db()"
echo "       app.register_blueprint(auth_bp, url_prefix='/api/v2/auth')"
echo "       app.register_blueprint(favorites_bp, url_prefix='/api/v2/favorites')"
echo "  2. Add TAIXUAN_JWT_SECRET to /etc/taixuan.env (32+ random bytes)"
echo "  3. Update requirements.txt: bcrypt>=4.1"
echo "  4. Restart supervisor: supervisorctl restart taixuan"
echo "  5. Verify: curl -s http://127.0.0.1:80/api/v2/auth/me -H 'Authorization: Bearer x'"
echo "     (should return 401 invalid_or_expired_token)"