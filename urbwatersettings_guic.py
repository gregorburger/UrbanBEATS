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
from urbwatersettings_gui import Ui_urbwatersettings_Dialog

class activateurbwatersettings_GUI(QtGui.QDialog):
    def __init__(self, m, parent=None):
        self.module = Module
        self.module = m
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_urbwatersettings_Dialog()
        self.ui.setupUi(self)
        
        self.caption = "Choose Climate File..."
        self.filter = "CityDrain3 Climate (*.ixx)"
        
        #Assign Default Values & Connect Signal/Slots
        #######################################
        #Climate Tab
        #######################################
        self.ui.rain_ts_box.setText(self.module.getParameterAsString("rain_ts"))
        self.ui.rain_in_box.setText(self.module.getParameterAsString("rain_fname"))
        self.ui.evap_ts_box.setText(self.module.getParameterAsString("evap_ts"))
        self.ui.evap_in_box.setText(self.module.getParameterAsString("evap_fname"))
        self.ui.solar_ts_box.setText(self.module.getParameterAsString("solar_ts"))
        self.ui.solar_in_box.setText(self.module.getParameterAsString("solar_fname"))
        
        QtCore.QObject.connect(self.ui.rain_in_browse, QtCore.SIGNAL("clicked()"), self.openFileChooserDialogRain)
        QtCore.QObject.connect(self.ui.evap_in_browse, QtCore.SIGNAL("clicked()"), self.openFileChooserDialogEvap)
        QtCore.QObject.connect(self.ui.solar_in_browse, QtCore.SIGNAL("clicked()"), self.openFileChooserDialogSolar)
        
        if self.module.getParameterAsString("rain_scale") == "1":
            self.ui.scale_rain_check.setChecked(1)
            self.ui.rain_month_01.setEnabled(1)
            self.ui.rain_month_02.setEnabled(1)
            self.ui.rain_month_03.setEnabled(1)
            self.ui.rain_month_04.setEnabled(1)
            self.ui.rain_month_05.setEnabled(1)
            self.ui.rain_month_06.setEnabled(1)
            self.ui.rain_month_07.setEnabled(1)
            self.ui.rain_month_08.setEnabled(1)
            self.ui.rain_month_09.setEnabled(1)
            self.ui.rain_month_10.setEnabled(1)
            self.ui.rain_month_11.setEnabled(1)
            self.ui.rain_month_12.setEnabled(1)
        else:
            self.ui.scale_rain_check.setChecked(0)
            self.ui.rain_month_01.setEnabled(0)
            self.ui.rain_month_02.setEnabled(0)
            self.ui.rain_month_03.setEnabled(0)
            self.ui.rain_month_04.setEnabled(0)
            self.ui.rain_month_05.setEnabled(0)
            self.ui.rain_month_06.setEnabled(0)
            self.ui.rain_month_07.setEnabled(0)
            self.ui.rain_month_08.setEnabled(0)
            self.ui.rain_month_09.setEnabled(0)
            self.ui.rain_month_10.setEnabled(0)
            self.ui.rain_month_11.setEnabled(0)
            self.ui.rain_month_12.setEnabled(0)
        
        if self.module.getParameterAsString("evap_scale") == "1":
            self.ui.scale_evap_check.setChecked(1)
            self.ui.evap_month_01.setEnabled(1)
            self.ui.evap_month_02.setEnabled(1)
            self.ui.evap_month_03.setEnabled(1)
            self.ui.evap_month_04.setEnabled(1)
            self.ui.evap_month_05.setEnabled(1)
            self.ui.evap_month_06.setEnabled(1)
            self.ui.evap_month_07.setEnabled(1)
            self.ui.evap_month_08.setEnabled(1)
            self.ui.evap_month_09.setEnabled(1)
            self.ui.evap_month_10.setEnabled(1)
            self.ui.evap_month_11.setEnabled(1)
            self.ui.evap_month_12.setEnabled(1)
        else:
            self.ui.scale_evap_check.setChecked(0)
            self.ui.evap_month_01.setEnabled(0)
            self.ui.evap_month_02.setEnabled(0)
            self.ui.evap_month_03.setEnabled(0)
            self.ui.evap_month_04.setEnabled(0)
            self.ui.evap_month_05.setEnabled(0)
            self.ui.evap_month_06.setEnabled(0)
            self.ui.evap_month_07.setEnabled(0)
            self.ui.evap_month_08.setEnabled(0)
            self.ui.evap_month_09.setEnabled(0)
            self.ui.evap_month_10.setEnabled(0)
            self.ui.evap_month_11.setEnabled(0)
            self.ui.evap_month_12.setEnabled(0)
        
        if self.module.getParameterAsString("solar_scale") == "1":
            self.ui.scale_solar_check.setChecked(1)
            self.ui.solar_month_01.setEnabled(1)
            self.ui.solar_month_02.setEnabled(1)
            self.ui.solar_month_03.setEnabled(1)
            self.ui.solar_month_04.setEnabled(1)
            self.ui.solar_month_05.setEnabled(1)
            self.ui.solar_month_06.setEnabled(1)
            self.ui.solar_month_07.setEnabled(1)
            self.ui.solar_month_08.setEnabled(1)
            self.ui.solar_month_09.setEnabled(1)
            self.ui.solar_month_10.setEnabled(1)
            self.ui.solar_month_11.setEnabled(1)
            self.ui.solar_month_12.setEnabled(1)
        else:
            self.ui.scale_solar_check.setChecked(0)
            self.ui.solar_month_01.setEnabled(0)
            self.ui.solar_month_02.setEnabled(0)
            self.ui.solar_month_03.setEnabled(0)
            self.ui.solar_month_04.setEnabled(0)
            self.ui.solar_month_05.setEnabled(0)
            self.ui.solar_month_06.setEnabled(0)
            self.ui.solar_month_07.setEnabled(0)
            self.ui.solar_month_08.setEnabled(0)
            self.ui.solar_month_09.setEnabled(0)
            self.ui.solar_month_10.setEnabled(0)
            self.ui.solar_month_11.setEnabled(0)
            self.ui.solar_month_12.setEnabled(0)
        
        self.ui.rain_month_01.setValue(float(self.module.getParameterAsString("rsf_01")))
        self.ui.rain_month_02.setValue(float(self.module.getParameterAsString("rsf_02")))
        self.ui.rain_month_03.setValue(float(self.module.getParameterAsString("rsf_03")))
        self.ui.rain_month_04.setValue(float(self.module.getParameterAsString("rsf_04")))
        self.ui.rain_month_05.setValue(float(self.module.getParameterAsString("rsf_05")))
        self.ui.rain_month_06.setValue(float(self.module.getParameterAsString("rsf_06")))
        self.ui.rain_month_07.setValue(float(self.module.getParameterAsString("rsf_07")))
        self.ui.rain_month_08.setValue(float(self.module.getParameterAsString("rsf_08")))
        self.ui.rain_month_09.setValue(float(self.module.getParameterAsString("rsf_09")))
        self.ui.rain_month_10.setValue(float(self.module.getParameterAsString("rsf_10")))
        self.ui.rain_month_11.setValue(float(self.module.getParameterAsString("rsf_11")))
        self.ui.rain_month_12.setValue(float(self.module.getParameterAsString("rsf_12")))
        
        self.ui.evap_month_01.setValue(float(self.module.getParameterAsString("esf_01")))
        self.ui.evap_month_02.setValue(float(self.module.getParameterAsString("esf_02")))
        self.ui.evap_month_03.setValue(float(self.module.getParameterAsString("esf_03")))
        self.ui.evap_month_04.setValue(float(self.module.getParameterAsString("esf_04")))
        self.ui.evap_month_05.setValue(float(self.module.getParameterAsString("esf_05")))
        self.ui.evap_month_06.setValue(float(self.module.getParameterAsString("esf_06")))
        self.ui.evap_month_07.setValue(float(self.module.getParameterAsString("esf_07")))
        self.ui.evap_month_08.setValue(float(self.module.getParameterAsString("esf_08")))
        self.ui.evap_month_09.setValue(float(self.module.getParameterAsString("esf_09")))
        self.ui.evap_month_10.setValue(float(self.module.getParameterAsString("esf_10")))
        self.ui.evap_month_11.setValue(float(self.module.getParameterAsString("esf_11")))
        self.ui.evap_month_12.setValue(float(self.module.getParameterAsString("esf_12")))
        
        self.ui.solar_month_01.setValue(float(self.module.getParameterAsString("ssf_01")))
        self.ui.solar_month_02.setValue(float(self.module.getParameterAsString("ssf_02")))
        self.ui.solar_month_03.setValue(float(self.module.getParameterAsString("ssf_03")))
        self.ui.solar_month_04.setValue(float(self.module.getParameterAsString("ssf_04")))
        self.ui.solar_month_05.setValue(float(self.module.getParameterAsString("ssf_05")))
        self.ui.solar_month_06.setValue(float(self.module.getParameterAsString("ssf_06")))
        self.ui.solar_month_07.setValue(float(self.module.getParameterAsString("ssf_07")))
        self.ui.solar_month_08.setValue(float(self.module.getParameterAsString("ssf_08")))
        self.ui.solar_month_09.setValue(float(self.module.getParameterAsString("ssf_09")))
        self.ui.solar_month_10.setValue(float(self.module.getParameterAsString("ssf_10")))
        self.ui.solar_month_11.setValue(float(self.module.getParameterAsString("ssf_11")))
        self.ui.solar_month_12.setValue(float(self.module.getParameterAsString("ssf_12")))
        
        QtCore.QObject.connect(self.ui.scale_rain_check, QtCore.SIGNAL("clicked()"), self.raindatascaling_check)
        QtCore.QObject.connect(self.ui.scale_evap_check, QtCore.SIGNAL("clicked()"), self.evapdatascaling_check)
        QtCore.QObject.connect(self.ui.scale_solar_check, QtCore.SIGNAL("clicked()"), self.solardatascaling_check)
        
        
        #######################################
        #Hydrology Tab
        #######################################
        self.ui.Simpmax_box.setText(self.module.getParameterAsString("Simpmax"))
        self.ui.Spervmax_box.setText(self.module.getParameterAsString("Spervmax"))
        self.ui.muskK_box.setText(self.module.getParameterAsString("muskK"))
        self.ui.muskTheta_box.setText(self.module.getParameterAsString("muskTheta"))
                
        if self.module.getParameterAsString("route_method") == "1":
            self.ui.route_method_musk_radio.setChecked(True)
        if self.module.getParameterAsString("route_method") == "2":
            self.ui.route_method_kwave_radio.setChecked(True)
        
        #######################################
        #Pollution/Treatment Tab
        #######################################
        
    
    
    
    
        #######################################
        #Demand Pattern Tab
        #######################################
        #LINE EDITS - INDOOR
        self.ui.freq_kitchen_box.setText(self.module.getParameterAsString("freq_kitchen"))
        self.ui.freq_shower_box.setText(self.module.getParameterAsString("freq_shower"))
        self.ui.freq_toilet_box.setText(self.module.getParameterAsString("freq_toilet"))
        self.ui.freq_laundry_box.setText(self.module.getParameterAsString("freq_laundry"))
        self.ui.dur_kitchen_box.setText(self.module.getParameterAsString("dur_kitchen"))
        self.ui.dur_shower_box.setText(self.module.getParameterAsString("dur_shower"))
        self.ui.demandvary_kitchen_box.setText(self.module.getParameterAsString("demandvary_kitchen"))
        self.ui.demandvary_shower_box.setText(self.module.getParameterAsString("demandvary_shower"))
        self.ui.demandvary_toilet_box.setText(self.module.getParameterAsString("demandvary_toilet"))
        self.ui.demandvary_laundry_box.setText(self.module.getParameterAsString("demandvary_laundry"))
        
        #COMBO BOXES - INDOOR
        if self.module.getParameterAsString("ffp_kitchen") == "PO":
            self.ui.ffp_kitchen_combo.setCurrentIndex(0)
        elif self.module.getParameterAsString("ffp_kitchen") == "NP":
            self.ui.ffp_kitchen_combo.setCurrentIndex(1)
        elif self.module.getParameterAsString("ffp_kitchen") == "RW":
            self.ui.ffp_kitchen_combo.setCurrentIndex(2)
        elif self.module.getParameterAsString("ffp_kitchen") == "SW":
            self.ui.ffp_kitchen_combo.setCurrentIndex(3)
        elif self.module.getParameterAsString("ffp_kitchen") == "GW":
            self.ui.ffp_kitchen_combo.setCurrentIndex(4)
        
        if self.module.getParameterAsString("ffp_shower") == "PO":
            self.ui.ffp_shower_combo.setCurrentIndex(0)
        elif self.module.getParameterAsString("ffp_shower") == "NP":
            self.ui.ffp_shower_combo.setCurrentIndex(1)
        elif self.module.getParameterAsString("ffp_shower") == "RW":
            self.ui.ffp_shower_combo.setCurrentIndex(2)
        elif self.module.getParameterAsString("ffp_shower") == "SW":
            self.ui.ffp_shower_combo.setCurrentIndex(3)
        elif self.module.getParameterAsString("ffp_shower") == "GW":
            self.ui.ffp_shower_combo.setCurrentIndex(4)
        
        if self.module.getParameterAsString("ffp_toilet") == "PO":
            self.ui.ffp_toilet_combo.setCurrentIndex(0)
        elif self.module.getParameterAsString("ffp_toilet") == "NP":
            self.ui.ffp_toilet_combo.setCurrentIndex(1)
        elif self.module.getParameterAsString("ffp_toilet") == "RW":
            self.ui.ffp_toilet_combo.setCurrentIndex(2)
        elif self.module.getParameterAsString("ffp_toilet") == "SW":
            self.ui.ffp_toilet_combo.setCurrentIndex(3)
        elif self.module.getParameterAsString("ffp_toilet") == "GW":
            self.ui.ffp_toilet_combo.setCurrentIndex(4)
        
        if self.module.getParameterAsString("ffp_laundry") == "PO":
            self.ui.ffp_laundry_combo.setCurrentIndex(0)
        elif self.module.getParameterAsString("ffp_laundry") == "NP":
            self.ui.ffp_laundry_combo.setCurrentIndex(1)
        elif self.module.getParameterAsString("ffp_laundry") == "RW":
            self.ui.ffp_laundry_combo.setCurrentIndex(2)
        elif self.module.getParameterAsString("ffp_laundry") == "SW":
            self.ui.ffp_laundry_combo.setCurrentIndex(3)
        elif self.module.getParameterAsString("ffp_laundry") == "GW":
            self.ui.ffp_laundry_combo.setCurrentIndex(4)
		
        #GARDEN - LINE & COMBO BOX
        self.ui.t2t_house_box.setText(self.module.getParameterAsString("t2t_household"))
        
        if self.module.getParameterAsString("ffp_garden") == "PO":
            self.ui.ffp_garden_combo.setCurrentIndex(0)
        elif self.module.getParameterAsString("ffp_garden") == "NP":
            self.ui.ffp_garden_combo.setCurrentIndex(1)
        elif self.module.getParameterAsString("ffp_garden") == "RW":
            self.ui.ffp_garden_combo.setCurrentIndex(2)
        elif self.module.getParameterAsString("ffp_garden") == "SW":
            self.ui.ffp_garden_combo.setCurrentIndex(3)
        elif self.module.getParameterAsString("ffp_garden") == "GW":
            self.ui.ffp_garden_combo.setCurrentIndex(4)
		
        #OTHER DEMANDS
        self.ui.other_demand_box.setText(self.module.getParameterAsString("other_demand"))
        self.ui.t2t_public_box.setText(self.module.getParameterAsString("t2t_public"))
        
            #CHECK BOXES
        if self.module.getParameterAsString("irrigate_commun") == "1":
            self.ui.choose_commun_check.setChecked(1)
        else:
            self.ui.choose_commun_check.setChecked(0)
        
        if self.module.getParameterAsString("irrigate_pg") == "1":
            self.ui.choose_pg_check.setChecked(1)
        else:
            self.ui.choose_pg_check.setChecked(0)
        
        if self.module.getParameterAsString("irrigate_resflood") == "1":
            self.ui.choose_resflood_check.setChecked(1)
        else:
            self.ui.choose_resflood_check.setChecked(0)
            
            #COMBO BOXES
        if self.module.getParameterAsString("ffp_public") == "PO":
            self.ui.ffp_public_combo.setCurrentIndex(0)
        elif self.module.getParameterAsString("ffp_public") == "NP":
            self.ui.ffp_public_combo.setCurrentIndex(1)
        elif self.module.getParameterAsString("ffp_public") == "RW":
            self.ui.ffp_public_combo.setCurrentIndex(2)
        elif self.module.getParameterAsString("ffp_public") == "SW":
            self.ui.ffp_public_combo.setCurrentIndex(3)
        elif self.module.getParameterAsString("ffp_public") == "GW":
            self.ui.ffp_public_combo.setCurrentIndex(4)
        
        #EFFICIENCY & IRRIGATION SETTINGS
        self.ui.efficiency_slider.setValue(int(self.module.getParameterAsString("start_efficiency")))
        
        if self.module.getParameterAsString("initial_irrigate") == "TSS":
            self.ui.irrigateinit_full_radio.setChecked(True)
        if self.module.getParameterAsString("initial_irrigate") == "PET":
            self.ui.irrigateinit_perc_radio.setChecked(True)
        if self.module.getParameterAsString("initial_irrigate") == "NON":
            self.ui.irrigateinit_none_radio.setChecked(True)
        
        QtCore.QObject.connect(self.ui.irrigateinit_full_radio, QtCore.SIGNAL("clicked()"), self.irrigateinit_full_radio_change)
        QtCore.QObject.connect(self.ui.irrigateinit_perc_radio, QtCore.SIGNAL("clicked()"), self.irrigateinit_perc_radio_change)
            
        self.ui.irrigateinit_full_spin.setValue(float(self.module.getParameterAsString("irrigatesim_dur")))
        self.ui.irrigateinit_perc_spin.setValue(float(self.module.getParameterAsString("irrigatepet_perc")))
            
        #DEMAND DISAGGREGATION (STILL NEED ENABLE/DISABLE CODE)
        if self.module.getParameterAsString("dagg_method") == "LD":
            self.ui.dagg_sds_radio.setChecked(True)
        if self.module.getParameterAsString("dagg_method") == "DP":
            self.ui.dagg_dp_radio.setChecked(True)
        
        QtCore.QObject.connect(self.ui.dagg_sds_radio, QtCore.SIGNAL("clicked()"), self.dagg_sds_radio_change)
        QtCore.QObject.connect(self.ui.dagg_sds_subp_check, QtCore.SIGNAL("clicked()"), self.dagg_sds_subp_change)
        #QtCore.QObject.connect(self.ui.dagg_dp_radio, QtCore.SIGNAL("clicked()"), self.dagg_dp_radio_change)
        QtCore.QObject.connect(self.ui.dagg_dp_predef_check, QtCore.SIGNAL("clicked()"), self.dagg_dp_predef_change)
        
        if self.module.getParameterAsString("daggld_subprop") == "1":
            self.ui.dagg_sds_subp_check.setChecked(1)
        else:
            self.ui.dagg_sds_subp_check.setChecked(0)

        self.ui.dagg_sds_vol_spin.setValue(float(self.module.getParameterAsString("daggld_dayprop")))

        if self.module.getParameterAsString("daggdp_predef") == "1":
            self.ui.dagg_dp_predef_check.setChecked(1)
        else:
            self.ui.dagg_dp_predef_check.setChecked(0)

        if self.module.getParameterAsString("daggdp_method") == "GJ":
            self.ui.dagg_dp_pdbox.setCurrentIndex(0)
        elif self.module.getParameterAsString("daggdp_method") == "MW":
            self.ui.dagg_dp_pdbox.setCurrentIndex(1)

        if self.module.getParameterAsString("daggdp_custom") == "1":
            self.ui.dagg_dp_custom_check.setChecked(1)
        else:
            self.ui.dagg_dp_custom_check.setChecked(0)
        
        self.ui.dagg_dp_morningspin.setValue(float(self.module.getParameterAsString("daggdp_morning")))
        self.ui.dagg_dp_noonspin.setValue(float(self.module.getParameterAsString("daggdp_noon")))
        self.ui.dagg_dp_eveningspin.setValue(float(self.module.getParameterAsString("daggdp_evening")))
        self.ui.dagg_dp_nightspin.setValue(float(self.module.getParameterAsString("daggdp_night")))
                
        #######################################
        #Supply & Wastewater Tab
        #######################################
                
        #######################################
        #Energy Tab
        #######################################
        
        #######################################
        #Economics Tab Tab
        #######################################
        
                
        QtCore.QObject.connect(self.ui.buttonBox, QtCore.SIGNAL("accepted()"), self.save_values)
        
    ##################################
    #CLIMATE & GENERAL TAB FUNCTIONS #
    ##################################
    def openFileChooserDialogRain(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, self.caption, os.curdir, self.filter)
        if fname: 
            self.ui.rain_in_box.setText(fname) 
    
    def openFileChooserDialogEvap(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, self.caption, os.curdir, self.filter)
        if fname: 
            self.ui.evap_in_box.setText(fname)
    
    def openFileChooserDialogSolar(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, self.caption, os.curdir, self.filter)
        if fname: 
            self.ui.solar_in_box.setText(fname)
    
    def raindatascaling_check(self):
        if self.ui.scale_rain_check.isChecked() == 1:
            self.ui.rain_month_01.setEnabled(1)
            self.ui.rain_month_02.setEnabled(1)
            self.ui.rain_month_03.setEnabled(1)
            self.ui.rain_month_04.setEnabled(1)
            self.ui.rain_month_05.setEnabled(1)
            self.ui.rain_month_06.setEnabled(1)
            self.ui.rain_month_07.setEnabled(1)
            self.ui.rain_month_08.setEnabled(1)
            self.ui.rain_month_09.setEnabled(1)
            self.ui.rain_month_10.setEnabled(1)
            self.ui.rain_month_11.setEnabled(1)
            self.ui.rain_month_12.setEnabled(1)
        else:
            self.ui.rain_month_01.setEnabled(0)
            self.ui.rain_month_02.setEnabled(0)
            self.ui.rain_month_03.setEnabled(0)
            self.ui.rain_month_04.setEnabled(0)
            self.ui.rain_month_05.setEnabled(0)
            self.ui.rain_month_06.setEnabled(0)
            self.ui.rain_month_07.setEnabled(0)
            self.ui.rain_month_08.setEnabled(0)
            self.ui.rain_month_09.setEnabled(0)
            self.ui.rain_month_10.setEnabled(0)
            self.ui.rain_month_11.setEnabled(0)
            self.ui.rain_month_12.setEnabled(0)

    def evapdatascaling_check(self):
        if self.ui.scale_evap_check.isChecked() == 1:
            self.ui.evap_month_01.setEnabled(1)
            self.ui.evap_month_02.setEnabled(1)
            self.ui.evap_month_03.setEnabled(1)
            self.ui.evap_month_04.setEnabled(1)
            self.ui.evap_month_05.setEnabled(1)
            self.ui.evap_month_06.setEnabled(1)
            self.ui.evap_month_07.setEnabled(1)
            self.ui.evap_month_08.setEnabled(1)
            self.ui.evap_month_09.setEnabled(1)
            self.ui.evap_month_10.setEnabled(1)
            self.ui.evap_month_11.setEnabled(1)
            self.ui.evap_month_12.setEnabled(1)
        else:
            self.ui.evap_month_01.setEnabled(0)
            self.ui.evap_month_02.setEnabled(0)
            self.ui.evap_month_03.setEnabled(0)
            self.ui.evap_month_04.setEnabled(0)
            self.ui.evap_month_05.setEnabled(0)
            self.ui.evap_month_06.setEnabled(0)
            self.ui.evap_month_07.setEnabled(0)
            self.ui.evap_month_08.setEnabled(0)
            self.ui.evap_month_09.setEnabled(0)
            self.ui.evap_month_10.setEnabled(0)
            self.ui.evap_month_11.setEnabled(0)
            self.ui.evap_month_12.setEnabled(0)

    def solardatascaling_check(self):
        if self.ui.scale_solar_check.isChecked() == 1:
            self.ui.solar_month_01.setEnabled(1)
            self.ui.solar_month_02.setEnabled(1)
            self.ui.solar_month_03.setEnabled(1)
            self.ui.solar_month_04.setEnabled(1)
            self.ui.solar_month_05.setEnabled(1)
            self.ui.solar_month_06.setEnabled(1)
            self.ui.solar_month_07.setEnabled(1)
            self.ui.solar_month_08.setEnabled(1)
            self.ui.solar_month_09.setEnabled(1)
            self.ui.solar_month_10.setEnabled(1)
            self.ui.solar_month_11.setEnabled(1)
            self.ui.solar_month_12.setEnabled(1)
        else:
            self.ui.solar_month_01.setEnabled(0)
            self.ui.solar_month_02.setEnabled(0)
            self.ui.solar_month_03.setEnabled(0)
            self.ui.solar_month_04.setEnabled(0)
            self.ui.solar_month_05.setEnabled(0)
            self.ui.solar_month_06.setEnabled(0)
            self.ui.solar_month_07.setEnabled(0)
            self.ui.solar_month_08.setEnabled(0)
            self.ui.solar_month_09.setEnabled(0)
            self.ui.solar_month_10.setEnabled(0)
            self.ui.solar_month_11.setEnabled(0)
            self.ui.solar_month_12.setEnabled(0)
    
    def irrigateinit_full_radio_change(self):
        if self.ui.irrigateinit_full_radio.isChecked() == 1:
            self.ui.irrigateinit_full_spin.setEnabled(1)
        else:
            self.ui.irrigateinit_full_spin.setEnabled(0)
    
    def irrigateinit_perc_radio_change(self):
        if self.ui.irrigateinit_perc_radio.isChecked() == 1:
            self.ui.irrigateinit_perc_spin.setEnabled(1)
        else:
            self.ui.irrigateinit_perc_spin.setEnabled(0)
    
    def dagg_sds_radio_change(self):
        if self.ui.irrigateinit_perc_radio.isChecked() == 1:
            self.ui.dagg_sds_subp_check.setEnabled(1)
            if self.ui.dagg_sds_subp_check.isChecked() == 1:
                self.ui.dagg_sds_vol_spin.setEnabled(1)
            else:
                self.ui.dagg_sds_vol_spin.setEnabled(0)
        else:
            self.ui.dagg_sds_subp_check.setEnabled(0)
            self.ui.dagg_sds_vol_spin.setEnabled(0)
    
    def dagg_sds_subp_change(self):
        if self.ui.dagg_sds_subp_check.isChecked() == 1:
            self.ui.dagg_sds_vol_spin.setEnabled(1)
        else:
            self.ui.dagg_sds_vol_spin.setEnabled(0)
        
