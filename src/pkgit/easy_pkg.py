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
from pkgit.utils import formulas, eggify_formulas, remove_temp, versions, deps
from pkgit.create import default_formula
#from pkgit.uninstall import uninstall
from pkgit.wininst import wininst

def main():
    version = "1.0"
    formula_list = formulas()
    formula_list = str(formula_list)[1:-1]

    # options
    parser = ArgumentParser(prog='easy_pkg')
    parser.add_argument('command', type=str,
                         help='Command to launch.',choices=["package", "wininst", "create_formula","display_dependencies","display_versions"])
    parser.add_argument('package', type=str,
                         help='''Package to work with. If you use command "create_formula", it is the name of your new formula.
If you use "wininst" it can be "openalea", "vplants" or "alinea".
If you use command "package" or "display_dependencies", it can be %s.''' %str(formula_list))

    parser.add_argument('-v', '--version', action='version', version='%s'%version)
    
    # parser.add_argument('--no-download',dest='dl' , default="False", help="Don't download any packages, just install the ones already downloaded")
    # parser.add_argument('--no-install',dest='inst' , default="False", help="Download and unpack all packages, but don't actually install them.")
    # parser.add_argument('--no-deps',dest='inst' , default="False", help="Don't install package dependencies.")
    
    # parser.add_argument('--force-download', default="False", help="Download even if already downloaded.")
    # parser.add_argument('--force-install', default="False", help="Install even if already installed.")
    # parser.add_argument('--force-build', default="False", help="Build even if already built.")
    # parser.add_argument('--force', default="False", help="Force all: download, install and build")
    
    parser.add_argument('--dest-dir', default=None, help="copy result to DIR")
    # parser.add_argument('--download-dir', default="", help="download package to DIR")
    # parser.add_argument('--install-dir', default="", help="install package to DIR")
    # parser.add_argument('--src-dir', default="", help="unpack archive to DIR")
    # parser.add_argument('--build-dir', default="", help="build package to DIR")
    # parser.add_argument('-d', '--dir', default=".", help="Working DIR in which package will be download, installed, unpacked, built...")
    parser.add_argument('--rm-tmp',action="store_const", const=True, default=False, help="Remove temporary files after packaging(except download).")
    parser.add_argument('--rm-tmp-all',action="store_const", const=True, default=False, help="Remove all temporary files after packaging.")
    
    parser.add_argument('--dry-run',action="store_const", const=True, default=False, help="Don't do anything")
    
    args = parser.parse_args()
    command = args.command
    package_name = args.package.lower()
    if command == "package":
        dest_dir = args.dest_dir
        dry_run = False
        if args.dry_run:
            dry_run = True
        eggify_formulas(package_name, dest_dir=dest_dir, dry_run=dry_run)
        if args.rm_tmp_all:
            remove_temp(package_name, True)
        elif args.rm_tmp:
            remove_temp(package_name)
    
    elif command == "create_formula":
        default_formula(package_name)
    
    elif command == "wininst":
        wininst(project=package_name)
   
    elif command == "display_dependencies":
        print deps(package_name)
        
    elif command == "display_versions":
        version_list = versions()
        for ver in version_list:
        	print ver
   
    # elif command == "uninstall":
        # print "Uninstall All OpenAlea for the moment..."
        # print "todo: uninstall just selected package"
        # uninstall() 
        
if __name__ == '__main__':
    main()