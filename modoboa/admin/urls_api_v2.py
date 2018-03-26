# -*- coding: utf-8 -*-

"""Admin API v2 urls."""

from __future__ import unicode_literals

from rest_framework import routers

from modoboa.admin import api_v2

router = routers.SimpleRouter()

router.register(r"domains", api_v2.DomainViewSet, base_name="domain")

urlpatterns = router.urls
