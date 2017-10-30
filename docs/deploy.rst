===================
Deploy instructions
===================

The Project include a self install script, witch must be execute on a different machine than it will be run later, the
will run via SSH to install the complete system.

Tested Operation Systems
------------------------

- Server Ubuntu 16.04 64Bit on https://www.digitalocean.com

- Client Mac

Requirements
------------

- SSH

Install
^^^^^^^

Linux / Mac
"""""""""""

Debian / Ubuntu::

    $ sudo apt-get install fabric

Mac
"""

Pip::

    $ pip install fabric

Deploy
------

Download the source from git::

    $ git clone git@github.com:linuxluigi/Django_CCTV.git

Create a ``local_settings.py`` in ``cctv`` & fill it with your settings. To see how to fill your ``local_settings.py``
look at :ref:`local-settings` ::

    $ cd cctv
    $ nano cctv/local_settings.py

Install the Server::

    $ fab install

Deploy or update::

    $ fab deploy

Troubleshoot
------------

If something funny goes on when deploying. Check if you using fabric with python 2.7.

Only tested on linux & mac, I don't know this will work correctly on windows machines.

Windows users may find that these command will only works if typed from Python's
installation directory.