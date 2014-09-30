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
from pkgit.utils import checkout, sh, StrictTemplate
from pkgit.path_solved import path


# NOT TESTED !
class Rhizoscan(Formula):
    version         = "0.1"  	 # Version of the dependency (not of the formula)
    description     = "OpenAlea is an open source project primarily aimed at the plant research community."     # Description of the dependency (not of the formula)
    homepage        = "http://openalea.gforge.inria.fr/dokuwiki/doku.php"     # Url of home-page of the dependency (not of the formula)
    license         = "Cecill-C License"     # License of the dependency (not of the formula)
    authors         = "Inria, INRA, CIRAD"     # Authors of the dependency (not of the formula)
    dependencies    = ["opencv", "skimage"]  # List of dependencies of the formula
    download_name   = "rhizoscan"     # Name of the local archive
    download_url    = "https://scm.gforge.inria.fr/svn/vplants/vplants/branches/rhizoscan"   	 # Url where to download sources (feel only if "DOWNLOAD = True")
    DOWNLOAD = BDIST_EGG = True

    def __init__(self,**kwargs):
        super(Rhizoscan, self).__init__(**kwargs)
        self.dist_dir = path(self._get_dist_path())/"rhizoscan"    
    
    def _download(self):
        return checkout(self.download_url, self.eggdir)

    def bdist_egg(self):
        cmd = "python setup.py build install bdist_egg -d %s"%(self.dist_dir,)
        print cmd
        return sh(cmd) == 0

    def _configure_script(self):
        return True
        
    def conf_dict(self):
        """
        Use it for inno_setup. Cf. openalea.deploy.makeWinInstaller
        
        :return: dict of configuration to generate windows installer with inno setup
        """
        return {"generate_pascal_install_code":generate_pascal_install_code}
        
def generate_pascal_install_code(eggmaxid):        
    tmpl = StrictTemplate("""
var i, incr:Integer;
var s:String;
begin
    Result:=False;
    incr := (100 - WizardForm.ProgressGauge.Position)/$EGGMAXID/2;
    for i:=0 to $EGGMAXID do begin
        s := ExtractFileName(Eggs[i]);
        WizardForm.StatusLabel.Caption:='Uncompressing '+s;
        WizardForm.Update();
        try
            ExtractTemporaryFile(s);
            InstallEgg( MyTempDir()+s, '-N');
        except
            Exit;
        end;
        WizardForm.ProgressGauge.Position := WizardForm.ProgressGauge.Position + incr;
    end;

    WizardForm.StatusLabel.Caption:='Installing Rhizoscan ';
    WizardForm.ProgressGauge.Position := 85;
    WizardForm.Update();    
    InstallEgg( 'OpenAlea.Deploy', '-H None -i ' + MyTempDir() + ' -f ' + MyTempDir());
        
    WizardForm.ProgressGauge.Position := 90;
    WizardForm.Update();        
    InstallEgg( 'OpenAlea', '-H None -i ' + MyTempDir() + ' -f ' + MyTempDir());
    Result := True;

    WizardForm.ProgressGauge.Position := 100;
    WizardForm.Update();                   
end;""")
    code = tmpl.substitute(EGGMAXID=eggmaxid)
    return code

