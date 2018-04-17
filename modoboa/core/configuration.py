# -*- coding: utf-8 -*-

"""Configuration for modoboa.core"""

import io
import logging
import sys

import pkg_resources

from django.utils import six
from django.utils.six.moves import configparser


if six.PY3:
    CONFIG = configparser.ConfigParser()
else:
    CONFIG = configparser.SafeConfigParser()

_LOG = logging.getLogger("modoboa.core")


def load_configuration(filenames=None):
    """Load configuration from ini file."""
    if filenames is None:
        filenames = []
    elif isinstance(filenames, six.text_type):
        filenames = [filenames]
    elif isinstance(filenames, [list, set]):
        # remove any empty strings or None values
        filenames = [
            filename
            for filename in filenames
            if filename is not None and filename
        ]
    else:
        raise ValueError(
            "filenames should be a list of configuration files to load"
        )

    filenames.insert(
        0, pkg_resources.resource_filename('modoboa', 'default_settings.ini')
    )

    read_ok = []
    for filename in filenames:
        try:
            with io.open(filename, encoding="utf-8") as fp:
                if six.PY3:
                    CONFIG.read_file(fp, filename)
                else:
                    CONFIG.readfp(fp, filename)
        except OSError:
            continue
        read_ok.append(filename)

    _LOG.debug("loaded configuration from %s", ", ".join(read_ok))
    print("loaded configuration from %s" % ", ".join(read_ok))
    CONFIG.write(sys.stdout)
