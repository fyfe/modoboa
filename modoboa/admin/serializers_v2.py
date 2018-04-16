# -*- coding: utf-8 -*-

"""Admin serializers for API v2."""

from __future__ import unicode_literals

from pprint import pprint

from rest_framework import serializers
from modoboa.parameters import tools as param_tools

from modoboa.admin import models as admin_models
from modoboa.lib.idn import convert_idn
from modoboa.transport.serializers_v2 import TransportSerializer
from django.utils.translation import ugettext as _
from modoboa.admin.lib import domain_has_authorized_mx


class DomainSerializer(serializers.ModelSerializer):
    """Domain serializer."""

    transport = TransportSerializer(allow_null=True)

    class Meta:
        model = admin_models.Domain
        fields = "__all__"
        read_only_fields = ("id", "creation", "last_modification")

    def to_representation(self, obj):
        rep = super(DomainSerializer, self).to_representation(obj)
        if self.context.get("export", False):
            # don't export auto-generated fields
            for field in self.meta.read_only_fields:
                del rep[field]
        else:
            rep["tags"] = obj.tags
            rep["dnsbl_status_color"] = obj.dnsbl_status_color
            if self.context.get("include_counts", False):
                rep["counts"] = {
                    "domain_alias": obj.domainalias_count,
                    "mailbox": obj.mailbox_count,
                    "mailbox_alias": obj.mbalias_count,
                    "identities": obj.identities_count,
                }
        if "name" in rep:
            rep["name"] = convert_idn(
                rep["name"], self.context.get("idn_as_ascii", True)
            )
        return rep

    def to_internal_value(self, data):
        pprint(data)
        value = super(DomainSerializer, self).to_internal_value(data)
        if "name" in value:
            # To maintain backward compatabity convert punycode domains
            # to unicode;  long term it's probably better to store the
            # domains in punycode to make external authentication (smtp/
            # imap/pop) easier.
            value["name"] = convert_idn(
                value["name"], self.context.get("idn_as_ascii", False)
            )
        return value

    def validate(self, data):
        if data.get("enable_dns_checks", True):
            self._validate_mx(data)
        self._validate_quota(data)
        return data

    def _validate_mx(self, data):
        """Check name constraints."""
        is_superuser = self.context["request"].user.is_superuser
        domains_must_have_authorized_mx = (
            param_tools.get_global_parameter("domains_must_have_authorized_mx")
        )
        domain_mx_authorized = (
            is_superuser or (
                domains_must_have_authorized_mx and
                domain_has_authorized_mx(data["name"])
            )
        )
        if not domain_mx_authorized:
            raise serializers.ValidationError(
                _("No authorized MX record found for this domain")
            )
        return data

    def _validate_quota(self, data):
        """Check quota values."""
        quota = data.get("quota", 0)
        default_mailbox_quota = data.get("default_mailbox_quota", 0)
        if quota != 0 and default_mailbox_quota > quota:
            raise serializers.ValidationError({
                "default_mailbox_quota":
                _("Cannot be greater than domain quota")
            })
        return data


class DomainAliasSerializer(serializers.ModelSerializer):
    """DomainAlias serializer."""

    target = serializers.StringRelatedField()

    class Meta:
        model = admin_models.DomainAlias
        fields = "__all__"

    def to_representation(self, obj):
        rep = super(DomainAliasSerializer, self).to_representation(obj)
        if self.context.get("export", False):
            # don't export auto-generated fields
            del rep["id"]
            del rep["creation"]
            del rep["last_modification"]
        if "name" in rep:
            rep["name"] = convert_idn(
                rep["name"], self.context.get("idn_as_ascii", True)
            )
        if "target" in rep:
            rep["target"] = convert_idn(
                rep["target"], self.context.get("idn_as_ascii", True)
            )
        return rep

    def to_internal_value(self, data):
        value = super(DomainAliasSerializer, self).to_internal_value(data)
        if "name" in value:
            # See note in DomainSerializer.to_internal_value()
            value["name"] = convert_idn(
                value["name"], self.context.get("idn_as_ascii", False)
            )
        if "target" in value:
            # See note in DomainSerializer.to_internal_value()
            value["target"] = convert_idn(
                value["target"], self.context.get("idn_as_ascii", False)
            )
        return value
