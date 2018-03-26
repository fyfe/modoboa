# -*- coding: utf-8 -*-

"""Utility functions for working with international domain names."""

from __future__ import unicode_literals

import idna


def convert_idn(value, to_ascii=True):
    """
    Convert an international domain name.

    If to_ascii == True the domain is converted to ascii (punycode) otherwise
    it will be converted to unicode.
    """
    return (
        idna.encode(value).decode("ascii") if to_ascii else idna.decode(value)
    )
