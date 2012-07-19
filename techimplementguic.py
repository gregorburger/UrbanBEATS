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
from techimplementgui import Ui_TechImplement_Dialog

class activatetechimplementGUI(QtGui.QDialog):
    def __init__(self, m, parent=None):
        self.module = Module
        self.module = m
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_TechImplement_Dialog()
        self.ui.setupUi(self)
        
        #Set all default parameters contained in the module file into the GUI's fields
        
        #DRIVERS
        if self.module.getParameterAsString("driver_people") == "1":
            self.ui.driver_people_check.setChecked(1)
        else:
            self.ui.driver_people_check.setChecked(0)
    
        if self.module.getParameterAsString("driver_legal") == "1":
            self.ui.driver_legal_check.setChecked(1)
        else:
            self.ui.driver_legal_check.setChecked(0)
        
        if self.module.getParameterAsString("driver_establish") == "1":
            self.ui.driver_establish_check.setChecked(1)
        else:
            self.ui.driver_establish_check.setChecked(0)
    
    
        #RULES AT DIFFERENT SCALES
        if self.module.getParameterAsString("lot_rule") == "G":
            self.ui.impl_rule_lot_combo.setCurrentIndex(0)
        elif self.module.getParameterAsString("lot_rule") == "I":
            self.ui.impl_rule_lot_combo.setCurrentIndex(1)
        elif self.module.getParameterAsString("lot_rule") == "D":
            self.ui.impl_rule_lot_combo.setCurrentIndex(2)
        
        if self.module.getParameterAsString("street_rule") == "G":
            self.ui.impl_rule_street_combo.setCurrentIndex(0)
        elif self.module.getParameterAsString("street_rule") == "I":
            self.ui.impl_rule_street_combo.setCurrentIndex(1)
        elif self.module.getParameterAsString("street_rule") == "D":
            self.ui.impl_rule_street_combo.setCurrentIndex(2)
        
        if self.module.getParameterAsString("neigh_rule") == "G":
            self.ui.impl_rule_neigh_combo.setCurrentIndex(0)
        elif self.module.getParameterAsString("neigh_rule") == "I":
            self.ui.impl_rule_neigh_combo.setCurrentIndex(1)
        elif self.module.getParameterAsString("neigh_rule") == "D":
            self.ui.impl_rule_neigh_combo.setCurrentIndex(2)
        
        if self.module.getParameterAsString("neigh_zone_ignore") == "1":
            self.ui.impl_rule_neigh_check.setChecked(1)
        else:
            self.ui.impl_rule_neigh_check.setChecked(0)
        
        if self.module.getParameterAsString("prec_rule") == "G":
            self.ui.impl_rule_prec_combo.setCurrentIndex(0)
        elif self.module.getParameterAsString("prec_rule") == "I":
            self.ui.impl_rule_prec_combo.setCurrentIndex(1)
        elif self.module.getParameterAsString("prec_rule") == "D":
            self.ui.impl_rule_prec_combo.setCurrentIndex(2)
        
        if self.module.getParameterAsString("prec_zone_ignore") == "1":
            self.ui.impl_rule_prec_check.setChecked(1)
        else:
            self.ui.impl_rule_prec_check.setChecked(0)
        
        if self.module.getParameterAsString("prec_dev_threshold") == "1":
            self.ui.impl_rule_prec_allow.setChecked(1)
            self.ui.impl_rule_prec_spin.setEnabled(1)
        else:
            self.ui.impl_rule_prec_allow.setChecked(0)
            self.ui.impl_rule_prec_spin.setEnabled(0)
    
        self.ui.impl_rule_prec_spin.setValue(float(self.module.getParameterAsString("prec_dev_percent")))
        
        QtCore.QObject.connect(self.ui.impl_rule_prec_allow, QtCore.SIGNAL("clicked()"), self.prec_threshold_enable)
        QtCore.QObject.connect(self.ui.buttonBox, QtCore.SIGNAL("accepted()"), self.save_values)
    
    
    def prec_threshold_enable(self):
        if self.ui.impl_rule_prec_allow.isChecked() == 1:
            self.ui.impl_rule_prec_spin.setEnabled(1)
        else:
            self.ui.impl_rule_prec_spin.setEnabled(0)
    
    
    def save_values(self):
        #DRIVERS
        if self.ui.driver_people_check.isChecked() == 1:
            driver_people = 1
        else:
            driver_people = 0
        self.module.setParameterValue("driver_people", str(driver_people))
        
        if self.ui.driver_legal_check.isChecked() == 1:
            driver_legal = 1
        else:
            driver_legal = 0
        self.module.setParameterValue("driver_legal", str(driver_legal))
        
        if self.ui.driver_establish_check.isChecked() == 1:
            driver_establish = 1
        else:
            driver_establish = 0
        self.module.setParameterValue("driver_establish", str(driver_establish))
        
        
        #RULES AT ALL SCALES
        
        rules_matrix = ["G", "I", "D"]
        
        lot_rule_index = self.ui.impl_rule_lot_combo.currentIndex()
        street_rule_index = self.ui.impl_rule_street_combo.currentIndex()
        neigh_rule_index = self.ui.impl_rule_neigh_combo.currentIndex()
        prec_rule_index = self.ui.impl_rule_prec_combo.currentIndex()
        
        lot_rule = rules_matrix[lot_rule_index]
        street_rule = rules_matrix[street_rule_index]
        neigh_rule = rules_matrix[neigh_rule_index]
        prec_rule = rules_matrix[prec_rule_index]
        
        self.module.setParameterValue("lot_rule", lot_rule)
        self.module.setParameterValue("street_rule", street_rule)
        self.module.setParameterValue("neigh_rule", neigh_rule)
        self.module.setParameterValue("prec_rule", prec_rule)
        
        
        if self.ui.impl_rule_neigh_check.isChecked() == 1:
            neigh_zone_ignore = 1
        else:
            neigh_zone_ignore = 0
        self.module.setParameterValue("neigh_zone_ignore", str(neigh_zone_ignore))
        
        if self.ui.impl_rule_prec_check.isChecked() == 1:
            prec_zone_ignore = 1
        else:
            prec_zone_ignore = 0
        self.module.setParameterValue("prec_zone_ignore", str(prec_zone_ignore))
        
        if self.ui.impl_rule_prec_allow.isChecked() == 1:
            prec_dev_threshold = 1
        else:
            prec_dev_threshold = 0
        self.module.setParameterValue("prec_dev_threshold", str(prec_dev_threshold))
        
        prec_dev_percent = str(self.ui.impl_rule_prec_spin.value())
        self.module.setParameterValue("prec_dev_percent", prec_dev_percent)
        
        
        
        
        
    