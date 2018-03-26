# -*- coding: utf-8 -*-

"""Export related test cases."""

from __future__ import unicode_literals

import json

from django.urls import reverse
from django.utils.encoding import force_text

from modoboa.admin import factories, models
from modoboa.admin.lib import export_data
from modoboa.lib.tests import ModoTestCase
from modoboa.transport import factories as tr_factories


class ExportTestCase(ModoTestCase):
    """Test case for export operations."""

    @classmethod
    def setUpTestData(cls):  # NOQA:N802
        """Create test data."""
        super(ExportTestCase, cls).setUpTestData()
        factories.populate_database()

    def __export_domains(self, domfilter=""):
        self.client.get(
            "{}?domfilter={}".format(
                reverse("admin:_domain_list"), domfilter))
        return self.client.post(
            reverse("admin:domain_export"), {"filename": "test.csv"}
        )

    def __export_identities(self, idtfilter="", grpfilter=""):
        self.client.get(
            reverse("admin:_identity_list") +
            "?grpfilter=%s&idtfilter=%s" % (grpfilter, idtfilter)
        )
        return self.client.post(
            reverse("admin:identity_export"),
            {"filename": "test.csv"}
        )

    def assertListEqual(self, list1, list2):  # NOQA:N802
        list1 = force_text(list1).split("\r\n")
        list2 = force_text(list2).split("\r\n")
        self.assertEqual(len(list1), len(list2))
        for entry in list1:
            if not entry:
                continue
            self.assertIn(entry, list2)

    def test_export_domains(self):
        """Check domain export."""
        dom = models.Domain.objects.get(name="test.com")
        factories.DomainAliasFactory(name="alias.test", target=dom)
        response = self.__export_domains()
        expected_response = [
            "domain;test.com;50;10;True",
            "domainalias;alias.test;test.com;True",
            "domain;test2.com;0;0;True",
        ]
        self.assertListEqual(
            "\r\n".join(expected_response),
            response.content.strip()
        )

    def test_export_identities(self):
        response = self.__export_identities()
        self.assertListEqual(
            "account;admin@test.com;{PLAIN}toto;;;True;DomainAdmins;admin@test.com;10;test.com\r\naccount;admin@test2.com;{PLAIN}toto;;;True;DomainAdmins;admin@test2.com;10;test2.com\r\naccount;user@test.com;{PLAIN}toto;;;True;SimpleUsers;user@test.com;10\r\naccount;user@test2.com;{PLAIN}toto;;;True;SimpleUsers;user@test2.com;10\r\nalias;alias@test.com;True;user@test.com\r\nalias;forward@test.com;True;user@external.com\r\nalias;postmaster@test.com;True;test@truc.fr;toto@titi.com\r\n",  # NOQA:E501
            response.content.strip()
        )

    def test_export_simpleusers(self):
        factories.MailboxFactory(
            user__username="toto@test.com",
            user__first_name="Léon", user__groups=("SimpleUsers", ),
            address="toto", domain__name="test.com",
        )
        response = self.__export_identities(
            idtfilter="account", grpfilter="SimpleUsers"
        )
        self.assertListEqual(
            "account;user@test.com;{PLAIN}toto;;;True;SimpleUsers;user@test.com;10\r\naccount;user@test2.com;{PLAIN}toto;;;True;SimpleUsers;user@test2.com;10\r\naccount;toto@test.com;{PLAIN}toto;Léon;;True;SimpleUsers;toto@test.com;10",  # NOQA:E501
            response.content.strip()
        )

    def test_export_superadmins(self):
        """A test to validate we only export 1 super admin.

        The password is removed since it is hashed using SHA512-CRYPT.
        """
        response = self.__export_identities(
            idtfilter="account", grpfilter="SuperAdmins"
        )
        elements = response.content.decode().strip().split(";")
        self.assertEqual(len(elements), 9)
        elements[2] = ""
        self.assertEqual(
            ";".join(elements), "account;admin;;;;True;SuperAdmins;;"
        )

    def test_export_domainadmins(self):
        response = self.__export_identities(
            idtfilter="account", grpfilter="DomainAdmins"
        )
        self.assertListEqual(
            "account;admin@test.com;{PLAIN}toto;;;True;DomainAdmins;admin@test.com;10;test.com\r\naccount;admin@test2.com;{PLAIN}toto;;;True;DomainAdmins;admin@test2.com;10;test2.com",  # NOQA:E501
            response.content.strip()
        )

    def test_export_aliases(self):
        response = self.__export_identities(idtfilter="alias")
        self.assertEqual(
            response.content.decode().strip(),
            "alias;alias@test.com;True;user@test.com\r\nalias;forward@test.com;True;user@external.com\r\nalias;postmaster@test.com;True;test@truc.fr;toto@titi.com"  # NOQA:E501
        )


