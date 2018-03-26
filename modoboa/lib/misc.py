# -*- coding: utf-8 -*-

"""Miscellaneous utility functions."""

from __future__ import unicode_literals

from django.utils import six


def to_bool(value):
    """Convert a true/false like string to boolean."""
    valid = {
        # True
        "true": True,
        "t": True,
        "yes": True,
        "y": True,
        "1": True,

        # False
        "false": False,
        "f": False,
        "no": False,
        "n": False,
        "0": False,
    }

    if isinstance(value, bool):
        return value

    if not isinstance(value, six.text_type):
        raise ValueError(
            "invalid literal for boolean: '%(value)s'; not a string" %
            {"value": value}
        )

    lower_value = value.lower()
    if lower_value in valid:
        return valid[lower_value]
    else:
        raise ValueError(
            "invalid literal for boolean: '%(value)s'" %
            {"value": value}
        )
