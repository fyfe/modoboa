# -*- coding: utf-8 -*-

"""Testing utilities."""

from __future__ import unicode_literals

import socket


def _smtp_available():
    try:
        smtp_connection = socket.create_connection(("127.0.0.1", 25))
        smtp_connection.close()
    except socket.error:
        return False
    return True


SMTP_AVAILABLE = _smtp_available()


def _ldap_available():
    try:
        import ldap  # noqa
        ldap_connection = socket.create_connection(("127.0.0.1", 3389))
        ldap_connection.close()
    except ImportError:
        return False
    except socket.error:
        return False
    return True


LDAP_AVAILABLE = _ldap_available()
