# -*- coding: utf-8 -*-

"""Test password schemes."""

from __future__ import unicode_literals

from django.test import SimpleTestCase

from modoboa.core.password_hashers import get_password_hasher
from modoboa.core.password_hashers.base import CRYPTHasher, PLAINHasher

try:
    # mock is part of the Python (>= 3.3) standard library
    from unittest import mock
except ImportError:
    # fall back to the mock backport
    import mock


def _rounds_number(name, app=None, **kwargs):
    """mock round_number so we don't need database access for these tests."""
    if name == "rounds_number":
        return 1000

    raise ValueError(
        "don't know how to mock %s value" % name
    )  # pragma: no cover


class PasswordSchemesTestCase(SimpleTestCase):
    """Tests for password hashers."""

    ascii_password = "Toto1234"
    unicode_password = "Tóto1234"

    @mock.patch("modoboa.parameters.tools.get_global_parameter")
    def _test_scheme(
        self, scheme_name, hash_prefix, password, mock_get_global_parameter
    ):
        mock_get_global_parameter.side_effect = _rounds_number

        password_hasher = get_password_hasher(scheme_name)()
        hashed_password = password_hasher.encrypt(password)
        self.assertTrue(hashed_password.startswith(hash_prefix))
        self.assertTrue(password_hasher.verify(
            password, hashed_password[len(hash_prefix):]
        ))

    def test_get_password_hasher(self):
        """Test get_password_hasher() helper function."""
        password_hasher = get_password_hasher("crypt")
        self.assertEqual(password_hasher, CRYPTHasher)

        password_hasher = get_password_hasher("does-no-exist")
        self.assertEqual(password_hasher, PLAINHasher)

    def test_b64encode_for_ldap(self):
        """Test passwords hashes for LDAP are base64 encoded."""
        password = "Toto1234"
        password_hasher = get_password_hasher("plain")(target="ldap")
        hashed_password = password_hasher.encrypt(password)
        expected_hash = "{PLAIN}VG90bzEyMzQ="
        self.assertEqual(hashed_password, expected_hash)

    # Basic (weak) hashers

    def test_plain(self):
        """Test plain password scheme."""
        self._test_scheme("plain", "{PLAIN}", self.ascii_password)
        self._test_scheme("plain", "{PLAIN}", self.unicode_password)

    def test_crypt(self):
        """Test crypt password scheme."""
        self._test_scheme("crypt", "{CRYPT}", self.ascii_password)
        self._test_scheme("crypt", "{CRYPT}", self.unicode_password)

    def test_md5_scheme(self):
        """Test md5 password scheme."""
        self._test_scheme("md5", "{MD5}", self.ascii_password)
        self._test_scheme("md5", "{MD5}", self.unicode_password)

    def test_sha256_scheme(self):
        """Test sha256 password scheme."""
        self._test_scheme("sha256", "{SHA256}", self.ascii_password)
        self._test_scheme("sha256", "{SHA256}", self.unicode_password)

    # Advanced (strong) hashers

    def test_bcrypt_scheme(self):
        """Test blfcrypt password scheme."""
        self._test_scheme("blfcrypt", "{BLF-CRYPT}", self.ascii_password)
        self._test_scheme("blfcrypt", "{BLF-CRYPT}", self.unicode_password)

    def test_md5crypt_scheme(self):
        """Test md5crypt password scheme."""
        self._test_scheme("md5crypt", "{MD5-CRYPT}", self.ascii_password)
        self._test_scheme("md5crypt", "{MD5-CRYPT}", self.unicode_password)

    def test_sha256crypt_scheme(self):
        """Test sha256crypt password scheme."""
        self._test_scheme("sha256crypt", "{SHA256-CRYPT}", self.ascii_password)
        self._test_scheme("sha256crypt", "{SHA256-CRYPT}", self.unicode_password)

    def test_sha512crypt_scheme(self):
        """Test sha512crypt password scheme."""
        self._test_scheme("sha512crypt", "{SHA512-CRYPT}", self.ascii_password)
        self._test_scheme("sha512crypt", "{SHA512-CRYPT}", self.unicode_password)
