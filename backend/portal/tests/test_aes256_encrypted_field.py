import pytest

from portal.models import AES256EncryptedField


@pytest.mark.parametrize(
    "value, expected",
    [
        ("", ""),
        ("lamarhealth", "lamarhealth"),
        ("alert@lamarhealth.com", "alert@lamarhealth.com"),
        ("test123", "test123"),
        ("1990.01.01", "1990.01.01"),
    ]
)
def test_encrypt_decrypt(value, expected):
    field = AES256EncryptedField()
    assert field._decrypt(field._encrypt(value)) == expected
