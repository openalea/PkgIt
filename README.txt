About
----------
PkgIt is an helper tool to package OpenAlea.

Description
-------------
The OpenAlea.PkgIt package is a package to help packaging Openalea and dependencies to create releases. 

Content
----------
The OpenAlea.PkgIt package contains :
* easy_pkg command
* formulas

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
Everything can be done by executing easy_pkg:

First, package everything:

>>> easy_pkg package vplants

It will package all dependencies in the local repository ./dist

Then, create windows installer:

>>> easy_pkg wininst vplants

It will create a windows installer with what is packaged in the local repository ./dist


*easy_pkg* was created to package OpenAlea but you can package single dependency too, for example you can package pyqglviewer with the line:

>>> easy_pkg package pyqglviewer

Documentation
-------------
http://openalea.gforge.inria.fr/doc/openalea/pkgit/doc/_build/html/contents.html

