# encoding: utf-8
import os.path

__all__ = [
    "__title__", "__summary__", "__uri__", "__version__",
    "__author__", "__email__", "__license__", "__copyright__",
]


try:
    base_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    base_dir = None


__title__ = "ciscoreputation"
__summary__ = "Get the Cisco's senderbase.org reputation for a hostname or ip address"
__uri__ = "https://github.com/cescobarresi/ciscoreputation"

# Versioning is a 3-part MAJOR.MINOR.MAINTENANCE numbering scheme, where the project author increments:
#
#    MAJOR version when they make incompatible API changes,
#    MINOR version when they add functionality in a backwards-compatible manner, and
#    MAINTENANCE version when they make backwards-compatible bug fixes.

#    zero or more dev releases (denoted with a ”.devN” suffix)
#    zero or more alpha releases (denoted with a ”.aN” suffix)
#    zero or more beta releases (denoted with a ”.bN” suffix)
#    zero or more release candidates (denoted with a ”.rcN” suffix)
# 

__version__ = "2.1.2"

__author__ = "Francesco Barresi"
__email__ = "francescobarresi@bbfactory.it"

__license__ = "MIT"
__copyright__ = "2018 %s" % __author__
