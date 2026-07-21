"""
gen_alipay_keys.py — generate RSA 2048 key pair for Alipay sandbox.

Usage:
    python tools/gen_alipay_keys.py

Output:
    - app_private_key.pem  (RSA PRIVATE KEY, your secret)
    - app_public_key.pem   (PUBLIC KEY, paste into Alipay sandbox dashboard)
    - prints both to stdout with markers for easy copy

Security:
    - app_private_key.pem must NEVER be committed to git
    - Already in .gitignore via *.pem pattern (verify before commit)
"""
import os
from pathlib import Path

try:
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.primitives import serialization
except ImportError:
    print("[ERROR] cryptography package not installed.")
    print("Install: pip install cryptography")
    raise SystemExit(1)

ROOT = Path(__file__).resolve().parent.parent
PRIV_PATH = ROOT / "app_private_key.pem"
PUB_PATH = ROOT / "app_public_key.pem"

print(f"[INFO] Generating RSA 2048 key pair in: {ROOT}")

# Generate private key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

# Serialize private key (PEM, no encryption)
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption(),
)

# Serialize public key
public_key = private_key.public_key()
public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo,
)

# Write to disk
PRIV_PATH.write_bytes(private_pem)
PUB_PATH.write_bytes(public_pem)

# Verify .gitignore
gitignore = ROOT / ".gitignore"
if gitignore.exists():
    content = gitignore.read_text(encoding="utf-8")
    if "*.pem" not in content and "app_*_key.pem" not in content:
        print("[WARN] .gitignore does NOT exclude .pem files")
        print("[WARN] Run: echo '*.pem' >> .gitignore")

print()
print("=" * 60)
print("[OK] Files written:")
print(f"   Private: {PRIV_PATH}")
print(f"   Public:  {PUB_PATH}")
print()
print("=" * 60)
print("[COPY BLOCK 1: app_public_key.pem]")
print("=" * 60)
print(public_pem.decode("utf-8").strip())
print()
print("=" * 60)
print("[COPY BLOCK 2: app_private_key.pem]  -- DO NOT SHARE")
print("=" * 60)
print(private_pem.decode("utf-8").strip())
print()
print("=" * 60)
print("[NEXT STEPS]")
print("=" * 60)
print("1. Copy [COPY BLOCK 1] content into Alipay sandbox dashboard")
print("   (Interface sign mode > Custom key > Public key mode > Upload)")
print("2. Save, then dashboard will SHOW the Alipay public key — copy it back to me")
print("3. Write app_private_key.pem content into fortune-web-v2/.env.local:")
print("   TAIXUAN_ALIPAY_APP_PRIVATE_KEY=\"<paste block 2, escaped newlines>\"")
print("   TAIXUAN_ALIPAY_ALIPAY_PUBLIC_KEY=\"<alipay pub key from dashboard>\"")
print("   TAIXUAN_ALIPAY_APP_ID=9021000165661383")
print("   TAIXUAN_ALIPAY_GATEWAY=https://openapi-sandbox.dl.alipaydev.com/gateway.do")
print("4. Verify .env.local is in .gitignore")
