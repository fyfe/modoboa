# -*- coding: utf-8 -*-

"""Core config for admin."""

from __future__ import unicode_literals

from django.apps import AppConfig
from django.db.models import signals
from django.utils.translation import ugettext_lazy

from modoboa.core.configuration import load_configuration


def load_core_settings():
    """Load core settings.

    This function must be manually called (see :file:`urls.py`) in
    order to load base settings.
    """
    from modoboa.parameters import tools as param_tools
    from .app_settings import GeneralParametersForm

    param_tools.registry.add(
        "global", GeneralParametersForm, ugettext_lazy("General"))


class CoreConfig(AppConfig):
    """App configuration."""

    name = "modoboa.core"
    verbose_name = "Modoboa core"

    def ready(self):
        load_configuration()
        load_core_settings()

        # Import these to force registration of checks and signals
        from . import checks  # NOQA:F401
        from . import handlers

        signals.post_migrate.connect(handlers.create_local_config, sender=self)
