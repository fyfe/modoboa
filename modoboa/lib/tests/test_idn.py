# -*- coding: utf-8 -*-

"""Tests for IDNA functions."""

from __future__ import unicode_literals

from django.test import SimpleTestCase

from modoboa.lib.idn import convert_idn


class ConvertIDNTest(SimpleTestCase):
    """Tests for convert_idn"""

    ascii_domain = "xn--fsq.com"
    unicode_domain = "例.com"  # 例 == example in Japanese

    def test_unicode_to_ascii(self):
        """Convert a unicode domain to ascii"""
        value = convert_idn(self.unicode_domain, to_ascii=True)
        self.assertEqual(value, self.ascii_domain)

    def test_unicode_to_unicode(self):
        """Convert a unicode domain to unicode"""
        value = convert_idn(self.unicode_domain, to_ascii=False)
        self.assertEqual(value, self.unicode_domain)

    def test_ascii_to_unicode(self):
        """Convert an ascii domain to unicode"""
        value = convert_idn(self.ascii_domain, to_ascii=False)
        self.assertEqual(value, self.unicode_domain)

    def test_ascii_to_ascii(self):
        """Convert an ascii domain to ascii"""
        value = convert_idn(self.ascii_domain, to_ascii=True)
        self.assertEqual(value, self.ascii_domain)
