PyCA – Opencast Capture Agent
=============================

.. image:: https://travis-ci.org/opencast/pyCA.svg?branch=master
    :target: https://travis-ci.org/opencast/pyCA

.. image:: https://coveralls.io/repos/github/opencast/pyCA/badge.svg?branch=master
    :target: https://coveralls.io/github/opencast/pyCA?branch=master


**PyCA** is a fully functional Opencast_ capture agent written in Python.
It is free software licensed under the terms of the `GNU Lesser General Public
License`_.

The goals of pyCA are to be…

 - flexible for any kind of capture device
 - simplistic in code and functionality
 - nonrestrictive in terms of choosing capture software

PyCA can be run on almost any kind of devices: A regular PC equipped with
capture cards, a server to capture network streams, small boards or embedded
devices like the `Raspberry Pi`_.

Python Versions
***************

PyCA supports both Python 2 and Python 3. For Python 2, we only support
version 2.7, while for Python 3 we test against all recent versions. For a
detailed list of supported versions, have a look at the `Travis
configuration`_.

While we will continue to support Python 2 for some time, we recommend using
Python 3 if possible.


Installation
************

Here is a short summary for Debian based OS like Raspian::

  git clone https://github.com/opencast/pyCA.git
  cd pyCA
  apt-get install python-configobj python-dateutil python-pycurl \
    python-flask python-sqlalchemy
  vim etc/pyca.conf <-- Edit the configuration
  ./start.sh

On Fedora::

  git clone https://github.com/opencast/pyCA.git
  cd pyCA
  dnf install python-pycurl python-dateutil python-configobj \
    python-flask python-sqlalchemy
  vim etc/pyca.conf <-- Edit the configuration
  ./start.sh

On RHEL/CentOS 7::

  git clone https://github.com/opencast/pyCA.git
  cd pyCA
  yum install python-pycurl python-dateutil python-configobj \
    python-flask python-sqlalchemy
  vim etc/pyca.conf  <-- Edit the configuration
  ./start.sh

On Arch Linux::

  git clone https://github.com/opencast/pyCA.git
  cd pyCA
  sudo pacman -S python-pycurl python-dateutil \
    python-configobj python-sqlalchemy
  vim etc/pyca.conf  <-- Edit the configuration
  ./start.sh

…or use the available AUR_ package.


User Interface
**************

PyCA comes with a web interface to check the status of capture agent and
recordings. It is built as WSGI application and can be run using many
different WSGI servers (Apache httpd + mod_wsgi, Gunicorn, …).

For testing, it also comes with a minimal built-in server. Note that it is
meant for testing only and should not be used in production. It will also
listen to localhost only. To start the server, run (additional to pyCA)::

  ./start.sh ui

To production deployment, use a WSGI server instead. A very simple example,
using Gunicorn, would be to run::

  gunicorn pyca.ui:app

For more information, have a look at the help option of gunicorn or go to the
`Gunicorn online documentation`_.


Backup Mode
***********

By setting ``backup_mode = True`` in the configuration file, the PyCA will go
into a backup mode. This means that capture agent will neither register itself
at the Opencast core, nor try to ingest any of the recorded media or set the
capture state. This is useful if the CA shall be used as backup in case a
regular capture agent fails to record (for whatever reasons). Just match the
name of the pyCA to that of the regular capture agent.


Preview
*******

The web interface can show preview images for running capture processes. To
enable this, the capture process must generate these still images and write
them to a pre-defined location. An simple example configuration using FFmpeg
could look like this::

    command          = '''ffmpeg -nostats -re
                          -f lavfi -r 25 -i testsrc
                          -f lavfi -i sine -t {{time}}
                          -map 0:v -map 1:a {{dir}}/{{name}}.webm
                          -map 0:v -r 1 -updatefirst 1 {{previewdir}}/preview.jpg'''

    preview = '{{previewdir}}/preview.jpg'

This command will record audio and video from a test source and write a WebM
file while simultaneously updating a still image every second.

.. _Opencast: http://opencast.org
.. _GNU Lesser General Public License: https://raw.githubusercontent.com/opencast/pyCA/master/license.lgpl
.. _Raspberry Pi: http://www.raspberrypi.org
.. _AUR: https://aur.archlinux.org/packages/pyca
.. _Gunicorn online documentation: http://gunicorn.org
.. _Travis configuration: https://raw.githubusercontent.com/opencast/pyCA/master/.travis.yml
