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
from pydynamind import *
from delinblocksgui import Ui_DelinBlocksDialog

class activatedelinblocksGUI(QtGui.QDialog):
    def __init__(self, m, parent=None):
        self.module = Module
        self.module = m
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_DelinBlocksDialog()
        self.ui.setupUi(self)
        
        #Set all default parameters contained in the module file into the GUI's fields
        
        #----------------------------------------------------------------------#
        #-------- GENERAL SIMULATION INPUTS------------------------------------#
        #----------------------------------------------------------------------#
        self.ui.blocksize_in.setText(self.module.getParameterAsString("BlockSize"))
        if self.module.getParameterAsString("input_from_urbansim") == "1":
            self.ui.urbansim_in_check.setChecked(1)
            self.ui.soc_par1_check.setEnabled(0)
            self.ui.soc_par2_check.setEnabled(0)
            self.ui.soc_par1_box.setEnabled(0)
            self.ui.soc_par2_box.setEnabled(0)
        else:
            self.ui.urbansim_in_check.setChecked(0)
            self.ui.soc_par1_check.setEnabled(1)
            self.ui.soc_par2_check.setEnabled(1)
            self.ui.soc_par1_box.setEnabled(1)
            self.ui.soc_par2_box.setEnabled(1)
        
        #----------------------------------------------------------------------#
        #-------- ADDITIONAL INPUTS--------------------------------------------#
        #----------------------------------------------------------------------#
        #additional parameters
        if self.module.getParameterAsString("include_plan_map") == "1":
            self.ui.planmap_check.setChecked(1)
        else:
            self.ui.planmap_check.setChecked(0)
        if self.module.getParameterAsString("include_local_map") == "1":
            self.ui.localmap_check.setChecked(1)
        else:
            self.ui.localmap_check.setChecked(0)
        if self.module.getParameterAsString("include_road_net") == "1":                ####ROAD NETWORK MAP NOT OPERATIONAL YET!!!!
            self.ui.roadnet_check.setChecked(1)
        else:
            self.ui.roadnet_check.setChecked(0)
        
        #conditions for what user inputs from main module are
        if self.module.getParameterAsString("include_soc_par1") == "1":
            self.ui.soc_par1_check.setChecked(1)
            self.ui.soc_par1_box.setText(self.module.getParameterAsString("social_par1_name"))
        else:
            self.ui.soc_par1_check.setChecked(0)
            self.ui.soc_par1_box.setEnabled(0)
            self.ui.soc_par1_box.setText(self.module.getParameterAsString("social_par1_name"))
            
        if self.module.getParameterAsString("include_soc_par2") == "1":
            self.ui.soc_par2_check.setChecked(1)
            self.ui.soc_par2_box.setText(self.module.getParameterAsString("social_par2_name"))
        else:
            self.ui.soc_par2_check.setChecked(0)
            self.ui.soc_par2_box.setEnabled(0)
            self.ui.soc_par2_box.setText(self.module.getParameterAsString("social_par2_name"))
        
        #----------------------------------------------------------------------#
        #-------- MAP CONNECTIVITY INPUTS -------------------------------------#
        #----------------------------------------------------------------------#
        if self.module.getParameterAsString("Neighbourhood") == "N":
            self.ui.radioVNeum.setChecked(True)
        if self.module.getParameterAsString("Neighbourhood") == "M":
            self.ui.radioMoore.setChecked(True)
            self.ui.neighb_vnfp_check.setEnabled(0)
            self.ui.neighb_vnpd_check.setEnabled(0)
        
        if self.module.getParameterAsString("vn4FlowPaths") == "1":
            self.ui.neighb_vnfp_check.setChecked(1)
        else:
            self.ui.neighb_vnfp_check.setChecked(0)
        
        if self.module.getParameterAsString("vn4Patches") == "1":
            self.ui.neighb_vnpd_check.setChecked(1)
        else:
            self.ui.neighb_vnpd_check.setChecked(0)
            
        #Flowpath COMBO BOX
        if self.module.getParameterAsString("flow_method") == "DI":
            self.ui.flowpath_combo.setCurrentIndex(0)
        elif self.module.getParameterAsString("flow_method") == "D8":
            self.ui.flowpath_combo.setCurrentIndex(1)
        
        if self.module.getParameterAsString("demsmooth_choose") == "1":
            self.ui.demsmooth_check.setChecked(1)
        else:
            self.ui.demsmooth_check.setChecked(0)
            self.ui.demsmooth_spin.setEnabled(0)
            
        self.ui.demsmooth_spin.setValue(int(self.module.getParameterAsString("demsmooth_passes")))
        
        if self.module.getParameterAsString("basinlimit") == "1":
            self.ui.delinbasin_check.setChecked(1)
        else:
            self.ui.delinbasin_check.setChecked(0)
            self.ui.delinbasin_box.setEnabled(0)
        
        self.ui.delinbasin_box.setText(self.module.getParameterAsString("basinAmax"))
            
        
        #QTCORE CONNECTS, REAL TIME GUI CHANGE COMMANDS
        QtCore.QObject.connect(self.ui.urbansim_in_check, QtCore.SIGNAL("clicked()"), self.social_parameters_urbansim)
        QtCore.QObject.connect(self.ui.soc_par1_check, QtCore.SIGNAL("clicked()"), self.social_par1_modify)
        QtCore.QObject.connect(self.ui.soc_par2_check, QtCore.SIGNAL("clicked()"), self.social_par2_modify)
        QtCore.QObject.connect(self.ui.radioVNeum, QtCore.SIGNAL("clicked()"), self.vnOptions_modify)
        QtCore.QObject.connect(self.ui.radioMoore, QtCore.SIGNAL("clicked()"), self.vnOptions_modify)
        QtCore.QObject.connect(self.ui.delinbasin_check, QtCore.SIGNAL("clicked()"), self.delinbasin_modify)
        QtCore.QObject.connect(self.ui.demsmooth_check, QtCore.SIGNAL("clicked()"), self.demsmooth_modify)
        QtCore.QObject.connect(self.ui.buttonBox, QtCore.SIGNAL("accepted()"), self.save_values)
        

    #Enable-Disable functions for social parameters based on QtCore.QObject.connect() lines
    def social_parameters_urbansim(self):
        if self.ui.urbansim_in_check.isChecked() == 1:
            self.ui.soc_par1_check.setEnabled(0)
            self.ui.soc_par2_check.setEnabled(0)
            self.ui.soc_par1_box.setEnabled(0)
            self.ui.soc_par2_box.setEnabled(0)
        else:
            self.ui.soc_par1_check.setEnabled(1)
            self.ui.soc_par2_check.setEnabled(1)
            self.social_par1_modify()
            self.social_par2_modify()
    
    def social_par1_modify(self):
        if self.ui.soc_par1_check.isChecked() == 1:
            self.ui.soc_par1_box.setEnabled(1)
        else:
            self.ui.soc_par1_box.setEnabled(0)
    
    def social_par2_modify(self):
        if self.ui.soc_par2_check.isChecked() == 1:
            self.ui.soc_par2_box.setEnabled(1)
        else:
            self.ui.soc_par2_box.setEnabled(0)
    
    def demsmooth_modify(self):
        if self.ui.demsmooth_check.isChecked() == 1:
            self.ui.demsmooth_spin.setEnabled(1)
        else:
            self.ui.demsmooth_spin.setEnabled(0)
    
    def vnOptions_modify(self):
        if self.ui.radioVNeum.isChecked() == 1:
            self.ui.neighb_vnfp_check.setEnabled(1)
            self.ui.neighb_vnpd_check.setEnabled(1)
        else:
            self.ui.neighb_vnfp_check.setEnabled(0)
            self.ui.neighb_vnpd_check.setEnabled(0)
    
    def delinbasin_modify(self):
        if self.ui.delinbasin_check.isChecked() == 1:
            self.ui.delinbasin_box.setEnabled(1)
        else:
            self.ui.delinbasin_box.setEnabled(0)
    
    
    #Save values function
    def save_values(self):
        #----------------------------------------------------------------------#
        #-------- GENERAL SIMULATION INPUTS------------------------------------#
        #----------------------------------------------------------------------#
        blocksize = str(self.ui.blocksize_in.text())
        self.module.setParameterValue("BlockSize", blocksize)
        
        if self.ui.urbansim_in_check.isChecked() == 1:
            input_from_urbansim = 1
        else:
            input_from_urbansim = 0
        self.module.setParameterValue("input_from_urbansim", str(input_from_urbansim))
        
        #----------------------------------------------------------------------#
        #-------- ADDITIONAL INPUTS--------------------------------------------#
        #----------------------------------------------------------------------#
        #additional urban planning inputs
        if self.ui.planmap_check.isChecked() == 1:
            include_plan_map = 1
        else:
            include_plan_map = 0
        self.module.setParameterValue("include_plan_map", str(include_plan_map))
        
        if self.ui.localmap_check.isChecked() == 1:
            include_local_map = 1
        else:
            include_local_map = 0
        self.module.setParameterValue("include_local_map", str(include_local_map))
        
        if self.ui.roadnet_check.isChecked() == 1:
            include_road_net = 1
        else:
            include_road_net = 0
        self.module.setParameterValue("include_road_net", str(include_road_net))
        
        #additional social parameter inputs        
        if self.ui.soc_par1_check.isChecked() == 1:
            include_soc_par1 = 1
            social_par1_name = str(self.ui.soc_par1_box.text())
            self.module.setParameterValue("social_par1_name", social_par1_name)
        else:
            include_soc_par1 = 0
        self.module.setParameterValue("include_soc_par1", str(include_soc_par1))
        
        if self.ui.soc_par2_check.isChecked() == 1:
            include_soc_par2 = 1
            social_par2_name = str(self.ui.soc_par2_box.text())
            self.module.setParameterValue("social_par2_name", social_par2_name)
        else:
            include_soc_par2 = 0
        self.module.setParameterValue("include_soc_par2", str(include_soc_par2))
        
        #----------------------------------------------------------------------#
        #-------- MAP CONNECTIVITY PARAMETERS----------------------------------#
        #----------------------------------------------------------------------#
        if self.ui.radioMoore.isChecked() == True:
            neighbourhood = "M"
        if self.ui.radioVNeum.isChecked() == True:
            neighbourhood = "N"
        self.module.setParameterValue("Neighbourhood", neighbourhood)
        
        if self.ui.neighb_vnfp_check.isChecked() == 1:
            vn4FlowPaths = 1
        else:
            vn4FlowPaths = 0
        self.module.setParameterValue("vn4FlowPaths", str(vn4FlowPaths))
        
        if self.ui.neighb_vnpd_check.isChecked() == 1:
            vn4Patches = 1
        else:
            vn4Patches = 0
        self.module.setParameterValue("vn4Patches", str(vn4Patches))
        
        #Combo Box
        flow_path_matrix = ["DI", "D8"]
        flow_pathindex = self.ui.flowpath_combo.currentIndex()
        flow_method = flow_path_matrix[flow_pathindex]
        self.module.setParameterValue("flow_method", flow_method)
        
        if self.ui.demsmooth_check.isChecked() == 1:
            demsmooth_choose = 1
        else:
            demsmooth_choose = 0
        self.module.setParameterValue("demsmooth_choose", str(demsmooth_choose))
        
        demsmooth_passes = str(self.ui.demsmooth_spin.value())
        self.module.setParameterValue("demsmooth_passes", demsmooth_passes)
        
        if self.ui.delinbasin_check.isChecked() == 1:
            basinlimit = 1
        else:
            basinlimit = 0
        self.module.setParameterValue("basinlimit", str(basinlimit))
        
        basinAmax = str(self.ui.delinbasin_box.text())
        self.module.setParameterValue("basinAmax", basinAmax)
        
        #CONCEPTUAL NETWORKS Checkboxes
        
        
