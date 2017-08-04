# -*- coding: utf-8 -*-
from pbr.version import VersionInfo
_v = VersionInfo(__name__).semantic_version()

__author__ = """Santiago Saavedra"""
__email__ = 'ssaavedra@openshine.com'

__version__ = _v.release_string()
version_info = _v.version_tuple()
