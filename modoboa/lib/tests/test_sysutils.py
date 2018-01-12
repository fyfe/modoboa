# -*- coding: utf-8 -*-

"""Tests for system utility functions."""

from __future__ import unicode_literals

from django.test import SimpleTestCase

from modoboa.lib.sysutils import which


class WhichTests(SimpleTestCase):

    """Tests for modoboa.lib.sysutils.which()"""

    def test_which_absolute_path(self):
        """Find a program using an absolute path"""
        program = "/usr/bin/env"
        expected_output = "/usr/bin/env"
        output = which(program)
        self.assertEqual(output, expected_output)

    def test_which_search_path(self):
        """Find a program searching PATH"""
        program = "env"
        expected_output = "/usr/bin/env"
        output = which(program)
        self.assertEqual(output, expected_output)

    def test_which_search_given_path(self):
        """Find a program using the search path provided"""
        program = "env"
        expected_output = "/usr/bin/env"
        output = which(program, search_path=["/usr/bin"])
        self.assertEqual(output, expected_output)

    def test_which_not_found(self):
        """Ensure None is returned when a program is not found"""
        program = "i-dont-exist"
        expected_output = None
        output = which(program, search_path=[])
        self.assertEqual(output, expected_output)
