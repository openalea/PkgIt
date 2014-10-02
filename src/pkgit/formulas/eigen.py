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
from pkgit.formulas.mingw import Mingw as mingw
from pkgit.path_solved import path
import os

class Eigen(Formula):
    version      = "3.0.7"
    download_url = "http://bitbucket.org/eigen/eigen/get/" + version + ".zip"
    homepage = "http://eigen.tuxfamily.org"
    download_name  = "eigen3.zip"
    license = "MPL2"
    authors = " Benoît Jacob and Gaël Guennebaud and others"
    description = "Eigen is a C++ template library for linear algebra: matrices, vectors, numerical solvers, and related algorithms."
    DOWNLOAD = UNPACK = BDIST_EGG = POST_INSTALL = True
    
    def setup(self):
        inc = str(path(self.sourcedir)/"eigen")
        return dict( 
                    VERSION  = self.version,
                    INC_DIRS = {'include' : inc },
                    LIB_DIRS = None,
                    BIN_DIRS = None,
                    )
