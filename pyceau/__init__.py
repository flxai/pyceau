from pbr.version import VersionInfo

__version__ = VersionInfo('pyceau').version_string()
__version_info__ = VersionInfo('pyceau').semantic_version().version_tuple()

from .pyceau import Board
