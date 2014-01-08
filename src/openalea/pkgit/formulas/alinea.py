# -*- coding: utf-8 -*- 
# -*- python -*-
#
#       Formula file for OpenAlea.release
# 
#       OpenAlea.release: tool for dependencies packaging
#
#       Copyright 2013 INRIA - CIRAD - INRA
#
#       File author(s):
#
#       File contributor(s):

#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################
from __future__ import absolute_import
__revision__ = "$Id: $"

from openalea.release.formula import Formula
from openalea.release.utils import sh, checkout
from path import path

class Alinea(Formula):
    version = '1.1.dev'
    homepage = "http://openalea.gforge.inria.fr/dokuwiki/doku.php"
    # download_url = "https://scm.gforge.inria.fr/svn/openaleapkg/branches/release_1_0"
    download_url = "https://scm.gforge.inria.fr/svn/openaleapkg/trunk"
    license = "Cecill-C License"
    authors = "INRA teams and Virtual Plants team (Inria)"
    description = "Set of packages to simulate ecophysiological and agronomical processes (crop 3D development, light distribution, interactions with diseasesâ¦)"
    download_name  = "Alinea"
    dependencies = ["vplants"]
    DOWNLOAD = BDIST_EGG = True
    
    def __init__(self,**kwargs):
        super(Alinea, self).__init__(**kwargs)
        self.dist_dir = path(self._get_dist_path())/"openalea"        
    
    def _download(self):
        return checkout(self.download_url, self.eggdir)

    def bdist_egg(self):
        return sh("python multisetup.py build bdist_egg -d %s"%(self.dist_dir,)) == 0