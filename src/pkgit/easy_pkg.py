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
__revision__ = "$Id: $"

from argparse import ArgumentParser
from pkgit.utils import formulas, eggify_formulas, remove_temp, versions, deps, packaged, post_install
from pkgit.create import default_formula
#from pkgit.uninstall import uninstall
from pkgit.wininst import wininst


def parse():
    version = "1.0"
    formula_list = formulas()
    formula_list = str(formula_list)[1:-1]

    # options
    parser = ArgumentParser(prog='pkgit', description="""Permit to package modules thanks to formulas. Main commands are
--package, --wininst, --create (package existing formula, create windows installer, create new formula).""")

    parser.add_argument('-v', '--version', action='version', version='%s'%version)
    
    parser.add_argument('-p', '--package', help="Package formula named PACKAGE. Available formulas are: %s." %str(formula_list))
    parser.add_argument('-i', '--install', help="Package formula named INSTALL if necessary and install it.")
    parser.add_argument('-w', '--wininst', help="Create Windows installer for formula WININST.")
    parser.add_argument('-c', '--create', help="Create a new formula named CREATE.")
    parser.add_argument('-y', '--packaged', help="Display if formula is yet packaged.")
    parser.add_argument('--ignore', help="Omit to package IGNORE and IGNORE's dependencies. If you use '--ignore all' omit all dependencies. Works with --package")
    parser.add_argument('--deps', help="Display dependencies of formula named DISP_DEPS.")
    parser.add_argument('--versions', action="store_true", default=False, help="Display all formulas available and versions of packages.")
    
    # parser.add_argument('--no-download',dest='dl' , default="False", help="Don't download any packages, just install the ones already downloaded")
    # parser.add_argument('--no-install',dest='inst' , default="False", help="Download and unpack all packages, but don't actually install them.")
    # parser.add_argument('--no-deps',dest='inst' , default="False", help="Don't install package dependencies.")
    
    # parser.add_argument('--force-download', default="False", help="Download even if already downloaded.")
    # parser.add_argument('--force-install', default="False", help="Install even if already installed.")
    # parser.add_argument('--force-build', default="False", help="Build even if already built.")
    parser.add_argument('--force', action="store_true", help="Force packaging. Works with --package")
    
    parser.add_argument('--dest-dir', default=None, help="copy result to DIR. Works with --package")
    # parser.add_argument('--download-dir', default="", help="download package to DIR")
    # parser.add_argument('--install-dir', default="", help="install package to DIR")
    # parser.add_argument('--src-dir', default="", help="unpack archive to DIR")
    # parser.add_argument('--build-dir', default="", help="build package to DIR")
    # parser.add_argument('-d', '--dir', default=".", help="Working DIR in which package will be download, installed, unpacked, built...")
    parser.add_argument('--rm-tmp',action="store_true", help="Remove temporary files after packaging(except download). Works with --package")
    parser.add_argument('--rm-tmp-all',action="store_true", help="Remove all temporary files after packaging. Works with --package")
    
    parser.add_argument('--dry-run',action="store_true", help="Don't do anything. Works with --package")
    parser.add_argument('--continue', action="store_true", dest="continue_", help="Continue packaging where it was stopped the last time. Works with --package.")   
    
    return parser
    
def main(argv=None):
    """
    Command PkgIt.
    
    Permit to package modules thanks to formulas. Main commands are --package, --wininst, --create (package existing formula, create windows installer, create new formula).
    """
    parser = parse()
    args = parser.parse_args()

    if args.create is not None:
        default_formula(args.create)
      
    if args.deps is not None:
        print deps(args.deps)
        
    if args.versions:
        version_list = versions()
        for ver in version_list:
        	print ver
   
    
    """
    Transform str of deps into python list.
    ex: "mingw,qt4,ann" --> ["mingw", "qt4", "ann"]
    """
    ignore = list()
    if args.ignore is not None:    
        ignore = list()
        if len(str(args.ignore).split(",")) > 1:
            for i in str(args.ignore).split(","):
                ignore.insert(0,i)
        else: ignore.insert(0,args.ignore)
   
   
    # Package Process
    if args.package is not None:
        dest_dir = args.dest_dir
        dry_run = False
        force = False
        continue_ = False
        skip = False
        if args.dry_run:
            dry_run = True
        if args.force:
            force = True
        if args.continue_:
            continue_ = True
       
        eggify_formulas(args.package, dest_dir=dest_dir, without=ignore, dry_run=dry_run, force=force, continue_=continue_)
        if args.rm_tmp_all:
            remove_temp(args.package, True)
        elif args.rm_tmp:
            remove_temp(args.package) 
   
    if args.wininst is not None:
        wininst(project=args.wininst)
    # elif command == "uninstall":
        # print "Uninstall All OpenAlea for the moment..."
        # print "todo: uninstall just selected package"
        # uninstall() 
        
    if args.packaged is not None:
        packaged(args.packaged)
    
    if args.install is not None:
        post_install(args.install)
        
if __name__ == '__main__':
    main()