#    def dagg_dp_radio_change(self):
#        if self.ui.irrigateinit_perc_radio.isChecked() == 1:
#            self.ui.dagg_dp_predef_check.setEnabled(1)
#            self.ui.dagg_dp_predef_check.setEnabled(1)
#        else:
#            self.ui.dagg_dp_predef_check.setEnabled(0)
#            self.ui.irrigateinit_perc_spin.setEnabled(0)
#            self.ui.irrigateinit_perc_spin.setEnabled(0)
#            self.ui.irrigateinit_perc_spin.setEnabled(0)
#            self.ui.irrigateinit_perc_spin.setEnabled(0)
#            self.ui.irrigateinit_perc_spin.setEnabled(0)
#            self.ui.irrigateinit_perc_spin.setEnabled(0)

    def dagg_dp_predef_change(self):
        if self.ui.dagg_dp_predef_check.isChecked() == 1:
            self.ui.dagg_dp_pdbox.setEnabled(1)
        else:
            self.ui.dagg_dp_pdbox.setEnabled(0)
        
    def save_values(self):
    
        #######################################
        #Climate Tab
        #######################################
        
        #### TIME SERIES ####
        rain_ts = str(self.ui.rain_ts_box.text())
        self.module.setParameterValue("rain_ts", rain_ts)
        
        evap_ts = str(self.ui.evap_ts_box.text())
        self.module.setParameterValue("evap_ts", evap_ts)
        
        solar_ts = str(self.ui.solar_ts_box.text())
        self.module.setParameterValue("solar_ts", solar_ts)
        
        rain_fname = str(self.ui.rain_in_box.text())
        self.module.setParameterValue("rain_fname", rain_fname)
        
        evap_fname = str(self.ui.evap_in_box.text())
        self.module.setParameterValue("evap_fname", evap_fname)
        
        solar_fname = str(self.ui.solar_in_box.text())
        self.module.setParameterValue("solar_fname", solar_fname)
        
        #### CLIMATE FACTORS ####
        #RAIN FACTORS
        rsf_01 = str(self.ui.rain_month_01.value())
        self.module.setParameterValue("rsf_01", rsf_01)
        
        rsf_02 = str(self.ui.rain_month_02.value())
        self.module.setParameterValue("rsf_02", rsf_02)
        
        rsf_03 = str(self.ui.rain_month_03.value())
        self.module.setParameterValue("rsf_03", rsf_03)
        
        rsf_04 = str(self.ui.rain_month_04.value())
        self.module.setParameterValue("rsf_04", rsf_04)
        
        rsf_05 = str(self.ui.rain_month_05.value())
        self.module.setParameterValue("rsf_05", rsf_05)
        
        rsf_06 = str(self.ui.rain_month_06.value())
        self.module.setParameterValue("rsf_06", rsf_06)
        
        rsf_07 = str(self.ui.rain_month_07.value())
        self.module.setParameterValue("rsf_07", rsf_07)
        
        rsf_08 = str(self.ui.rain_month_08.value())
        self.module.setParameterValue("rsf_08", rsf_08)
        
        rsf_09 = str(self.ui.rain_month_09.value())
        self.module.setParameterValue("rsf_09", rsf_09)
        
        rsf_10 = str(self.ui.rain_month_10.value())
        self.module.setParameterValue("rsf_10", rsf_10)
        
        rsf_11 = str(self.ui.rain_month_11.value())
        self.module.setParameterValue("rsf_11", rsf_11)
        
        rsf_12 = str(self.ui.rain_month_12.value())
        self.module.setParameterValue("rsf_12", rsf_12)
        
        #EVAPORATION FACTORS
        esf_01 = str(self.ui.evap_month_01.value())
        self.module.setParameterValue("esf_01", esf_01)
        
        esf_02 = str(self.ui.evap_month_02.value())
        self.module.setParameterValue("esf_02", esf_02)
        
        esf_03 = str(self.ui.evap_month_03.value())
        self.module.setParameterValue("esf_03", esf_03)
        
        esf_04 = str(self.ui.evap_month_04.value())
        self.module.setParameterValue("esf_04", esf_04)
        
        esf_05 = str(self.ui.evap_month_05.value())
        self.module.setParameterValue("esf_05", esf_05)
        
        esf_06 = str(self.ui.evap_month_06.value())
        self.module.setParameterValue("esf_06", esf_06)
        
        esf_07 = str(self.ui.evap_month_07.value())
        self.module.setParameterValue("esf_07", esf_07)
        
        esf_08 = str(self.ui.evap_month_08.value())
        self.module.setParameterValue("esf_08", esf_08)
        
        esf_09 = str(self.ui.evap_month_09.value())
        self.module.setParameterValue("esf_09", esf_09)
        
        esf_10 = str(self.ui.evap_month_10.value())
        self.module.setParameterValue("esf_10", esf_10)
        
        esf_11 = str(self.ui.evap_month_11.value())
        self.module.setParameterValue("esf_11", esf_11)
        
        esf_12 = str(self.ui.evap_month_12.value())
        self.module.setParameterValue("esf_12", esf_12)
        
        #SOLAR RADIATION FACTORS
        ssf_01 = str(self.ui.solar_month_01.value())
        self.module.setParameterValue("ssf_01", ssf_01)
        
        ssf_02 = str(self.ui.solar_month_02.value())
        self.module.setParameterValue("ssf_02", ssf_02)
        
        ssf_03 = str(self.ui.solar_month_03.value())
        self.module.setParameterValue("ssf_03", ssf_03)
        
        ssf_04 = str(self.ui.solar_month_04.value())
        self.module.setParameterValue("ssf_04", ssf_04)
        
        ssf_05 = str(self.ui.solar_month_05.value())
        self.module.setParameterValue("ssf_05", ssf_05)
        
        ssf_06 = str(self.ui.solar_month_06.value())
        self.module.setParameterValue("ssf_06", ssf_06)
        
        ssf_07 = str(self.ui.solar_month_07.value())
        self.module.setParameterValue("ssf_07", ssf_07)
        
        ssf_08 = str(self.ui.solar_month_08.value())
        self.module.setParameterValue("ssf_08", ssf_08)
        
        ssf_09 = str(self.ui.solar_month_09.value())
        self.module.setParameterValue("ssf_09", ssf_09)
        
        ssf_10 = str(self.ui.solar_month_10.value())
        self.module.setParameterValue("ssf_10", ssf_10)
        
        ssf_11 = str(self.ui.solar_month_11.value())
        self.module.setParameterValue("ssf_11", ssf_11)
        
        ssf_12 = str(self.ui.solar_month_12.value())
        self.module.setParameterValue("ssf_12", ssf_12)
        
        #######################################
        #Hydrology Tab
        #######################################
        Simpmax = str(self.ui.Simpmax_box.text())
        self.module.setParameterValue("Simpmax", Simpmax)
        
        Spervmax = str(self.ui.Spervmax_box.text())
        self.module.setParameterValue("Spervmax", Spervmax)
        
        muskK = str(self.ui.muskK_box.text())
        self.module.setParameterValue("muskK", muskK)
        
        muskTheta = str(self.ui.muskTheta_box.text())
        self.module.setParameterValue("muskTheta", muskTheta)
        
        if self.ui.route_method_musk_radio.isChecked() == True:
            route_method = "1"
        if self.ui.route_method_kwave_radio.isChecked() == True:
            route_method = "2"
        self.module.setParameterValue("route_method", route_method)
    
        #######################################
        #Pollution/Treatment Tab
        #######################################
    
    
        
        
        
        #######################################
        #Demand Pattern Tab
        #######################################
            #LINE EDITS
        freq_kitchen = str(self.ui.freq_kitchen_box.text())
        self.module.setParameterValue("freq_kitchen", freq_kitchen)    
            
        freq_shower = str(self.ui.freq_shower_box.text())
        self.module.setParameterValue("freq_shower", freq_shower)
        
        freq_toilet = str(self.ui.freq_toilet_box.text())
        self.module.setParameterValue("freq_toilet", freq_toilet)
        
        freq_laundry = str(self.ui.freq_laundry_box.text())
        self.module.setParameterValue("freq_laundry", freq_laundry)
        
        dur_kitchen = str(self.ui.dur_kitchen_box.text())
        self.module.setParameterValue("dur_kitchen", dur_kitchen)
        
        dur_shower = str(self.ui.dur_shower_box.text())
        self.module.setParameterValue("dur_shower", dur_shower)
        
        demandvary_kitchen = str(self.ui.demandvary_kitchen_box.text())
        self.module.setParameterValue("demandvary_kitchen", demandvary_kitchen)
        
        demandvary_shower = str(self.ui.demandvary_shower_box.text())
        self.module.setParameterValue("demandvary_shower", demandvary_shower)
        
        demandvary_toilet = str(self.ui.demandvary_toilet_box.text())
        self.module.setParameterValue("demandvary_toilet", demandvary_toilet)
        
        demandvary_laundry = str(self.ui.demandvary_laundry_box.text())
        self.module.setParameterValue("demandvary_laundry", demandvary_laundry)
        
        t2t_household = str(self.ui.t2t_house_box.text())
        self.module.setParameterValue("t2t_household", t2t_household)
        
        t2t_public = str(self.ui.t2t_public_box.text())
        self.module.setParameterValue("t2t_public", t2t_public)
        
        other_demand = str(self.ui.other_demand_box.text())
        self.module.setParameterValue("other_demand", other_demand)    
            
            #CHECK BOXES
        if self.ui.choose_commun_check.isChecked() == 1:
            irrigate_commun = 1
        else:
            irrigate_commun = 0
        self.module.setParameterValue("irrigate_commun", str(irrigate_commun))
    
        if self.ui.choose_pg_check.isChecked() == 1:
            irrigate_pg = 1
        else:
            irrigate_pg = 0
        self.module.setParameterValue("irrigate_pg", str(irrigate_pg))
        
        if self.ui.choose_resflood_check.isChecked() == 1:
            irrigate_resflood = 1
        else:
            irrigate_resflood = 0
        self.module.setParameterValue("irrigate_resflood", str(irrigate_resflood))
        
            #COMBO BOXES
        ffp_matrix = ["PO", "NP", "RW", "SW", "GW"]
        
        ffp_kitchen_index = self.ui.ffp_kitchen_combo.currentIndex()
        ffp_kitchen = ffp_matrix[ffp_kitchen_index]
        self.module.setParameterValue("ffp_kitchen", ffp_kitchen)
        
        ffp_shower_index = self.ui.ffp_shower_combo.currentIndex()
        ffp_shower = ffp_matrix[ffp_shower_index]
        self.module.setParameterValue("ffp_shower", ffp_shower)
        
        ffp_toilet_index = self.ui.ffp_toilet_combo.currentIndex()
        ffp_toilet = ffp_matrix[ffp_toilet_index]
        self.module.setParameterValue("ffp_toilet", ffp_toilet)
        
        ffp_laundry_index = self.ui.ffp_laundry_combo.currentIndex()
        ffp_laundry = ffp_matrix[ffp_laundry_index]
        self.module.setParameterValue("ffp_laundry", ffp_laundry)
        
        ffp_garden_index = self.ui.ffp_garden_combo.currentIndex()
        ffp_garden = ffp_matrix[ffp_garden_index]
        self.module.setParameterValue("ffp_garden", ffp_garden)
        
        ffp_public_index = self.ui.ffp_public_combo.currentIndex()
        ffp_public = ffp_matrix[ffp_public_index]
        self.module.setParameterValue("ffp_public", ffp_public)
        
        #EFFICIENCY AND IRRIGATION
        start_efficiency = str(self.ui.efficiency_slider.value())
        self.module.setParameterValue("start_efficiency", start_efficiency)
        
        irrigatesim_dur = str(self.ui.irrigateinit_full_spin.value())
        self.module.setParameterValue("irrigatesim_dur", irrigatesim_dur)        
                
        irrigatepet_perc = str(self.ui.irrigateinit_perc_spin.value())
        self.module.setParameterValue("irrigatepet_perc", irrigatepet_perc)         
                
        if self.ui.irrigateinit_full_radio.isChecked() == True:
            initial_irrigate = "TSS"
        if self.ui.irrigateinit_perc_radio.isChecked() == True:
            initial_irrigate = "PET"
        if self.ui.irrigateinit_none_radio.isChecked() == True:
            initial_irrigate = "NON"
        self.module.setParameterValue("initial_irrigate", initial_irrigate)        
        
        #DEMAND DISAGGREGATION
        if self.ui.dagg_sds_radio.isChecked() == True:
            dagg_method = "LD"
        if self.ui.dagg_dp_radio.isChecked() == True:
            dagg_method = "DP"
        self.module.setParameterValue("dagg_method", dagg_method)         
        
        if self.ui.dagg_sds_subp_check.isChecked() == 1:
            daggld_subprop = 1
        else:
            daggld_subprop = 0
        self.module.setParameterValue("daggld_subprop", str(daggld_subprop))
        
        daggld_dayprop = str(self.ui.dagg_sds_vol_spin.value())
        self.module.setParameterValue("daggld_dayprop", daggld_dayprop)
        
        if self.ui.dagg_dp_predef_check.isChecked() == 1:
            daggdp_predef = 1
            daggdp_custom = 0
        else:
            daggdp_predef = 0
            daggdp_custom = 1
        self.module.setParameterValue("daggdp_predef", str(daggdp_predef))
        self.module.setParameterValue("daggdp_custom", str(daggdp_custom))
        
        if self.ui.dagg_dp_custom_check.isChecked() == 1:
            daggdp_custom = 1
        else:
            daggdp_custom = 0
        self.module.setParameterValue("daggdp_custom", str(daggdp_custom))
        
        daggdp_morning = str(self.ui.dagg_dp_morningspin.value())
        self.module.setParameterValue("daggld_dayprop", daggld_dayprop)
        
        daggdp_noon = str(self.ui.dagg_dp_noonspin.value())
        self.module.setParameterValue("daggdp_noon", daggdp_noon)
        
        daggdp_evening = str(self.ui.dagg_dp_eveningspin.value())
        self.module.setParameterValue("daggdp_evening", daggdp_evening)
        
        daggdp_night = str(self.ui.dagg_dp_nightspin.value())
        self.module.setParameterValue("daggdp_night", daggdp_night)
        
                
        #######################################
        #Supply & Wastewater Tab
        #######################################
        
        #######################################
        #Energy Tab
        #######################################
        
        #######################################
        #Economics Tab Tab
        #######################################
        
        
        
    
        