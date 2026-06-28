from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from app.models.user import User
from app.schemas.user import UserCreate, UserRead


VALID_PASSWORD = "correct horse battery staple"


def test_valid_registration_data_is_accepted():
    payload = {
        "email": "user@example.com",
        "password": VALID_PASSWORD,
    }

    user_data = UserCreate.model_validate(payload)

    assert user_data.email == "user@example.com"
    assert user_data.password == VALID_PASSWORD


def test_invalid_email_is_rejected():
    payload = {
        "email": "not-an-email",
        "password": VALID_PASSWORD,
    }

    with pytest.raises(ValidationError):
        UserCreate.model_validate(payload)


def test_short_password_is_rejected():
    payload = {
        "email": "user@example.com",
        "password": "short",
    }

    with pytest.raises(ValidationError):
        UserCreate.model_validate(payload)


def test_unexpected_admin_field_is_rejected():
    payload = {
        "email": "user@example.com",
        "password": VALID_PASSWORD,
        "is_admin": True,
    }

    with pytest.raises(ValidationError):
        UserCreate.model_validate(payload)


def test_user_response_does_not_expose_password_hash():
    database_user = User(
        id=1,
        email="user@example.com",
        password_hash="secret-hash",
        is_active=True,
        created_at=datetime.now(timezone.utc),
    )

    response = UserRead.model_validate(database_user)
    response_data = response.model_dump()

    assert "password" not in response_data
    assert "password_hash" not in response_data