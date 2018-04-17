# -*- coding: utf-8 -*-

"""Configuration for modoboa.core"""

import logging
import os
import sys
from pprint import pprint

import pkg_resources

from django.utils import six
from django.utils.six.moves import configparser


if six.PY3:
    CONFIG = configparser.ConfigParser()
else:
    CONFIG = configparser.SafeConfigParser()

_LOG = logging.getLogger("modoboa.core")


def load_configuration(file_path=None):
    file_paths = [
        pkg_resources.resource_filename('modoboa', 'default_settings.ini')
    ]

    if file_path is not None:
        file_paths.insert(0, file_path)
    else:
        env_var = os.environ.get("MODOBOA_SETTINGS", None)
        if env_var is not None:
            file_paths.insert(0, env_var)
        else:
            pprint(os.environ)

    loaded_from = CONFIG.read(file_paths, encoding="utf-8")
    _LOG.debug("loaded configuration from %s", ", ".join(loaded_from))
    print("loaded configuration from %s", ", ".join(loaded_from))
    CONFIG.write(sys.stdout)