class DRFExportTestCase(ModoTestCase):
    """Test cases for the new export system using DRF serializers."""

    def test_export_domain(self):
        """Ensure domains are exported correctly."""
        factories.DomainFactory(name="example.com")

        expected = {
            "name": "example.com",
            "type": "domain",
            "quota": 0,
            "default_mailbox_quota": 10,
            "enabled": True,

            "transport": None,
            "enable_dns_checks": True,

            "enable_dkim": False,
            "dkim_key_selector": "modoboa",
            "dkim_key_length": None,
            "dkim_public_key": "",
            "dkim_private_key_path": "",
        }

        json_data = export_data("domains").decode("utf-8")
        data = json.loads(json_data)

        self.assertEqual(len(data["Domain"]), 1)
        self.assertEqual(data["Domain"][0], expected)

    def test_export_unicode_domain(self):
        """Ensure unicode domain names are correctly exported."""
        # 例.com == xn--fsq.com ; aka example.com in Japanese
        factories.DomainFactory(name="例.com")

        json_data = export_data("domains").decode("utf-8")
        data = json.loads(json_data)

        self.assertEqual(len(data["Domain"]), 1)
        self.assertEqual(data["Domain"][0]["name"], "xn--fsq.com")

    def test_export_punycode_domain(self):
        """Ensure punycode domain names are correctly exported."""
        # 例.com == xn--fsq.com ; aka example.com in Japanese
        factories.DomainFactory(name="xn--fsq.com")

        json_data = export_data("domains").decode("utf-8")
        data = json.loads(json_data)

        self.assertEqual(len(data["Domain"]), 1)
        self.assertEqual(data["Domain"][0]["name"], "xn--fsq.com")

    def test_export_domain_alias(self):
        """Ensure domain aliases are exported correctly."""
        domain = factories.DomainFactory(name="example.com")
        factories.DomainAliasFactory(name="example.net", target=domain)

        expected = {
            "name": "example.net",
            "target": "example.com",
            "enabled": True,
        }

        json_data = export_data("domains").decode("utf-8")
        data = json.loads(json_data)

        self.assertEqual(len(data["DomainAlias"]), 1)
        self.assertEqual(data["DomainAlias"][0], expected)

    def test_export_unicode_domain_alias(self):
        """Ensure unicode domain aliases are exported correctly."""
        # 例.com == xn--fsq.com ; aka example.com in Japanese
        # उदाहरण.com == xn--p1b6ci4b4b3a.com ; aka example.com in Hindi
        domain = factories.DomainFactory(name="例.com")
        factories.DomainAliasFactory(name="उदाहरण.com", target=domain)

        json_data = export_data("domains").decode("utf-8")
        data = json.loads(json_data)

        self.assertEqual(len(data["DomainAlias"]), 1)
        self.assertEqual(data["DomainAlias"][0]["name"], "xn--p1b6ci4b4b3a.com")
        self.assertEqual(data["DomainAlias"][0]["target"], "xn--fsq.com")

    def test_export_punycode_domain_alias(self):
        """Ensure punycode domain aliases are exported correctly."""
        # 例.com == xn--fsq.com ; aka example.com in Japanese
        # उदाहरण.com == xn--p1b6ci4b4b3a.com ; aka example.com in Hindi
        domain = factories.DomainFactory(name="xn--fsq.com")
        factories.DomainAliasFactory(name="xn--p1b6ci4b4b3a.com", target=domain)

        json_data = export_data("domains").decode("utf-8")
        data = json.loads(json_data)

        self.assertEqual(len(data["DomainAlias"]), 1)
        self.assertEqual(data["DomainAlias"][0]["name"], "xn--p1b6ci4b4b3a.com")
        self.assertEqual(data["DomainAlias"][0]["target"], "xn--fsq.com")

    def test_export_relaydomain(self):
        """Ensure relay domain is exported correctly."""
        transport = tr_factories.TransportFactory(
            pattern="relay.example.com", service="relay",
            _settings={
                "relay_target_host": "external.example.com",
                "relay_target_port": "25",
                "relay_verify_recipients": False
            }
        )
        factories.DomainFactory(
            name="relay.example.com", type="relaydomain", transport=transport
        )

        expected = {
            "pattern": "relay.example.com",
            "service": "relay",
            "next_hop": "[external.example.com]:25",
            "_settings": {
                "relay_target_host": "external.example.com",
                "relay_target_port": "25",
                "relay_verify_recipients": False,
            },
        }

        json_data = export_data("domains").decode("utf-8")
        data = json.loads(json_data)

        self.assertEqual(len(data["Domain"]), 1)
        self.assertEqual(data["Domain"][0]["name"], "relay.example.com")
        self.assertEqual(data["Domain"][0]["type"], "relaydomain")
        self.assertEqual(data["Domain"][0]["transport"], expected)
