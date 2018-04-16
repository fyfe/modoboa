# -*- coding: utf-8 -*-

"""Admin API v2 related tests."""

from __future__ import unicode_literals

from pprint import pprint

from django.urls import reverse

from modoboa.admin import factories, models
from modoboa.lib.tests import ModoAPITestCase


class DomainAPITestCase(ModoAPITestCase):
    """Check API."""

    domain_list_url = reverse("api_v2:domain-list")

    @classmethod
    def setUpTestData(cls):  # NOQA:N802
        """Create test data."""
        super(DomainAPITestCase, cls).setUpTestData()
        factories.populate_database()

    def test_get_domains(self):
        """Retrieve a list of domains."""
        response = self.client.get(self.domain_list_url)
        pprint(response.data)
        pprint(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        pprint(response.data)

    def test_create(self):
        data = {
            "name": "example.com",
        }
        response = self.client.post(self.domain_list_url, data)
        pprint(response)

    def test_create_idn_as_ascii(self):
        data = {
            "name": "xn--fsq.com",  # 例.com; 例 == example in Japanese
        }
        response = self.client.post(self.domain_list_url, data)
        pprint(response)

    def test_create_idn_as_unicode(self):
        data = {
            "name": "例.com",  # xn--fsq.com; 例 == example in Japanese
        }
        response = self.client.post(self.domain_list_url, data)
        pprint(response)
