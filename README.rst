ciscoreputation
===============

Get the Cisco's `senderbase.org`_ reputation for a Host or IP address

Usage
-----

.. code-block::

    ciscoreputation
    Get the email reputation for a hostname or IP address from senderbase.org

    Usage:
        ciscoreputation <query> [options]
        ciscoreputation reputation <query> [options]
        ciscoreputation volumes <query> [options]
        ciscoreputation alldata <query> [options]
        ciscoreputation --help

    Commands:
        reputation      Get the reputation
        volumes         Get the volume for last month and current day
        alldata         Get the unparsed tabbed data

    Arguments:
        query           The hostname or IP to query for

    Options:
        --tos                  Accept SenderBase Term of Service
        --values               Output only the requested value, useful when using in another script
        --version              Print version.
        -h --help              Show this screen.

    Note: Cisco requires not to exceed 1000 queries per calendar day per IP or subnet.

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
* `BeautifulSoup4`_
* `requests`_
* `docopts`_

Licence
-------

MIT. See LICENCE

Authors
-------

`ciscoreputation` was written by `Francesco Barresi`_ `@cescobarresi`_.

.. _senderbase.org: http://www.senderbase.org/
.. _BeautifulSoup4: https://www.crummy.com/software/BeautifulSoup
.. _requests: http://python-requests.org/
.. _docopts: https://github.com/docopt/docopt
.. _Francesco Barresi: https://github.com/cescobarresi
.. _@cescobarresi: https://twitter.com/cescobarresi

