# -*- coding: utf-8 -*-

"""Configuration for modoboa.core"""

import logging
import os
import sys
from pprint import pprint

import pkg_resources

from django.utils.six.moves import configparser


class ModoboaConfiguration(configparser.SafeConfigParser()):

    def __init__(self, *args, **kwargs):
        super(ModoboaConfiguration, self).__init__(*args, **kwargs)
        self._log = logging.getLogger("modoboa.core")

    def load(self, file_path=None):
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

        loaded_from = self.read(file_paths, encoding="utf-8")
        self._log.debug("loaded configuration from %s", ", ".join(loaded_from))
        print("loaded configuration from %s", ", ".join(loaded_from))
        self.write(sys.stdout)


CONFIG = ModoboaConfiguration()
