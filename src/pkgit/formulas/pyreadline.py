# -*- coding: utf-8 -*- 
# -*- python -*-
#
#       Formula file for pkgit
# 
#       pkgit: tool for dependencies packaging
#
#       Copyright 2014 INRIA - CIRAD - INRA
#
#       File author(s):
#
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################
from __future__ import absolute_import
__revision__ = "$$Id: $$"

from pkgit.formula import Formula

class Pyreadline(Formula):
    version         = "2.0"  	 # Version of the dependency (not of the formula)
    description     = "a ctypes-based readline for Windows"     # Description of the dependency (not of the formula)
    homepage        = "http://ipython.org/pyreadline.html"     # Url of home-page of the dependency (not of the formula)
    license         = "BSD"     # License of the dependency (not of the formula)
    authors         = "Gary and others"     # Authors of the dependency (not of the formula)
    dependencies    = []     # List of dependencies of the formula
    download_name   = "pyreadline.exe"     # Name of the local archive
    download_url    = "https://pypi.python.org/packages/any/p/pyreadline/pyreadline-" + version + ".win32.exe"   	 # Url where to download sources (feel only if "DOWNLOAD = True")
    DOWNLOAD = COPY_INSTALLER = True