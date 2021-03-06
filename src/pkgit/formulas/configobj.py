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
from pkgit.utils import sh, in_dir, try_except


# NOT TESTED !
class Configobj(Formula):
    version         = "4.7.2"  	 # Version of the dependency (not of the formula)
    description     = "Config file reading, writing and validation."     # Description of the dependency (not of the formula)
    homepage        = "http://www.voidspace.org.uk/python/configobj.html"     # Url of home-page of the dependency (not of the formula)
    license         = "BSD License"     # License of the dependency (not of the formula)
    authors         = "Michael Foord and Nicola Larosa"     # Authors of the dependency (not of the formula)
    dependencies    = []     # List of dependencies of the formula
    download_name   = "configobj.zip"     # Name of the local archive
    download_url    = "http://www.voidspace.org.uk/downloads/configobj-" + version + ".zip"   	 # Url where to download sources (feel only if "DOWNLOAD = True")
    DOWNLOAD = UNPACK = BDIST_EGG = True
    
    @in_dir("sourcedir")
    @try_except
    def _bdist_egg(self):
        return sh('python "configobj-4.7.2\setup.py" bdist_egg -d %s'%(self.dist_dir,)) == 0