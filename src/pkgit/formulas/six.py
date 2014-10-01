# -*- coding: utf-8 -*- 
# -*- python -*-
#
#       Formula file for pkgit
# 
#       pkgit: tool for dependencies packaging
#
#       Copyright 2013 INRIA - CIRAD - INRA
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
__revision__ = "$Id: $"

from pkgit.formula import Formula
from pkgit.utils import sh

class Six(Formula):
    version = '1.8.0'
    homepage = "http://pythonhosted.org/six/"
    download_url = "https://pypi.python.org/packages/source/s/six/six-" + version + ".tar.gz"
    license = "MIT"
    authors = "Benjamin Peterson"
    description = "Python 2 and 3 compatibility utilities"
    download_name  = "six.tgz"
    DOWNLOAD = UNPACK = MAKE_INSTALL = BDIST_EGG = True
    
    def make_install(self):
        cmd = "python setup.py install"
        print cmd
        return sh(cmd) == 0