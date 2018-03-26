# -*- coding: utf-8 -*-

"""Admin API v2."""

from __future__ import unicode_literals

from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from modoboa.admin import models, serializers_v2
from modoboa.lib.misc import to_bool
from modoboa.lib.permissions import ExtendedDjangoModelPermissions


class DomainViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, ExtendedDjangoModelPermissions,)
    serializer_class = serializers_v2.DomainSerializer

    pagination_class = PageNumberPagination
    page_size_query_param = "page_size"
    page_size = 25
    max_page_size = 100

    def get_queryset(self):
        """Filter queryset based on current user."""
        return models.Domain.objects.get_for_admin(self.request.user)

    def get_serializer_context(self):
        context = super(DomainViewSet, self).get_serializer_context()
        context["idn_as_ascii"] = to_bool(
            self.request.query_params.get("idn_as_ascii", True)
        )
        return context

    def perform_destroy(self, instance):
        """Add custom args to delete call."""
        instance.delete(self.request.user)
