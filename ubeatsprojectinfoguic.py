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
from PyQt4 import QtCore, QtGui
from pyvibe import *
from ubeatsprojectinfogui import Ui_UBeatsProjectInfoDialog

class activateubeatsprojectinfoGUI(QtGui.QDialog):
    def __init__(self, m, parent=None):
        self.module = Module
        self.module = m
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_UBeatsProjectInfoDialog()
        self.ui.setupUi(self)
        
        #Set all default parameters contained in the module file into the GUI's fields
    
        self.ui.name_box.setText(self.module.getParameterAsString("project_name"))
        self.ui.modellername_box.setText(self.module.getParameterAsString("modeller_name"))
        self.ui.affiliation_box.setText(self.module.getParameterAsString("modeller_affil"))
        self.ui.othermodellers_box.setText(self.module.getParameterAsString("othermodellers"))
        self.ui.city_box.setText(self.module.getParameterAsString("region_name"))
        self.ui.state_box.setText(self.module.getParameterAsString("state_name"))
        self.ui.country_box.setText(self.module.getParameterAsString("region_country"))
    
        #Date Box
        project_date = self.module.getParameterAsString("project_date")
        project_date = project_date.split(',')
        a = QtCore.QDate(int(project_date[0]),int(project_date[1]),int(project_date[2]))
        self.ui.date_spin.setDate(a)
        
        #Text Field
        self.ui.synopsis_box.setPlainText(self.module.getParameterAsString("project_descr"))
        
        QtCore.QObject.connect(self.ui.buttonBox, QtCore.SIGNAL("accepted()"), self.save_values)
    
    #Save values function
    def save_values(self):
        project_name = str(self.ui.name_box.text())
        self.module.setParameterValue("project_name", project_name)
        
        modeller_name = str(self.ui.modellername_box.text())
        self.module.setParameterValue("modeller_name", modeller_name)
        
        modeller_affil = str(self.ui.affiliation_box.text())
        self.module.setParameterValue("modeller_affil", modeller_affil)
        
        othermodellers = str(self.ui.othermodellers_box.text())
        self.module.setParameterValue("othermodellers", othermodellers)
        
        region_name = str(self.ui.city_box.text())
        self.module.setParameterValue("region_name", region_name)
        
        state_name = str(self.ui.state_box.text())
        self.module.setParameterValue("state_name", state_name)
        
        region_country = str(self.ui.country_box.text())
        self.module.setParameterValue("region_country", region_country)
        
        project_descr = str(self.ui.synopsis_box.toPlainText())
        self.module.setParameterValue("project_descr", project_descr)
        
        #Date Box
        a = self.ui.date_spin.date()
        day = a.day()
        month = a.month()
        year = a.year()
        finaldate = str(year)+","+str(month)+","+str(day)
        self.module.setParameterValue("project_date", finaldate)
    
    