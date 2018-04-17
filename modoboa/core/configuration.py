# -*- coding: utf-8 -*-

"""Configuration for modoboa.core"""

import io
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


def load_configuration(filename=None):
    filenames = [
        pkg_resources.resource_filename('modoboa', 'default_settings.ini')
    ]

    if filename is not None:
        filenames.insert(0, filename)
    else:
        env_var = os.environ.get("MODOBOA_SETTINGS", None)
        if env_var is not None:
            filenames.insert(0, env_var)
        else:
            pprint(os.environ)

    read_ok = []
    for filename in filenames:
        try:
            with io.open(filename, encoding="utf-8") as fp:
                CONFIG.read_file(fp, filename)
        except OSError:
            continue
        read_ok.append(filename)

    _LOG.debug("loaded configuration from %s", ", ".join(read_ok))
    print("loaded configuration from %s", ", ".join(read_ok))
    CONFIG.write(sys.stdout)
