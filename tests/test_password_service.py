import pytest
from app.services.password_service import get_password_hash, verify_password


def test_get_password_hash_returns_string():
    password = "mysecretpassword"
    hashed = get_password_hash(password)

    assert isinstance(hashed, str)
    assert len(hashed) > 0


def test_verify_password_correct_password():
    """
    Test that verify_password returns True when the correct plain password is verified against its hash
    """
    password = "securepass123"
    hashed = get_password_hash(password)

    assert verify_password(password, hashed) is True


def test_verify_password_wrong_password():
    """
    Test that verify_password returns False when the wrong plain password is verified
    """
    password = "correctpass"
    wrong_password = "wrongpass"
    hashed = get_password_hash(password)

    assert verify_password(wrong_password, hashed) is False


def test_verify_password_invalid_hash():
    """
    Test that verify_password returns False if the hashed password format is invalid
    """
    plain = "any_password"
    invalid_hash = "not_a_valid_hash"

    assert verify_password(plain, invalid_hash) is False
