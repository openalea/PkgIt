Create a release: VPlants example
##################################

Package dependencies and VPlants
---------------------------------

>>> pkgit -p vplants --without openalea

.. note::
    If you already packaged OpenAlea and you don't want to do it again, so you can add option --without openalea.
    
.. note::
    You need to install OpenAlea.misc before bdist_egg for VPlants

If one package doesn't work, you can get old package from gforge and put it inside repository C:\\temp_pkgit\\dist\\thirdpart.

.. warning::
    Following formulas doesn't work. So please download old version on GForge and put them in repo C:\\temp_pkgit\\dist\\thirdpart.
    
    * pyqglviewer
    * rpy2 (apply_patch_from_string pb?)

.. note::

    If you already have VPlants fully installed, maybe you don't want to download it.
    In this case, add --without vplants:

    >>> pkgit -p vplants --without vplants

    It will package only dependencies.
.
    And then package VPlants by hand doing:

    >>> python multisetup.py clean build install bdist_egg -d C:\temp_pkgit\dist\vplants
    
.. note:: Don't forget that a file formula.py in current directory (C:\\temp_pkgit) is helpful for debugging.

Build Windows installer
-----------------------

>>> pkgit -w vplants

Get result (VPlants)
---------------------

Result is now in: C:\\temp_pkgit\\dist\\result\\vplants_win32_2.7\\Output\\vplants-1.1.dev-Installer-Py2.7.exe

After packaging and moving your result, don't forget to remove temporary files in C:\\temp_pkgit.
