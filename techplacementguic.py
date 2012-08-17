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
import os

from PyQt4 import QtCore, QtGui
from pyvibe import *
from techplacementgui import Ui_TechPlace_Dialog

class activatetechplacementGUI(QtGui.QDialog):
    def __init__(self, m, parent=None):
        self.module = Module
        self.module = m
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_TechPlace_Dialog()
        self.ui.setupUi(self)
    
        #Assign Default Values & Connect Signal/Slots
        
        #######################################
        #General Strategy Tab
        #######################################
        #----------------------------------------------------------------------#
        #-------- DESIGN RATIONALE --------------------------------------------#
        #----------------------------------------------------------------------#
        if self.module.getParameterAsString("ration_runoff") == "1":
            self.ui.ration_runoff_check.setChecked(1)
        else:
            self.ui.ration_runoff_check.setChecked(0)
        
        if self.module.getParameterAsString("ration_pollute") == "1":
            self.ui.ration_pollute_check.setChecked(1)
        else:
            self.ui.ration_pollute_check.setChecked(0)
        
        if self.module.getParameterAsString("ration_harvest") == "1":
            self.ui.ration_harvest_check.setChecked(1)
        else:
            self.ui.ration_harvest_check.setChecked(0)
        
        self.ui.runoff_pri_spin.setValue(int(self.module.getParameterAsString("runoff_pri")))
        self.ui.pollute_pri_spin.setValue(int(self.module.getParameterAsString("pollute_pri")))
        self.ui.harvest_pri_spin.setValue(int(self.module.getParameterAsString("harvest_pri")))
        
        #----------------------------------------------------------------------#
        #-------- MANAGEMENT TARGETS ------------------------------------------#
        #----------------------------------------------------------------------#
        self.ui.targets_runoff_spin.setValue(float(self.module.getParameterAsString("targets_runoff")))
        self.ui.targets_TSS_spin.setValue(float(self.module.getParameterAsString("targets_TSS")))
        self.ui.targets_TN_spin.setValue(float(self.module.getParameterAsString("targets_TN")))
        self.ui.targets_TP_spin.setValue(float(self.module.getParameterAsString("targets_TP")))
        self.ui.targets_reuse_spin.setValue(float(self.module.getParameterAsString("targets_harvest")))
        
        if self.module.getParameterAsString("runoff_auto") == "1":
            self.ui.targets_runoff_auto.setChecked(1)
        else:
            self.ui.targets_runoff_auto.setChecked(0)
        
        if self.module.getParameterAsString("TSS_auto") == "1":
            self.ui.targets_TSS_auto.setChecked(1)
        else:
            self.ui.targets_TSS_auto.setChecked(0)

        if self.module.getParameterAsString("TN_auto") == "1":
            self.ui.targets_TN_auto.setChecked(1)
        else:
            self.ui.targets_TN_auto.setChecked(0)
        
        if self.module.getParameterAsString("TP_auto") == "1":
            self.ui.targets_TP_auto.setChecked(1)
        else:
            self.ui.targets_TP_auto.setChecked(0)
        
        if self.module.getParameterAsString("harvest_auto") == "1":
            self.ui.targets_reuse_auto.setChecked(1)
        else:
            self.ui.targets_reuse_auto.setChecked(0)
        
        #----------------------------------------------------------------------#
        #-------- STRATEGY SETUP ----------------------------------------------#
        #----------------------------------------------------------------------#
        if self.module.getParameterAsString("strategy_lot_check") == "1":
            self.ui.strategy_lot_check.setChecked(1)
        else:
            self.ui.strategy_lot_check.setChecked(0)
        
        self.ui.strategy_lot_spin.setValue(float(self.module.getParameterAsString("lot_increment")))
        
        if self.module.getParameterAsString("strategy_street_check") == "1":
            self.ui.strategy_str_check.setChecked(1)
        else:
            self.ui.strategy_str_check.setChecked(0)
        
        self.ui.strategy_str_spin.setValue(float(self.module.getParameterAsString("street_increment")))
        
        if self.module.getParameterAsString("strategy_neigh_check") == "1":
            self.ui.strategy_neigh_check.setChecked(1)
        else:
            self.ui.strategy_neigh_check.setChecked(0)
        
        self.ui.strategy_neigh_spin.setValue(float(self.module.getParameterAsString("neigh_increment")))
        
        if self.module.getParameterAsString("strategy_prec_check") == "1":
            self.ui.strategy_prec_check.setChecked(1)
        else:
            self.ui.strategy_prec_check.setChecked(0)
        
        self.ui.strategy_prec_spin.setValue(float(self.module.getParameterAsString("prec_increment")))
        
        self.ui.basin_target_min_box.setText(self.module.getParameterAsString("basin_target_min"))
        self.ui.basin_target_max_box.setText(self.module.getParameterAsString("basin_target_max"))
        
        #SPECIAL CASES STRATEGIES
        if self.module.getParameterAsString("strategy_specific1") == "1":
            self.ui.strategy_specific1_check.setChecked(1)
        else:
            self.ui.strategy_specific1_check.setChecked(0)
            
        if self.module.getParameterAsString("strategy_specific2") == "1":
            self.ui.strategy_specific2_check.setChecked(1)
        else:
            self.ui.strategy_specific2_check.setChecked(0)
        
        if self.module.getParameterAsString("strategy_specific3") == "1":
            self.ui.strategy_specific3_check.setChecked(1)
        else:
            self.ui.strategy_specific3_check.setChecked(0)
        
        if self.module.getParameterAsString("strategy_specific4") == "1":
            self.ui.strategy_specific4_check.setChecked(1)
        else:
            self.ui.strategy_specific4_check.setChecked(0)
            
        if self.module.getParameterAsString("strategy_specific5") == "1":
            self.ui.strategy_specific5_check.setChecked(1)
        else:
            self.ui.strategy_specific5_check.setChecked(0)
        
        if self.module.getParameterAsString("strategy_specific6") == "1":
            self.ui.strategy_specific6_check.setChecked(1)
        else:
            self.ui.strategy_specific6_check.setChecked(0)
        
        
        #######################################
        #Retrofit Tab
        #######################################
        if self.module.getParameterAsString("retrofit_scenario") == "N":
            self.ui.area_retrofit_combo.setCurrentIndex(0)
            self.ui.lot_renew_check.setEnabled(0)
            self.ui.lot_decom_check.setEnabled(0)
            self.ui.street_decom_check.setEnabled(0)
            self.ui.street_renew_check.setEnabled(0)
            self.ui.neigh_renew_check.setEnabled(0)
            self.ui.neigh_decom_check.setEnabled(0)
            self.ui.prec_renew_check.setEnabled(0)
            self.ui.prec_decom_check.setEnabled(0)
            self.ui.decom_slider.setEnabled(0)
            self.ui.decom_box.setEnabled(0)
            self.ui.renew_slider.setEnabled(0)
            self.ui.renew_box.setEnabled(0)
            self.ui.radioKeep.setEnabled(0)
            self.ui.radioDecom.setEnabled(0)
        elif self.module.getParameterAsString("retrofit_scenario") == "R":
            self.ui.area_retrofit_combo.setCurrentIndex(1)
            self.ui.lot_renew_check.setEnabled(1)
            self.ui.lot_decom_check.setEnabled(1)
            self.ui.street_decom_check.setEnabled(1)
            self.ui.street_renew_check.setEnabled(1)
            self.ui.neigh_renew_check.setEnabled(1)
            self.ui.neigh_decom_check.setEnabled(1)
            self.ui.prec_renew_check.setEnabled(1)
            self.ui.prec_decom_check.setEnabled(1)
            self.ui.decom_slider.setEnabled(1)
            self.ui.decom_box.setEnabled(1)
            self.ui.renew_slider.setEnabled(1)
            self.ui.renew_box.setEnabled(1)
            self.ui.radioKeep.setEnabled(1)
            self.ui.radioDecom.setEnabled(1)
        elif self.module.getParameterAsString("retrofit_scenario") == "F":
            self.ui.area_retrofit_combo.setCurrentIndex(2)
            self.ui.lot_renew_check.setEnabled(1)
            self.ui.lot_decom_check.setEnabled(1)
            self.ui.street_decom_check.setEnabled(1)
            self.ui.street_renew_check.setEnabled(1)
            self.ui.neigh_renew_check.setEnabled(1)
            self.ui.neigh_decom_check.setEnabled(1)
            self.ui.prec_renew_check.setEnabled(1)
            self.ui.prec_decom_check.setEnabled(1)
            self.ui.decom_slider.setEnabled(1)
            self.ui.decom_box.setEnabled(1)
            self.ui.renew_slider.setEnabled(1)
            self.ui.renew_box.setEnabled(1)
            self.ui.radioKeep.setEnabled(1)
            self.ui.radioDecom.setEnabled(1)
        
        if self.module.getParameterAsString("renewal_cycle_def") == "1":
            self.ui.retrofit_renewal_check.setChecked(1)
        else:
            self.ui.retrofit_renewal_check.setChecked(0)
        
        self.ui.renewal_lot_years.setValue(float(self.module.getParameterAsString("renewal_lot_years")))
        self.ui.renewal_lot_spin.setValue(float(self.module.getParameterAsString("renewal_lot_perc")))
        self.ui.renewal_street_years.setValue(float(self.module.getParameterAsString("renewal_street_years")))
        self.ui.renewal_neigh_years.setValue(float(self.module.getParameterAsString("renewal_neigh_years")))
        
        if self.module.getParameterAsString("force_street") == "1":
            self.ui.retrofit_forced_street_check.setChecked(1)
        else:
            self.ui.retrofit_forced_street_check.setChecked(0)
        
        if self.module.getParameterAsString("force_neigh") == "1":
            self.ui.retrofit_forced_neigh_check.setChecked(1)
        else:
            self.ui.retrofit_forced_neigh_check.setChecked(0)
        
        if self.module.getParameterAsString("force_prec") == "1":
            self.ui.retrofit_forced_prec_check.setChecked(1)
        else:
            self.ui.retrofit_forced_prec_check.setChecked(0)
        
        
        if self.module.getParameterAsString("lot_renew") == "1":
            self.ui.lot_renew_check.setChecked(1)
        else:
            self.ui.lot_renew_check.setChecked(0)
        
        if self.module.getParameterAsString("lot_decom") == "1":
            self.ui.lot_decom_check.setChecked(1)
        else:
            self.ui.lot_decom_check.setChecked(0)
        
        if self.module.getParameterAsString("street_renew") == "1":
            self.ui.street_renew_check.setChecked(1)
        else:
            self.ui.street_renew_check.setChecked(0)
        
        if self.module.getParameterAsString("street_decom") == "1":
            self.ui.street_decom_check.setChecked(1)
        else:
            self.ui.street_decom_check.setChecked(0)
        
        if self.module.getParameterAsString("neigh_renew") == "1":
            self.ui.neigh_renew_check.setChecked(1)
        else:
            self.ui.neigh_renew_check.setChecked(0)
        
        if self.module.getParameterAsString("neigh_decom") == "1":
            self.ui.neigh_decom_check.setChecked(1)
        else:
            self.ui.neigh_decom_check.setChecked(0)
        
        if self.module.getParameterAsString("prec_renew") == "1":
            self.ui.prec_renew_check.setChecked(1)
        else:
            self.ui.prec_renew_check.setChecked(0)
        
        if self.module.getParameterAsString("prec_decom") == "1":
            self.ui.prec_decom_check.setChecked(1)
        else:
            self.ui.prec_decom_check.setChecked(0)
        
        self.ui.decom_slider.setValue(int(self.module.getParameterAsString("decom_thresh")))
        self.ui.decom_box.setText(self.module.getParameterAsString("decom_thresh")+"%")
        self.ui.renew_slider.setValue(int(self.module.getParameterAsString("renewal_thresh")))
        self.ui.renew_box.setText(self.module.getParameterAsString("renewal_thresh")+"%")
        QtCore.QObject.connect(self.ui.decom_slider, QtCore.SIGNAL("valueChanged(int)"), self.decom_update)
        QtCore.QObject.connect(self.ui.renew_slider, QtCore.SIGNAL("valueChanged(int)"), self.renew_update)
        
        if self.module.getParameterAsString("renewal_alternative") == "K":
            self.ui.radioKeep.setChecked(True)
        if self.module.getParameterAsString("renewal_alternative") == "D":
            self.ui.radioDecom.setChecked(True)
        
        QtCore.QObject.connect(self.ui.area_retrofit_combo, QtCore.SIGNAL("currentIndexChanged(int)"), self.update_retrofitoptions)
        
        #######################################
        #Choose & Customize Technologies Tab
        #######################################
        
        #----------------------------------------------------------------------#
        #--------- Advanced Stormwater Harvesting Plant -----------------------#
        #----------------------------------------------------------------------#
        if self.module.getParameterAsString("ASHPstatus") == "1": 
            self.ui.ASHPstatus_box.setChecked(1)
        else:
            self.ui.ASHPstatus_box.setChecked(0)
        
        self.ui.ASHPtl_spin.setValue(float(self.module.getParameterAsString("ASHPlevel")))
        self.ui.ASHPtg_spin.setValue(float(self.module.getParameterAsString("ASHPgroup")))
        
        #----------------------------------------------------------------------#
        #--------- Aquaculture/LivingSystems ----------------------------------#
        #----------------------------------------------------------------------#
        if self.module.getParameterAsString("AQstatus") == "1": 
            self.ui.AQstatus_box.setChecked(1)
        else:
            self.ui.AQstatus_box.setChecked(0)
        
        self.ui.AQtl_spin.setValue(float(self.module.getParameterAsString("AQlevel")))
        self.ui.AQtg_spin.setValue(float(self.module.getParameterAsString("AQgroup")))
        
        #----------------------------------------------------------------------#
        #--------- Aquifer Storage/Recovery -----------------------------------#
        #----------------------------------------------------------------------#
        if self.module.getParameterAsString("ASRstatus") == "1":
            self.ui.ASRstatus_box.setChecked(1)
        else:
            self.ui.ASRstatus_box.setChecked(0)
        
        self.ui.ASRtl_spin.setValue(float(self.module.getParameterAsString("ASRlevel")))
        self.ui.ASRtg_spin.setValue(float(self.module.getParameterAsString("ASRgroup")))
        
        #----------------------------------------------------------------------#
        #--------- Biofiltration/Raingardens ----------------------------------################################################################
        #----------------------------------------------------------------------#
        if self.module.getParameterAsString("BFstatus") == "1":
            self.ui.BFstatus_box.setChecked(1)
        else:
            self.ui.BFstatus_box.setChecked(0)
        
        self.ui.BFtl_spin.setValue(float(self.module.getParameterAsString("BFlevel")))
        self.ui.BFtg_spin.setValue(float(self.module.getParameterAsString("BFgroup")))
        
        #Available Scales
        if self.module.getParameterAsString("BFlot") == "1":
            self.ui.BFlot_check.setChecked(1)
        else:
            self.ui.BFlot_check.setChecked(0)
        
        if self.module.getParameterAsString("BFstreet") == "1":
            self.ui.BFstreet_check.setChecked(1)
        else:
            self.ui.BFstreet_check.setChecked(0)
        
        if self.module.getParameterAsString("BFneigh") == "1":
            self.ui.BFneigh_check.setChecked(1)
        else:
            self.ui.BFneigh_check.setChecked(0)
        
        if self.module.getParameterAsString("BFprec") == "1":
            self.ui.BFprec_check.setChecked(1)
        else:
            self.ui.BFprec_check.setChecked(0)
        
        #Available Applications
        if self.module.getParameterAsString("BFpollute") == "1":
            self.ui.BFpollute_check.setChecked(1)
        else:
            self.ui.BFpollute_check.setChecked(0)
        
        #Design Curves
        if self.module.getParameterAsString("BFdesignUB") == "1":
            self.ui.BFdesignUB_box.setChecked(1)
        else:
            self.ui.BFdesignUB_box.setChecked(0)
        
        if self.module.getParameterAsString("BFdesignUB") == "1":
            self.ui.BFdesignUB_box.setChecked(1)
            self.ui.BFdesigncurve_browse.setEnabled(0)
            self.ui.BFdesigncurve_pathbox.setText("no file")
        else:
            self.ui.BFdesignUB_box.setChecked(0)
            self.ui.BFdesigncurve_browse.setEnabled(1)
            self.ui.BFdesigncurve_pathbox.setText(self.module.getParameterAsString("BFdescur_path"))
        
        QtCore.QObject.connect(self.ui.BFdesigncurve_browse, QtCore.SIGNAL("clicked()"), self.openFileDialog_BF)
        QtCore.QObject.connect(self.ui.BFdesignUB_box, QtCore.SIGNAL("clicked()"), self.BFdesign_enable)
        
        #Design Information
        
        #COMBO BOXES CONTAINING EDD AND FD SPECS
        if self.module.getParameterAsString("BFspec_EDD") == "0":
            self.ui.BFspecs_EDD_combo.setCurrentIndex(0)
        elif self.module.getParameterAsString("BFspec_EDD") == "0.1":
            self.ui.BFspecs_EDD_combo.setCurrentIndex(1)
        elif self.module.getParameterAsString("BFspec_EDD") == "0.2":
            self.ui.BFspecs_EDD_combo.setCurrentIndex(2)
        elif self.module.getParameterAsString("BFspec_EDD") == "0.3":
            self.ui.BFspecs_EDD_combo.setCurrentIndex(3)
        elif self.module.getParameterAsString("BFspec_EDD") == "0.4":
            self.ui.BFspecs_EDD_combo.setCurrentIndex(4)
        
        if self.module.getParameterAsString("BFspec_FD") == "0.2":
            self.ui.BFspecs_FD_combo.setCurrentIndex(0)
        elif self.module.getParameterAsString("BFspec_FD") == "0.4":
            self.ui.BFspecs_FD_combo.setCurrentIndex(1)
        elif self.module.getParameterAsString("BFspec_FD") == "0.6":
            self.ui.BFspecs_FD_combo.setCurrentIndex(2)
        elif self.module.getParameterAsString("BFspec_FD") == "0.8":
            self.ui.BFspecs_FD_combo.setCurrentIndex(3)
        
        self.ui.BFmaxsize_box.setText(self.module.getParameterAsString("BFmaxsize"))
        self.ui.BFavglifespin.setValue(float(self.module.getParameterAsString("BFavglife")))
        
        if self.module.getParameterAsString("BFlined") == "1":
            self.ui.BFlined_check.setChecked(1)
        else:
            self.ui.BFlined_check.setChecked(0)
        
        #futher design info coming soon
        
        #----------------------------------------------------------------------#
        #--------- Green Roof -------------------------------------------------#
        #----------------------------------------------------------------------#
        if self.module.getParameterAsString("GRstatus") == "1":
            self.ui.GRstatus_box.setChecked(1)
        else:
            self.ui.GRstatus_box.setChecked(0)
        
        self.ui.GRtl_spin.setValue(float(self.module.getParameterAsString("GRlevel")))
        self.ui.GRtg_spin.setValue(float(self.module.getParameterAsString("GRgroup")))
        
        #----------------------------------------------------------------------#
        #--------- Greywater Tank/Treatment -----------------------------------#
        #----------------------------------------------------------------------#
        if self.module.getParameterAsString("GTstatus") == "1":
            self.ui.GTstatus_box.setChecked(1)
        else:
            self.ui.GTstatus_box.setChecked(0)
        
        self.ui.GTtl_spin.setValue(float(self.module.getParameterAsString("GTlevel")))
        self.ui.GTtg_spin.setValue(float(self.module.getParameterAsString("GTgroup")))
        
        #----------------------------------------------------------------------#
        #--------- Gross Pollutant Trap ---------------------------------------#
        #----------------------------------------------------------------------#
        if self.module.getParameterAsString("GPTstatus") == "1":
            self.ui.GPTstatus_box.setChecked(1)
        else:
            self.ui.GPTstatus_box.setChecked(0)
        
        self.ui.GPTtl_spin.setValue(float(self.module.getParameterAsString("GPTlevel")))
        self.ui.GPTtg_spin.setValue(float(self.module.getParameterAsString("GPTgroup")))
        
        #----------------------------------------------------------------------#
        #--------- Infiltration System ----------------------------------------################################################################
        #----------------------------------------------------------------------#
        if self.module.getParameterAsString("ISstatus") == "1":
            self.ui.ISstatus_box.setChecked(1)
        else:
            self.ui.ISstatus_box.setChecked(0)
        
        self.ui.IStl_spin.setValue(float(self.module.getParameterAsString("ISlevel")))
        self.ui.IStg_spin.setValue(float(self.module.getParameterAsString("ISgroup")))
        
        #Available Scales
        if self.module.getParameterAsString("ISlot") == "1":
            self.ui.ISlot_check.setChecked(1)
        else:
            self.ui.ISlot_check.setChecked(0)
        
        if self.module.getParameterAsString("ISstreet") == "1":
            self.ui.ISstreet_check.setChecked(1)
        else:
            self.ui.ISstreet_check.setChecked(0)
        
        if self.module.getParameterAsString("ISneigh") == "1":
            self.ui.ISneigh_check.setChecked(1)
        else:
            self.ui.ISneigh_check.setChecked(0)
        
        #Available Applications
        if self.module.getParameterAsString("ISflow") == "1":
            self.ui.ISflow_check.setChecked(1)
        else:
            self.ui.ISflow_check.setChecked(0)
            
        if self.module.getParameterAsString("ISpollute") == "1":
            self.ui.ISpollute_check.setChecked(1)
        else:
            self.ui.ISpollute_check.setChecked(0)
        
        #Design Curves
        if self.module.getParameterAsString("ISdesignUB") == "1":
            self.ui.ISdesignUB_box.setChecked(1)
            self.ui.ISdesigncurve_browse.setEnabled(0)
            self.ui.ISdesigncurve_pathbox.setText("no file")
        else:
            self.ui.ISdesignUB_box.setChecked(0)
            self.ui.ISdesigncurve_browse.setEnabled(1)
            self.ui.ISdesigncurve_pathbox.setText(self.module.getParameterAsString("ISdescur_path"))
        
        QtCore.QObject.connect(self.ui.ISdesigncurve_browse, QtCore.SIGNAL("clicked()"), self.openFileDialog_IS)
        QtCore.QObject.connect(self.ui.ISdesignUB_box, QtCore.SIGNAL("clicked()"), self.ISdesign_enable)
        
        #Design Information
        
        #COMBO BOXES CONTAINING EDD AND FD SPECS
        if self.module.getParameterAsString("ISspec_EDD") == "0.1":
            self.ui.ISspecs_EDD_combo.setCurrentIndex(0)
        elif self.module.getParameterAsString("ISspec_EDD") == "0.2":
            self.ui.ISspecs_EDD_combo.setCurrentIndex(1)
        elif self.module.getParameterAsString("ISspec_EDD") == "0.3":
            self.ui.ISspecs_EDD_combo.setCurrentIndex(2)
        elif self.module.getParameterAsString("ISspec_EDD") == "0.4":
            self.ui.ISspecs_EDD_combo.setCurrentIndex(3)
        
        if self.module.getParameterAsString("ISspec_FD") == "0.2":
            self.ui.ISspecs_FD_combo.setCurrentIndex(0)
        elif self.module.getParameterAsString("ISspec_FD") == "0.4":
            self.ui.ISspecs_FD_combo.setCurrentIndex(1)
        elif self.module.getParameterAsString("ISspec_FD") == "0.6":
            self.ui.ISspecs_FD_combo.setCurrentIndex(2)
        elif self.module.getParameterAsString("ISspec_FD") == "0.8":
            self.ui.ISspecs_FD_combo.setCurrentIndex(3)
        
        self.ui.ISmaxsize_box.setText(self.module.getParameterAsString("ISmaxsize"))
        self.ui.ISavglifespin.setValue(float(self.module.getParameterAsString("ISavglife")))

        if self.module.getParameterAsString("IS_2Dmodel") == "1":
            self.ui.IS_2Dmodel_box.setChecked(1)
        else:
            self.ui.IS_2Dmodel_box.setChecked(0)
        
        #futher design info coming soon
        
        #----------------------------------------------------------------------#
        #--------- Packaged Plant ---------------------------------------------#
        #----------------------------------------------------------------------#
        if self.module.getParameterAsString("PPLstatus") == "1":
            self.ui.PPLstatus_box.setChecked(1)
        else:
            self.ui.PPLstatus_box.setChecked(0)
        
        self.ui.PPLtl_spin.setValue(float(self.module.getParameterAsString("PPLlevel")))
        self.ui.PPLtg_spin.setValue(float(self.module.getParameterAsString("PPLgroup")))
        
        #----------------------------------------------------------------------#
        #--------- Ponds/Sedimentation Basin ----------------------------------################################################################
        #----------------------------------------------------------------------#
        if self.module.getParameterAsString("PBstatus") == "1":
            self.ui.PBstatus_box.setChecked(1)
        else:
            self.ui.PBstatus_box.setChecked(0)
        
        self.ui.PBtl_spin.setValue(float(self.module.getParameterAsString("PBlevel")))
        self.ui.PBtg_spin.setValue(float(self.module.getParameterAsString("PBgroup")))
        
        #Available Scales
        if self.module.getParameterAsString("PBneigh") == "1":
            self.ui.PBneigh_check.setChecked(1)
        else:
            self.ui.PBneigh_check.setChecked(0)
        
        if self.module.getParameterAsString("PBprec") == "1":
            self.ui.PBprec_check.setChecked(1)
        else:
            self.ui.PBprec_check.setChecked(0)
        
        #Available Applications
        if self.module.getParameterAsString("PBflow") == "1":
            self.ui.PBflow_check.setChecked(1)
        else:
            self.ui.PBflow_check.setChecked(0)
            
        if self.module.getParameterAsString("PBpollute") == "1":
            self.ui.PBpollute_check.setChecked(1)
        else:
            self.ui.PBpollute_check.setChecked(0)
        
        #Design Curves
        if self.module.getParameterAsString("PBdesignUB") == "1":
            self.ui.PBdesignUB_box.setChecked(1)
        else:
            self.ui.PBdesignUB_box.setChecked(0)
        
        if self.module.getParameterAsString("PBdesignUB") == "1":
            self.ui.PBdesignUB_box.setChecked(1)
            self.ui.PBdesigncurve_browse.setEnabled(0)
            self.ui.PBdesigncurve_pathbox.setText("no file")
        else:
            self.ui.PBdesignUB_box.setChecked(0)
            self.ui.PBdesigncurve_browse.setEnabled(1)
            self.ui.PBdesigncurve_pathbox.setText(self.module.getParameterAsString("PBdescur_path"))
        
        QtCore.QObject.connect(self.ui.PBdesigncurve_browse, QtCore.SIGNAL("clicked()"), self.openFileDialog_PB)
        QtCore.QObject.connect(self.ui.PBdesignUB_box, QtCore.SIGNAL("clicked()"), self.PBdesign_enable)
        
        #Design Information
        
        #combo box with specs
        if self.module.getParameterAsString("PBspec_MD") == "0.25":
            self.ui.PBspecs_combo.setCurrentIndex(0)
        elif self.module.getParameterAsString("PBspec_MD") == "0.50":
            self.ui.PBspecs_combo.setCurrentIndex(1)
        elif self.module.getParameterAsString("PBspec_MD") == "0.75":
            self.ui.PBspecs_combo.setCurrentIndex(2)
        elif self.module.getParameterAsString("PBspec_MD") == "1.00":
            self.ui.PBspecs_combo.setCurrentIndex(3)
        elif self.module.getParameterAsString("PBspec_MD") == "1.25":
            self.ui.PBspecs_combo.setCurrentIndex(4)    
        
        self.ui.PBmaxsize_box.setText(self.module.getParameterAsString("PBmaxsize"))
        self.ui.PBavglifespin.setValue(float(self.module.getParameterAsString("PBavglife")))

        #futher design info coming soon
        
        #----------------------------------------------------------------------#
        #---------- Porous/Pervious Pavement ----------------------------------#
        #----------------------------------------------------------------------#
        if self.module.getParameterAsString("PPstatus") == "1":
            self.ui.PPstatus_box.setChecked(1)
        else:
            self.ui.PPstatus_box.setChecked(0)
        
        self.ui.PPtl_spin.setValue(float(self.module.getParameterAsString("PPlevel")))
        self.ui.PPtg_spin.setValue(float(self.module.getParameterAsString("PPgroup")))
        
        #----------------------------------------------------------------------#
        #---------- Rainwater Tank --------------------------------------------#
        #----------------------------------------------------------------------#
        if self.module.getParameterAsString("RTstatus") == "1":
            self.ui.RTstatus_box.setChecked(1)
        else:
            self.ui.RTstatus_box.setChecked(0)
        
        self.ui.RTtl_spin.setValue(float(self.module.getParameterAsString("RTlevel")))
        self.ui.RTtg_spin.setValue(float(self.module.getParameterAsString("RTgroup")))
        
        self.ui.RT_maxdepth_box.setText(self.module.getParameterAsString("RT_maxdepth"))
        self.ui.RT_mindead_box.setText(self.module.getParameterAsString("RT_mindead"))
        self.ui.RT_firstflush_box.setText(self.module.getParameterAsString("RT_firstflush"))
        
        if self.module.getParameterAsString("RTscale_lot") == "1":
            self.ui.RTscale_lot_box.setChecked(1)
        else:
            self.ui.RTscale_lot_box.setChecked(0)
        
        if self.module.getParameterAsString("RTscale_street") == "1":
            self.ui.RTscale_street_box.setChecked(1)
        else:
            self.ui.RTscale_street_box.setChecked(0)
                
        if self.module.getParameterAsString("RTpurp_flood") == "1":
            self.ui.RTpurp_flood_box.setChecked(1)
        else:
            self.ui.RTpurp_flood_box.setChecked(0)
        
        if self.module.getParameterAsString("RTpurp_recyc") == "1":
            self.ui.RTpurp_recyc_box.setChecked(1)
        else:
            self.ui.RTpurp_recyc_box.setChecked(0)
        
        if self.module.getParameterAsString("RT_shape_circ") == "1":
            self.ui.RT_shape_circ_check.setChecked(1)
        else:
            self.ui.RT_shape_circ_check.setChecked(0)
        
        if self.module.getParameterAsString("RT_shape_rect") == "1":
            self.ui.RT_shape_rect_check.setChecked(1)
        else:
            self.ui.RT_shape_rect_check.setChecked(0)
        
        if self.module.getParameterAsString("RT_sbmodel") == "ybs":
            self.ui.RT_sbmodel_ybs_radio.setChecked(True)
        if self.module.getParameterAsString("RT_sbmodel") == "yas":
            self.ui.RT_sbmodel_yas_radio.setChecked(True)
        
        if self.module.getParameterAsString("RTdesignD4W") == "1":
            self.ui.RTdesignD4W_box.setChecked(1)
            self.ui.RTdesigncurve_browse.setEnabled(0)
            self.ui.RTdesigncurve_pathbox.setText("no file")
        else:
            self.ui.RTdesignD4W_box.setChecked(0)
            self.ui.RTdesigncurve_browse.setEnabled(1)
            self.ui.RTdesigncurve_pathbox.setText(self.module.getParameterAsString("RTdescur_path"))
        
        self.ui.RTavglifespin.setValue(float(self.module.getParameterAsString("RTavglife")))
        
        QtCore.QObject.connect(self.ui.RTdesigncurve_browse, QtCore.SIGNAL("clicked()"), self.openFileDialog_RT)
        QtCore.QObject.connect(self.ui.RTdesignD4W_box, QtCore.SIGNAL("clicked()"), self.RTdesign_enable)
        
        #----------------------------------------------------------------------#
        #---------- Sand/Peat/Gravel Filter -----------------------------------#
        #----------------------------------------------------------------------#
        if self.module.getParameterAsString("SFstatus") == "1":
            self.ui.SFstatus_box.setChecked(1)
        else:
            self.ui.SFstatus_box.setChecked(0)
        
        self.ui.SFtl_spin.setValue(float(self.module.getParameterAsString("SFlevel")))
        self.ui.SFtg_spin.setValue(float(self.module.getParameterAsString("SFgroup")))
        
        #----------------------------------------------------------------------#
        #---------- Septic Tank -----------------------------------------------#
        #----------------------------------------------------------------------#
        if self.module.getParameterAsString("STstatus") == "1":
            self.ui.STstatus_box.setChecked(1)
        else:
            self.ui.STstatus_box.setChecked(0)
        
        self.ui.STtl_spin.setValue(float(self.module.getParameterAsString("STlevel")))
        self.ui.STtg_spin.setValue(float(self.module.getParameterAsString("STgroup")))
        
        #----------------------------------------------------------------------#
        #---------- Subsurface Irrigation System ------------------------------#
        #----------------------------------------------------------------------#
        if self.module.getParameterAsString("IRRstatus") == "1":
            self.ui.IRRstatus_box.setChecked(1)
        else:
            self.ui.IRRstatus_box.setChecked(0)
        
        self.ui.IRRtl_spin.setValue(float(self.module.getParameterAsString("IRRlevel")))
        self.ui.IRRtg_spin.setValue(float(self.module.getParameterAsString("IRRgroup")))
        
        #----------------------------------------------------------------------#
        #---------- Subsurface Wetland/Reed Bed -------------------------------#
        #----------------------------------------------------------------------#
        if self.module.getParameterAsString("WSUBstatus") == "1":
            self.ui.WSUBstatus_box.setChecked(1)
        else:
            self.ui.WSUBstatus_box.setChecked(0)
        
        self.ui.WSUBtl_spin.setValue(float(self.module.getParameterAsString("WSUBlevel")))
        self.ui.WSUBtg_spin.setValue(float(self.module.getParameterAsString("WSUBgroup")))
        
        #----------------------------------------------------------------------#
        #---------- Surface Wetland -------------------------------------------################################################################
        #----------------------------------------------------------------------#
        if self.module.getParameterAsString("WSURstatus") == "1":
            self.ui.WSURstatus_box.setChecked(1)
        else:
            self.ui.WSURstatus_box.setChecked(0)
        
        self.ui.WSURtl_spin.setValue(float(self.module.getParameterAsString("WSURlevel")))
        self.ui.WSURtg_spin.setValue(float(self.module.getParameterAsString("WSURgroup")))
        
        #Available Scales
        if self.module.getParameterAsString("WSURneigh") == "1":
            self.ui.WSURneigh_check.setChecked(1)
        else:
            self.ui.WSURneigh_check.setChecked(0)
        
        if self.module.getParameterAsString("PBprec") == "1":
            self.ui.WSURprec_check.setChecked(1)
        else:
            self.ui.WSURprec_check.setChecked(0)
        
        #Available Applications
        if self.module.getParameterAsString("WSURflow") == "1":
            self.ui.WSURflow_check.setChecked(1)
        else:
            self.ui.WSURflow_check.setChecked(0)
            
        if self.module.getParameterAsString("WSURpollute") == "1":
            self.ui.WSURpollute_check.setChecked(1)
        else:
            self.ui.WSURpollute_check.setChecked(0)
        
        #Design Curves
        if self.module.getParameterAsString("WSURdesignUB") == "1":
            self.ui.WSURdesignUB_box.setChecked(1)
        else:
            self.ui.WSURdesignUB_box.setChecked(0)
        
        if self.module.getParameterAsString("WSURdesignUB") == "1":
            self.ui.WSURdesignUB_box.setChecked(1)
            self.ui.WSURdesigncurve_browse.setEnabled(0)
            self.ui.WSURdesigncurve_pathbox.setText("no file")
        else:
            self.ui.WSURdesignUB_box.setChecked(0)
            self.ui.WSURdesigncurve_browse.setEnabled(1)
            self.ui.WSURdesigncurve_pathbox.setText(self.module.getParameterAsString("PBdescur_path"))
        
        QtCore.QObject.connect(self.ui.WSURdesigncurve_browse, QtCore.SIGNAL("clicked()"), self.openFileDialog_WSUR)
        QtCore.QObject.connect(self.ui.WSURdesignUB_box, QtCore.SIGNAL("clicked()"), self.WSURdesign_enable)
        
        #Design Information
        
        #combo box with specs
        if self.module.getParameterAsString("WSURspec_EDD") == "0.25":
            self.ui.WSURspecs_combo.setCurrentIndex(0)
        elif self.module.getParameterAsString("WSURspec_EDD") == "0.50":
            self.ui.WSURspecs_combo.setCurrentIndex(1)
        elif self.module.getParameterAsString("WSURspec_EDD") == "0.75":
            self.ui.WSURspecs_combo.setCurrentIndex(2)
        elif self.module.getParameterAsString("WSURspec_EDD") == "0.25":
            self.ui.WSURspecs_combo.setCurrentIndex(3)
        elif self.module.getParameterAsString("WSURspec_EDD") == "0.50":
            self.ui.WSURspecs_combo.setCurrentIndex(4)  
        elif self.module.getParameterAsString("WSURspec_EDD") == "0.75":
            self.ui.WSURspecs_combo.setCurrentIndex(5)
        
        self.ui.WSURmaxsize_box.setText(self.module.getParameterAsString("WSURmaxsize"))
        self.ui.WSURavglifespin.setValue(float(self.module.getParameterAsString("WSURavglife")))

        #futher design info coming soon
        
        #----------------------------------------------------------------------#
        #---------- Swales/Buffer Strips --------------------------------------################################################################
        #----------------------------------------------------------------------#
        if self.module.getParameterAsString("SWstatus") == "1":
            self.ui.SWstatus_box.setChecked(1)
        else:
            self.ui.SWstatus_box.setChecked(0)
        
        self.ui.SWtl_spin.setValue(float(self.module.getParameterAsString("SWlevel")))
        self.ui.SWtg_spin.setValue(float(self.module.getParameterAsString("SWgroup")))
        
        #Available Scales
        if self.module.getParameterAsString("SWstreet") == "1":
            self.ui.SWstreet_check.setChecked(1)
        else:
            self.ui.SWstreet_check.setChecked(0)
        
        #Available Applications
        if self.module.getParameterAsString("SWflow") == "1":
            self.ui.SWflow_check.setChecked(1)
        else:
            self.ui.SWflow_check.setChecked(0)
            
        if self.module.getParameterAsString("SWpollute") == "1":
            self.ui.SWpollute_check.setChecked(1)
        else:
            self.ui.SWpollute_check.setChecked(0)
        
        #Design Curves
        if self.module.getParameterAsString("SWdesignUB") == "1":
            self.ui.SWdesignUB_box.setChecked(1)
        else:
            self.ui.SWdesignUB_box.setChecked(0)
        
        if self.module.getParameterAsString("SWdesignUB") == "1":
            self.ui.SWdesignUB_box.setChecked(1)
            self.ui.SWdesigncurve_browse.setEnabled(0)
            self.ui.SWdesigncurve_pathbox.setText("no file")
        else:
            self.ui.SWdesignUB_box.setChecked(0)
            self.ui.SWdesigncurve_browse.setEnabled(1)
            self.ui.SWdesigncurve_pathbox.setText(self.module.getParameterAsString("SWdescur_path"))
        
        QtCore.QObject.connect(self.ui.SWdesigncurve_browse, QtCore.SIGNAL("clicked()"), self.openFileDialog_SW)
        QtCore.QObject.connect(self.ui.SWdesignUB_box, QtCore.SIGNAL("clicked()"), self.SWdesign_enable)
        
        #Design Information
        
        #combo box with specs
        self.ui.SWmaxsize_box.setText(self.module.getParameterAsString("SWmaxsize"))
        self.ui.SWavglifespin.setValue(float(self.module.getParameterAsString("SWavglife")))

        #futher design info coming soon
        
        #----------------------------------------------------------------------#
        #--------- Tree Pits --------------------------------------------------#
        #----------------------------------------------------------------------#
        if self.module.getParameterAsString("TPSstatus") == "1": 
            self.ui.TPSstatus_box.setChecked(1)
        else:
            self.ui.TPSstatus_box.setChecked(0)
        
        self.ui.TPStl_spin.setValue(float(self.module.getParameterAsString("TPSlevel")))
        self.ui.TPStg_spin.setValue(float(self.module.getParameterAsString("TPSgroup")))
        
        #----------------------------------------------------------------------#
        #---------- Urine-Separation Toilets ----------------------------------#
        #----------------------------------------------------------------------#
        if self.module.getParameterAsString("UTstatus") == "1":
            self.ui.UTstatus_box.setChecked(1)
        else:
            self.ui.UTstatus_box.setChecked(0)
        
        self.ui.UTtl_spin.setValue(float(self.module.getParameterAsString("UTlevel")))
        self.ui.UTtg_spin.setValue(float(self.module.getParameterAsString("UTgroup")))
        
        #----------------------------------------------------------------------#
        #---------- Wastewater Recovery/Recycling Plant -----------------------#
        #----------------------------------------------------------------------#
        if self.module.getParameterAsString("WWRRstatus") == "1":
            self.ui.WWRRstatus_box.setChecked(1)
        else:
            self.ui.WWRRstatus_box.setChecked(0)
        
        self.ui.WWRRtl_spin.setValue(float(self.module.getParameterAsString("WWRRlevel")))
        self.ui.WWRRtg_spin.setValue(float(self.module.getParameterAsString("WWRRgroup")))
        
        #----------------------------------------------------------------------#
        #---------- Waterless/Composting Toilet -------------------------------#
        #----------------------------------------------------------------------#
        if self.module.getParameterAsString("WTstatus") == "1":
            self.ui.WTstatus_box.setChecked(1)
        else:
            self.ui.WTstatus_box.setChecked(0)
        
        self.ui.WTtl_spin.setValue(float(self.module.getParameterAsString("WTlevel")))
        self.ui.WTtg_spin.setValue(float(self.module.getParameterAsString("WTgroup")))
        
        #----------------------------------------------------------------------#
        #---------- Water Efficient Appliances --------------------------------#
        #----------------------------------------------------------------------#
        if self.module.getParameterAsString("WEFstatus") == "1":
            self.ui.WEFstatus_box.setChecked(1)
        else:
            self.ui.WEFstatus_box.setChecked(0)
        
        self.ui.WEFtl_spin.setValue(float(self.module.getParameterAsString("WEFlevel")))
        self.ui.WEFtg_spin.setValue(float(self.module.getParameterAsString("WEFgroup")))
        
        ### NOTE: Not linking Rating System Combo box, AS6400 the only available system currently
        
        self.ui.LEG_minrate_spin.setValue(int(self.module.getParameterAsString("LEG_minrate")))
        self.ui.PPP_likelihood_spin.setValue(int(self.module.getParameterAsString("PPP_likelihood")))
        
        if self.module.getParameterAsString("WEF_implement_method") == "LEG":
            self.ui.WEF_implement_method_combo.setCurrentIndex(0)
        elif self.module.getParameterAsString("WEF_implement_method") == "PPP":
            self.ui.WEF_implement_method_combo.setCurrentIndex(1)
        elif self.module.getParameterAsString("WEF_implement_method") == "SEC":
            self.ui.WEF_implement_method_combo.setCurrentIndex(2)
        elif self.module.getParameterAsString("WEF_implement_method") == "D4W":
            self.ui.WEF_implement_method_combo.setCurrentIndex(3)
        
        if self.module.getParameterAsString("LEG_force") == "1":
            self.ui.LEG_force_check.setChecked(1)
        else:
            self.ui.LEG_force_check.setChecked(0)
            
        if self.module.getParameterAsString("PPP_force") == "1":
            self.ui.PPP_force_check.setChecked(1)
        else:
            self.ui.PPP_force_check.setChecked(0)
        
        if self.module.getParameterAsString("SEC_force") == "1":
            self.ui.SEC_force_check.setChecked(1)
        else:
            self.ui.SEC_force_check.setChecked(0)
        
        if self.module.getParameterAsString("SEC_urbansim") == "1":
            self.ui.SEC_urbansim_check.setChecked(1)
        else:
            self.ui.SEC_urbansim_check.setChecked(0)
            
        if self.module.getParameterAsString("D4W_UDMactive") == "1":
            self.ui.D4W_UDMactive_check.setChecked(1)
        else:
            self.ui.D4W_UDMactive_check.setChecked(0)
        
        if self.module.getParameterAsString("D4W_STMactive") == "1":
            self.ui.D4W_STMactive_check.setChecked(1)
        else:
            self.ui.D4W_STMactive_check.setChecked(0)
        
        if self.module.getParameterAsString("D4W_EVMactive") == "1":
            self.ui.D4W_EVMactive_check.setChecked(1)
        else:
            self.ui.D4W_EVMactive_check.setChecked(0)
        
        if self.module.getParameterAsString("WEF_loc_famhouse") == "1":
            self.ui.WEF_loc_famhouse_check.setChecked(1)
        else:
            self.ui.WEF_loc_famhouse_check.setChecked(0)
        
        if self.module.getParameterAsString("WEF_loc_apart") == "1":
            self.ui.WEF_loc_apart_check.setChecked(1)
        else:
            self.ui.WEF_loc_apart_check.setChecked(0)
            
        if self.module.getParameterAsString("WEF_loc_nonres") == "1":
            self.ui.WEF_loc_nonres_check.setChecked(1)
        else:
            self.ui.WEF_loc_nonres_check.setChecked(0)
        
        if self.module.getParameterAsString("WEF_flow_method") == "M":
            self.ui.WEF_radio_medflow.setChecked(True)
        if self.module.getParameterAsString("WEF_flow_method") == "S":
            self.ui.WEF_radio_stochflow.setChecked(True)
            
        
        #----------------------------------------------------------------------#
        #--- ## --- <TechnologyTitle> -----------------------------------------#
        #----------------------------------------------------------------------#
        #if self.module.getParameterAsString("<abbrev.>status") == "1":
        #    self.ui.<abbrev.>status_box.setChecked(1)
        #else:
        #    self.ui.<abbrev.>status_box.setChecked(0)
            
        #----------------------------------------------------------------------#
        #--- ## --- Regional Information --------------------------------------#
        #----------------------------------------------------------------------#
        if self.module.getParameterAsString("regioncity") == "Adelaide":
            self.ui.regioncity_combo.setCurrentIndex(0)
        elif self.module.getParameterAsString("regioncity") == "Brisbane":
            self.ui.regioncity_combo.setCurrentIndex(1)
        elif self.module.getParameterAsString("regioncity") == "Melbourne":
            self.ui.regioncity_combo.setCurrentIndex(2)
        elif self.module.getParameterAsString("regioncity") == "Perth":
            self.ui.regioncity_combo.setCurrentIndex(3)
        elif self.module.getParameterAsString("regioncity") == "Sydney":
            self.ui.regioncity_combo.setCurrentIndex(4)
        
        #######################################
        #Select Evaluation Criteria Tab
        #######################################
        #----------------------------------------------------------------------#
        #-------- Evaluation Metrics Select------------------------------------#
        #----------------------------------------------------------------------#
        if self.module.getParameterAsString("scoringmatrix_default") == "1":
            self.ui.mca_scoringmat_check.setChecked(1)
            self.ui.mca_scoringmat_browse.setEnabled(0)
            self.ui.mca_scoringmat_box.setText("no file")
            self.ui.bottomlines_techN_spin.setEnabled(0)
            self.ui.bottomlines_envN_spin.setEnabled(0)
            self.ui.bottomlines_ecnN_spin.setEnabled(0)
            self.ui.bottomlines_socN_spin.setEnabled(0)
            self.ui.mca_metrics_check.setEnabled(1)
        else:
            self.ui.mca_scoringmat_check.setChecked(0)
            self.ui.mca_scoringmat_browse.setEnabled(1)
            self.ui.mca_scoringmat_box.setText(self.module.getParameterAsString("scoringmatrix_path"))
            self.ui.bottomlines_techN_spin.setEnabled(1)
            self.ui.bottomlines_envN_spin.setEnabled(1)
            self.ui.bottomlines_ecnN_spin.setEnabled(1)
            self.ui.bottomlines_socN_spin.setEnabled(1)
            self.ui.mca_metrics_check.setEnabled(0)
        
        QtCore.QObject.connect(self.ui.mca_scoringmat_browse, QtCore.SIGNAL("clicked()"), self.openFileDialog_mca)
        QtCore.QObject.connect(self.ui.mca_scoringmat_check, QtCore.SIGNAL("clicked()"), self.mca_scoringmat_enable)
    
        if self.module.getParameterAsString("scoring_include_all") == "1":
            self.ui.mca_metrics_check.setChecked(1)
        else:
            self.ui.mca_metrics_check.setChecked(0)
    
        #----------------------------------------------------------------------#
        #-------- Customize Evaluation Criteria--------------------------------#
        #----------------------------------------------------------------------#
        if self.module.getParameterAsString("bottomlines_tech") == "1":
            self.ui.bottomlines_tech_check.setChecked(1)
        else:
            self.ui.bottomlines_tech_check.setChecked(0)
        
        if self.module.getParameterAsString("bottomlines_env") == "1":
            self.ui.bottomlines_env_check.setChecked(1)
        else:
            self.ui.bottomlines_env_check.setChecked(0)
        
        if self.module.getParameterAsString("bottomlines_ecn") == "1":
            self.ui.bottomlines_ecn_check.setChecked(1)
        else:
            self.ui.bottomlines_ecn_check.setChecked(0)
        
        if self.module.getParameterAsString("bottomlines_soc") == "1":
            self.ui.bottomlines_soc_check.setChecked(1)
        else:
            self.ui.bottomlines_soc_check.setChecked(0)

        self.ui.bottomlines_techN_spin.setValue(int(self.module.getParameterAsString("bottomlines_tech_n")))
        self.ui.bottomlines_envN_spin.setValue(int(self.module.getParameterAsString("bottomlines_env_n")))
        self.ui.bottomlines_ecnN_spin.setValue(int(self.module.getParameterAsString("bottomlines_ecn_n")))
        self.ui.bottomlines_socN_spin.setValue(int(self.module.getParameterAsString("bottomlines_soc_n")))
        
        if self.module.getParameterAsString("eval_mode") == "W":
            self.ui.mode_combo_box.setCurrentIndex(0)
        elif self.module.getParameterAsString("eval_mode") == "P":
            self.ui.mode_combo_box.setCurrentIndex(1)
        
        self.ui.bottomlines_techW_pareto.setValue(int(self.module.getParameterAsString("bottomlines_tech_p")))
        self.ui.bottomlines_envW_pareto.setValue(int(self.module.getParameterAsString("bottomlines_env_p")))
        self.ui.bottomlines_ecnW_pareto.setValue(int(self.module.getParameterAsString("bottomlines_ecn_p")))
        self.ui.bottomlines_socW_pareto.setValue(int(self.module.getParameterAsString("bottomlines_soc_p")))
        
        self.ui.bottomlines_techW_spin.setValue(int(self.module.getParameterAsString("bottomlines_tech_w")))
        self.ui.bottomlines_envW_spin.setValue(int(self.module.getParameterAsString("bottomlines_env_w")))
        self.ui.bottomlines_ecnW_spin.setValue(int(self.module.getParameterAsString("bottomlines_ecn_w")))
        self.ui.bottomlines_socW_spin.setValue(int(self.module.getParameterAsString("bottomlines_soc_w")))
        
        #----------------------------------------------------------------------#
        #-------- EVALUATION SCOPE & METHOD -----------------------------------#
        #----------------------------------------------------------------------#
        if self.module.getParameterAsString("tech2strat_method") == "EqW":
            self.ui.eval_tech2strat_combo.setCurrentIndex(0)
        elif self.module.getParameterAsString("tech2strat_method") == "SeW":
            self.ui.eval_tech2strat_combo.setCurrentIndex(1)
        
        if self.module.getParameterAsString("score_method") == "AHP":
            self.ui.eval_method_combo.setCurrentIndex(0)
        elif self.module.getParameterAsString("score_method") == "RAHP":
            self.ui.eval_method_combo.setCurrentIndex(1)
        elif self.module.getParameterAsString("score_method") == "WPM":
            self.ui.eval_method_combo.setCurrentIndex(2)
        elif self.module.getParameterAsString("score_method") == "WSM":
            self.ui.eval_method_combo.setCurrentIndex(3)
        
        if self.module.getParameterAsString("scope_stoch") == "1":
            self.ui.scope_stoch_check.setChecked(1)
        else:
            self.ui.scope_stoch_check.setChecked(0)
    
        #----------------------------------------------------------------------#
        #-------- RANKING OF STRATEGIES ---------------------------------------#
        #----------------------------------------------------------------------#
        if self.module.getParameterAsString("ranktype") == "RK":
            self.ui.top_score_combo.setCurrentIndex(0)
            self.ui.top_rank_spin.setEnabled(1)
            self.ui.top_CI_spin.setEnabled(0)
        elif self.module.getParameterAsString("ranktype") == "CI":
            self.ui.top_score_combo.setCurrentIndex(1)
            self.ui.top_rank_spin.setEnabled(0)
            self.ui.top_CI_spin.setEnabled(1)
            
        QtCore.QObject.connect(self.ui.top_score_combo, QtCore.SIGNAL("currentIndexChanged(int)"), self.top_score_change)
        
        self.ui.top_rank_spin.setValue(int(self.module.getParameterAsString("topranklimit")))
        self.ui.top_CI_spin.setValue(int(self.module.getParameterAsString("conf_int")))
        
        if self.module.getParameterAsString("ingroup_scoring") == "Avg":
            self.ui.radioScoreAvg.setChecked(True)
        if self.module.getParameterAsString("ingroup_scoring") == "Med":
            self.ui.radioScoreMed.setChecked(True)
        if self.module.getParameterAsString("ingroup_scoring") == "Min":
            self.ui.radioScoreMin.setChecked(True)
        if self.module.getParameterAsString("ingroup_scoring") == "Max":
            self.ui.radioScoreMax.setChecked(True)
 
        #CONNECT DETAILS WITH THE OK BUTTON SO THAT GUI UPDATES MODULE
        QtCore.QObject.connect(self.ui.buttonBox, QtCore.SIGNAL("accepted()"), self.save_values)

    def top_score_change(self):
        if self.ui.top_score_combo.currentIndex() == 0:         #RK option
            self.ui.top_rank_spin.setEnabled(1)
            self.ui.top_CI_spin.setEnabled(0)
        if self.ui.top_score_combo.currentIndex() == 1:         #CI option
            self.ui.top_rank_spin.setEnabled(0)
            self.ui.top_CI_spin.setEnabled(1)
    
    def decom_update(self, currentValue):
        self.ui.decom_box.setText(str(currentValue)+"%")
        self.module.setParameterValue("decom_thresh", str(currentValue))
        if self.ui.renew_slider.value() > self.ui.decom_slider.value():
            self.renew_all_update(self.ui.decom_slider.value())
    
    def renew_update(self, currentValue):
        self.ui.renew_box.setText(str(currentValue)+"%")
        self.module.setParameterValue("renewal_thresh", str(currentValue))
        if self.ui.renew_slider.value() > self.ui.decom_slider.value():
            self.renew_all_update(self.ui.decom_slider.value())
    
    def renew_all_update(self, currentValue):
        self.ui.renew_box.setText(str(currentValue)+"%")
        self.ui.renew_slider.setValue(currentValue)
        self.module.setParameterValue("renewal_thresh", str(currentValue))
    
    def update_retrofitoptions(self, currentind):
        if currentind == 0:
            self.ui.lot_renew_check.setEnabled(0)
            self.ui.lot_decom_check.setEnabled(0)
            self.ui.street_decom_check.setEnabled(0)
            self.ui.street_renew_check.setEnabled(0)
            self.ui.neigh_renew_check.setEnabled(0)
            self.ui.neigh_decom_check.setEnabled(0)
            self.ui.prec_renew_check.setEnabled(0)
            self.ui.prec_decom_check.setEnabled(0)
            self.ui.decom_slider.setEnabled(0)
            self.ui.decom_box.setEnabled(0)
            self.ui.renew_slider.setEnabled(0)
            self.ui.renew_box.setEnabled(0)
            self.ui.radioKeep.setEnabled(0)
            self.ui.radioDecom.setEnabled(0)
        else:
            self.ui.lot_renew_check.setEnabled(1)
            self.ui.lot_decom_check.setEnabled(1)
            self.ui.street_decom_check.setEnabled(1)
            self.ui.street_renew_check.setEnabled(1)
            self.ui.neigh_renew_check.setEnabled(1)
            self.ui.neigh_decom_check.setEnabled(1)
            self.ui.prec_renew_check.setEnabled(1)
            self.ui.prec_decom_check.setEnabled(1)
            self.ui.decom_slider.setEnabled(1)
            self.ui.decom_box.setEnabled(1)
            self.ui.renew_slider.setEnabled(1)
            self.ui.renew_box.setEnabled(1)
            self.ui.radioKeep.setEnabled(1)
            self.ui.radioDecom.setEnabled(1)    
    
    ### BIOFILTRATION SYSTEMS SIGNAL-SLOT FUNCTIONS
    def openFileDialog_BF(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, "Choose Design Curve File...", os.curdir, str("Design Curves (*.dcv *.txt)"))
        if fname: 
            self.ui.BFdesigncurve_pathbox.setText(fname) 
    def BFdesign_enable(self):
        if self.ui.BFdesignUB_box.isChecked() == 1:
            self.ui.BFdesigncurve_browse.setEnabled(0)
        else:
            self.ui.BFdesigncurve_browse.setEnabled(1)

    ### INFILTRATION SYSTEMS SIGNAL-SLOT FUNCTIONS
    def openFileDialog_IS(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, "Choose Design Curve File...", os.curdir, str("Design Curves (*.dcv *.txt)"))
        if fname: 
            self.ui.ISdesigncurve_pathbox.setText(fname) 
    def ISdesign_enable(self):
        if self.ui.ISdesignUB_box.isChecked() == 1:
            self.ui.ISdesigncurve_browse.setEnabled(0)
        else:
            self.ui.ISdesigncurve_browse.setEnabled(1)

    ### PONDS/BASIN SYSTEM SIGNAL-SLOT FUNCTIONS
    def openFileDialog_PB(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, "Choose Design Curve File...", os.curdir, str("Design Curves (*.dcv *.txt)"))
        if fname: 
            self.ui.PBdesigncurve_pathbox.setText(fname) 
    def PBdesign_enable(self):
        if self.ui.PBdesignUB_box.isChecked() == 1:
            self.ui.PBdesigncurve_browse.setEnabled(0)
        else:
            self.ui.PBdesigncurve_browse.setEnabled(1)

    ### RAINWATER TANK SIGNAL-SLOT FUNCTIONS
    def openFileDialog_RT(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, "Choose Design Curve File...", os.curdir, str("Design Curves (*.dcv *.txt)"))
        if fname: 
            self.ui.RTdesigncurve_pathbox.setText(fname) 
    def RTdesign_enable(self):
        if self.ui.RTdesignD4W_box.isChecked() == 1:
            self.ui.RTdesigncurve_browse.setEnabled(0)
        else:
            self.ui.RTdesigncurve_browse.setEnabled(1)
    
    ### SURFACE WETLAND SYSTEMS SIGNAL-SLOT FUNCTIONS
    def openFileDialog_WSUR(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, "Choose Design Curve File...", os.curdir, str("Design Curves (*.dcv *.txt)"))
        if fname: 
            self.ui.WSURdesigncurve_pathbox.setText(fname) 
    def WSURdesign_enable(self):
        if self.ui.WSURdesignUB_box.isChecked() == 1:
            self.ui.WSURdesigncurve_browse.setEnabled(0)
        else:
            self.ui.WSURdesigncurve_browse.setEnabled(1)
    
    ### SWALE SYSTEMS SIGNAL-SLOT FUNCTIONS
    def openFileDialog_SW(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, "Choose Design Curve File...", os.curdir, str("Design Curves (*.dcv *.txt)"))
        if fname: 
            self.ui.SWdesigncurve_pathbox.setText(fname) 
    def SWdesign_enable(self):
        if self.ui.SWdesignUB_box.isChecked() == 1:
            self.ui.SWdesigncurve_browse.setEnabled(0)
        else:
            self.ui.SWdesigncurve_browse.setEnabled(1)
    
    ### EVALUATION CRITERIA SIGNAL-SLOT FUNCTIONS
    def openFileDialog_mca(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, "Choose scoring matrix...", os.curdir, str("Scoring Matrix (*.csv)"))
        if fname: 
            self.ui.mca_scoringmat_box.setText(fname) 
    def mca_scoringmat_enable(self):
        if self.ui.mca_scoringmat_check.isChecked() == 1:
            self.ui.mca_scoringmat_browse.setEnabled(0)
            self.ui.bottomlines_techN_spin.setEnabled(0)
            self.ui.bottomlines_envN_spin.setEnabled(0)
            self.ui.bottomlines_ecnN_spin.setEnabled(0)
            self.ui.bottomlines_socN_spin.setEnabled(0)
            self.ui.mca_metrics_check.setEnabled(1)
        else:
            self.ui.mca_scoringmat_browse.setEnabled(1)
            self.ui.bottomlines_techN_spin.setEnabled(1)
            self.ui.bottomlines_envN_spin.setEnabled(1)
            self.ui.bottomlines_ecnN_spin.setEnabled(1)
            self.ui.bottomlines_socN_spin.setEnabled(1)
            self.ui.mca_metrics_check.setEnabled(0)
        
    #OK BUTTON PRESS FUNCTION        
    def save_values(self):
        
        ################################
        #Select Design Criteria Tab
        ################################    
        #----------------------------------------------------------------------#
        #-------- DESIGN RATIONALE --------------------------------------------#
        #----------------------------------------------------------------------#
        if self.ui.ration_runoff_check.isChecked() == 1:
            ration_runoff = 1
        else:
            ration_runoff = 0
        self.module.setParameterValue("ration_runoff", str(ration_runoff))
        
        if self.ui.ration_pollute_check.isChecked() == 1:
            ration_pollute = 1
        else:
            ration_pollute = 0
        self.module.setParameterValue("ration_pollute", str(ration_pollute))
        
        if self.ui.ration_harvest_check.isChecked() == 1:
            ration_harvest = 1
        else:
            ration_harvest = 0
        self.module.setParameterValue("ration_harvest", str(ration_harvest))
        
        runoff_pri = str(self.ui.runoff_pri_spin.value())
        self.module.setParameterValue("runoff_pri", runoff_pri)
        
        pollute_pri = str(self.ui.pollute_pri_spin.value())
        self.module.setParameterValue("pollute_pri", pollute_pri)
        
        harvest_pri = str(self.ui.harvest_pri_spin.value())
        self.module.setParameterValue("harvest_pri", harvest_pri)
        
        
        #----------------------------------------------------------------------#
        #-------- MANAGEMENT TARGETS ------------------------------------------#
        #----------------------------------------------------------------------#
        targets_runoff = str(self.ui.targets_runoff_spin.value())
        self.module.setParameterValue("targets_runoff", targets_runoff)
        
        targets_TSS = str(self.ui.targets_TSS_spin.value())
        self.module.setParameterValue("targets_TSS", targets_TSS)

        targets_TN = str(self.ui.targets_TN_spin.value())
        self.module.setParameterValue("targets_TN", targets_TN)
        
        targets_TP = str(self.ui.targets_TP_spin.value())
        self.module.setParameterValue("targets_TP", targets_TP)
        
        targets_harvest = str(self.ui.targets_reuse_spin.value())
        self.module.setParameterValue("targets_harvest", targets_harvest)
        
        if self.ui.targets_runoff_auto.isChecked() == 1:
            runoff_auto = 1
        else:
            runoff_auto = 0
        self.module.setParameterValue("runoff_auto", str(runoff_auto))

        if self.ui.targets_TSS_auto.isChecked() == 1:
            TSS_auto = 1
        else:
            TSS_auto = 0
        self.module.setParameterValue("TSS_auto", str(TSS_auto))

        if self.ui.targets_TN_auto.isChecked() == 1:
            TN_auto = 1
        else:
            TN_auto = 0
        self.module.setParameterValue("TN_auto", str(TN_auto))
        
        if self.ui.targets_TP_auto.isChecked() == 1:
            TP_auto = 1
        else:
            TP_auto = 0
        self.module.setParameterValue("TP_auto", str(TP_auto))
        
        if self.ui.targets_reuse_auto.isChecked() == 1:
            harvest_auto = 1
        else:
            harvest_auto = 0
        self.module.setParameterValue("harvest_auto", str(harvest_auto))
        
        #----------------------------------------------------------------------#
        #-------- STRATEGY SETUP ----------------------------------------------#
        #----------------------------------------------------------------------#
        if self.ui.strategy_lot_check.isChecked() == 1:
            strategy_lot_check = 1
        else:
            strategy_lot_check = 0
        self.module.setParameterValue("strategy_lot_check", str(strategy_lot_check))

        lot_increment = str(self.ui.strategy_lot_spin.value())
        self.module.setParameterValue("lot_increment", lot_increment)
        
        if self.ui.strategy_str_check.isChecked() == 1:
            strategy_street_check = 1
        else:
            strategy_street_check = 0
        self.module.setParameterValue("strategy_street_check", str(strategy_street_check))
        
        street_increment = str(self.ui.strategy_str_spin.value())
        self.module.setParameterValue("street_increment", street_increment)
        
        if self.ui.strategy_neigh_check.isChecked() == 1:
            strategy_neigh_check = 1
        else:
            strategy_neigh_check = 0
        self.module.setParameterValue("strategy_neigh_check", str(strategy_neigh_check))
        
        neigh_increment = str(self.ui.strategy_neigh_spin.value())
        self.module.setParameterValue("neigh_increment", neigh_increment)
        
        if self.ui.strategy_prec_check.isChecked() == 1:
            strategy_prec_check = 1
        else:
            strategy_prec_check = 0
        self.module.setParameterValue("strategy_prec_check", str(strategy_prec_check))
        
        prec_increment = str(self.ui.strategy_prec_spin.value())
        self.module.setParameterValue("prec_increment", prec_increment)
        
        basin_target_min = str(self.ui.basin_target_min_box.text())
        self.module.setParameterValue("basin_target_min", basin_target_min)
        
        basin_target_max = str(self.ui.basin_target_max_box.text())
        self.module.setParameterValue("basin_target_max", basin_target_max)
        
        #Specific Strategies
        if self.ui.strategy_specific1_check.isChecked() == 1:
            strategy_specific1 = 1
        else:
            strategy_specific1 = 0
        self.module.setParameterValue("strategy_specific1", str(strategy_specific1))
        
        if self.ui.strategy_specific2_check.isChecked() == 1:
            strategy_specific2 = 1
        else:
            strategy_specific2 = 0
        self.module.setParameterValue("strategy_specific2", str(strategy_specific2))
        
        if self.ui.strategy_specific3_check.isChecked() == 1:
            strategy_specific3 = 1
        else:
            strategy_specific3 = 0
        self.module.setParameterValue("strategy_specific3", str(strategy_specific3))
        
        if self.ui.strategy_specific4_check.isChecked() == 1:
            strategy_specific4 = 1
        else:
            strategy_specific4 = 0
        self.module.setParameterValue("strategy_specific4", str(strategy_specific4))
        
        if self.ui.strategy_specific5_check.isChecked() == 1:
            strategy_specific5 = 1
        else:
            strategy_specific5 = 0
        self.module.setParameterValue("strategy_specific5", str(strategy_specific5))
        
        if self.ui.strategy_specific6_check.isChecked() == 1:
            strategy_specific6 = 1
        else:
            strategy_specific6 = 0
        self.module.setParameterValue("strategy_specific6", str(strategy_specific6))
        
        #######################################
        #Retrofit Tab
        #######################################
        retrofit_scenario_matrix = ["N", "R", "F"]
        retrofit_index = self.ui.area_retrofit_combo.currentIndex()
        retrofit_scenario = retrofit_scenario_matrix[retrofit_index]
        self.module.setParameterValue("retrofit_scenario", str(retrofit_scenario))
        
        if self.ui.retrofit_renewal_check.isChecked() == 1:
            renewal_cycle_def = 1
        else:
            renewal_cycle_def = 0
        self.module.setParameterValue("renewal_cycle_def", str(renewal_cycle_def))
        
        renewal_lot_years = str(self.ui.renewal_lot_years.value())
        self.module.setParameterValue("renewal_lot_years", renewal_lot_years)
        
        renewal_lot_perc = str(self.ui.renewal_lot_spin.value())
        self.module.setParameterValue("renewal_lot_perc", renewal_lot_perc)
        
        renewal_street_years = str(self.ui.renewal_street_years.value())
        self.module.setParameterValue("renewal_street_years", renewal_street_years)
        
        renewal_neigh_years = str(self.ui.renewal_neigh_years.value())
        self.module.setParameterValue("renewal_neigh_years", renewal_neigh_years)
        
        if self.ui.retrofit_forced_street_check.isChecked() == 1:
            force_street = 1
        else:
            force_street = 0
        self.module.setParameterValue("force_street", str(force_street))
        
        if self.ui.retrofit_forced_neigh_check.isChecked() == 1:
            force_neigh = 1
        else:
            force_neigh = 0
        self.module.setParameterValue("force_neigh", str(force_neigh))
        
        if self.ui.retrofit_forced_prec_check.isChecked() == 1:
            force_prec = 1
        else:
            force_prec = 0
        self.module.setParameterValue("force_prec", str(force_prec))
        
        if self.ui.lot_renew_check.isChecked() == 1:
            lot_renew = 1
        else:
            lot_renew = 0
        self.module.setParameterValue("lot_renew", str(lot_renew))
        
        if self.ui.lot_decom_check.isChecked() == 1:
            lot_decom = 1
        else:
            lot_decom = 0
        self.module.setParameterValue("lot_decom", str(lot_decom))
        
        if self.ui.street_renew_check.isChecked() == 1:
            street_renew = 1
        else:
            street_renew = 0
        self.module.setParameterValue("street_renew", str(street_renew))
        
        if self.ui.street_decom_check.isChecked() == 1:
            street_decom = 1
        else:
            street_decom = 0
        self.module.setParameterValue("street_decom", str(street_decom))
        
        if self.ui.neigh_renew_check.isChecked() == 1:
            neigh_renew = 1
        else:
            neigh_renew = 0
        self.module.setParameterValue("neigh_renew", str(neigh_renew))
        
        if self.ui.neigh_decom_check.isChecked() == 1:
            neigh_decom = 1
        else:
            neigh_decom = 0
        self.module.setParameterValue("neigh_decom", str(neigh_decom))
        
        if self.ui.prec_renew_check.isChecked() == 1:
            prec_renew = 1
        else:
            prec_renew = 0
        self.module.setParameterValue("prec_renew", str(prec_renew))
        
        if self.ui.prec_decom_check.isChecked() == 1:
            prec_decom = 1
        else:
            prec_decom = 0
        self.module.setParameterValue("prec_decom", str(prec_decom))
        
        decom_thresh = str(self.ui.decom_slider.value())
        self.module.setParameterValue("decom_thresh", decom_thresh)
        
        renewal_thresh = str(self.ui.renew_slider.value())
        self.module.setParameterValue("renewal_thresh", renewal_thresh)
        
        if self.ui.radioKeep.isChecked() == True:
            renewal_alternative = "K"
        if self.ui.radioDecom.isChecked() == True:
            renewal_alternative = "D"
        self.module.setParameterValue("renewal_alternative", renewal_alternative)
        
        
        #######################################
        #Choose & Customize Technologies Tab
        #######################################
        
        #----------------------------------------------------------------------#
        #--------- Advanced Stormwater Harvesting Plant -----------------------#
        #----------------------------------------------------------------------#
        if self.ui.ASHPstatus_box.isChecked() == 1:
            ASHPstatus = 1
        else:
            ASHPstatus = 0
        self.module.setParameterValue("ASHPstatus", str(ASHPstatus))
        
        ASHPlevel = str(self.ui.ASHPtl_spin.value())
        self.module.setParameterValue("ASHPlevel", ASHPlevel)
        
        ASHPgroup = str(self.ui.ASHPtg_spin.value())
        self.module.setParameterValue("ASHPgroup", ASHPgroup)
        
        #----------------------------------------------------------------------#
        #--------- Aquaculture/Living Systems ---------------------------------#
        #----------------------------------------------------------------------#
        if self.ui.AQstatus_box.isChecked() == 1:
            AQstatus = 1
        else:
            AQstatus = 0
        self.module.setParameterValue("AQstatus", str(AQstatus))
        
        AQlevel = str(self.ui.AQtl_spin.value())
        self.module.setParameterValue("AQlevel", AQlevel)
        
        AQgroup = str(self.ui.AQtg_spin.value())
        self.module.setParameterValue("AQgroup", AQgroup)
        
        #----------------------------------------------------------------------#
        #--------- Aquifer Storage & Recovery ---------------------------------#
        #----------------------------------------------------------------------#
        if self.ui.ASRstatus_box.isChecked() == 1:
            ASRstatus = 1
        else:
            ASRstatus = 0
        self.module.setParameterValue("ASRstatus", str(ASRstatus))
        
        ASRlevel = str(self.ui.ASRtl_spin.value())
        self.module.setParameterValue("ASRlevel", ASRlevel)
        
        ASRgroup = str(self.ui.ASRtg_spin.value())
        self.module.setParameterValue("ASRgroup", ASRgroup)
        
        #----------------------------------------------------------------------#
        #--------- Biofiltration/Raingardens ----------------------------------################################################################
        #----------------------------------------------------------------------#
        if self.ui.BFstatus_box.isChecked() == 1:
            BFstatus = 1
        else:
            BFstatus = 0
        self.module.setParameterValue("BFstatus", str(BFstatus))
        
        BFlevel = str(self.ui.BFtl_spin.value())
        self.module.setParameterValue("BFlevel", BFlevel)
        
        BFgroup = str(self.ui.BFtg_spin.value())
        self.module.setParameterValue("BFgroup", BFgroup)
        
        #Available Scales
        if self.ui.BFlot_check.isChecked() == 1:
            BFlot = 1
        else:
            BFlot = 0
        self.module.setParameterValue("BFlot", str(BFlot))
        
        if self.ui.BFstreet_check.isChecked() == 1:
            BFstreet = 1
        else:
            BFstreet = 0
        self.module.setParameterValue("BFstreet", str(BFstreet))
        
        if self.ui.BFneigh_check.isChecked() == 1:
            BFneigh = 1
        else:
            BFneigh = 0
        self.module.setParameterValue("BFneigh", str(BFneigh))
        
        if self.ui.BFprec_check.isChecked() == 1:
            BFprec = 1
        else:
            BFprec = 0
        self.module.setParameterValue("BFprec", str(BFprec))
        
        #Available Applications
        if self.ui.BFpollute_check.isChecked() == 1:
            BFpollute = 1
        else:
            BFpollute = 0
        self.module.setParameterValue("BFpollute", str(BFpollute))
        
        #Design Curves
        if self.ui.BFdesignUB_box.isChecked() == 1:
            BFdesignUB = 1
        else:
            BFdesignUB = 0
        self.module.setParameterValue("BFdesignUB", str(BFdesignUB))
        
        BFdescur_path = str(self.ui.BFdesigncurve_pathbox.text())
        self.module.setParameterValue("BFdescur_path", BFdescur_path)
        
        #Design Information
        
        #combo box
        BFspec_matrix = [[0,0.1,0.2,0.3,0.4],[0.2,0.4,0.6,0.8]]
        BFspec_EDDindex = self.ui.BFspecs_EDD_combo.currentIndex()
        BFspec_FDindex = self.ui.BFspecs_FD_combo.currentIndex()
        print BFspec_EDDindex
        print BFspec_FDindex
        BFspec_EDD = BFspec_matrix[0][BFspec_EDDindex]
        BFspec_FD = BFspec_matrix[1][BFspec_FDindex]
        print BFspec_EDD
        print BFspec_FD
        self.module.setParameterValue("BFspec_EDD", str(BFspec_EDD))
        self.module.setParameterValue("BFspec_FD", str(BFspec_FD))
        
        BFmaxsize = str(self.ui.BFmaxsize_box.text())
        self.module.setParameterValue("BFmaxsize", BFmaxsize)
        
        BFavglife = str(self.ui.BFavglifespin.value())
        self.module.setParameterValue("BFavglife", BFavglife)
        
        if self.ui.BFlined_check.isChecked() == 1:
            BFlined = 1
        else:
            BFlined = 0
        self.module.setParameterValue("BFlined", str(BFlined))
        
        #further design parameters coming soon...
        
        #----------------------------------------------------------------------#
        #--------- Green Roof -------------------------------------------------#
        #----------------------------------------------------------------------#
        if self.ui.GRstatus_box.isChecked() == 1:
            GRstatus = 1
        else:
            GRstatus = 0
        self.module.setParameterValue("GRstatus", str(GRstatus))
        
        GRlevel = str(self.ui.GRtl_spin.value())
        self.module.setParameterValue("GRlevel", GRlevel)
        
        GRgroup = str(self.ui.GRtg_spin.value())
        self.module.setParameterValue("GRgroup", GRgroup)
        
        
        #----------------------------------------------------------------------#
        #--------- Greywater Tank/Treatment -----------------------------------#
        #----------------------------------------------------------------------#
        if self.ui.GTstatus_box.isChecked() == 1:
            GTstatus = 1
        else:
            GTstatus = 0
        self.module.setParameterValue("GTstatus", str(GTstatus))
        
        GTlevel = str(self.ui.GTtl_spin.value())
        self.module.setParameterValue("GTlevel", GTlevel)
        
        GTgroup = str(self.ui.GTtg_spin.value())
        self.module.setParameterValue("GTgroup", GTgroup)
        
        
        #----------------------------------------------------------------------#
        #--------- Gross Pollutant Trap ---------------------------------------#
        #----------------------------------------------------------------------#
        if self.ui.GPTstatus_box.isChecked() == 1:
            GPTstatus = 1
        else:
            GPTstatus = 0
        self.module.setParameterValue("GPTstatus", str(GPTstatus))
        
        GPTlevel = str(self.ui.GPTtl_spin.value())
        self.module.setParameterValue("GPTlevel", GPTlevel)
        
        GPTgroup = str(self.ui.GPTtg_spin.value())
        self.module.setParameterValue("GPTgroup", GPTgroup)
        
        
        #----------------------------------------------------------------------#
        #--------- Infiltration System ----------------------------------------############################################################
        #----------------------------------------------------------------------#
        if self.ui.ISstatus_box.isChecked() == 1:
            ISstatus = 1
        else:
            ISstatus = 0
        self.module.setParameterValue("ISstatus", str(ISstatus))
        
        ISlevel = str(self.ui.IStl_spin.value())
        self.module.setParameterValue("ISlevel", ISlevel)
        
        ISgroup = str(self.ui.IStg_spin.value())
        self.module.setParameterValue("ISgroup", ISgroup)
        
        
        #Available Scales
        if self.ui.ISlot_check.isChecked() == 1:
            ISlot = 1
        else:
            ISlot = 0
        self.module.setParameterValue("ISlot", str(ISlot))
        
        if self.ui.ISstreet_check.isChecked() == 1:
            ISstreet = 1
        else:
            ISstreet = 0
        self.module.setParameterValue("ISstreet", str(ISstreet))
        
        if self.ui.ISneigh_check.isChecked() == 1:
            ISneigh = 1
        else:
            ISneigh = 0
        self.module.setParameterValue("ISneigh", str(ISneigh))
        
        #Available Applications
        if self.ui.ISflow_check.isChecked() == 1:
            ISflow = 1
        else:
            ISflow = 0
        self.module.setParameterValue("ISflow", str(ISflow))
        
        if self.ui.ISpollute_check.isChecked() == 1:
            ISpollute = 1
        else:
            ISpollute = 0
        self.module.setParameterValue("ISpollute", str(ISpollute))
        
        #Design Curves
        if self.ui.ISdesignUB_box.isChecked() == 1:
            ISdesignUB = 1
        else:
            ISdesignUB = 0
        self.module.setParameterValue("ISdesignUB", str(ISdesignUB))
        
        ISdescur_path = str(self.ui.ISdesigncurve_pathbox.text())
        self.module.setParameterValue("ISdescur_path", ISdescur_path)
        
        #Design Information
        #combo box
        ISspec_matrix = [[0.1,0.2,0.3,0.4,0.5],[0.2,0.4,0.6,0.8]]
        ISspec_EDDindex = self.ui.ISspecs_EDD_combo.currentIndex()
        ISspec_FDindex = self.ui.ISspecs_FD_combo.currentIndex()
        ISspec_EDD = ISspec_matrix[0][ISspec_EDDindex]
        ISspec_FD = ISspec_matrix[1][ISspec_FDindex]
        self.module.setParameterValue("ISspec_EDD", str(ISspec_EDD))
        self.module.setParameterValue("ISspec_FD", str(ISspec_FD))
        
        ISmaxsize = str(self.ui.ISmaxsize_box.text())
        self.module.setParameterValue("ISmaxsize", ISmaxsize)
        
        ISavglife = str(self.ui.ISavglifespin.value())
        self.module.setParameterValue("ISavglife", ISavglife)
        
        if self.ui.IS_2Dmodel_box.isChecked() == 1:
            IS_2Dmodel = 1
        else:
            IS_2Dmodel = 0
        self.module.setParameterValue("IS_2Dmodel", str(IS_2Dmodel))
        
        #further design parameters coming soon...
        
        #----------------------------------------------------------------------#
        #--------- Packaged Plants --------------------------------------------#
        #----------------------------------------------------------------------#
        if self.ui.PPLstatus_box.isChecked() == 1:
            PPLstatus = 1
        else:
            PPLstatus = 0
        self.module.setParameterValue("PPLstatus", str(PPLstatus))
        
        PPLlevel = str(self.ui.PPLtl_spin.value())
        self.module.setParameterValue("PPLlevel", PPLlevel)
        
        PPLgroup = str(self.ui.PPLtg_spin.value())
        self.module.setParameterValue("PPLgroup", PPLgroup)
        
        
        #----------------------------------------------------------------------#
        #--------- Ponds/Sedimentation Basins ---------------------------------###############################################################
        #----------------------------------------------------------------------#
        if self.ui.PBstatus_box.isChecked() == 1:
            PBstatus = 1
        else:
            PBstatus = 0
        self.module.setParameterValue("PBstatus", str(PBstatus))
        
        PBlevel = str(self.ui.PBtl_spin.value())
        self.module.setParameterValue("PBlevel", PBlevel)
        
        PBgroup = str(self.ui.PBtg_spin.value())
        self.module.setParameterValue("PBgroup", PBgroup)
        
        
        #Available Scales
        if self.ui.PBneigh_check.isChecked() == 1:
            PBneigh = 1
        else:
            PBneigh = 0
        self.module.setParameterValue("PBneigh", str(PBneigh))
        
        if self.ui.PBprec_check.isChecked() == 1:
            PBprec = 1
        else:
            PBprec = 0
        self.module.setParameterValue("PBprec", str(PBprec))
        
        #Available Applications
        if self.ui.PBflow_check.isChecked() == 1:
            PBflow = 1
        else:
            PBflow = 0
        self.module.setParameterValue("PBflow", str(PBflow))
        
        if self.ui.PBpollute_check.isChecked() == 1:
            PBpollute = 1
        else:
            PBpollute = 0
        self.module.setParameterValue("PBpollute", str(PBpollute))
        
        #Design Curves
        if self.ui.PBdesignUB_box.isChecked() == 1:
            PBdesignUB = 1
        else:
            PBdesignUB = 0
        self.module.setParameterValue("PBdesignUB", str(PBdesignUB))
        
        PBdescur_path = str(self.ui.PBdesigncurve_pathbox.text())
        self.module.setParameterValue("PBdescur_path", PBdescur_path)
        
        #Design Information
        #combo box
        PBspec_matrix = ["0.25", "0.50", "0.75", "1.00", "1.25"]
        PBspec_MDindex = self.ui.PBspecs_combo.currentIndex()
        PBspec_MD = PBspec_matrix[PBspec_MDindex]
        self.module.setParameterValue("PBspec_MD", str(PBspec_MD))
        print PBspec_MD
        
        PBmaxsize = str(self.ui.PBmaxsize_box.text())
        self.module.setParameterValue("PBmaxsize", PBmaxsize)
        #further design parameters coming soon...
        
        PBavglife = str(self.ui.PBavglifespin.value())
        self.module.setParameterValue("PBavglife", PBavglife)
        
        #----------------------------------------------------------------------#
        #---------- Porous/Pervious Pavements ---------------------------------#
        #----------------------------------------------------------------------#
        if self.ui.PPstatus_box.isChecked() == 1:
            PPstatus = 1
        else:
            PPstatus = 0
        self.module.setParameterValue("PPstatus", str(PPstatus))
        
        PPlevel = str(self.ui.PPtl_spin.value())
        self.module.setParameterValue("PPlevel", PPlevel)
        
        PPgroup = str(self.ui.PPtg_spin.value())
        self.module.setParameterValue("PPgroup", PPgroup)
        
        
        #----------------------------------------------------------------------#
        #---------- Rainwater Tank --------------------------------------------#
        #----------------------------------------------------------------------#
        if self.ui.RTstatus_box.isChecked() == 1:
            RTstatus = 1
        else:
            RTstatus = 0
        self.module.setParameterValue("RTstatus", str(RTstatus))
        
        RTlevel = str(self.ui.RTtl_spin.value())
        self.module.setParameterValue("RTlevel", RTlevel)
        
        RTgroup = str(self.ui.RTtg_spin.value())
        self.module.setParameterValue("RTgroup", RTgroup)
        
        
        RT_maxdepth = str(self.ui.RT_maxdepth_box.text())
        self.module.setParameterValue("RT_maxdepth", RT_maxdepth)
        RT_mindead = str(self.ui.RT_mindead_box.text())
        self.module.setParameterValue("RT_mindead", RT_mindead)
        RT_firstflush = str(self.ui.RT_firstflush_box.text())
        self.module.setParameterValue("RT_firstflush", RT_firstflush)
        
        if self.ui.RTscale_lot_box.isChecked() == 1:
            RTscale_lot = 1
        else:
            RTscale_lot = 0
        self.module.setParameterValue("RTscale_lot", str(RTscale_lot))
        
        if self.ui.RTscale_street_box.isChecked() == 1:
            RTscale_street = 1
        else:
            RTscale_street = 0
        self.module.setParameterValue("RTscale_street", str(RTscale_street))
        
        if self.ui.RTpurp_flood_box.isChecked() == 1:
            RTpurp_flood = 1
        else:
            RTpurp_flood = 0
        self.module.setParameterValue("RTpurp_flood", str(RTpurp_flood))
        
        if self.ui.RTpurp_recyc_box.isChecked() == 1:
            RTpurp_recyc = 1
        else:
            RTpurp_recyc = 0
        self.module.setParameterValue("RTpurp_recyc", str(RTpurp_recyc))
        
        if self.ui.RT_shape_circ_check.isChecked() == 1:
            RT_shape_circ = 1
        else:
            RT_shape_circ = 0
        self.module.setParameterValue("RT_shape_circ", str(RT_shape_circ))
        
        if self.ui.RT_shape_rect_check.isChecked() == 1:
            RT_shape_rect = 1
        else:
            RT_shape_rect = 0
        self.module.setParameterValue("RT_shape_rect", str(RT_shape_rect))
        
        if self.ui.RTdesignD4W_box.isChecked() == 1:
            RTdesignD4W = 1
        else:
            RTdesignD4W = 0
        self.module.setParameterValue("RTdesignD4W", str(RTdesignD4W))
        
        RTdescur_path = str(self.ui.RTdesigncurve_pathbox.text())
        self.module.setParameterValue("RTdescur_path", RTdescur_path)
        
        RTavglife = str(self.ui.RTavglifespin.value())
        self.module.setParameterValue("RTavglife", RTavglife)
        
        if self.ui.RT_sbmodel_ybs_radio.isChecked() == True:
            RT_sbmodel = "ybs"
        elif self.ui.RT_sbmodel_yas_radio.isChecked() == True:
            RT_sbmodel = "yas"
        self.module.setParameterValue("RT_sbmodel", RT_sbmodel)
        
        #----------------------------------------------------------------------#
        #---------- Sand/Peat/Gravel Filter -----------------------------------#
        #----------------------------------------------------------------------#
        if self.ui.SFstatus_box.isChecked() == 1:
            SFstatus = 1
        else:
            SFstatus = 0
        self.module.setParameterValue("SFstatus", str(SFstatus))
        
        SFlevel = str(self.ui.SFtl_spin.value())
        self.module.setParameterValue("SFlevel", SFlevel)
        
        SFgroup = str(self.ui.SFtg_spin.value())
        self.module.setParameterValue("SFgroup", SFgroup)
        
        
        #----------------------------------------------------------------------#
        #---------- Septic Tank -----------------------------------------------#
        #----------------------------------------------------------------------#
        if self.ui.STstatus_box.isChecked() == 1:
            STstatus = 1
        else:
            STstatus = 0
        self.module.setParameterValue("STstatus", str(STstatus))
        
        STlevel = str(self.ui.STtl_spin.value())
        self.module.setParameterValue("STlevel", STlevel)
        
        STgroup = str(self.ui.STtg_spin.value())
        self.module.setParameterValue("STgroup", STgroup)
        
        
        #----------------------------------------------------------------------#
        #---------- Subsurface Irrigation System ------------------------------#
        #----------------------------------------------------------------------#
        if self.ui.IRRstatus_box.isChecked() == 1:
            IRRstatus = 1
        else:
            IRRstatus = 0
        self.module.setParameterValue("IRRstatus", str(IRRstatus))
        
        IRRlevel = str(self.ui.IRRtl_spin.value())
        self.module.setParameterValue("IRRlevel", IRRlevel)
        
        IRRgroup = str(self.ui.IRRtg_spin.value())
        self.module.setParameterValue("IRRgroup", IRRgroup)
        
        
        #----------------------------------------------------------------------#
        #---------- Subsurface Wetland/Reed Bed -------------------------------#
        #----------------------------------------------------------------------#
        if self.ui.WSUBstatus_box.isChecked() == 1:
            WSUBstatus = 1
        else:
            WSUBstatus = 0
        self.module.setParameterValue("WSUBstatus", str(WSUBstatus))
        
        WSUBlevel = str(self.ui.WSUBtl_spin.value())
        self.module.setParameterValue("WSUBlevel", WSUBlevel)
        
        WSUBgroup = str(self.ui.BFtg_spin.value())
        self.module.setParameterValue("WSUBgroup", WSUBgroup)
        
        
        #----------------------------------------------------------------------#
        #---------- Surface Wetland -------------------------------------------###############################################################
        #----------------------------------------------------------------------#
        if self.ui.WSURstatus_box.isChecked() == 1:
            WSURstatus = 1
        else:
            WSURstatus = 0
        self.module.setParameterValue("WSURstatus", str(WSURstatus))
        
        WSURlevel = str(self.ui.WSURtl_spin.value())
        self.module.setParameterValue("WSURlevel", WSURlevel)
        
        WSURgroup = str(self.ui.WSURtg_spin.value())
        self.module.setParameterValue("WSURgroup", WSURgroup)
        
        
        #Available Scales
        if self.ui.WSURneigh_check.isChecked() == 1:
            WSURneigh = 1
        else:
            WSURneigh = 0
        self.module.setParameterValue("WSURneigh", str(WSURneigh))
        
        if self.ui.WSURprec_check.isChecked() == 1:
            WSURprec = 1
        else:
            WSURprec = 0
        self.module.setParameterValue("WSURprec", str(WSURprec))
        
        #Available Applications
        if self.ui.WSURflow_check.isChecked() == 1:
            WSURflow = 1
        else:
            WSURflow = 0
        self.module.setParameterValue("WSURflow", str(WSURflow))
        
        if self.ui.WSURpollute_check.isChecked() == 1:
            WSURpollute = 1
        else:
            WSURpollute = 0
        self.module.setParameterValue("WSURpollute", str(WSURpollute))
        
        #Design Curves
        if self.ui.WSURdesignUB_box.isChecked() == 1:
            WSURdesignUB = 1
        else:
            WSURdesignUB = 0
        self.module.setParameterValue("WSURdesignUB", str(WSURdesignUB))
        
        WSURdescur_path = str(self.ui.WSURdesigncurve_pathbox.text())
        self.module.setParameterValue("WSURdescur_path", WSURdescur_path)
        
        #Design Information
        #combo box
        WSURspec_matrix = ["0.25", "0.50", "0.75", "0.25", "0.50", "0.75"]
        WSURspec_EDDindex = self.ui.WSURspecs_combo.currentIndex()
        WSURspec_EDD = WSURspec_matrix[WSURspec_EDDindex]
        self.module.setParameterValue("WSURspec_EDD", str(WSURspec_EDD))
        
        WSURmaxsize = str(self.ui.WSURmaxsize_box.text())
        self.module.setParameterValue("WSURmaxsize", WSURmaxsize)
        
        WSURavglife = str(self.ui.WSURavglifespin.value())
        self.module.setParameterValue("WSURavglife", WSURavglife)
        #further design parameters coming soon...
        
        
        #----------------------------------------------------------------------#
        #---------- Swales/Buffer Strips --------------------------------------###############################################################
        #----------------------------------------------------------------------#
        if self.ui.SWstatus_box.isChecked() == 1:
            SWstatus = 1
        else:
            SWstatus = 0
        self.module.setParameterValue("SWstatus", str(SWstatus))
        
        SWlevel = str(self.ui.SWtl_spin.value())
        self.module.setParameterValue("SWlevel", SWlevel)
        
        SWgroup = str(self.ui.SWtg_spin.value())
        self.module.setParameterValue("SWgroup", SWgroup)
        
        
        #Available Scales
        if self.ui.SWstreet_check.isChecked() == 1:
            SWstreet = 1
        else:
            SWstreet = 0
        self.module.setParameterValue("SWstreet", str(SWstreet))
        
        #Available Applications
        if self.ui.SWflow_check.isChecked() == 1:
            SWflow = 1
        else:
            SWflow = 0
        self.module.setParameterValue("SWflow", str(SWflow))
        
        if self.ui.SWpollute_check.isChecked() == 1:
            SWpollute = 1
        else:
            SWpollute = 0
        self.module.setParameterValue("SWpollute", str(SWpollute))
        
        #Design Curves
        if self.ui.SWdesignUB_box.isChecked() == 1:
            SWdesignUB = 1
        else:
            SWdesignUB = 0
        self.module.setParameterValue("SWdesignUB", str(SWdesignUB))
        
        SWdescur_path = str(self.ui.SWdesigncurve_pathbox.text())
        self.module.setParameterValue("SWdescur_path", SWdescur_path)
        
        #Design Information
        #combo box
        SWmaxsize = str(self.ui.SWmaxsize_box.text())
        self.module.setParameterValue("SWmaxsize", SWmaxsize)
        
        SWavglife = str(self.ui.SWavglifespin.value())
        self.module.setParameterValue("SWavglife", SWavglife)
        #further design parameters coming soon...
        
        #----------------------------------------------------------------------#
        #--------- Tree Pits --------------------------------------------------#
        #----------------------------------------------------------------------#
        if self.ui.TPSstatus_box.isChecked() == 1:
            TPSstatus = 1
        else:
            TPSstatus = 0
        self.module.setParameterValue("TPSstatus", str(TPSstatus))
        
        TPSlevel = str(self.ui.TPStl_spin.value())
        self.module.setParameterValue("TPSlevel", TPSlevel)
        
        TPSgroup = str(self.ui.TPStg_spin.value())
        self.module.setParameterValue("TPSgroup", TPSgroup)
        
        
        #----------------------------------------------------------------------#
        #---------- Urine-separating Toilets ----------------------------------#
        #----------------------------------------------------------------------#
        if self.ui.UTstatus_box.isChecked() == 1:
            UTstatus = 1
        else:
            UTstatus = 0
        self.module.setParameterValue("UTstatus", str(UTstatus))
        
        UTlevel = str(self.ui.BFtl_spin.value())
        self.module.setParameterValue("UTlevel", UTlevel)
        
        UTgroup = str(self.ui.UTtg_spin.value())
        self.module.setParameterValue("UTgroup", UTgroup)
        
        
        #----------------------------------------------------------------------#
        #---------- Wastwater Recovery/Recycling Plant ------------------------#
        #----------------------------------------------------------------------#
        if self.ui.WWRRstatus_box.isChecked() == 1:
            WWRRstatus = 1
        else:
            WWRRstatus = 0
        self.module.setParameterValue("WWRRstatus", str(WWRRstatus))
        
        WWRRlevel = str(self.ui.WWRRtl_spin.value())
        self.module.setParameterValue("WWRRlevel", WWRRlevel)
        
        WWRRgroup = str(self.ui.WWRRtg_spin.value())
        self.module.setParameterValue("WWRRgroup", WWRRgroup)
        
        
        #----------------------------------------------------------------------#
        #---------- Waterless/Composting Toilets ------------------------------#
        #----------------------------------------------------------------------#
        if self.ui.WTstatus_box.isChecked() == 1:
            WTstatus = 1
        else:
            WTstatus = 0
        self.module.setParameterValue("WTstatus", str(WTstatus))
        
        WTlevel = str(self.ui.WTtl_spin.value())
        self.module.setParameterValue("WTlevel", WTlevel)
        
        WTgroup = str(self.ui.WTtg_spin.value())
        self.module.setParameterValue("WTgroup", WTgroup)
        
        
        #----------------------------------------------------------------------#
        #---------- Water Efficient Appliances --------------------------------#
        #----------------------------------------------------------------------#
        if self.ui.WEFstatus_box.isChecked() == 1:
            WEFstatus = 1
        else:
            WEFstatus = 0
        self.module.setParameterValue("WEFstatus", str(WEFstatus))
        
        WEFlevel = str(self.ui.BFtl_spin.value())
        self.module.setParameterValue("WEFlevel", WEFlevel)
        
        WEFgroup = str(self.ui.WEFtg_spin.value())
        self.module.setParameterValue("WEFgroup", WEFgroup)
        
        
        ###NOTE: NOT LINKING COMBO BOX WITH RATING SYSTEM, AS6400 the only one for now
        
        LEG_minrate = str(self.ui.LEG_minrate_spin.value())
        self.module.setParameterValue("LEG_minrate", LEG_minrate)
        
        PPP_likelihood = str(self.ui.PPP_likelihood_spin.value())
        self.module.setParameterValue("PPP_likelihood", PPP_likelihood)
        
            #COMBO BOXES
        WEF_implement_method_matrix = ["LEG", "PPP", "SEC", "D4W"]
        
        WEF_implement_index = self.ui.WEF_implement_method_combo.currentIndex()
        WEF_implement_method = WEF_implement_method_matrix[WEF_implement_index]
        self.module.setParameterValue("WEF_implement_method", WEF_implement_method)
        
        if self.ui.LEG_force_check.isChecked() == 1:
            LEG_force = 1
        else:
            LEG_force = 0
        self.module.setParameterValue("LEG_force", str(LEG_force))
        
        if self.ui.PPP_force_check.isChecked() == 1:
            PPP_force = 1
        else:
            PPP_force = 0
        self.module.setParameterValue("PPP_force", str(PPP_force))
        
        if self.ui.SEC_force_check.isChecked() == 1:
            SEC_force = 1
        else:
            SEC_force = 0
        self.module.setParameterValue("SEC_force", str(SEC_force))
        
        if self.ui.SEC_urbansim_check.isChecked() == 1:
            SEC_urbansim = 1
        else:
            SEC_urbansim = 0
        self.module.setParameterValue("SEC_urbansim", str(SEC_urbansim))
        
        if self.ui.D4W_UDMactive_check.isChecked() == 1:
            D4W_UDMactive = 1
        else:
            D4W_UDMactive = 0
        self.module.setParameterValue("D4W_UDMactive", str(D4W_UDMactive))
        
        if self.ui.D4W_STMactive_check.isChecked() == 1:
            D4W_STMactive = 1
        else:
            D4W_STMactive = 0
        self.module.setParameterValue("D4W_STMactive", str(D4W_STMactive))
        
        if self.ui.D4W_EVMactive_check.isChecked() == 1:
            D4W_EVMactive = 1
        else:
            D4W_EVMactive = 0
        self.module.setParameterValue("D4W_EVMactive", str(D4W_EVMactive))
        
        if self.ui.WEF_loc_famhouse_check.isChecked() == 1:
            WEF_loc_famhouse = 1
        else:
            WEF_loc_famhouse = 0
        self.module.setParameterValue("WEF_loc_famhouse", str(WEF_loc_famhouse))
        
        if self.ui.WEF_loc_apart_check.isChecked() == 1:
            WEF_loc_apart = 1
        else:
            WEF_loc_apart = 0
        self.module.setParameterValue("WEF_loc_apart", str(WEF_loc_apart))
        
        if self.ui.WEF_loc_nonres_check.isChecked() == 1:
            WEF_loc_nonres = 1
        else:
            WEF_loc_nonres = 0
        self.module.setParameterValue("WEF_loc_nonres", str(WEF_loc_nonres))
        
        if self.ui.WEF_radio_medflow.isChecked() == True:
            WEF_flow_method = "M"
        elif self.ui.WEF_radio_stochflow.isChecked() == True:
            WEF_flow_method = "S"
        self.module.setParameterValue("WEF_flow_method", WEF_flow_method)
        
        #----------------------------------------------------------------------#
        #--- ## --- <TechnologyTitle> -----------------------------------------#
        #----------------------------------------------------------------------#
        #if self.ui.<abbrev.>status_box.isChecked() == 1:
        #    <abbrev.>status = 1
        #else:
        #    <abbrev.>status = 0
        #self.module.setParameterValue("<abbrev.>status", str(<abbrev.>status))
        
        
        #----------------------------------------------------------------------#
        #--- ## --- REGIONAL INFORMATION---------------------------------------#
        #----------------------------------------------------------------------#
        regioncity_matrix = ["Adelaide", "Brisbane", "Melbourne", "Perth", "Sydney"]
        
        regioncity_index = self.ui.regioncity_combo.currentIndex()
        regioncity = regioncity_matrix[regioncity_index]
        self.module.setParameterValue("regioncity", regioncity)
        
        
        ################################
        #Select Evaluation Criteria Tab
        ################################ 
        #----------------------------------------------------------------------#
        #-------- Evaluation Metrics Select------------------------------------#
        #----------------------------------------------------------------------#
        
        if self.ui.mca_scoringmat_check.isChecked() == 1:
            scoringmatrix_default = 1
        else:
            scoringmatrix_default = 0
        self.module.setParameterValue("scoringmatrix_default", str(scoringmatrix_default))
        
        scoringmatrix_path = str(self.ui.mca_scoringmat_box.text())
        self.module.setParameterValue("scoringmatrix_path", scoringmatrix_path)
        
        if self.ui.mca_metrics_check.isChecked() == 1:
            scoring_include_all = 1
        else:
            scoring_include_all = 0
        self.module.setParameterValue("scoring_include_all", str(scoring_include_all))
        
        
        #----------------------------------------------------------------------#
        #-------- Customize Evaluation Criteria--------------------------------#
        #----------------------------------------------------------------------#
        if self.ui.bottomlines_tech_check.isChecked() == 1:
            bottomlines_tech = 1
        else:
            bottomlines_tech = 0
        self.module.setParameterValue("bottomlines_tech", str(bottomlines_tech))

        if self.ui.bottomlines_env_check.isChecked() == 1:
            bottomlines_env = 1
        else:
            bottomlines_env = 0
        self.module.setParameterValue("bottomlines_env", str(bottomlines_env))

        if self.ui.bottomlines_ecn_check.isChecked() == 1:
            bottomlines_ecn = 1
        else:
            bottomlines_ecn = 0
        self.module.setParameterValue("bottomlines_ecn", str(bottomlines_ecn))
        
        if self.ui.bottomlines_soc_check.isChecked() == 1:
            bottomlines_soc = 1
        else:
            bottomlines_soc = 0
        self.module.setParameterValue("bottomlines_soc", str(bottomlines_soc))

        bottomlines_tech_n = str(self.ui.bottomlines_techN_spin.value())
        self.module.setParameterValue("bottomlines_tech_n", bottomlines_tech_n)

        bottomlines_env_n = str(self.ui.bottomlines_envN_spin.value())
        self.module.setParameterValue("bottomlines_env_n", bottomlines_env_n)

        bottomlines_ecn_n = str(self.ui.bottomlines_ecnN_spin.value())
        self.module.setParameterValue("bottomlines_ecn_n", bottomlines_ecn_n)
        
        bottomlines_soc_n = str(self.ui.bottomlines_socN_spin.value())
        self.module.setParameterValue("bottomlines_soc_n", bottomlines_soc_n)
        
        eval_mode_matrix = ["W", "P"]
        evalmode_index = self.ui.mode_combo_box.currentIndex()
        eval_mode = eval_mode_matrix[evalmode_index]
        self.module.setParameterValue("eval_mode", eval_mode)
    
        bottomlines_tech_p = str(self.ui.bottomlines_techW_pareto.value())
        self.module.setParameterValue("bottomlines_tech_p", bottomlines_tech_p)

        bottomlines_env_p = str(self.ui.bottomlines_envW_pareto.value())
        self.module.setParameterValue("bottomlines_env_p", bottomlines_env_p)

        bottomlines_ecn_p = str(self.ui.bottomlines_ecnW_pareto.value())
        self.module.setParameterValue("bottomlines_ecn_p", bottomlines_ecn_p)
        
        bottomlines_soc_p = str(self.ui.bottomlines_socW_pareto.value())
        self.module.setParameterValue("bottomlines_soc_p", bottomlines_soc_p)

        bottomlines_tech_w = str(self.ui.bottomlines_techW_spin.value())
        self.module.setParameterValue("bottomlines_tech_w", bottomlines_tech_w)

        bottomlines_env_w = str(self.ui.bottomlines_envW_spin.value())
        self.module.setParameterValue("bottomlines_env_w", bottomlines_env_w)

        bottomlines_ecn_w = str(self.ui.bottomlines_ecnW_spin.value())
        self.module.setParameterValue("bottomlines_ecn_w", bottomlines_ecn_w)
        
        bottomlines_soc_w = str(self.ui.bottomlines_socW_spin.value())
        self.module.setParameterValue("bottomlines_soc_w", bottomlines_soc_w)

        #----------------------------------------------------------------------#
        #-------- EVALUATION SCOPE & METHOD -----------------------------------#
        #----------------------------------------------------------------------#
        
        tech2strat_method_matrix = ["EqW", "SeW"]
        tech2strat_index = self.ui.eval_tech2strat_combo.currentIndex()
        tech2strat_method = tech2strat_method_matrix[tech2strat_index]
        self.module.setParameterValue("tech2strat_method", tech2strat_method)
    
        score_method_matrix = ["AHP", "RAHP", "WPM", "WSM"]
        score_index = self.ui.eval_method_combo.currentIndex()
        score_method = score_method_matrix[score_index]
        self.module.setParameterValue("score_method", score_method)
    
        if self.ui.scope_stoch_check.isChecked() == 1:
            scope_stoch = 1
        else:
            scope_stoch = 0
        self.module.setParameterValue("scope_stoch", str(scope_stoch))

        #----------------------------------------------------------------------#
        #-------- RANKING OF STRATEGIES ---------------------------------------#
        #----------------------------------------------------------------------#
        
        rank_method_matrix = ["RK", "CI"]
        rank_index = self.ui.top_score_combo.currentIndex()
        ranktype = rank_method_matrix[rank_index]
        self.module.setParameterValue("ranktype", ranktype)
        
        topranklimit = str(self.ui.top_rank_spin.value())
        self.module.setParameterValue("topranklimit", topranklimit)
        
        conf_int = str(self.ui.top_CI_spin.value())
        self.module.setParameterValue("conf_int", conf_int)
        
        if self.ui.radioScoreAvg.isChecked() == True:
            ingroup_scoring = "Avg"
        if self.ui.radioScoreMed.isChecked() == True:
            ingroup_scoring = "Med"
        if self.ui.radioScoreMin.isChecked() == True:
            ingroup_scoring = "Min"
        if self.ui.radioScoreMax.isChecked() == True:
            ingroup_scoring = "Max"
        self.module.setParameterValue("ingroup_scoring", ingroup_scoring)
        
    