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

class Git(Formula):
    license         = "GNU GPL v2"
    authors         = "TortoiseGit team"
    description     = "TortoiseGit is a Windows Shell Interface to Git and based on TortoiseSVN."
    version         = "1.8.11.0"       
    download_url    = "http://download.tortoisegit.org/tgit/" + version + "/TortoiseGit-" + version + "-32bit.msi"
    homepage        = "https://code.google.com/p/tortoisegit/"
    download_name   = "git.msi"
    DOWNLOAD = INSTALL = COPY_INSTALLER = True 