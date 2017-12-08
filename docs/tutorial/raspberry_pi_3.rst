Raspberry Pi 3
==============

Tutorial Requirements
---------------------

This tutorial is written for a Mac and Linux system. Workaround for Windows Users will follow in the future if requested.
Skilled windows users can run everything on a Raspberry Pi.

Also is a Raspberry Pi 3 required with at least 16gb SD Card (more space is better).

For the OS we will use the Raspbian Strecht Lite: https://www.raspberrypi.org/downloads/raspbian/

Preparing the Raspberry Pi
--------------------------

Download the Raspbian Image from https://www.raspberrypi.org/downloads/raspbian/ and follow the official tutorial
for installing the operation system on your Raspberry Pi. https://www.raspberrypi.org/documentation/installation/installing-images/

After the image was successfully installed on the SD Card, activate SSH through writing an ``ssh`` file on the Boot
partition. (You need maybe to unmount & mount your device first to create the file)::

    sudo touch /path-to-boot-partion/ssh

In most cases for the Mac it's::

    sudo touch /Volumes/boot/ssh

Don't forget to unmount the SD Card before eject it.

Basic setup for new Raspbian installation
-----------------------------------------

Log on your fresh installed Raspberry Pi with::

    ssh pi@raspberrypi

The Password is ``raspberry`` & change at least the following things with.::

    sudo raspi-config

To setup:

* 1 Change User Password
* 4 Localisation Options

  - I1 Change Locale
  - I2 Change Timezone
* 7 Advance Options

  - A1 Expand Filesystem
  - A4 Memory Split

    + yet another sub-list

``<Finish>`` and reboot your device.

Next copy your SSH Public Key to your Raspberry Pi.::

    ssh-copy-id pi@raspberrypi

And Update the Pi.::

    sudo apt-get update
    sudo apt-get dist-upgrade

Prepare the installation
------------------------

Install fabric
^^^^^^^^^^^^^^

http://www.fabfile.org/installing.html

Via Pip::

    pip install fabric

On Ubunut / Debian::

    sudo apt-get install fabric

Install Git
^^^^^^^^^^^

Mac with homebrew::

    brew install git

Ubunut / Debian::

    sudo apt-get install git

Download the latest version of Django-CCTV
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Download via git::

    git clone git@github.com:linuxluigi/Django_CCTV.git

.. _tutorial_raspberrypi3_setup_configuration:

Setup your configuration
------------------------

Go to the just downloaded project and create the config file::

    cd Django_CCTV
    cp cctv/local_settings.example.py cctv/local_settings.py

and change everything under::

    ###################
    # DEPLOY SETTINGS #
    ###################

A complete guide for the ``cctv/local_settings.py`` your find at :ref:`local_settings`

Install & Deploy Django-CCTV
----------------------------

To install your Django-CCTV instance use the fabric.::

    fab install

This could take some time, you can get now a coffee.

When everything is done your can start to deploy with::

    fab deploy

Enable access over the Internet
-------------------------------

Django-CCTV is ship with a internal DynDns client for https://www.cloudflare.com
To use follow the documentation on :ref:`cloudflare`

Log into your Django-CCTV instance
----------------------------------

When everything works fine, your can start using Django-CCTV on your domain
(witch was setup in this step :ref:`tutorial_raspberrypi3_setup_configuration`) with the domain ending ``admin``::

    https://example.com/admin

The default login is ``admin`` with the password on ``cctv/local_settings.py`` in ``ADMIN_PASS``.

Have fun :)