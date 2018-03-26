# -*- coding: utf-8 -*-

"""Admin API v2 related tests."""

from __future__ import unicode_literals

from pprint import pprint

from django.urls import reverse

from modoboa.admin import factories
from modoboa.lib.tests import ModoAPITestCase


class DomainAPITestCase(ModoAPITestCase):
    """Check API."""

    @classmethod
    def setUpTestData(cls):  # NOQA:N802
        """Create test data."""
        super(DomainAPITestCase, cls).setUpTestData()
        factories.populate_database()

    def test_get_domains(self):
        """Retrieve a list of domains."""
        url = reverse("api_v2:domain-list")
        response = self.client.get(url)
        pprint(response.data)
        pprint(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        pprint(response.data)
