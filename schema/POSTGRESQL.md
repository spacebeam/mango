============================
Install PostgreSQL on Debian
============================

.. default-domain:: postgresql

This tutorial outlines the steps to install :term:`PostgreSQL` on Debian
systems. The tutorial uses ``.deb`` packages to install. While some
Debian distributions include their own PostgreSQL packages, the official
PostgreSQL packages are generally more up to date.

Package Options
---------------

The downloads repository provides the ``mongodb-10gen`` package,
which contains the latest **stable** release. Additionally you can
:ref:`install previous releases <install-debian-version-pinning>` of MongoDB.

You cannot install this package concurrently with the ``mongodb``,
``mongodb-server``, or ``mongodb-clients`` packages that
your release of Debian may include.

Install MongoDB
---------------

Configure Package Management System (APT)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Debian package management tools (i.e. ``dpkg`` and ``apt``) ensure
package consistency and authenticity by requiring that distributors
sign packages with GPG keys.

.. include:: /includes/steps/install-configure-debian-packages.rst


Install Packages
~~~~~~~~~~~~~~~~

Issue the following command to install the latest stable version of
MongoDB:

.. code-block:: sh

   sudo apt-get install mongodb-10gen

When this command completes, you have successfully installed MongoDB!
