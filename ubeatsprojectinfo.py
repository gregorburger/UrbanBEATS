# -*- coding: utf-8 -*-
"""
@file
@author  Peter M Bach <peterbach@gmail.com>
@version 0.5
@section LICENSE

This file is part of VIBe2
Copyright (C) 2011  Peter M Bach

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

from ubeatsprojectinfoguic import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from pyvibe import *

class ubeatsprojectinfo(Module):
    """description of this module
        
    Describe the inputs and outputso f this module.
	- <description of inputs/outputs>
    
    Log of Updates made at each version:
    
    v0.80 update (March 2012):
        - Created file
        -
        Future work:
            -
            -
    
	@ingroup DAnCE4Water
	@author Peter M Bach
	"""

    def __init__(self):
        Module.__init__(self)
        self.project_info = VectorDataIn()
        self.addParameter(self, "project_info", VIBe2.VECTORDATA_OUT)
        
        self.project_name = "none"
        self.project_date = "2000,1,5"
        self.modeller_name = "none"
        self.modeller_affil = "none"
        self.othermodellers = "none"
        self.region_name = "none"
        self.state_name = "none"
        self.region_country = "none"
        self.addParameter(self, "project_name", VIBe2.STRING)
        self.addParameter(self, "project_date", VIBe2.STRING)
        self.addParameter(self, "modeller_name", VIBe2.STRING)
        self.addParameter(self, "modeller_affil", VIBe2.STRING)
        self.addParameter(self, "othermodellers", VIBe2.STRING)
        self.addParameter(self, "region_name", VIBe2.STRING)
        self.addParameter(self, "state_name", VIBe2.STRING)
        self.addParameter(self, "region_country", VIBe2.STRING)
        
        self.project_descr = "none"
        self.addParameter(self, "project_descr", VIBe2.STRING)
    
    def run(self):
        project_info = self.project_info.getItem()
        
        project_attr = Attribute()
        project_attr.setAttribute("project_name", self.project_name)
        project_attr.setAttribute("project_date", self.project_date)
        project_attr.setAttribute("modeller_name", self.modeller_name)
        project_attr.setAttribute("modeller_affil", self.modeller_affil)
        project_attr.setAttribute("othermodellers", self.othermodellers)
        project_attr.setAttribute("region_name", self.region_name)
        project_attr.setAttribute("state_name", self.state_name)
        project_attr.setAttribute("region_country", self.region_country)
        project_attr.setAttribute("project_descr", self.project_descr)
        
        project_info.setAttributes("Configuration_Details", project_attr)
        
        print self.project_name
        
    ########################################################
    #LINK WITH GUI                                         #
    ########################################################
    
    def createInputDialog(self):
        form = activateubeatsprojectinfoGUI(self, QApplication.activeWindow())
        form.show()
        return True  