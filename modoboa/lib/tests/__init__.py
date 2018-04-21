# -*- coding: utf-8 -*-

"""Testing utilities."""

from __future__ import unicode_literals

from modoboa.test_utils.external_services import (
    LDAP_AVAILABLE as _LDAP_AVAILABLE, SMTP_AVAILABLE as _SMTP_AVAILABLE
)
from modoboa.test_utils.testcases import (
    ModoAPITestCase as _ModoAPITestCase, ModoTestCase as _ModoTestCase
)

NO_SMTP = not _SMTP_AVAILABLE
NO_LDAP = not _LDAP_AVAILABLE

ModoTestCase = _ModoTestCase
ModoAPITestCase = _ModoAPITestCase
