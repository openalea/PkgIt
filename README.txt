Description
-------------

The PkgIt package is a package to help packaging dependencies and so to create releases. 

Download
----------

>>> svn co https://scm.gforge.inria.fr/svn/openalea/trunk/pkgit pkgit

Installation
------------

>>> python setup.py install

Requirements
------------

* Setuptools
* SVN
* python-requests
* path.py
* Scons >= 0.96.93
* SconsX
* OpenAlea.Deploy

Utilisation
------------

.. TODO:: Complete doc!

.. note:: Everything can be done by executing pkgit.

>>> pkgit package vplants

It will package all dependencies in the local repository ./dist

Then, create windows installer:

>>> pkgit wininst vplants

It will create a windows installer with what is packaged in the local repository ./dist

That's all!

Documentation
-------------
http://openalea.gforge.inria.fr/doc/openalea/pkgit/doc/_build/html/contents.html

