# -*- coding: utf-8 -*-

"""
This module extra functions/shortcuts to communicate with the system
(executing commands, etc.)
"""

from __future__ import unicode_literals

import codecs
import contextlib
import inspect
import io
import re
import subprocess
import sys


def exec_cmd(cmd, sudo_user=None, pinput=None, capture_output=True, **kwargs):
    """Execute a shell command.

    Run a command using the current user. Set :keyword:`sudo_user` if
    you need different privileges.

    :param str cmd: the command to execute
    :param str sudo_user: a valid system username
    :param str pinput: data to send to process's stdin
    :param bool capture_output: capture process output or not
    :rtype: tuple
    :return: return code, command output
    """
    if sudo_user is not None:
        cmd = "sudo -u %s %s" % (sudo_user, cmd)
    kwargs["shell"] = True
    if pinput is not None:
        kwargs["stdin"] = subprocess.PIPE
    if capture_output:
        kwargs.update(stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    process = subprocess.Popen(cmd, **kwargs)
    if pinput or capture_output:
        c_args = [pinput] if pinput is not None else []
        output = process.communicate(*c_args)[0]
    else:
        output = None
        process.wait()
    return process.returncode, output


def guess_extension_name():
    """Tries to guess the application's name by inspecting the stack.

    :return: a string or None
    """
    modname = inspect.getmodule(inspect.stack()[2][0]).__name__
    match = re.match(r"(?:modoboa\.)?(?:extensions\.)?([^\.$]+)", modname)
    if match is not None:
        return match.group(1)
    return None


@contextlib.contextmanager
def smart_open(filename, *args, **kwargs):
    """Wrapper for open to allow '-' to be used as an alias to open stdout."""
    if filename != "-":
        fh = io.open(filename, *args, **kwargs)
    else:
        # stdout on Python 2 expects bytes, wrap stdout with a StreamWriter to
        # encode ouput correctly.
        if sys.stdout.isatty():
            # use console encoding
            encoding = sys.stdout.encoding
        else:
            # output is being piped somewhere ie less or gz
            encoding = kwargs.get("encoding", "utf-8")
        fh = codecs.getwriter(encoding)(sys.stdout)

    try:
        yield fh
    finally:
        if not isinstance(fh, codecs.StreamWriter):
            # don't try closing stdout (wrapped in a StreamWriter)
            fh.close()
