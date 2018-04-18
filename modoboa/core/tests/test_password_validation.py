# -*- coding: utf-8 -*-

"""Test password validators."""

from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from modoboa.core.password_validation import ComplexityValidator


class ComplexityValidatorTestCase(SimpleTestCase):
    """Tests for ComplexityValidator."""

    def test_contains_digits(self):
        """test a password contains numerical digits."""
        validator = ComplexityValidator()
        validator.validate("!Password1")
        with self.assertRaises(ValidationError):
            validator.validate("!Password")

    def test_contains_lowercase(self):
        """test a password contains lower case characters."""
        validator = ComplexityValidator()
        validator.validate("!Password1")
        with self.assertRaises(ValidationError):
            validator.validate("!PASSWORD1")

    def test_contains_uppercase(self):
        """test a password contains upper case characters."""
        validator = ComplexityValidator()
        validator.validate("!Password1")
        with self.assertRaises(ValidationError):
            validator.validate("!password1")

    def test_contains_special(self):
        """test a password contains special characters."""
        validator = ComplexityValidator()
        validator.validate("!Password1")
        with self.assertRaises(ValidationError):
            validator.validate("Password1")
