import hashlib
import hmac
import os

from db_utils import create_user, get_user_by_username


def _hash_password(password: str) -> str:
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 120_000)
    return f"pbkdf2_sha256${salt.hex()}${digest.hex()}"


def _verify_password(password: str, stored_hash: str) -> bool:
    try:
        algorithm, salt_hex, digest_hex = stored_hash.split("$", 2)
    except ValueError:
        return False

    if algorithm != "pbkdf2_sha256":
        return False

    salt = bytes.fromhex(salt_hex)
    expected = bytes.fromhex(digest_hex)
    actual = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 120_000)
    return hmac.compare_digest(actual, expected)


def register_user(username: str, password: str):
    username = username.strip()
    if not username or not password:
        return None
    return create_user(username, _hash_password(password))


def login_user(username: str, password: str):
    username = username.strip()
    if not username or not password:
        return None

    user = get_user_by_username(username)
    if user and _verify_password(password, user["password_hash"]):
        return {"id": user["id"], "username": user["username"]}
    return None
