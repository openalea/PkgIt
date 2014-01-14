Create a release: OpenAlea example
##################################

Prepare your computer
---------------------

* install PkgIt and dependencies (Python, ...)
* please check you can access to python and pkgit in cmd in launching >>> python and >>> pkgit -v . If not, please adapt your PATH (cf after).
* create a temp repo (here we create C:\\temp_pkgit)
* go inside temp repo

.. note::
    
    You can change your PATH to add Python doing:
    
    >>> set path=%path%;C:\Python27;C:\Python27\Scripts
    >>> reg.exe ADD "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path /t REG_EXPAND_SZ /d ^%path^% /f

Package dependencies and OpenAlea
---------------------------------

>>> pkgit -p openalea

If one package doesn't work, you can get old package from gforge.

.. warning::
    Following formulas doesn't works. So please download old version on GForge and put them in repo C:\\temp_pkgit\\dist\\thirdpart.
    
    * **Qhull** 2012.1 doesn't work with PlantGL (todo: download Qhull 2003.1).
    * **Qt4**, **Qt4_dev**, Qscintilla, PyQscintilla doesn't works (todo: download qt4 and qt4_dev).
    * **pylsm** doesn't work (check why... And download pylsm).
    
    Indeed, you can download by hand Qhull, Qt4, Qt4_dev and pylsm, put them into C:\\temp_pkgit\\dist\\thirdpart and launch command:
    
    >>> pkgit -p openalea --without qhull,qt4,qt4_dev,qscintilla,pyqscintilla,sip,pylsm
    
    .. note::
        
        * Sometimes mingw and mingw_rt formulas doesn't works: problem with "mingw-get" command. 
        
        You can add mingw-get in your PATH doing:
            
        >>> set path=%path%;C:\MinGW\bin
        >>> reg.exe ADD "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path /t REG_EXPAND_SZ /d ^%path^% /f

.. note::

    If you already have OpenAlea fully installed, maybe you don't want to download it.
    In this case, in the openalea formula, begin by comment line 40: 

    >>> #DOWNLOAD = BDIST_EGG = True

    After use:

    >>> pkgit -p openalea

    It will package dependencies.

    And then package OpenAlea by hand doing:

    >>> python multisetup.py clean build develop bdist_egg -d C:\temp_pkgit\dist\openalea
    
.. note:: Don't forget that a file formula.py in C:\\temp_pkgit is helpful for debugging.

Build Windows installer
-----------------------

>>> pkgit -w openalea

Get result (OpenAlea)
---------------------

Result is now in: C:\\temp_pkgit\\dist\\result\\openalea_win32_2.7\\Output\\openalea-1.1.dev-Installer-Py2.7.exe

After packaging and moving your result, don't forget to remove C:\temp_pkgit.


Create a release: VPlants example
##################################

Package dependencies and VPlants
---------------------------------

>>> pkgit -p vplants --without openalea

.. note::
    If you already packaged OpenAlea and you don't want to do it again, so you can add option --without openalea.
    
.. note::
    You need to install OpenAlea.misc before bdist_egg for VPlants

If one package doesn't work, you can get old package from gforge.

.. warning::
    Following formulas doesn't works. So please download old version on GForge and put them in repo C:\\temp_pkgit\\dist\\thirdpart.
    
    * boost
    * cgal
    * pyqglviewer
    * rpy2 (apply_patch_from_string pb?)
    
    .. TODO:: List exactly what is not working


.. note::

    If you already have VPlants fully installed, maybe you don't want to download it.
    In this case, in the VPlants formula, begin by comment line 40: 

    >>> #DOWNLOAD = BDIST_EGG = True

    After use:

    >>> pkgit -p vplants

    It will package dependencies.

    And then package VPlants by hand doing:

    >>> python multisetup.py clean build develop bdist_egg -d C:\temp_pkgit\dist\vplants
    
.. note:: Don't forget that a file formula.py in C:\\temp_pkgit is helpful for debugging.

Build Windows installer
-----------------------

>>> pkgit -w vplants

Get result (VPlants)
---------------------

Result is now in: C:\\temp_pkgit\\dist\\result\\vplants_win32_2.7\\Output\\vplants-1.1.dev-Installer-Py2.7.exe

After packaging and moving your result, don't forget to remove C:\temp_pkgit.





