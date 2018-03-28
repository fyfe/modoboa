# -*- coding: utf-8 -*-

"""Django management command to export admin objects."""

from __future__ import unicode_literals

import os

from django.core.management.base import BaseCommand, CommandError
from django.utils import six
from django.utils.translation import ugettext as _

from rest_framework.renderers import JSONRenderer

from modoboa.admin import models
from modoboa.admin.lib import export_data
from modoboa.core.extensions import exts_pool
from modoboa.core.models import User
from modoboa.lib.sysutils import smart_open

if six.PY2:
    from backports import csv
else:
    import csv


class ExportCommand(BaseCommand):
    """Command class."""

    help = _("Export domains or identities using CSV format")  # NOQA:A003

    def add_arguments(self, parser):
        """Add arguments to command."""
        parser.add_argument(
            "--sepchar", type=six.text_type, default=";",
            help=_("Separator used in generated file")
        )
        parser.add_argument(
            "--output", "-o", type=six.text_type, default="-",
            help=_("Where to output the data")
        )
        parser.add_argument(
            "--format", "-f",
            type=six.text_type, default="csv", choices=["csv", "json"],
            help=_("File format to export the data in")
        )
        parser.add_argument(
            "objtype", type=six.text_type, choices=["domains", "identities"],
            help=_("The type of object to export (domains or identities)")
        )

    def export_domains(self):
        """Export all domains."""
        for dom in models.Domain.objects.all():
            dom.to_csv(self.csvwriter)

    def export_identities(self):
        """Export all identities."""
        for u in User.objects.all():
            u.to_csv(self.csvwriter)
        dumped_aliases = []
        qset = (
            models.Alias.objects.exclude(alias_recipient_aliases=None)
            .distinct().prefetch_related("aliasrecipient_set")
        )
        for alias in qset:
            alias.to_csv(self.csvwriter)
            dumped_aliases += [alias.pk]
        qset = (
            models.Alias.objects.exclude(pk__in=dumped_aliases)
            .prefetch_related("aliasrecipient_set")
        )
        for alias in qset:
            alias.to_csv(self.csvwriter)

    def handle(self, *args, **options):
        exts_pool.load_all()

        if options["output"] == "-":
            pass
        elif os.path.exists(options["output"]):
            raise CommandError(_("output file already exists"))

        if options["format"] == "csv":
            with smart_open(
                options["output"], mode="w", encoding="utf-8", newline=""
            ) as fp:
                self.csvwriter = csv.writer(fp, delimiter=options["sepchar"])
                if options["objtype"] == "domains":
                    self.export_domains()
                elif options["objtype"] == "identities":
                    self.export_identities()
                else:
                    raise CommandError(
                        _("unsupported object type %(objtype)s") % options
                    )
        elif options["format"] == "json":
            try:
                data_bytes = export_data(options["objtype"], JSONRenderer)
                with smart_open(options["output"], mode="wb") as fp:
                    fp.write(data_bytes)
            except Exception as exc:
                six.raise_from(
                    CommandError(
                        _("unable to export data; %(error)s") %
                        {"error": six.text_type(exc)}
                    ),
                    exc
                )
