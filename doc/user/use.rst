Create a release: OpenAlea example
##################################

Prepare your computer
---------------------

* install Python and PkgIt.
* install subversion.
* please check you can access to python and pkgit in cmd in launching >>> python and >>> pkgit -v . If not, please adapt your PATH (cf after).
* create a temp repo. Here we create C:\\temp_pkgit. >>> mkdir C:\\temp_pkgit
* go inside temp repo. >>> cd C:\\temp_pkgit

.. note::
    
    You can change your PATH to add Python doing:
    
    >>> set PATH=C:\Python27;C:\Python27\Scripts;%PATH%
    >>> reg.exe ADD "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path /t REG_EXPAND_SZ /d ^%PATH^% /f

Package dependencies and OpenAlea
---------------------------------

>>> pkgit --package openalea

Or

>>> pkgit -p openalea

If one package doesn't work, you can get old package from gforge and put it inside repository C:\\temp_pkgit\\dist\\thirdpart.

.. warning::
    Following formulas doesn't work. So please download old version on GForge and put them in repo C:\\temp_pkgit\\dist\\thirdpart.
    
    * **Qhull** 2012.1 doesn't work with PlantGL (todo: download Qhull 2003.1).
    * **Qt4**, **Qt4_dev**, Qscintilla, PyQscintilla doesn't work (todo: download qt4 and qt4_dev).
    
    Indeed, you can download by hand Qhull, Qt4, Qt4_dev and pylsm, put them into C:\\temp_pkgit\\dist\\thirdpart and launch command:
    
    >>> pkgit -p openalea --without qhull,qt4,qt4_dev,qscintilla,pyqscintilla,sip
    
    .. note::
        
        * Sometimes mingw and mingw_rt formulas doesn't work: problem with "mingw-get" command. 
        
        You can add mingw-get in your PATH doing:
            
        >>> set PATH=C:\MinGW\bin;%PATH%
        >>> reg.exe ADD "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path /t REG_EXPAND_SZ /d ^%PATH^% /f

.. note::

    If you already have OpenAlea fully installed, maybe you don't want to download it.
    In this case, add --without openalea:

    >>> pkgit -p openalea --without openalea

    It will package only dependencies.

    And then package OpenAlea by hand doing:

    >>> cd where_is_my_openalea
    >>> python multisetup.py clean build install bdist_egg -d C:\\temp_pkgit\\dist\\openalea

Build Windows installer
-----------------------

>>> pkgit --wininst openalea

Or

>>> pkgit -w openalea

Get result (OpenAlea)
---------------------

Result is now in: C:\\temp_pkgit\\dist\\result\\openalea_win32_2.7\\Output\\openalea-1.1.dev-Installer-Py2.7.exe

After packaging and moving your result, don't forget to remove temporary files in C:\\temp_pkgit.
