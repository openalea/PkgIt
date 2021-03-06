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
from pkgit.utils import sh, apply_patch_from_string
from pkgit.path_solved import path
import os

class Ann(Formula):
    version = '1.1.2'
    homepage = "http://www.cs.umd.edu/~mount/ANN/"
    download_url = "http://www.cs.umd.edu/~mount/ANN/Files/"+version+"/ann_"+version+".zip"
    license = "GNU Lesser Public License"
    authors = "Copyright (c) 1997-2010 University of Maryland and Sunil Arya and David Mount"
    description = "Windows gcc libs and headers of ANN"
    download_name  = "ann.zip"
    # download_name  = "ann_" + version + ".zip"
    DOWNLOAD = UNPACK = MAKE_INSTALL = BDIST_EGG = True
    
    def unpack(self):
        ret = super(Ann, self).unpack()
        root = str(self.sourcedir)
        if str(self.sourcedir).endswith('ann_%s'%self.version):
            root = str(path(self.sourcedir)/'..')
            # self.sourcedir = path(self.sourcedir)/'ann_%s'%self.version
        print(root)

        print "Apply PATCH part1"
        apply_patch_from_string(PATCH, root=root)
        print "Apply PATCH part2"
        apply_patch_from_string(PATCH2, root=root)
        
        
        if not str(self.sourcedir).endswith('ann_%s'%self.version):
            self.sourcedir = path(self.sourcedir)/'ann_%s'%self.version

        return ret

    def make_install(self):
        # import os
        # from pkgit.utils import in_dir
        sh("dir")
        # os.chdir("cd ./ann_%s"%self.version)

        # sh("dir")
        
        # dir = "ann_%s"%self.version
        # @in_dir(dir)
        def compile_():
            return sh("mingw32-make win32-g++")
        r = compile_()
        
        
        # os.chdir("..")
        
        return r == 0
        
    def setup(self):
        return dict(DATA_FILES = [('doc' , [str(path(self.sourcedir)/('ann_%s'%self.version)/'doc'/'ANNmanual.pdf')] )],
                    LIB_DIRS   = {'lib' : str(path(self.sourcedir)/('ann_%s'%self.version)/'lib' )},
                    INC_DIRS   = {'include' : str(path(self.sourcedir)/('ann_%s'%self.version)/'include') },
                    BIN_DIRS   = {'bin' : str(path(self.sourcedir)/('ann_%s'%self.version)/'bin') },
                    )
                    
