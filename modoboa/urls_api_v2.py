# -*- coding: utf-8 -*-

"""External API v2 urls."""

from __future__ import unicode_literals

from django.conf.urls import include, url

app_name = "api_v2"

urlpatterns = [
    url("", include("modoboa.admin.urls_api_v2")),
]
