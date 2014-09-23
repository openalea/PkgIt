
The goal of this user guide is to explain how to use and extend PkgIt module.

Packaging difficulties
##############################

Overview
--------

Many projects contain heterogeneous components implemented in different languages (python, C++,...). 
Deploy this projects can be very difficult: how to know where a c++ library is installed on a computer?
Moreover if we don't know if the architecture of the machine is Windows, Linux or Mac OS...

For example, the packages of OpenAlea are pure Python packages but depends on PyQt and numpy, scipy and matplotlib.
The VPlants packages are mainly in C++ and Python and have dependencies on other C++ libraries like Qt, Boost, CGAL, eigen...
The Alinea packages depends also on R, Fortran compilers.

The goal is to transform everything in egg (cf. Python eggs). Indeed, once a library is installed like a egg, it is really easy to find where are sources, headers...

To release frequently all these packages and the dependencies on different OS, we need to automate the construction of binary packages,
and to share the work between different expert, knowing the subtilities of each OS or working on new problems arising with new release of some dependencies.

Propose solution : Formula
--------------------------

Each dependency or package will be describe in a Formula.

A Formula file contains all the information needed to download, 
build, package a library on different OS (Windows, Linux and Mac OS X). 
Each Formula is independent from the others, in a separate file, but may contains dependencies on other Formulas.

Based on the set of existing Formula, it is easy to create a new one.

The concept of Formula has been copied from HomeBrew, but is implemented in Python and multi-platform.

.. warning ::
    Today (january 2014) Formulas work only for Windows... 
    It will be adapted soon for other OS.

Related Projects
--------------------------

* Conda http://docs.continuum.io/conda/index.html
* Enstaller http://code.enthought.com/projects/enstaller/
* Wheels https://pypi.python.org/pypi/wheel (PEP 376 http://www.python.org/dev/peps/pep-0376/ , PEP 427 http://www.python.org/dev/peps/pep-0427/ ,PEP 425 http://www.python.org/dev/peps/pep-0425/ ,PEP 426 http://www.python.org/dev/peps/pep-0426/ )
* Homebrew http://brew.sh/
* MacPorts http://www.macports.org/
* Old OpenAlea Way http://openalea.gforge.inria.fr/wiki/doku.php?id=documentation:developper:release:windows (but it is not supported and will become obsolete.)

Install a formula
##################

PkgIt command with option -i, --install will check if you already have packaged your formula (and packaged it if necessary) and then will install it.

>>> pkgit --install mingw
>>> pkgit -i ann
>>> pkgit -i cgal
>>> ...

.. note:: Don't forget that a file formula.py in current directory is helpful for debugging.

Package a formula
##################

Everything can be done by executing pkgit!

Package everything you want:

>>> pkgit --package mingw
>>> pkgit --package ann
>>> pkgit --package cgal
>>> pkgit --package vplants
>>> ...

It will package all dependencies in the local repository ./dist

To omit a dependency, use option --without. Following line will package mingw_rt without packaging mingw (use it if you laready packaged mingw earlier).

>>> pkgit --package mingw_rt --without mingw

.. note:: Don't forget that a file formula.log in current directory is helpful for debugging.

Create Windows installer
########################

For some formulas, you can create windows installer (OpenAlea, VPlants and Alinea only for the moment):

>>> pkgit --wininst openalea
>>> pkgit --wininst vplants --without openalea
>>> pkgit --wininst alinea --without vplants,openalea

It will create a windows installer with what is packaged in the local repository ./dist

OpenAlea exemple
################

We used pkgit to package OpenAlea and VPlants the 10th january 2014. To have more details, please read:

.. toctree::

    use.rst
        
.. toctree::

    use_vplants_example.rst
        
Extend pkgit: create a formula
########################################

pkgit is designed to be easily extensible. So, you can create new formulas.

To create a new formula to dependency "my_amazing_package", you have to:

* Create Formula file
* Fill it
* Share it

>>> pkgit create my_amazing_package

This command will create a file my_amazing_package.py, create the main class and put this file into the formula directory.

File my_amazing_package.py:
::
    from pkgit.formula import Formula
    
    class My_amazing_package(Formula):
        ...

After that, you have to fill your formula. You can watch classical use-cases.

When your formula is working, you can share it in adding the file on the web repository.

.. note:: One dependency = One formula file

Case 1: download only
---------------------

If installer exists yet and you don't need to build anything. Just download installer and copy it in the "dist" repository.
This is the case for Python, Numpy, Scipy, Matplotlib, Pillow, PyOpenGl, GnuPlot...

Example of formula:
::
    from pkgit.formula import Formula
     
    class Numpy(Formula):
        license         = "Numpy License"
        authors         = "(c) Numpy Developers"
        description     = "NumPy is the fundamental package for scientific computing with Python."    
        version         = "1.7.1"
        homepage        = "http://www.numpy.org/"
        download_url    = "http://freefr.dl.sourceforge.net/project/numpy/NumPy/1.7.1/numpy-1.7.1-win32-superpack-python2.7.exe"
        download_name   = "numpy.exe"
        DOWNLOAD = COPY_INSTALLER = True

