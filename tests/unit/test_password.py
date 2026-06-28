from app.security.passwords import hash_password, verify_password

PASSWORD = "superpass"
WRONG_PASSWORD = "lox"

def test_hash_is_not_plaintext():
    hashed_password = hash_password(PASSWORD)

    assert hashed_password != PASSWORD


def test_correct_password_is_verified():
    hashed_password = hash_password(PASSWORD)

    assert verify_password(PASSWORD, hashed_password)


def test_incorrect_password_is_rejected():
    hashed_password = hash_password(PASSWORD)

    assert not verify_password(WRONG_PASSWORD, hashed_password)


def test_same_password_produces_different_hashes():
    first_hash = hash_password(PASSWORD)
    second_hash = hash_password(PASSWORD)

    assert first_hash != second_hash
    assert verify_password(PASSWORD, first_hash)
    assert verify_password(PASSWORD, second_hash)