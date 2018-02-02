# -*- coding: utf-8 -*-

"""Tests for system utility functions."""

from __future__ import unicode_literals

import os
import unittest

from django.test import SimpleTestCase
from django.utils.encoding import smart_bytes

from modoboa.lib.sysutils import exec_cmd, which


ON_TRAVIS = os.environ.get("TRAVIS", None) is not None


class ExecCmdTests(SimpleTestCase):

    """Tests for modoboa.lib.sysutils.exec_cmd()"""

    @unittest.skipIf(ON_TRAVIS, "sudo isn't available in travis-ci")
    def test_sudo_str_cmd(self):
        """Call a command (as string) using sudo"""
        cmd = "true"
        expected_return_code = 0
        return_code, output = exec_cmd(cmd, sudo_user="nobody")
        self.assertEqual(return_code, expected_return_code)

    @unittest.skipIf(ON_TRAVIS, "sudo isn't available in travis-ci")
    def test_sudo_list_cmd(self):
        """Call a command (as list) using sudo"""
        cmd = ["true"]
        expected_return_code = 0
        return_code, output = exec_cmd(cmd, sudo_user="nobody")
        self.assertEqual(return_code, expected_return_code)

    def test_dont_capture_output(self):
        """Don't capture a commands output"""
        cmd = ["true"]
        expected_return_code = 0
        return_code, output = exec_cmd(cmd, capture_output=False)
        self.assertEqual(return_code, expected_return_code)

    def test_input(self):
        """Pass input on stdin to a command"""
        cmd = "tee"
        mesg = "hello world!"
        expected_output = smart_bytes("hello world!")
        return_code, output = exec_cmd(cmd, pinput=mesg)
        self.assertEqual(output, expected_output)


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
