# -*- coding: utf-8 -*-

"""Configuration for modoboa.core"""

import io
import logging
import sys
from importlib import import_module

import pkg_resources

from django.utils import six
from django.utils.six.moves import configparser

if six.PY3:
    CONFIG = configparser.ConfigParser()
else:
    CONFIG = configparser.SafeConfigParser()

_LOG = logging.getLogger("modoboa.core")


def defaults_loaded():
    loaded = False
    try:
        loaded = CONFIG.getboolean("modoboa", "configuration_loaded")
    except (configparser.NoSectionError, configparser.NoOptionError):
        pass
    return loaded


def load(filenames=None, apps=None):
    """Load configuration from ini file."""
    if filenames is None:
        filenames = []
    if apps is None:
        apps = ["modoboa"]

    filenames = [
        pkg_resources.resource_filename(app, "default_settings.ini")
        for app in apps
    ] + filenames

    if six.PY3:
        read_ok = CONFIG.read(filenames, encoding="utf-8")
    else:
        read_ok = []
        for filename in filenames:
            try:
                with io.open(filename, encoding="utf-8") as fp:
                    CONFIG.readfp(fp, filename)
            except IOError:
                continue
            read_ok.append(filename)

    _LOG.debug("loaded configuration from %s", ", ".join(read_ok))
    print("loaded configuration from %s" % ", ".join(read_ok))
    CONFIG.write(sys.stdout)


def apply_to_settings(settings):
    for app in settings["MODOBOA_APPS"]:
        if app == "modoboa.core":
            # avoid an infinite loop
            continue
        try:
            config = import_module(".configuration", app)
            config.apply_to_settings(settings)
        except ImportError:
            pass
