# -*- coding: utf-8 -*- 
# -*- python -*-
#
#       Formula file for openalea.pkgit
# 
#       openalea.pkgit: tool for dependencies packaging
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
__revision__ = "$Id: $"

import sys, os
import datetime
from path import path, glob, shutil
from .utils import unpack as utils_unpack
from .utils import install as util_install
from .utils import in_dir, try_except, TemplateStr, sh, sj, makedirs
from .utils import Pattern, recursive_glob_as_dict, get_logger, url

logger = get_logger()   

############################################
# Formula                                  #
############################################
class Formula(object):
    version         = "1.0"  # Version of the dependency (not of the formula)
    description     = ""     # Description of the dependency (not of the formula)
    homepage        = ""     # Url of home-page of the dependency (not of the formula)
    license         = ""     # License of the dependency (not of the formula)
    authors         = ""     # Authors of the dependency (not of the formula)
    dependencies    = ""     # List of dependencies of the formula
    download_name   = ""     # Name of the local archive
    download_url    = None   # Url where to download sources (feel only if "DOWNLOAD = True")
    # Only for package like Pillow which use another name for import (<<import Pil>> and not <<import Pillow>>)
    __packagename__ = None
    required_tools  = None
    working_path  = os.getcwd()

    DOWNLOAD = UNPACK = INSTALL = CONFIGURE = MAKE = MAKE_INSTALL = BDIST_EGG = COPY_INSTALLER = INSTALL_EGG = False
    
    def __init__(self,**kwargs):
        logger.debug("__init__ %s" %self.__class__)
        self.options = {} 
        
        self.dldir          = path(self._get_dl_path())
        self.archname       = path(self._get_dl_path())/self.download_name
        self.sourcedir      = path(self._get_src_path())/self.download_name
        self.sourcedir      = self.sourcedir.splitext()[0]
        self.installdir     = path( self._get_install_path())/self.download_name
        self.installdir     = self.installdir.splitext()[0]
        self.install_inc_dir = path(self.installdir)/"include"
        self.install_lib_dir = path(self.installdir)/"lib"    
        self.dist_dir       = path(self._get_dist_path())/"thirdpart"
        self.eggdir         = path(self._get_egg_path())/self.egg_name()
        self.setup_in_name  = path(__file__).abspath().dirname()/"setup.py.in"
        self.setup_out_name = path(self.eggdir)/"setup.py"
        self.use_cfg_login  = False #unused for the moment
        
        makedirs(self._get_src_path())
        makedirs(self._get_install_path())
        makedirs(self.sourcedir)
        makedirs(self._get_dl_path())
        makedirs(self.dist_dir)
        makedirs(self.eggdir)
        makedirs(self.installdir)
        
    def default_substitutions_setup_py(self):
        """
        :return: default dict to fill "setup.py" files
        """
        # if package is python and yet installed
        try:
            packages, package_dirs = self.find_packages_and_directories()
            install_dir = path(self.package.__file__).abspath().dirname()
            # py_modules = recursive_glob(self.install_dir, Pattern.pymod)
            data_files = recursive_glob_as_dict(install_dir,
                        ",".join(["*.example","*.txt",Pattern.pyext,"*.c",".1"])).items()
        # evreything else
        except:
            packages, package_dirs, data_files = None, None, None
                        
        d = dict ( NAME                 = self.egg_name(),
                   VERSION              = self.version,
                   THIS_YEAR            = datetime.date.today().year,
                   SETUP_AUTHORS        = "Openalea Team",
                   CODE_AUTHOR          = self.authors,
                   DESCRIPTION          = self.description,
                   HOMEPAGE             = self.homepage,
                   URL                  = self.download_url,
                   LICENSE              = self.license,
                   ZIP_SAFE             = False,
                   PYTHON_MODS          = None,
                   PACKAGE_DATA         = {},
                   INSTALL_REQUIRES     = self.required_tools,
                   PACKAGES             = packages,
                   PACKAGE_DIRS         = package_dirs,
                   DATA_FILES           = data_files,
                   LIB_DIRS             = None,
                   INC_DIRS             = None,
                   BIN_DIRS             = None,
                  )
            
        lib = path(self.sourcedir)/'lib'
        inc = path(self.sourcedir)/'include'
        bin = path(self.sourcedir)/'bin'
        if lib.exists(): d['LIB_DIRS'] = {'lib' : lib }
        if inc.exists(): d['INC_DIRS'] = {'include' : inc }
        if bin.exists(): d['BIN_DIRS'] = {'bin' : bin }
        
        return d

    def get_dependencies(self):
        """
        :return: list of dependencies of the formula 
        """
        if self.dependencies is None:
            self.dependencies = ""
        return list(self.dependencies)
    
    @property
    def name(self):
        return self.__class__.__name__
    
    @classmethod
    def egg_name(cls):
        return cls.__name__.split("egg_")[-1]
        
    def _download(self):
        if self.DOWNLOAD:
            logger.debug("==DOWNLOAD==") 
            # a formula with a none url implicitely means
            # the sources are already here because some
            # other formula installed it.
            # If not downloadable : do nothing
            if self.download_url is None:
                return True    
            dir=self._get_dl_path()
            # If already downloaded : do nothing
            if self.download_name in os.listdir(dir):
                message = "%s already downloaded!" %self.download_name
                logger.debug(message) 
                return True
            # Else: download
            else:
                ret = url(self.download_url, dir=self._get_dl_path(), dl_name=self.download_name)
                logger.debug("Download %s" %ret)
                return bool(ret)
        return True
    
    def _unpack(self):
        if self.UNPACK:
            logger.debug("==UNPACK==") 
            # a formula with a none url implicitely means
            # the sources are already here because some
            # other formula installed it.
            # If not downloadable : do nothing
            if self.download_url is None:
                logger.debug("No url")
                ret = True
            if path(self.sourcedir).exists():
                # If already unpacked and size > 0 : do nothing
                if path(self.sourcedir).getsize() > 0:
                    message =  'already unpacked in %s' %repr(self.sourcedir)
                    logger.debug(message)
                    ret = True
                # If already unpacked but size = 0 : unpack
                else:
                    ret = self.unpack()
            # Else: unpack
            else:
                ret = self.unpack()
            logger.debug("Unpack %s" %ret)
            return ret 
        return True
    
    # def _permanent_extend_sys_path(self):
        #### Do NOT USE "REG ADD..." !!!
        # """
        # Warnings: this method extend PERMANENTLY Path for WINDOWS (and only windows) and need a REBOOT of the computer
        
        # more here:
        # http://fr.wikipedia.org/wiki/Variable_d%27environnement#.3CPATH.3E_pour_l.27emplacement_des_ex.C3.A9cutables
        # and here:
        # http://technet.microsoft.com/fr-fr/library/cc742162%28v=ws.10%29.aspx
        
        # Modifie register... So, please use it carefully...
        
        ### TODO: test it...
        # """
        # exp = self.extra_paths()
        # if exp is not None:
            ### _permanent_extend_sys_path not tested...
            # warnnings.warn("You need to restart the computer to really extend the Path!")
            # cmd = 'REG ADD "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path /d "%PATH%;%s" /f', %exp
            # return sh(cmd) == 0
        ### nothing to add in sys path
        # return True
            
    # def _permanent_extend_python_path(self):
        # """
        # See _permanent_extend_sys_path
        
        # Same for PYTHON_PATH and not PATH
        # """
        # exp = self.extra_python_paths()
        # if exp is not None:
            ### _permanent_extend_python_path not tested...
            # warnnings.warn("You need to restart the computer to really extend the Python_Path!")
            # cmd = 'REG ADD "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Python_path /d "%PYTHON_PATH%;%s" /f', %exp
            # return sh(cmd) == 0
        ### nothing to add in sys path
        # return True
        
    def _extend_sys_path(self):
        # TODO : check if it works...
        exp = self.extra_paths()
        if exp is not None:
            if isinstance(exp, tuple):
                exp = sj(exp)
                
            path_splited = os.environ["PATH"].split(";")
            # Check if not already set
            if not exp in path_splited:
                #os.environ["PATH"] = sj([exp,os.environ["PATH"]])
                old_path = os.environ["PATH"]
                
                os.environ["PATH"] += os.pathsep + exp

                # cmd = " PATH "
                # for e in exp.split(";"):
                    # cmd = cmd + "\"" + e + "\";"
                # cmd = cmd + "%PATH%"
                cmd = ""
                for e in exp.split(";"):
                    cmd = cmd + e + ";"
                cmd = cmd + old_path + "\""            
                
                # set temp PATH
                cmd1 = "SET PATH=\"" + cmd
                logger.debug( cmd1 )
                sh(cmd1)
                
                # set permanent PATH
                cmd2 = "SETX PATH \"" + cmd
                logger.debug( cmd2 )
                sh(cmd2)
            
        return True

    def _extend_python_path(self):
        # Use PYTHONPATH instead PYTHON_PATH

        exp = self.extra_python_paths()
        if exp is not None:
            if isinstance(exp, tuple):
                for e in exp:
                    e = path(e).normpath()
                    sys.path.extend(e)
                exp = sj(exp)
            elif isinstance(exp, str):
                exp = path(exp).normpath()
                sys.path.extend(exp.split(os.pathsep))

            path_splited = os.environ.get("PYTHONPATH","").split(";")
            # Check if not already set
            if not exp in path_splited:
                os.environ["PYTHONPATH"] = sj([exp,os.environ.get("PYTHONPATH","")])
                
                cmd = " PYTHONPATH "
                for e in exp.split(";"):
                    cmd = cmd + "\"" + e + "\";"
                cmd = cmd + "%PYTHONPATH%"
                
                # set temp PYTHON_PATH
                cmd1 = "SET" + cmd
                logger.debug( cmd1 )
                sh(cmd1)
                
                # set permanent PYTHONPATH
                cmd2 = "SETX" + cmd
                logger.debug( cmd2 )
                sh(cmd2)

        return True

    # -- Top level process, they delegate to abstract methods, try not to override --
    @in_dir("sourcedir")
    @try_except
    def _configure(self):
        if self.CONFIGURE:
            logger.debug("==CONFIGURE==") 
            self._extend_sys_path()
            self._extend_python_path()
            ret = self.configure()
            logger.debug("Configure %s" %ret)
            return ret
        return True
        
    @in_dir("sourcedir")
    @try_except
    def _make(self):
        if self.MAKE:
            logger.debug("==MAKE==") 
            ret = self.make()
            logger.debug("Make %s" %ret)
            return ret
        return True
        
    @in_dir("sourcedir")
    @try_except
    def _make_install(self):
        if self.MAKE_INSTALL:
            logger.debug("==MAKE__INSTALL==") 
            ret = self.make_install()
            logger.debug("Make_install %s" %ret)
            return ret 
        return True
        
    @in_dir("dldir") 
    @try_except
    def _install(self):
        if self.INSTALL:
            logger.debug("==INSTALL==") 
            ret = self.install()
            logger.debug("Install %s" %ret)
            return ret
        return True
        
    @try_except
    def _configure_script(self):
        with open( self.setup_in_name, "r") as input, \
             open( self.setup_out_name, "w") as output:
             
            conf = self.default_substitutions_setup_py()
            conf.update(self.setup())
            conf = dict( (k,repr(v)) for k,v in conf.iteritems() )
            template = TemplateStr(input.read())
            output.write(template.substitute(conf))
        return True

    @in_dir("eggdir")
    @try_except
    def _bdist_egg(self):
        if self.BDIST_EGG:
            logger.debug("==BDIST_EGG==") 
            ret = self._configure_script()     
            ret = ret & self.bdist_egg()
            logger.debug("Bdist_egg %s" %ret)
            return ret
        return True
        
    @in_dir("eggdir")
    @try_except
    def _upload_egg(self):
        return True
        # if not self.options["login"] or not self.options["passwd"]:
            # self.use_cfg_login = True
            # ret = self.upload_egg()
            # if not ret:
                # warnings.warn("No login or passwd provided, skipping egg upload")
                # logger.warn( "No login or passwd provided, skipping egg upload" )
                # return Later
            # return ret
        # return self.upload_egg()
    
    @in_dir("dldir") 
    @try_except    
    def _copy_installer(self):
        if self.COPY_INSTALLER:
            logger.debug("==COPY_INSTALLER==") 
            ret = self.copy_installer()
            logger.debug("Copy_installer %s" %ret)
            return ret
        return True
        
    @in_dir("dist_dir") 
    @try_except  
    def _install_egg(self):
        if self.INSTALL_EGG:
            logger.debug("==INSTALL_EGG==") 
            ret = self.install_egg()
            logger.debug("Install_egg %s" %ret)
            return ret
        return True

    def unpack(self):
        return utils_unpack(self.archname, self.sourcedir)
            
    def setup(self):
        return(dict())

    # -- The ones you can override are these ones --
    def copy_installer(self):
        shutil.copy(self.download_name, path(self.dist_dir)/self.download_name)
        return True
    
    def extra_paths(self):
        return None
        
    def extra_python_paths(self):
        return None 
        
    def install(self):
        return util_install(self.download_name)

    def configure(self):
        return True
        
    def make(self):
        try:
            opt = str(self.options["jobs"])
        except:
            opt = None
            
        n = os.environ.get("NUMBER_OF_PROCESSORS")
        if opt:
            cmd = "mingw32-make -j " + str(self.options["jobs"])
        elif n > 1 :
            cmd = "mingw32-make -j " + str(n)
        else:
            cmd = "mingw32-make"
        print
        print cmd
        print
        logger.debug(cmd)  
        return sh( cmd ) == 0

    def make_install(self):
        return sh("mingw32-make install") == 0

    def _glob_egg(self):
        eggs = glob.glob( path(self.dist_dir)/(self.egg_name()+"*.egg") )
        return None if not eggs else eggs[0]    
        
    def bdist_egg(self):
        return sh(sys.executable + " setup.py bdist_egg -d %s"%(self.dist_dir,)) == 0
        
    def install_egg(self):
        # Try to install egg (to call after bdist_egg)
        egg_search = self.egg_name() + "*"
        egg = glob.glob( path(".")/egg_search )
        if egg:
            egg = egg[0]
        else: 
            return False
        cmd = "alea_install -H None -f . %s" %egg
        return sh(cmd) == 0

    def upload_egg(self):
        if not self.use_cfg_login:
            opts = self.options["login"], self.options["passwd"], \
                    self.egg_name(), "\"ThirdPartyLibraries\"", "vplants" if not self.options["release"] else "openalea"
            return sh(sys.executable + " setup.py egg_upload --yes-to-all --login %s --password %s --release %s --package %s --project %s"%opts) == 0
        else:
            opts = self.egg_name(), "\"ThirdPartyLibraries\"", "vplants" if not self.options["release"] else "openalea"
            return sh(sys.executable + " setup.py egg_upload --yes-to-all --release %s --package %s --project %s"%opts) == 0
            
    def conf_dict(self):
        """
        Use it for inno_setup. Cf. openalea.deploy.makeWinInstaller
        
        :return: dict of configuration to generate windows installer with inno setup
        """
        return dict()
    
    #################################
    ## Come from InstalledPackageEggBuilder
    #################################
    @property
    def package(self):
        return __import__(self.packagename)

    @property
    def packagename(self):
        return self.__packagename__ or self.egg_name()

    def _filter_packages(self, pkgs):
        parpkg = self.packagename + "."
        return [ p for p in pkgs if (p == self.packagename or p.startswith(parpkg))]

    def find_packages(self):
        from setuptools import find_packages
        install_dir = path(self.package.__file__).abspath().dirname()
        pkgs   = find_packages( path(install_dir)/os.pardir )
        pkgs = self._filter_packages(pkgs)
        return pkgs

    def find_packages_and_directories(self):
        pkgs = self.find_packages()
        dirs = {}
        install_dir = path(self.package.__file__).abspath().dirname()
        base = (path(install_dir)/os.pardir).abspath()
        for pk in pkgs:
            dirs[pk] =  path(base)/pk.replace(".", os.sep)
        return pkgs, dirs          
            
    #################################
    ## Get PATHs
    #################################
    def get_working_path(self):
        return self.working_path
        
    def _get_dl_path(self):
        return path(self.get_working_path())/"download"
    
    def _get_src_path(self):
        return path(self.get_working_path())/"src"
    
    def _get_install_path(self):
        return path(self.get_working_path())/"install"
        
    def _get_egg_path(self):
        return path(self.get_working_path())/"egg"
        
    def _get_dist_path(self):
        return path(self.get_working_path())/"dist"