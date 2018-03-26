# -*- coding: utf-8 -*-

"""Transport serializers for API v2."""

from __future__ import unicode_literals

import re
from ipaddress import ip_address

import idna

from rest_framework import serializers

from modoboa.transport import models as transport_models

RE_nexthop = re.compile(r"^\[(?P<host>[^\:\]]+)\](?:|\:(?P<port>[0-9]+))$")


class TransportSerializer(serializers.ModelSerializer):
    """Base Transport serializer."""

    _settings = serializers.JSONField()

    class Meta:
        model = transport_models.Transport
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(TransportSerializer, self).__init__(*args, **kwargs)

    def to_representation(self, obj):
        rep = super(TransportSerializer, self).to_representation(obj)
        if self.context.get("export", False):
            del rep["id"]
        if "pattern" in rep:
            rep["pattern"] = idna.encode(rep["pattern"]).decode("ascii")
        if "next_hop" in rep:
            matches = RE_nexthop.match(rep["next_hop"])
            if matches is not None:
                matches = matches.groupdict()
                next_hop = ""
                if "host" in matches:
                    try:
                        host = ip_address(matches["host"]).compressed
                    except ValueError:
                        host = idna.encode(matches["host"]).decode("ascii")
                    next_hop = "[%s]" % host
                if "port" in matches:
                    next_hop += ":%s" % matches["port"]
                rep["next_hop"] = next_hop
            else:
                # XXX - FIX ME
                raise ValueError("next_hop is not valid!")
        return rep

    def to_internal_value(self, data):
        value = super(TransportSerializer, self).to_internal_value(data)
        if "pattern" in value:
            # XXX - To maintain backward compatabity convert punycode domains
            #       to unicode;  long term it's probably better to store the
            #       domains in punycode to make external authentication (smtp/
            #       imap/pop) easier.
            value["pattern"] = idna.decode(value["pattern"])
        if "next_hop" in value:
            matches = RE_nexthop.match(value["next_hop"])
            if matches is not None:
                matches = matches.groupdict()
                next_hop = ""
                if "host" in matches:
                    try:
                        host = ip_address(matches["host"]).compressed
                    except ValueError:
                        host = idna.decode(matches["host"])
                    next_hop = "[%s]" % host
                if "port" in matches:
                    next_hop += ":%s" % matches["port"]
                value["next_hop"] = next_hop
            else:
                # XXX - FIX ME
                raise ValueError("next_hop is not valid!")
        return value