PATCH = """diff -abur ..\ann_1.1.2/ann2fig/Makefile ./ann_1.1.2/ann2fig/Makefile
--- ..\ann_1.1.2/ann2fig/Makefile	2012-03-22 15:37:56.852259200 +0100
+++ ./ann_1.1.2/ann2fig/Makefile	2012-03-23 12:12:55.759431900 +0100
@@ -47,7 +47,7 @@
 #	ANN2FIG		name of executable
 #-----------------------------------------------------------------------------
 
-ANN2FIG = ann2fig
+ANN2FIG = ann2fig.exe
 SOURCES = ann2fig.cpp
 OBJECTS = $(SOURCES:.cpp=.o)
 
@@ -62,7 +62,7 @@
 
 $(BINDIR)/$(ANN2FIG): $(OBJECTS)
 	$(C++) $(OBJECTS) -o $(ANN2FIG) $(LDFLAGS) $(ANNLIBS) $(OTHERLIBS)
-	mv $(ANN2FIG) $(BINDIR)
+	move $(ANN2FIG) "$(BINDIR)"
 
 #-----------------------------------------------------------------------------
 # configuration definitions
diff -abur ..\ann_1.1.2/include/ANN/ANN.h ./include/ANN/ANN.h
--- ..\ann_1.1.2/include/ANN/ANN.h	2012-03-22 15:37:56.985507200 +0100
+++ ./ann_1.1.2/include/ANN/ANN.h	2012-03-23 12:16:09.801756400 +0100
@@ -59,7 +59,7 @@
 #ifndef ANN_H
 #define ANN_H
 
-#ifdef WIN32
+#if defined (_MSC_VER) // #ifdef WIN32
   //----------------------------------------------------------------------
   // For Microsoft Visual C++, externally accessible symbols must be
   // explicitly indicated with DLL_API, which is somewhat like "extern."
diff -abur ..\ann_1.1.2/Makefile ./Makefile
--- ..\ann_1.1.2/Makefile	2012-03-22 15:37:57.105430400 +0100
+++ ./ann_1.1.2/Makefile	2012-03-23 13:26:46.055555200 +0100
@@ -42,6 +42,7 @@
 default:
 	@echo "Enter one of the following:"
 	@echo "  make linux-g++            for Linux and g++"
+	@echo "  make win32-g++            for Win32 and g++ (mingw)." 
 	@echo "  make macosx-g++           for Mac OS X and g++"
 	@echo "  make sunos5               for Sun with SunOS 5.x"
 	@echo "  make sunos5-sl            for Sun with SunOS 5.x, make shared libs"
@@ -62,6 +63,12 @@
 	cd sample ; $(MAKE) $@
 	cd ann2fig ; $(MAKE) $@
 
+win32-g++:
+	cd src && $(MAKE) $@
+	cd test && $(MAKE) $@
+	cd sample && $(MAKE) $@
+	cd ann2fig && $(MAKE) $@
+
 #-----------------------------------------------------------------------------
 # Remove .o files and core files
 #-----------------------------------------------------------------------------
diff -abur ..\ann_1.1.2/sample/Makefile ./sample/Makefile
--- ..\ann_1.1.2/sample/Makefile	2012-03-22 15:37:57.411900800 +0100
+++ ./ann_1.1.2/sample/Makefile	2012-03-23 12:12:21.159679900 +0100
@@ -49,7 +49,7 @@
 #		ANNSAMP		name of sample program
 #-----------------------------------------------------------------------------
 
-ANNSAMP = ann_sample
+ANNSAMP = ann_sample.exe
 
 SAMPSOURCES = ann_sample.cpp
 SAMPOBJECTS = $(SAMPSOURCES:.cpp=.o)
@@ -65,7 +65,7 @@
 
 $(BINDIR)/$(ANNSAMP): $(SAMPOBJECTS) $(LIBDIR)/$(ANNLIB)
 	$(C++) $(SAMPOBJECTS) -o $(ANNSAMP) $(LDFLAGS) $(ANNLIBS)
-	mv $(ANNSAMP) $(BINDIR)
+	move $(ANNSAMP) "$(BINDIR)"
 
 #-----------------------------------------------------------------------------
 # configuration definitions
diff -abur ..\ann_1.1.2/src/Makefile ./src/Makefile
--- ..\ann_1.1.2/src/Makefile	2012-03-22 15:37:57.838294400 +0100
+++ ./ann_1.1.2/src/Makefile	2012-03-23 12:08:25.766132800 +0100
@@ -56,7 +56,7 @@
 $(LIBDIR)/$(ANNLIB): $(OBJECTS)
 	$(MAKELIB) $(ANNLIB) $(OBJECTS)
 	$(RANLIB) $(ANNLIB)
-	mv $(ANNLIB) $(LIBDIR)
+	move $(ANNLIB) "$(LIBDIR)"
 
 #-----------------------------------------------------------------------------
 # Make object files
diff -abur ..\ann_1.1.2/test/Makefile ./test/Makefile
--- ..\ann_1.1.2/test/Makefile	2012-03-22 15:37:57.958217600 +0100
+++ ./ann_1.1.2/test/Makefile	2012-03-23 12:11:46.820302300 +0100
@@ -51,7 +51,7 @@
 #		ANNTEST		name of test program
 #-----------------------------------------------------------------------------
 
-ANNTEST = ann_test
+ANNTEST = ann_test.exe
 
 HEADERS = rand.h
 TESTSOURCES = ann_test.cpp rand.cpp
@@ -68,7 +68,7 @@
 
 $(BINDIR)/$(ANNTEST): $(TESTOBJECTS) $(LIBDIR)/$(ANNLIB)
 	$(C++) $(TESTOBJECTS) -o $(ANNTEST) $(LDFLAGS) $(ANNLIBS) $(OTHERLIBS)
-	mv $(ANNTEST) $(BINDIR)
+	move $(ANNTEST) "$(BINDIR)"
 
 #-----------------------------------------------------------------------------
 # configuration definitions

"""
PATCH2 = r"""diff -abur ..\ann_1.1.2/Make-config ./Make-config
--- ..\ann_1.1.2/Make-config	Wed Oct 01 13:49:48 2014
+++ ./ann_1.1.2/Make-config Wed Oct 01 13:53:48 2014
@@ -76,4 +76,13 @@
 	"MAKELIB = ar ruv" \
 	"RANLIB = true"
+    
+#					Win32 using g++
+win32-g++:
+	$(MAKE) targets \
+	"ANNLIB = libANN.a" \
+	"C++ = g++" \
+	"CFLAGS = -O3 -DANN_NO_RANDOM" \
+	"MAKELIB = ar ruv" \
+	"RANLIB = ranlib"
 
 #					Mac OS X using g++
"""
