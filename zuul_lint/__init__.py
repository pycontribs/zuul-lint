from __future__ import absolute_import, division, print_function

__metaclass__ = type

try:
    import pkg_resources

    __version__ = pkg_resources.get_distribution("zuul_lint").version
except Exception:
    __version__ = "unknown"
