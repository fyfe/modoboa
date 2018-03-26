# -*- coding: utf-8 -*-

"""Tests for miscellaneous utility functions."""

from __future__ import unicode_literals

from django.test import SimpleTestCase

from modoboa.lib.misc import to_bool


class MiscellaneousUtilityFunctionsTest(SimpleTestCase):
    """Tests for miscellaneous utility functions."""

    def test_str2bool_true(self):
        """Convert true values with st2bool"""
        true_values = [True, "t", "Yes", "Y", "1"]
        for value in true_values:
            result = to_bool(value)
            self.assertTrue(result)

    def test_str2bool_false(self):
        """Convert false values with st2bool"""
        false_values = [False, "f", "No", "N", "0"]
        for value in false_values:
            result = to_bool(value)
            self.assertFalse(result)

    def test_str2bool_invalid(self):
        """Convert invalid values with st2bool"""
        invalid_values = [0, object()]
        for value in invalid_values:
            with self.assertRaises(ValueError):
                to_bool(value)