Typical flags:
::
    DOWNLOAD = COPY_INSTALLER = True

Case 2: install only
---------------------

If installer exists and you need to install dependency without packaging it. (This is the case for Inno, PyWin32, R, SetupTools, SVN.) Just download installer and install it.

Example of formula:
::
    from pkgit.formula import Formula
     
    class Inno(Formula):
        license         = "Free of charge but not public domain : http://www.jrsoftware.org/files/is/license.txt"
        authors         = "(C) 1997-2013 Jordan Russell"
        description     = "Inno Setup is a free installer for Windows programs"  
        version         = "5.5.3"       
        download_url    = "http://mlaan2.home.xs4all.nl/ispack/isetup-5.5.3.exe"
        homepage        = "http://www.jrsoftware.org/"
        download_name   = "innosetup.exe"
        DOWNLOAD = INSTALL = True

Typical flags:
::
    DOWNLOAD = INSTALL = True

Case 3: compile only
---------------------

This is the case for SIP, PyQt4, Qscintilla, PyQScintilla.
Building is usually done in 3 steps "configure", "make" and "make install". Here, by default, "configure" do nothing, "make" launch command "mingw32-make" and "make install" launch command "mingw32-make install". You can put needed flags to True (ex: if you don't need to configure, just set MAKE = MAKE_INSTALL = True).

This case is really particular one. You can watch the code for SIP, PyQt... but it can be terrifying...

Typical flags:
::
    DOWNLOAD = UNPACK = CONFIGURE = MAKE = MAKE_INSTALL = True

Case 4: package only
---------------------

This is the case for Qhull, Qt4_dev.

Exemple of Formula:
::
    from pkgit.formula import Formula
     
    class Qhull(Formula):
        version         = "2012.1"
        download_url    = "http://www.qhull.org/download/qhull-2012.1.zip"
        download_name   = "qhull.zip"
        description     = "Qhull computes the convex hull, Delaunay triangulation, Voronoi diagram, halfspace intersection about a point, furthest-site Delaunay triangulation, and furthest-site Voronoi diagram"
        homepage        = "http://www.qhull.org/"
        authors         = "Barber, C.B., Dobkin, D.P., and Huhdanpaa, H.T."
        DOWNLOAD = UNPACK = BDIST_EGG = True

Typical flags:
::
    DOWNLOAD = UNPACK = BDIST_EGG = True

Case 5: package and post-install
---------------------------------

This is the case for Boost, CMake.

Exemple of Formula:
::
    from pkgit.formula import Formula
     
    class CMake(Formula):
        version        = '2.8.11.2'
        homepage       = "http://www.cmake.org/"
        download_url   = "http://www.cmake.org/files/v2.8/cmake-2.8.11.2-win32-x86.zip"
        download_name  = "cmake.zip"
        license        = "Copyright 2000-2009 Kitware, Inc., Insight Software Consortium"
        authors        = "Bill Hoffman, Ken Martin, Brad King, Dave Cole, Alexander Neundorf, Clinton Stimpson..."
        DOWNLOAD = UNPACK = BDIST_EGG = INSTALL_EGG = True

Typical flags:
::
    DOWNLOAD = UNPACK = BDIST_EGG = INSTALL_EGG = True

Case 6: "General case" compile and package
------------------------------------------

This is the case for PyQGLViewer, SCons, RPy2, Qt4.

Exemple of Formula:
::
    import sys, os
    from pkgit.utils import sh
    from pkgit.formula import Formula
    from setuptools import find_packages
    from path import path
     
    class SCons(Formula):
        license         = "MIT license"
        authors         = "Steven Knight and The SCons Foundation"
        description     = "SCons is an Open Source software construction tool."    
        version         = "2.3.0"      
        homepage        = "http://scons.org/"
        download_url    = "http://downloads.sourceforge.net/project/scons/scons/2.3.0/scons-2.3.0.zip"
        download_name   = "scons.zip"
        DOWNLOAD = UNPACK = MAKE = BDIST_EGG = True   
     
        _packages = dict()
        _package_dir = dict()
        _bin_dir = dict()
     
        def make(self):
            ret = sh(sys.executable + " setup.py build") == 0
            os.chdir("engine")
            self._packages=[pkg.replace('.','/') for pkg in find_packages('.')]
            self._package_dir = dict([(pkg, str(path(pkg).abspath())) for pkg in self._packages])
            os.chdir("..")
            self._bin_dir = {'EGG-INFO/scripts': str(path('script').abspath())}
            return ret

Typical flags:
::
    DOWNLOAD = UNPACK = CONFIGURE = MAKE = MAKE_INSTALL = BDIST_EGG = True

Case 7: Meta-packages hosted on gforge: openalea/vplants/alinea
--------------------------------

This is the case for OpenAlea, Vplants, Alinea.
::
    from pkgit.formula import Formula
    from pkgit.utils import sh, checkout
     
    class Openalea(Formula):
        version = '1.0'
        homepage = "http://openalea.gforge.inria.fr/dokuwiki/doku.php"
        #download_url = "https://scm.gforge.inria.fr/svn/openalea/branches/release_1_0"
        download_url = "https://scm.gforge.inria.fr/svn/openalea/trunk"
        license = "Cecill-C License"
        authors = "Inria, INRA, CIRAD"
        description = "OpenAlea is an open source project primarily aimed at the plant research community."
        download_name  = "OpenAlea"
        dependencies = ["mingw", "mingw_rt", "pyqt4", "numpy", "scipy", "matplotlib", "pyqscintilla", "setuptools", "pillow", "pylsm", "pylibtiff", "pywin32"]
        DOWNLOAD = BDIST_EGG = True
     
        def _download(self):
            return checkout(self.download_url, self.eggdir)
     
        def bdist_egg(self):
            return sh("python multisetup.py bdist_egg -d %s"%(self.dist_dir,)) == 0

Typical flags:
::
    DOWNLOAD = BDIST_EGG = True

Specials methods
----------------

Patch a package
===============

This is the case for ann, rpy2.

* Add your patch in the Formula directory (here the patch name is "rpy2.patch").
* Add code << from pkgit.utils import apply_patch_from_string >> at the begining of your formula
* Write your patch << PATCH = ... >>
* Apply your patch where you want << def make(self): apply_patch_from_string( PATCH )  >>

For example for rpy2:
::
    from pkgit.formula import Formula
    from pkgit.utils apply_patch_from_string
     
    class rpy2(Formula):
       ...
     
       def make(self):
            apply_patch_from_string( PATCH ) 
            ...
     
    PATCH = """
    ...
    ...
    """

Extend path
===========

Overload method extra_path().

.. note:: Is called in method "configure". So Check than flag CONFIGURE is set to True.

Exemple in SIP Formula:
::
    from path import path
    ...
     
        def extra_paths(self):
            return self.sourcedir, path(self.sourcedir)/"sipgen"

Extend python path
==================

Overload method extra_python_paths().

.. note:: Is called in method "configure". So Check than flag CONFIGURE is set to True.

Exemple in SIP Formula:
::
    from path import path
    ...
     
        def extra_python_paths(self):
            return self.sourcedir, path(self.sourcedir)/"siplib"

How Formulas work
###################

When you launch command pkgit package, the corresponding formula is instantiated and some methods are called.

Each main method is associated to a flag. If the flag is set to True, the method can run. By default, every flags are set to False.

Flags
-----

Here are the methods (in the called order) and corresponding flags:

================  ================  ==================================================================
  Methods            Flags              Comments
================  ================  ==================================================================
download() 	       DOWNLOAD 	     Will download sources or installer from "download_url" parameter
unpack() 	       UNPACK 	         Unpack downloaded sources if it is a .zip or .tgz
install() 	       INSTALL 	         Install downloaded installer if it is a .exe or .msi
copy_installer()   COPY_INSTALLER 	 Copy downloaded installer into final directory
configure() 	   CONFIGURE 	     Configure sources to prepare building (prepare "make")
make() 	           MAKE 	         Prepare "make_install" in doing "mingw32-make"
make_install()     MAKE_INSTALL 	 Build sources in doing "mingw32-make install"
bdist_egg() 	   BDIST_EGG 	     Create .egg from sources
install_egg() 	   INSTALL_EGG 	     Install .egg created by "bdist_egg()"
================  ================  ==================================================================

Methods
-------

Each method has a default implementation that formula's creator can overwrite.

* download

Download file locate in "download_url" parameter in "download" repo.

* unpack

Unpack what is in "download" repo into "src" repo.

* install

Install what is in "download" repo if it is a ".msi" or a ".exe".

* configure

In "src" repo, actually by default do nothing.

* make

In "src" repo, launch command "mingw32-make".

* make_install

In "src" repo, launch command "mingw32-make install".

* bdist_egg

Prepare an egg in "egg" repo and create it in "dist" repo.
You can overwrite method "setup".

"setup" method return a python dict which permit to choose what will be in the egg. "setup dict" is used to fill the file "setup.py" in the "egg" repo.

* copy_installer

Copy installer file from "download" to "dist" repo. Use it only if you download a ".exe" or a ".msi" file.

* install_egg

Install a just created egg from "dist" repo. Use it only after a "bdist_egg".

Parameters
----------

When you create a new formula, you have to fill some informations:
::
    version         = "1.0"  # Version of the dependency (not of the formula)
    description     = "This is a beautiful package"     # Description of the dependency (not of the formula)
    homepage        = "http://beautiful_package.com"     # Url of home-page of the dependency (not of the formula)
    license         = "CECILL C"     # License of the dependency (not of the formula)
    authors         = "my_name"     # Authors of the dependency (not of the formula)
    dependencies    = ""     # List of dependencies of the formula
    download_name   = "beautiful_package.zip"     # Name of the local archive
    download_url    = "http://beautiful_package.com/download/"   # Url where to download sources (feel only if "DOWNLOAD = True")

Repositories
------------

pkgit will create repositories.

Temporary repositories:

* download (where sources/archives/installers are downloaded)
* src (where sources are unpack)
* install (where temporary install is done, if necessary)
* egg (where egg is prepared)

Result repository:

* dist (where eggs or installers are finally put)

Status today
############

.. toctree::

    status.rst