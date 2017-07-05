ciscoreputation
===============

Get the Cisco's `talosintelligence.com`_ email reputation for an IP address

Usage
-----

.. code-block::

    ciscoreputation
    Get the email reputation for an IP address from talosintelligence.com

    Usage:
        ciscoreputation <query> [options]
        ciscoreputation reputation <query> [options]
        ciscoreputation volumes <query> [options]
        ciscoreputation --help

    Commands:
        reputation      Get the reputation for the given <query>
        volumes         Get the volume for last month and current day for the given <query>

    Arguments:
        query           The ip address to query for.

    Options:
        --tos                  Accept TalosIntelligence Term of Service
        --values               Output only the requested value, useful when using in another script
        --version              Print version.
        -h --help              Show this screen.

    Note: Use wisely, don't query like crazy.

Installation
------------

Install directly from PyPi:

.. code-block::
    $ pip install ciscoreputation
    
Or from the debian package:

.. code-block::
    $ sudo gdebi ciscoreputation-[version]_[platform].deb

Requirements
^^^^^^^^^^^^
* `requests`_
* `docopts`_

Licence
-------

MIT. See LICENCE

Authors
-------

`ciscoreputation` was written by `Francesco Barresi`_ `@cescobarresi`_.

.. _talosintelligence.com: https://talosintelligence.com/reputation_center/
.. _requests: http://python-requests.org/
.. _docopts: https://github.com/docopt/docopt
.. _Francesco Barresi: https://github.com/cescobarresi
.. _@cescobarresi: https://twitter.com/cescobarresi

