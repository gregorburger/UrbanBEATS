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
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See thepyui
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""
from PyQt4 import QtCore, QtGui
from pyvibe import *
from urbplanbbgui import Ui_BuildingBlockDialog
from urbplanbb_c1gui import Ui_c1_subDialog

class activateurbplanbbGUI(QtGui.QDialog):
    def __init__(self, m, parent=None):
        self.module = Module
        self.module = m
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_BuildingBlockDialog()
        self.ui.setupUi(self)
        
        #Assign Default Values & Connect Signal/Slots
        
        ##########################
        #General Rules Tab
        ##########################
        self.ui.maximperv_slider_2.setValue(int(self.module.getParameterAsString("maximperv")))
        self.ui.maximperv_boxval_2.setText(self.module.getParameterAsString("maximperv")+"%")
        self.ui.maxsitecover_slider_2.setValue(int(self.module.getParameterAsString("maxsitecover")))
        self.ui.maxsitecover_boxval_2.setText(self.module.getParameterAsString("maxsitecover")+"%")
        QtCore.QObject.connect(self.ui.maximperv_slider_2, QtCore.SIGNAL("valueChanged(int)"), self.maximperv_update)
        QtCore.QObject.connect(self.ui.maxsitecover_slider_2, QtCore.SIGNAL("valueChanged(int)"), self.maxsitecover_update)
        
        if self.module.getParameterAsString("locality_mun_trans") == "1":
            self.ui.mun_localmap_check.setChecked(1)
        else:
            self.ui.mun_localmap_check.setChecked(0)
#        if self.module.getParameterAsString("district_age_infer") == "1":
#            self.ui.district_age_check.setChecked(1)
#        else:
#            self.ui.district_age_check.setChecked(0)
        
        #variables for building block dynamics...
        
        ##########################
        #Residential Tab
        ##########################
        self.ui.occup_avg_box.setText(self.module.getParameterAsString("occup_avg"))
        self.ui.occup_max_box.setText(self.module.getParameterAsString("occup_max"))
        self.ui.person_space_box.setText(self.module.getParameterAsString("person_space"))
        self.ui.extra_comm_area_box.setText(self.module.getParameterAsString("extra_comm_area"))
        self.ui.setback_f_min_box.setText(self.module.getParameterAsString("setback_f_min"))
        self.ui.setback_f_max_box.setText(self.module.getParameterAsString("setback_f_max"))
        self.ui.setback_s_min_box.setText(self.module.getParameterAsString("setback_s_min"))
        self.ui.setback_s_max_box.setText(self.module.getParameterAsString("setback_s_max"))
        self.ui.carports_max_box.setText(self.module.getParameterAsString("carports_max"))
        
        if self.module.getParameterAsString("garage_incl") == "1":
            self.ui.garage_incl_box.setChecked(1)
        else:
            self.ui.garage_incl_box.setChecked(0)
        
        self.ui.w_driveway_min_box.setText(self.module.getParameterAsString("w_driveway_min"))
        self.ui.patio_area_max_box.setText(self.module.getParameterAsString("patio_area_max"))
        
        if self.module.getParameterAsString("patio_covered") == "1":
            self.ui.patio_covered_box.setChecked(1)
        else:
            self.ui.patio_covered_box.setChecked(0)
            
        self.ui.floor_num_max_box.setText(self.module.getParameterAsString("floor_num_max"))
        
        if self.module.getParameterAsString("floor_autobuild") == "1":
            self.ui.floor_autobuild_box.setChecked(1)
        else:
            self.ui.floor_autobuild_box.setChecked(0)
        
        self.ui.occup_flat_avg_box.setText(self.module.getParameterAsString("occup_flat_avg"))
        self.ui.commspace_indoor_box.setText(self.module.getParameterAsString("commspace_indoor"))
        self.ui.commspace_outdoor_box.setText(self.module.getParameterAsString("commspace_outdoor"))
        self.ui.flat_area_max_box.setText(self.module.getParameterAsString("flat_area_max"))
        self.ui.setback_HDR_avg_box.setText(self.module.getParameterAsString("setback_HDR_avg"))
        
        if self.module.getParameterAsString("setback_HDR_auto") == "1":
            self.ui.setback_HDR_auto_box.setChecked(1)
        else:
            self.ui.setback_HDR_auto_box.setChecked(0)
        
        if self.module.getParameterAsString("roof_connected") == "Direct":
            self.ui.roof_connected_radiodirect.setChecked(True)
        if self.module.getParameterAsString("roof_connected") == "Disconnect":
            self.ui.roof_connected_radiodisc.setChecked(True)
        if self.module.getParameterAsString("roof_connected") == "Vary":
            self.ui.roof_connected_radiovary.setChecked(True)
        
        self.ui.imperv_prop_dced_box.setText(self.module.getParameterAsString("imperv_prop_dced"))
        
        ##########################
        #Non-Residential Tab
        ##########################
        #--> Employment Details
        if self.module.getParameterAsString("employment_data") == "D":
            self.ui.jobs_direct_radio.setChecked(True)
            self.ui.jobs_radius_box.setEnabled(0)
            self.ui.jobs_rate_spin.setEnabled(0)
            self.ui.jobs_ratefactor_spin.setEnabled(0)
        if self.module.getParameterAsString("employment_data") == "P":
            self.ui.jobs_pop_radio.setChecked(True)
            self.ui.jobs_radius_box.setEnabled(1)
            self.ui.jobs_rate_spin.setEnabled(1)
            self.ui.jobs_ratefactor_spin.setEnabled(1)
        
        QtCore.QObject.connect(self.ui.jobs_direct_radio, QtCore.SIGNAL("clicked()"), self.employdatagetdirect)
        QtCore.QObject.connect(self.ui.jobs_pop_radio, QtCore.SIGNAL("clicked()"), self.employdatagetpop)
        
        self.ui.jobs_radius_box.setText(self.module.getParameterAsString("employment_rad"))
        self.ui.jobs_rate_spin.setValue(float(self.module.getParameterAsString("employment_rate")))
        self.ui.jobs_ratefactor_spin.setValue(float(self.module.getParameterAsString("employment_adjust")))
        
        if self.module.getParameterAsString("com_spacevary_check") == "1":
            self.ui.jobs_spacevary_check.setChecked(1)
        else:
            self.ui.jobs_spacevary_check.setChecked(0)
        
        #--> Site Layout
        self.ui.com_minfsetback_box.setText(self.module.getParameterAsString("com_fsetback_min"))
        
        if self.module.getParameterAsString("com_setback_auto") == "1":
            self.ui.com_minfsetback_auto.setChecked(1)
        else:
            self.ui.com_minfsetback_auto.setChecked(0)
        
        self.ui.com_maxfloors_spin.setValue(float(self.module.getParameterAsString("com_floors_max")))    
        
        #--> Car Parking and Service Areas
        self.ui.carpark_depth_box.setText(self.module.getParameterAsString("com_carpark_dmin"))
        self.ui.carpark_dimW_box.setText(self.module.getParameterAsString("com_carparkW"))
        self.ui.carpark_dimD_box.setText(self.module.getParameterAsString("com_carparkD"))
        self.ui.carpark_imp_spin.setValue(float(self.module.getParameterAsString("com_carpark_avgimp")))
        
        if self.module.getParameterAsString("com_carpark_share") == "1":
            self.ui.carpark_share_check.setChecked(1)
        else:
            self.ui.carpark_share_check.setChecked(0)
            
        self.ui.service_depth_box.setText(self.module.getParameterAsString("com_service_dmin"))
        
        #--> Service/Access Road
        if self.module.getParameterAsString("access_perp") == "1":
            self.ui.acc_typeperp_check.setChecked(1)
        else:
            self.ui.acc_typeperp_check.setChecked(0)
        
        if self.module.getParameterAsString("access_parall") == "1":
            self.ui.acc_typeparall_check.setChecked(1)
            self.ui.acc_typeparall_med_box.setEnabled(1)
        else:
            self.ui.acc_typeparall_check.setChecked(0)
            self.ui.acc_typeparall_med_box.setEnabled(0)
        QtCore.QObject.connect(self.ui.acc_typeparall_check, QtCore.SIGNAL("clicked()"), self.acc_typeparall_enable)
           
        if self.module.getParameterAsString("access_cds") == "1":
            self.ui.acc_typecds_check.setChecked(1)
            self.ui.acc_typecds_dia_box.setEnabled(1)
        else:
            self.ui.acc_typecds_check.setChecked(0)
            self.ui.acc_typecds_dia_box.setEnabled(0)
        QtCore.QObject.connect(self.ui.acc_typecds_check, QtCore.SIGNAL("clicked()"), self.acc_typecds_enable)
        
        if self.module.getParameterAsString("access_ped_include") == "1":
            self.ui.acc_includepeds_check.setChecked(1)
        else:
            self.ui.acc_includepeds_check.setChecked(0)
        
        self.ui.acc_typeparall_med_box.setText(self.module.getParameterAsString("access_parall_medwidth"))
        self.ui.acc_typecds_dia_box.setText(self.module.getParameterAsString("access_cds_circlerad"))    
        
        #--> Landscape & Drainage
        self.ui.lscape_hsbalance_slide.setValue(int(self.module.getParameterAsString("lscape_hsbal")))
        self.ui.com_impdced_box.setText(self.module.getParameterAsString("lscape_avgimp_dced"))
        
        #--> Municipal Facilities
        if self.module.getParameterAsString("mun_explicit") == "1":
            self.ui.mun_on_off_check.setChecked(1)
            self.ui.edu_school_box.setEnabled(1)
            self.ui.edu_uni_box.setEnabled(1)
            self.ui.edu_lib_box.setEnabled(1)
            self.ui.civ_hospital_box.setEnabled(1)
            self.ui.civ_clinic_box.setEnabled(1)
            self.ui.civ_police_box.setEnabled(1)
            self.ui.civ_fire_box.setEnabled(1)
            self.ui.civ_jail_box.setEnabled(1)
            self.ui.civ_religion_box.setEnabled(1)
            self.ui.civ_leisure_box.setEnabled(1)
            self.ui.civ_museum_box.setEnabled(1)
            self.ui.civ_zoo_box.setEnabled(1)
            self.ui.civ_sports_box.setEnabled(1)
            self.ui.civ_race_box.setEnabled(1)
            self.ui.civ_dead_box.setEnabled(1)
            self.ui.sut_waste_box.setEnabled(1)
            self.ui.sut_gas_box.setEnabled(1)
            self.ui.sut_electricity_box.setEnabled(1)
            self.ui.sut_water_box.setEnabled(1)
            self.ui.sut_lgoffice_box.setEnabled(1)
        else:
            self.ui.mun_on_off_check.setChecked(0)
            self.ui.edu_school_box.setEnabled(0)
            self.ui.edu_uni_box.setEnabled(0)
            self.ui.edu_lib_box.setEnabled(0)
            self.ui.civ_hospital_box.setEnabled(0)
            self.ui.civ_clinic_box.setEnabled(0)
            self.ui.civ_police_box.setEnabled(0)
            self.ui.civ_fire_box.setEnabled(0)
            self.ui.civ_jail_box.setEnabled(0)
            self.ui.civ_religion_box.setEnabled(0)
            self.ui.civ_leisure_box.setEnabled(0)
            self.ui.civ_museum_box.setEnabled(0)
            self.ui.civ_zoo_box.setEnabled(0)
            self.ui.civ_sports_box.setEnabled(0)
            self.ui.civ_race_box.setEnabled(0)
            self.ui.civ_dead_box.setEnabled(0)
            self.ui.sut_waste_box.setEnabled(0)
            self.ui.sut_gas_box.setEnabled(0)
            self.ui.sut_electricity_box.setEnabled(0)
            self.ui.sut_water_box.setEnabled(0)
            self.ui.sut_lgoffice_box.setEnabled(0)
        QtCore.QObject.connect(self.ui.mun_on_off_check, QtCore.SIGNAL("clicked()"), self.mun_on_off_enable)
                
                #EDUCATION
        if self.module.getParameterAsString("edu_school") == "1":
            self.ui.edu_school_box.setChecked(1)
        else:
            self.ui.edu_school_box.setChecked(0)
        
        if self.module.getParameterAsString("edu_uni") == "1":
            self.ui.edu_uni_box.setChecked(1)
        else:
            self.ui.edu_uni_box.setChecked(0)
        
        if self.module.getParameterAsString("edu_lib") == "1":
            self.ui.edu_lib_box.setChecked(1)
        else:
            self.ui.acc_typeperp_check.setChecked(0)
        #>>>>>ADDITIONAL PARAMETERS FOR CUSTOMISATION
        
                #CIVIC
        if self.module.getParameterAsString("civ_hospital") == "1":
            self.ui.civ_hospital_box.setChecked(1)
        else:
            self.ui.civ_hospital_box.setChecked(0)
        if self.module.getParameterAsString("civ_clinic") == "1":
            self.ui.civ_clinic_box.setChecked(1)
        else:
            self.ui.civ_clinic_box.setChecked(0)
        if self.module.getParameterAsString("civ_police") == "1":
            self.ui.civ_police_box.setChecked(1)
        else:
            self.ui.civ_police_box.setChecked(0)
        if self.module.getParameterAsString("civ_fire") == "1":
            self.ui.civ_fire_box.setChecked(1)
        else:
            self.ui.civ_fire_box.setChecked(0)
        if self.module.getParameterAsString("civ_jail") == "1":
            self.ui.civ_jail_box.setChecked(1)
        else:
            self.ui.civ_jail_box.setChecked(0)
        if self.module.getParameterAsString("civ_worship") == "1":
            self.ui.civ_religion_box.setChecked(1)
        else:
            self.ui.civ_religion_box.setChecked(0)
        if self.module.getParameterAsString("civ_leisure") == "1":
            self.ui.civ_leisure_box.setChecked(1)
        else:
            self.ui.civ_leisure_box.setChecked(0)
        if self.module.getParameterAsString("civ_museum") == "1":
            self.ui.civ_museum_box.setChecked(1)
        else:
            self.ui.civ_museum_box.setChecked(0)
        if self.module.getParameterAsString("civ_zoo") == "1":
            self.ui.civ_zoo_box.setChecked(1)
        else:
            self.ui.civ_zoo_box.setChecked(0)
        if self.module.getParameterAsString("civ_stadium") == "1":
            self.ui.civ_sports_box.setChecked(1)
        else:
            self.ui.civ_sports_box.setChecked(0)
        if self.module.getParameterAsString("civ_racing") == "1":
            self.ui.civ_race_box.setChecked(1)
        else:
            self.ui.civ_race_box.setChecked(0)
        if self.module.getParameterAsString("civ_cemetery") == "1":
            self.ui.civ_dead_box.setChecked(1)
        else:
            self.ui.civ_dead_box.setChecked(0)
        #>>>>>ADDITIONAL PARAMETERS FOR CUSTOMISATION
        
            #SERVICES & UTILITY
        if self.module.getParameterAsString("sut_waste") == "1":
            self.ui.sut_waste_box.setChecked(1)
        else:
            self.ui.sut_waste_box.setChecked(0)
        
        if self.module.getParameterAsString("sut_gas") == "1":
            self.ui.sut_gas_box.setChecked(1)
        else:
            self.ui.sut_gas_box.setChecked(0)
        
        if self.module.getParameterAsString("sut_electricity") == "1":
            self.ui.sut_electricity_box.setChecked(1)
        else:
            self.ui.sut_electricity_box.setChecked(0)
        
        if self.module.getParameterAsString("sut_water") == "1":
            self.ui.sut_water_box.setChecked(1)
        else:
            self.ui.sut_water_box.setChecked(0)
        
        if self.module.getParameterAsString("sut_lgoffice") == "1":
            self.ui.sut_lgoffice_box.setChecked(1)
        else:
            self.ui.sut_lgoffice_box.setChecked(0)
        #>>>>>ADDITIONAL PARAMETERS FOR CUSTOMISATION
        
        ##########################
        #Transport Tab
        ##########################
        #--> Frontage & Pedestrian Information
        self.ui.w_resfootpath_min_box.setText(self.module.getParameterAsString("w_resfootpath_min"))
        self.ui.w_resfootpath_max_box.setText(self.module.getParameterAsString("w_resfootpath_max"))
        self.ui.w_resnaturestrip_min_box.setText(self.module.getParameterAsString("w_resnaturestrip_min"))
        self.ui.w_resnaturestrip_max_box.setText(self.module.getParameterAsString("w_resnaturestrip_max"))
        
        if self.module.getParameterAsString("w_resfootpath_med") == "1":
            self.ui.w_resfootpath_med_check.setChecked(1)
        else:
            self.ui.w_resfootpath_med_check.setChecked(0)
        
        if self.module.getParameterAsString("w_resnaturestrip_med") == "1":
            self.ui.w_resnaturestrip_med_check.setChecked(1)
        else:
            self.ui.w_resnaturestrip_med_check.setChecked(0)
        
        self.ui.w_comfootpath_min_box.setText(self.module.getParameterAsString("w_comfootpath_min"))
        self.ui.w_comfootpath_max_box.setText(self.module.getParameterAsString("w_comfootpath_max"))
        self.ui.w_comnaturestrip_min_box.setText(self.module.getParameterAsString("w_comnaturestrip_min"))
        self.ui.w_comnaturestrip_max_box.setText(self.module.getParameterAsString("w_comnaturestrip_max"))
        
        if self.module.getParameterAsString("w_comfootpath_med") == "1":
            self.ui.w_comfootpath_med_check.setChecked(1)
        else:
            self.ui.w_comfootpath_med_check.setChecked(0)
        
        if self.module.getParameterAsString("w_comnaturestrip_med") == "1":
            self.ui.w_comnaturestrip_med_check.setChecked(1)
        else:
            self.ui.w_comnaturestrip_med_check.setChecked(0)
        
        #--> Local Access/Service/Collector Roads
        self.ui.w_collectlane_min_box.setText(self.module.getParameterAsString("w_collectlane_min"))
        self.ui.w_collectlane_max_box.setText(self.module.getParameterAsString("w_collectlane_max"))
        self.ui.collect_crossfall_box.setText(self.module.getParameterAsString("collect_crossfall")+"%")
        
        if self.module.getParameterAsString("w_collectlane_med") == "1":
            self.ui.w_collectlane_med_check.setChecked(1)
        else:
            self.ui.w_collectlane_med_check.setChecked(0)
        
        #--> Arterials/Direct Distributors/Dual Carriageways
        self.ui.w_arterial_min_box.setText(self.module.getParameterAsString("w_artlane_min"))
        self.ui.w_arterial_max_box.setText(self.module.getParameterAsString("w_artlane_max"))
        self.ui.w_arterialmed_box.setText(self.module.getParameterAsString("w_artmedian"))
        self.ui.arterial_crossfall_box.setText(self.module.getParameterAsString("art_crossfall")+"%")
        
        if self.module.getParameterAsString("w_artlane_med") == "1":
            self.ui.w_arterial_med_check.setChecked(1)
        else:
            self.ui.w_arterial_med_check.setChecked(0)
        
        if self.module.getParameterAsString("artmedian_reserved") == "1":
            self.ui.w_arterialmed_nodev_check.setChecked(1)
        else:
            self.ui.w_arterialmed_nodev_check.setChecked(0)
        
        #--> Highways/Freeways/Motorways
        self.ui.w_highwaylane_box.setText(self.module.getParameterAsString("w_hwylane_avg"))
        self.ui.w_highwaymed_box.setText(self.module.getParameterAsString("w_hwymedian"))
        self.ui.highway_crossfall_box.setText(self.module.getParameterAsString("hwy_crossfall")+"%")
        
        if self.module.getParameterAsString("hwy_buffered") == "1":
            self.ui.highway_buffer_check.setChecked(1)
        else:
            self.ui.highway_buffer_check.setChecked(0)
        
        if self.module.getParameterAsString("hwymedian_reserved") == "1":
            self.ui.w_highwaymed_nodev_check.setChecked(1)
        else:
            self.ui.w_highwaymed_nodev_check.setChecked(0)
        
        #--> Other Transport
        if self.module.getParameterAsString("trans_explicit") == "1":
            self.ui.trans_on_off_check.setChecked(1)
            self.ui.trans_airport_box.setEnabled(1)
            self.ui.trans_comseaport_box.setEnabled(1)
            self.ui.trans_indseaport_box.setEnabled(1)
            self.ui.trans_busdepot_box.setEnabled(1)
            self.ui.trans_rail_box.setEnabled(1)
        else:
            self.ui.trans_on_off_check.setChecked(0)
            self.ui.trans_airport_box.setEnabled(0)
            self.ui.trans_comseaport_box.setEnabled(0)
            self.ui.trans_indseaport_box.setEnabled(0)
            self.ui.trans_busdepot_box.setEnabled(0)
            self.ui.trans_rail_box.setEnabled(0)
        QtCore.QObject.connect(self.ui.trans_on_off_check, QtCore.SIGNAL("clicked()"), self.trans_on_off_enable)
        
        if self.module.getParameterAsString("trans_airport") == "1":
            self.ui.trans_airport_box.setChecked(1)
        else:
            self.ui.trans_airport_box.setChecked(0)
        
        if self.module.getParameterAsString("trans_comseaport") == "1":
            self.ui.trans_comseaport_box.setChecked(1)
        else:
            self.ui.trans_comseaport_box.setChecked(0)

        if self.module.getParameterAsString("trans_indseaport") == "1":
            self.ui.trans_indseaport_box.setChecked(1)
        else:
            self.ui.trans_indseaport_box.setChecked(0)
        
        if self.module.getParameterAsString("trans_busdepot") == "1":
            self.ui.trans_busdepot_box.setChecked(1)
        else:
            self.ui.trans_busdepot_box.setChecked(0)
        
        if self.module.getParameterAsString("trans_railterminal") == "1":
            self.ui.trans_rail_box.setChecked(1)
        else:
            self.ui.trans_rail_box.setChecked(0)
        

        ##########################
        #Open Space Tab
        ##########################
        #--> General Config
        self.ui.pg_clustering_slide.setValue(int(self.module.getParameterAsString("pg_clustering_degree")))
        self.ui.pg_ggratio_slide.setValue(int(self.module.getParameterAsString("pg_greengrey_ratio")))
        self.ui.pg_ggratio_box.setText(self.module.getParameterAsString("pg_greengrey_ratio"))
        QtCore.QObject.connect(self.ui.pg_ggratio_slide, QtCore.SIGNAL("valueChanged(int)"), self.ggratio_update)
        #CONNECT GREYGREEN SLIDER TO TEXTBOX
        
        self.ui.pg_aspectratio_spin.setValue(float(self.module.getParameterAsString("pg_linear_threshold")))
        
        #--> Green Space Config
        if self.module.getParameterAsString("pg_footpath_cross") == "1":
            self.ui.pg_fpathcross_check.setChecked(1)
        else:
            self.ui.pg_fpathcross_check.setChecked(0)
        
        if self.module.getParameterAsString("pg_footpath_circle") == "1":
            self.ui.pg_fpathcirc_check.setChecked(1)
            self.ui.pg_fpathcirc_rad_spin.setEnabled(1)
            self.ui.pg_fpathcirc_acc_spin.setEnabled(1)
        else:
            self.ui.pg_fpathcirc_check.setChecked(0)
            self.ui.pg_fpathcirc_rad_spin.setEnabled(0)
            self.ui.pg_fpathcirc_acc_spin.setEnabled(0)
        QtCore.QObject.connect(self.ui.pg_fpathcirc_check, QtCore.SIGNAL("clicked()"), self.pg_fpathcirc_enable)
            
        if self.module.getParameterAsString("pg_footpath_perimeter") == "1":
            self.ui.pg_fpathper_check.setChecked(1)
            self.ui.pg_fpathper_sb_spin.setEnabled(1)
            self.ui.pg_fpathper_acc_spin.setEnabled(1)
        else:
            self.ui.pg_fpathper_check.setChecked(0)
            self.ui.pg_fpathper_sb_spin.setEnabled(0)
            self.ui.pg_fpathper_acc_spin.setEnabled(0)
        QtCore.QObject.connect(self.ui.pg_fpathper_check, QtCore.SIGNAL("clicked()"), self.pg_fpathper_enable)
            
        self.ui.pg_fpathcirc_rad_spin.setValue(float(self.module.getParameterAsString("pg_circle_radius")))
        self.ui.pg_fpathcirc_acc_spin.setValue(float(self.module.getParameterAsString("pg_circle_accesses")))
        self.ui.pg_fpathper_sb_spin.setValue(float(self.module.getParameterAsString("pg_perimeter_setback")))
        self.ui.pg_fpathper_acc_spin.setValue(float(self.module.getParameterAsString("pg_perimeter_accesses")))
        self.ui.pg_fpath_width_box.setText(self.module.getParameterAsString("pg_footpath_avgW"))
        self.ui.pg_impdced_box.setText(self.module.getParameterAsString("pg_footpath_impdced"))
        
        if self.module.getParameterAsString("pg_footpath_varyW") == "1":
            self.ui.pg_fpath_width_check.setChecked(1)
        else:
            self.ui.pg_fpath_width_check.setChecked(0)
        
        if self.module.getParameterAsString("pg_footpath_multiply") == "1":
            self.ui.pg_fpathmultiply_check.setChecked(1)
        else:
            self.ui.pg_fpathmultiply_check.setChecked(0)
        
        #--> Reserves & Floodways
        if self.module.getParameterAsString("rfw_partialimp_check") == "1":
            self.ui.rfw_partimp_check.setChecked(1)
            self.ui.rfw_partimp_spin.setEnabled(1)
        else:
            self.ui.rfw_partimp_check.setChecked(0)
            self.ui.rfw_partimp_spin.setEnabled(0)
        QtCore.QObject.connect(self.ui.rfw_partimp_check, QtCore.SIGNAL("clicked()"), self.rfw_partimp_enable)
            
        if self.module.getParameterAsString("rfw_areausable_check") == "1":
            self.ui.rfw_restrict_check.setChecked(1)
            self.ui.rfw_restrict_spin.setEnabled(1)
        else:
            self.ui.rfw_restrict_check.setChecked(0)
            self.ui.rfw_restrict_spin.setEnabled(0)
        QtCore.QObject.connect(self.ui.rfw_restrict_check, QtCore.SIGNAL("clicked()"), self.rfw_restrict_enable)
        
        self.ui.rfw_partimp_spin.setValue(float(self.module.getParameterAsString("rfw_partialimp")))
        self.ui.rfw_restrict_spin.setValue(float(self.module.getParameterAsString("rfw_areausable")))
        
        
        ##########################
        #Others Tab
        ##########################
        #--> Unclassified Land
        if self.module.getParameterAsString("unc_merge") == "1":
            self.ui.unc_merge_check.setChecked(1)
            self.ui.unc_merge2imp_check.setEnabled(1)
            self.ui.unc_merge2pg_check.setEnabled(1)
            self.ui.unc_merge2trans_check.setEnabled(1)
            self.ui.unc_merge2imp_spin.setEnabled(1)
            self.ui.unc_merge2pg_spin.setEnabled(1)
            self.ui.unc_merge2trans_spin.setEnabled(1)
        else:
            self.ui.unc_merge_check.setChecked(0)
            self.ui.unc_merge2imp_check.setEnabled(0)
            self.ui.unc_merge2pg_check.setEnabled(0)
            self.ui.unc_merge2trans_check.setEnabled(0)
            self.ui.unc_merge2imp_spin.setEnabled(0)
            self.ui.unc_merge2pg_spin.setEnabled(0)
            self.ui.unc_merge2trans_spin.setEnabled(0)
        QtCore.QObject.connect(self.ui.unc_merge_check, QtCore.SIGNAL("clicked()"), self.unc_merge_enable)
        
        if self.module.getParameterAsString("unc_unc2square") == "1":
            self.ui.unc_merge2imp_check.setChecked(1)
        else:
            self.ui.unc_merge2imp_check.setChecked(0)
            self.ui.unc_merge2imp_spin.setEnabled(0)
        QtCore.QObject.connect(self.ui.unc_merge2imp_check, QtCore.SIGNAL("clicked()"), self.unc_merge2imp_enable)
        
        if self.module.getParameterAsString("unc_unc2park") == "1":
            self.ui.unc_merge2pg_check.setChecked(1)
        else:
            self.ui.unc_merge2pg_check.setChecked(0)
            self.ui.unc_merge2pg_spin.setEnabled(0)
        QtCore.QObject.connect(self.ui.unc_merge2pg_check, QtCore.SIGNAL("clicked()"), self.unc_merge2pg_enable)
        
        if self.module.getParameterAsString("unc_unc2road") == "1":
            self.ui.unc_merge2trans_check.setChecked(1)
        else:
            self.ui.unc_merge2trans_check.setChecked(0)
            self.ui.unc_merge2trans_spin.setEnabled(0)
        QtCore.QObject.connect(self.ui.unc_merge2trans_check, QtCore.SIGNAL("clicked()"), self.unc_merge2trans_enable)
        
        self.ui.unc_merge2imp_spin.setValue(float(self.module.getParameterAsString("unc_unc2square_weight")))
        self.ui.unc_merge2pg_spin.setValue(float(self.module.getParameterAsString("unc_unc2park_weight")))
        self.ui.unc_merge2trans_spin.setValue(float(self.module.getParameterAsString("unc_unc2road_weight")))
        
        if self.module.getParameterAsString("unc_landmark") == "1":
            self.ui.unc_landmark_check.setChecked(1)
            self.ui.unc_landmarkthresh_spin.setEnabled(1)
            self.ui.unc_landmarkimp_spin.setEnabled(1)
            self.ui.unc_landmarkwater_check.setEnabled(1)
        else:
            self.ui.unc_landmark_check.setChecked(0)
            self.ui.unc_landmarkthresh_spin.setEnabled(0)
            self.ui.unc_landmarkimp_spin.setEnabled(0)
            self.ui.unc_landmarkwater_check.setEnabled(0)
        QtCore.QObject.connect(self.ui.unc_landmark_check, QtCore.SIGNAL("clicked()"), self.unc_landmark_enable)
        
        self.ui.unc_landmarkthresh_spin.setValue(float(self.module.getParameterAsString("unc_landmark_threshold")))
        self.ui.unc_landmarkimp_spin.setValue(float(self.module.getParameterAsString("unc_landmark_avgimp")))
        
        if self.module.getParameterAsString("unc_landmark_otherwater") == "1":
            self.ui.unc_landmarkwater_check.setChecked(1)
        else:
            self.ui.unc_landmarkwater_check.setChecked(0)
        
        #--> Undeveloped
        if self.module.getParameterAsString("und_whattodo") == "N":
            self.ui.und_notouch_radio.setChecked(True)
            self.ui.und_allowdev_spin.setEnabled(0)
        if self.module.getParameterAsString("und_whattodo") == "Y":
            self.ui.und_allowdev_radio.setChecked(True)
            self.ui.und_allowdev_spin.setEnabled(1)
        QtCore.QObject.connect(self.ui.und_notouch_radio, QtCore.SIGNAL("clicked()"), self.und_allowdev_disable)
        QtCore.QObject.connect(self.ui.und_allowdev_radio, QtCore.SIGNAL("clicked()"), self.und_allowdev_enable)
            
        self.ui.und_allowdev_spin.setValue(float(self.module.getParameterAsString("und_allowspace")))
         
        if self.module.getParameterAsString("und_autodeterminetype") == "1":
            self.ui.und_typeget_check.setChecked(1)
        else:
            self.ui.und_typeget_check.setChecked(0)
        
        
        #CONNECT DETAILS WITH THE OK BUTTON SO THAT GUI UPDATES MODULE
        QtCore.QObject.connect(self.ui.buttonBox, QtCore.SIGNAL("accepted()"), self.save_values)
        QtCore.QObject.connect(self.ui.jobs_spacevary_customise, QtCore.SIGNAL("clicked()"), self.create_c1InputDialog)
        
    ###############################
    #   Update functions          #
    ###############################
    
    def maximperv_update(self, currentValue):
        self.ui.maximperv_boxval_2.setText(str(currentValue)+"%")
        self.module.setParameterValue("maximperv", str(currentValue))

    def maxsitecover_update(self, currentValue):
        self.ui.maxsitecover_boxval_2.setText(str(currentValue)+"%")
        self.module.setParameterValue("maximperv", str(currentValue))
    
    def employdatagetdirect(self):
        if self.ui.jobs_direct_radio.isChecked() == 1:
            self.ui.jobs_radius_box.setEnabled(0)
            self.ui.jobs_rate_spin.setEnabled(0)
            self.ui.jobs_ratefactor_spin.setEnabled(0)
        else:
            self.ui.jobs_radius_box.setEnabled(1)
            self.ui.jobs_rate_spin.setEnabled(1)
            self.ui.jobs_ratefactor_spin.setEnabled(1)
            
    def employdatagetpop(self):
        if self.ui.jobs_pop_radio.isChecked() == 1:
            self.ui.jobs_radius_box.setEnabled(1)
            self.ui.jobs_rate_spin.setEnabled(1)
            self.ui.jobs_ratefactor_spin.setEnabled(1)
        else:
            self.ui.jobs_radius_box.setEnabled(0)
            self.ui.jobs_rate_spin.setEnabled(0)
            self.ui.jobs_ratefactor_spin.setEnabled(0)
    
    def acc_typeparall_enable(self):
        if self.ui.acc_typeparall_check.isChecked() == 1:
            self.ui.acc_typeparall_med_box.setEnabled(1)
        else:
            self.ui.acc_typeparall_med_box.setEnabled(0)
    
    def acc_typecds_enable(self):
        if self.ui.acc_typecds_check.isChecked() == 1:
            self.ui.acc_typecds_dia_box.setEnabled(1)
        else:
            self.ui.acc_typecds_dia_box.setEnabled(0)
    
    def mun_on_off_enable(self):
        if self.ui.mun_on_off_check.isChecked() == 1:
            self.ui.edu_school_box.setEnabled(1)
            self.ui.edu_uni_box.setEnabled(1)
            self.ui.edu_lib_box.setEnabled(1)
            self.ui.civ_hospital_box.setEnabled(1)
            self.ui.civ_clinic_box.setEnabled(1)
            self.ui.civ_police_box.setEnabled(1)
            self.ui.civ_fire_box.setEnabled(1)
            self.ui.civ_jail_box.setEnabled(1)
            self.ui.civ_religion_box.setEnabled(1)
            self.ui.civ_leisure_box.setEnabled(1)
            self.ui.civ_museum_box.setEnabled(1)
            self.ui.civ_zoo_box.setEnabled(1)
            self.ui.civ_sports_box.setEnabled(1)
            self.ui.civ_race_box.setEnabled(1)
            self.ui.civ_dead_box.setEnabled(1)
            self.ui.sut_waste_box.setEnabled(1)
            self.ui.sut_gas_box.setEnabled(1)
            self.ui.sut_electricity_box.setEnabled(1)
            self.ui.sut_water_box.setEnabled(1)
            self.ui.sut_lgoffice_box.setEnabled(1)
        else:
            self.ui.edu_school_box.setEnabled(0)
            self.ui.edu_uni_box.setEnabled(0)
            self.ui.edu_lib_box.setEnabled(0)
            self.ui.civ_hospital_box.setEnabled(0)
            self.ui.civ_clinic_box.setEnabled(0)
            self.ui.civ_police_box.setEnabled(0)
            self.ui.civ_fire_box.setEnabled(0)
            self.ui.civ_jail_box.setEnabled(0)
            self.ui.civ_religion_box.setEnabled(0)
            self.ui.civ_leisure_box.setEnabled(0)
            self.ui.civ_museum_box.setEnabled(0)
            self.ui.civ_zoo_box.setEnabled(0)
            self.ui.civ_sports_box.setEnabled(0)
            self.ui.civ_race_box.setEnabled(0)
            self.ui.civ_dead_box.setEnabled(0)
            self.ui.sut_waste_box.setEnabled(0)
            self.ui.sut_gas_box.setEnabled(0)
            self.ui.sut_electricity_box.setEnabled(0)
            self.ui.sut_water_box.setEnabled(0)
            self.ui.sut_lgoffice_box.setEnabled(0)
    
    def trans_on_off_enable(self):
        if self.ui.trans_on_off_check.isChecked() == 1:
            self.ui.trans_airport_box.setEnabled(1)
            self.ui.trans_comseaport_box.setEnabled(1)
            self.ui.trans_indseaport_box.setEnabled(1)
            self.ui.trans_busdepot_box.setEnabled(1)
            self.ui.trans_rail_box.setEnabled(1)
        else:
            self.ui.trans_airport_box.setEnabled(0)
            self.ui.trans_comseaport_box.setEnabled(0)
            self.ui.trans_indseaport_box.setEnabled(0)
            self.ui.trans_busdepot_box.setEnabled(0)
            self.ui.trans_rail_box.setEnabled(0)
    
    def ggratio_update(self, currentValue):
        self.ui.pg_ggratio_box.setText(str(currentValue))
        self.module.setParameterValue("pg_greengrey_ratio", str(currentValue))  
    
    def pg_fpathcirc_enable(self):
        if self.ui.pg_fpathcirc_check.isChecked() == 1:
            self.ui.pg_fpathcirc_rad_spin.setEnabled(1)
            self.ui.pg_fpathcirc_acc_spin.setEnabled(1)
        else:
            self.ui.pg_fpathcirc_rad_spin.setEnabled(0)
            self.ui.pg_fpathcirc_acc_spin.setEnabled(0)
            
    def pg_fpathper_enable(self):
        if self.ui.pg_fpathper_check.isChecked() == 1:
            self.ui.pg_fpathper_sb_spin.setEnabled(1)
            self.ui.pg_fpathper_acc_spin.setEnabled(1)
        else:
            self.ui.pg_fpathper_sb_spin.setEnabled(0)
            self.ui.pg_fpathper_acc_spin.setEnabled(0)
    
    def rfw_partimp_enable(self):
        if self.ui.rfw_partimp_check.isChecked() == 1:
            self.ui.rfw_partimp_spin.setEnabled(1)
        else:
            self.ui.rfw_partimp_spin.setEnabled(0)
    
    def rfw_restrict_enable(self):
        if self.ui.rfw_restrict_check.isChecked() == 1:
            self.ui.rfw_restrict_spin.setEnabled(1)
        else:
            self.ui.rfw_restrict_spin.setEnabled(0)
    
    def unc_merge_enable(self):
        if self.ui.unc_merge_check.isChecked() == 1:
            self.ui.unc_merge2imp_check.setEnabled(1)
            self.ui.unc_merge2pg_check.setEnabled(1)
            self.ui.unc_merge2trans_check.setEnabled(1)
            self.unc_merge2imp_enable()
            self.unc_merge2pg_enable()
            self.unc_merge2trans_enable()
        else:
            self.ui.unc_merge2imp_check.setEnabled(0)
            self.ui.unc_merge2pg_check.setEnabled(0)
            self.ui.unc_merge2trans_check.setEnabled(0)
            self.ui.unc_merge2imp_spin.setEnabled(0)
            self.ui.unc_merge2pg_spin.setEnabled(0)
            self.ui.unc_merge2trans_spin.setEnabled(0)
        
    def unc_merge2imp_enable(self):
        if self.ui.unc_merge2imp_check.isChecked() == 1:
            self.ui.unc_merge2imp_spin.setEnabled(1)
        else:
            self.ui.unc_merge2imp_spin.setEnabled(0)
        
    def unc_merge2pg_enable(self):
        if self.ui.unc_merge2pg_check.isChecked() == 1:
            self.ui.unc_merge2pg_spin.setEnabled(1)
        else:
            self.ui.unc_merge2pg_spin.setEnabled(0)
        
    def unc_merge2trans_enable(self):
        if self.ui.unc_merge2trans_check.isChecked() == 1:
            self.ui.unc_merge2trans_spin.setEnabled(1)
        else:
            self.ui.unc_merge2trans_spin.setEnabled(0)
    
    def unc_landmark_enable(self):
        if self.ui.unc_landmark_check.isChecked() == 1:
            self.ui.unc_landmarkthresh_spin.setEnabled(1)
            self.ui.unc_landmarkimp_spin.setEnabled(1)
            self.ui.unc_landmarkwater_check.setEnabled(1)
        else:
            self.ui.unc_landmarkthresh_spin.setEnabled(0)
            self.ui.unc_landmarkimp_spin.setEnabled(0)
            self.ui.unc_landmarkwater_check.setEnabled(0) 
    
    def und_allowdev_disable(self):
        if self.ui.und_notouch_radio.isChecked() == 1:
            self.ui.und_allowdev_spin.setEnabled(0)
        else:
            self.ui.und_allowdev_spin.setEnabled(1)
    
    def und_allowdev_enable(self):
        if self.ui.und_allowdev_radio.isChecked() == 1:
            self.ui.und_allowdev_spin.setEnabled(1)
        else:
            self.ui.und_allowdev_spin.setEnabled(0) 
    
        
    #################################
    # OK Button/Cancel Button Click # 
    #################################     
      
    def save_values(self):
        
        ##########################
        #General Rules Tab
        ##########################
        maximperv = str(self.ui.maximperv_slider_2.value())
        self.module.setParameterValue("maximperv", maximperv)
        maxsitecover = str(self.ui.maxsitecover_slider_2.value())
        self.module.setParameterValue("maxsitecover", maxsitecover)
        
        if self.ui.mun_localmap_check.isChecked() == 1:
            locality_mun_trans = 1
        else:
            locality_mun_trans = 0
        self.module.setParameterValue("locality_mun_trans", str(locality_mun_trans))
#        if self.ui.district_age_check.isChecked() == 1:
#            district_age_infer = 1
#        else:
#            district_age_infer = 0
#        self.module.setParameterValue("district_age_infer", str(district_age_infer))
        
        #building block dynamics parameters
        
        ##########################
        #Residential Tab
        ##########################
        occup_avg = str(self.ui.occup_avg_box.text())
        self.module.setParameterValue("occup_avg", occup_avg)
        
        occup_max = str(self.ui.occup_max_box.text())
        self.module.setParameterValue("occup_max", occup_max)
        
        person_space = str(self.ui.person_space_box.text())
        self.module.setParameterValue("person_space", person_space)
        
        extra_comm_area = str(self.ui.extra_comm_area_box.text())
        self.module.setParameterValue("extra_comm_area", extra_comm_area)
        
        setback_f_min = str(self.ui.setback_f_min_box.text())
        self.module.setParameterValue("setback_f_min", setback_f_min)
        
        setback_f_max = str(self.ui.setback_f_max_box.text())
        self.module.setParameterValue("setback_f_max", setback_f_max)
        
        setback_s_min = str(self.ui.setback_s_min_box.text())
        self.module.setParameterValue("setback_s_min", setback_s_min)
        
        setback_s_max = str(self.ui.setback_s_max_box.text())
        self.module.setParameterValue("setback_s_max", setback_s_max)
        
        carports_max = str(self.ui.carports_max_box.text())
        self.module.setParameterValue("carports_max", carports_max)
        
        if self.ui.garage_incl_box.isChecked() == 1:
            garage_incl = 1
        else:
            garage_incl = 0
        self.module.setParameterValue("garage_incl", str(garage_incl))
        
        w_driveway_min = str(self.ui.w_driveway_min_box.text())
        self.module.setParameterValue("w_driveway_min", w_driveway_min)
        
        patio_area_max = str(self.ui.patio_area_max_box.text())
        self.module.setParameterValue("patio_area_max", patio_area_max)
        
        if self.ui.patio_covered_box.isChecked() == 1:
            patio_covered = 1
        else:
            patio_covered = 0
        self.module.setParameterValue("patio_covered", str(patio_covered))
                
        floor_num_max = str(self.ui.floor_num_max_box.text())
        self.module.setParameterValue("floor_num_max", floor_num_max)
        
        if self.ui.floor_autobuild_box.isChecked() == 1:
            floor_autobuild = 1
        else:
            floor_autobuild = 0
        self.module.setParameterValue("floor_autobuild", str(floor_autobuild))
        
        occup_flat_avg = str(self.ui.occup_flat_avg_box.text())
        self.module.setParameterValue("occup_flat_avg", occup_flat_avg)
        
        commspace_indoor = str(self.ui.commspace_indoor_box.text())
        self.module.setParameterValue("commspace_indoor", commspace_indoor)
        
        commspace_outdoor = str(self.ui.commspace_outdoor_box.text())
        self.module.setParameterValue("commspace_outdoor", commspace_outdoor)
        
        flat_area_max = str(self.ui.flat_area_max_box.text())
        self.module.setParameterValue("flat_area_max", flat_area_max)
        
        setback_HDR_avg = str(self.ui.setback_HDR_avg_box.text())
        self.module.setParameterValue("setback_HDR_avg", setback_HDR_avg)
        
        if self.ui.setback_HDR_auto_box.isChecked() == 1:
            setback_HDR_auto = 1
        else:
            setback_HDR_auto = 0
        self.module.setParameterValue("setback_HDR_auto", str(setback_HDR_auto))
        
        if self.ui.roof_connected_radiodirect.isChecked() == True:
            roof_connected = "Direct"
        if self.ui.roof_connected_radiodisc.isChecked() == True:
            roof_connected = "Disconnect"
        if self.ui.roof_connected_radiovary.isChecked() == True:
            roof_connected = "Vary"
        self.module.setParameterValue("roof_connected", roof_connected)
        
        imperv_prop_dced = str(self.ui.imperv_prop_dced_box.text())
        self.module.setParameterValue("imperv_prop_dced", imperv_prop_dced)
    
        ##########################
        #Non-Residential Tab
        ##########################
        #--> Employment Details
        if self.ui.jobs_direct_radio.isChecked() == True:
            employment_data = "D"
        if self.ui.jobs_pop_radio.isChecked() == True:
            employment_data = "P"
        self.module.setParameterValue("employment_data", employment_data)
        
        employment_rad = str(self.ui.jobs_radius_box.text())
        self.module.setParameterValue("employment_rad", employment_rad)
        
        employment_rate = str(self.ui.jobs_rate_spin.value())
        self.module.setParameterValue("employment_rate", employment_rate)
        
        employment_adjust = str(self.ui.jobs_ratefactor_spin.value())
        self.module.setParameterValue("employment_adjust", employment_adjust)
        
        if self.ui.jobs_spacevary_check.isChecked() == 1:
            com_spacevary_check = 1
        else:
            com_spacevary_check = 0
        self.module.setParameterValue("com_spacevary_check", str(com_spacevary_check))
        
        #--> Site Layout and Building Form
        com_fsetback_min = str(self.ui.com_minfsetback_box.text())
        self.module.setParameterValue("com_fsetback_min", com_fsetback_min)
        
        if self.ui.com_minfsetback_auto.isChecked() == 1:
            com_setback_auto = 1
        else:
            com_setback_auto = 0
        self.module.setParameterValue("com_setback_auto", str(com_setback_auto))
        
        com_floors_max = str(self.ui.com_maxfloors_spin.value())
        self.module.setParameterValue("com_floors_max", com_floors_max)
        
        #--> Car Parking and Service Area
        com_carpark_dmin = str(self.ui.carpark_depth_box.text())
        self.module.setParameterValue("com_carpark_dmin", com_carpark_dmin)
        
        com_carparkW = str(self.ui.carpark_dimW_box.text())
        self.module.setParameterValue("com_carparkW", com_carparkW)
        
        com_carparkD = str(self.ui.carpark_dimD_box.text())
        self.module.setParameterValue("com_carparkD", com_carparkD)
        
        com_carpark_avgimp = str(self.ui.carpark_imp_spin.value())
        self.module.setParameterValue("com_carpark_avgimp", com_carpark_avgimp)
        
        if self.ui.carpark_share_check.isChecked() == 1:
            com_carpark_share = 1
        else:
            com_carpark_share = 0
        self.module.setParameterValue("com_carpark_share", str(com_carpark_share))
        
        com_service_dmin = str(self.ui.service_depth_box.text())
        self.module.setParameterValue("com_service_dmin", com_service_dmin)
        
        #--> Service/Access Road
        if self.ui.acc_typeperp_check.isChecked() == 1:
            access_perp = 1
        else:
            access_perp = 0
        self.module.setParameterValue("access_perp", str(access_perp))
        
        if self.ui.acc_typeparall_check.isChecked() == 1:
            access_parall = 1
        else:
            access_parall = 0
        self.module.setParameterValue("access_parall", str(access_parall))
        
        if self.ui.acc_typecds_check.isChecked() == 1:
            access_cds = 1
        else:
            access_cds = 0
        self.module.setParameterValue("access_cds", str(access_cds))
        
        if self.ui.acc_includepeds_check.isChecked() == 1:
            access_ped_include = 1
        else:
            access_ped_include = 0
        self.module.setParameterValue("access_ped_include", str(access_ped_include))
        
        access_parall_medwidth = str(self.ui.acc_typeparall_med_box.text())
        self.module.setParameterValue("access_parall_medwidth", access_parall_medwidth)
        
        access_cds_circlerad = str(self.ui.acc_typecds_dia_box.text())
        self.module.setParameterValue("access_cds_circlerad", access_cds_circlerad)
        
        #--> Landscaping & Drainage
        lscape_hsbal = str(self.ui.lscape_hsbalance_slide.value())
        self.module.setParameterValue("lscape_hsbal", lscape_hsbal)
        
        lscape_avgimp_dced = str(self.ui.com_impdced_box.text())
        self.module.setParameterValue("lscape_avgimp_dced", lscape_avgimp_dced)
        
        #--> Municipal Facilities
        if self.ui.mun_on_off_check.isChecked() == 1:
            mun_explicit = 1
        else:
            mun_explicit = 0
        self.module.setParameterValue("mun_explicit", str(mun_explicit))
        
            #EDUCATION
        if self.ui.edu_school_box.isChecked() == 1:
            edu_school = 1
        else:
            edu_school = 0
        self.module.setParameterValue("edu_school", str(edu_school))
        
        if self.ui.edu_uni_box.isChecked() == 1:
            edu_uni = 1
        else:
            edu_uni = 0
        self.module.setParameterValue("edu_uni", str(edu_uni))
        
        if self.ui.edu_lib_box.isChecked() == 1:
            edu_lib = 1
        else:
            edu_lib = 0
        self.module.setParameterValue("edu_lib", str(edu_lib))
        #>>>>>ADDITIONAL PARAMETERS FOR CUSTOMISATION
        
            #CIVIC
        if self.ui.civ_hospital_box.isChecked() == 1:
            civ_hospital = 1
        else:
            civ_hospital = 0
        self.module.setParameterValue("civ_hospital", str(civ_hospital))
        
        if self.ui.civ_clinic_box.isChecked() == 1:
            civ_clinic = 1
        else:
            civ_clinic = 0
        self.module.setParameterValue("civ_clinic", str(civ_clinic))
        
        if self.ui.civ_police_box.isChecked() == 1:
            civ_police = 1
        else:
            civ_police = 0
        self.module.setParameterValue("civ_police", str(civ_police))
        
        if self.ui.civ_fire_box.isChecked() == 1:
            civ_fire = 1
        else:
            civ_fire = 0
        self.module.setParameterValue("civ_fire", str(civ_fire))
        
        if self.ui.civ_jail_box.isChecked() == 1:
            civ_jail = 1
        else:
            civ_jail = 0
        self.module.setParameterValue("civ_jail", str(civ_jail))
        
        if self.ui.civ_religion_box.isChecked() == 1:
            civ_worship = 1
        else:
            civ_worship = 0
        self.module.setParameterValue("civ_worship", str(civ_worship))
        
        if self.ui.civ_leisure_box.isChecked() == 1:
            civ_leisure = 1
        else:
            civ_leisure = 0
        self.module.setParameterValue("civ_leisure", str(civ_leisure))
        
        if self.ui.civ_museum_box.isChecked() == 1:
            civ_museum = 1
        else:
            civ_museum = 0
        self.module.setParameterValue("civ_museum", str(civ_museum))
        
        if self.ui.civ_zoo_box.isChecked() == 1:
            civ_zoo = 1
        else:
            civ_zoo = 0
        self.module.setParameterValue("civ_zoo", str(civ_zoo))
        
        if self.ui.civ_sports_box.isChecked() == 1:
            civ_stadium = 1
        else:
            civ_stadium = 0
        self.module.setParameterValue("civ_stadium", str(civ_stadium))
        
        if self.ui.civ_race_box.isChecked() == 1:
            civ_racing = 1
        else:
            civ_racing = 0
        self.module.setParameterValue("civ_racing", str(civ_racing))
        
        if self.ui.civ_dead_box.isChecked() == 1:
            civ_cemetery = 1
        else:
            civ_cemetery = 0
        self.module.setParameterValue("civ_cemetery", str(civ_cemetery))
        #>>>>>ADDITIONAL PARAMETERS FOR CUSTOMISATION
        
            #SERVICES & UTILITY
        if self.ui.sut_waste_box.isChecked() == 1:
            sut_waste = 1
        else:
            sut_waste = 0
        self.module.setParameterValue("sut_waste", str(sut_waste))
        
        if self.ui.sut_gas_box.isChecked() == 1:
            sut_gas = 1
        else:
            sut_gas = 0
        self.module.setParameterValue("sut_gas", str(sut_gas))
        
        if self.ui.sut_electricity_box.isChecked() == 1:
            sut_electricity = 1
        else:
            sut_electricity = 0
        self.module.setParameterValue("sut_electricity", str(sut_electricity))
        
        if self.ui.sut_water_box.isChecked() == 1:
            sut_water = 1
        else:
            sut_water = 0
        self.module.setParameterValue("sut_water", str(sut_water))
        
        if self.ui.sut_lgoffice_box.isChecked() == 1:
            sut_lgoffice = 1
        else:
            sut_lgoffice = 0
        self.module.setParameterValue("sut_lgoffice", str(sut_lgoffice))
        #>>>>>ADDITIONAL PARAMETERS FOR CUSTOMISATION
        
        ##########################
        #Transport Tab
        ##########################
        #--> Frontage & Pedestrian Information
        w_resfootpath_min = str(self.ui.w_resfootpath_min_box.text())
        self.module.setParameterValue("w_resfootpath_min", w_resfootpath_min)
        
        w_resfootpath_max = str(self.ui.w_resfootpath_max_box.text())
        self.module.setParameterValue("w_resfootpath_max", w_resfootpath_max)
        
        w_resnaturestrip_min = str(self.ui.w_resnaturestrip_min_box.text())
        self.module.setParameterValue("w_resnaturestrip_min", w_resnaturestrip_min)
        
        w_resnaturestrip_max = str(self.ui.w_resnaturestrip_max_box.text())
        self.module.setParameterValue("w_resnaturestrip_max", w_resnaturestrip_max)
        
        if self.ui.w_resfootpath_med_check.isChecked() == 1:
            w_resfootpath_med = 1
        else:
            w_resfootpath_med = 0
        self.module.setParameterValue("w_resfootpath_med", str(w_resfootpath_med))
        
        if self.ui.w_resnaturestrip_med_check.isChecked() == 1:
            w_resnaturestrip_med = 1
        else:
            w_resnaturestrip_med = 0
        self.module.setParameterValue("w_resnaturestrip_med", str(w_resnaturestrip_med))
        
        w_comfootpath_min = str(self.ui.w_comfootpath_min_box.text())
        self.module.setParameterValue("w_comfootpath_min", w_comfootpath_min)
        
        w_comfootpath_max = str(self.ui.w_comfootpath_max_box.text())
        self.module.setParameterValue("w_comfootpath_max", w_comfootpath_max)
        
        w_comnaturestrip_min = str(self.ui.w_resnaturestrip_min_box.text())
        self.module.setParameterValue("w_comnaturestrip_min", w_comnaturestrip_min)
        
        w_comnaturestrip_max = str(self.ui.w_comnaturestrip_max_box.text())
        self.module.setParameterValue("w_comnaturestrip_max", w_comnaturestrip_max)
        
        if self.ui.w_comfootpath_med_check.isChecked() == 1:
            w_comfootpath_med = 1
        else:
            w_comfootpath_med = 0
        self.module.setParameterValue("w_comfootpath_med", str(w_comfootpath_med))
        
        if self.ui.w_comnaturestrip_med_check.isChecked() == 1:
            w_comnaturestrip_med = 1
        else:
            w_comnaturestrip_med = 0
        self.module.setParameterValue("w_comnaturestrip_med", str(w_comnaturestrip_med))
        
        #--> Local Access/Service/Collector Roads
        w_collectlane_min = str(self.ui.w_collectlane_min_box.text())
        self.module.setParameterValue("w_collectlane_min", w_collectlane_min)
        
        w_collectlane_max = str(self.ui.w_collectlane_max_box.text())
        self.module.setParameterValue("w_collectlane_max", w_collectlane_max)
        
        collect_crossfall = str(self.ui.collect_crossfall_box.text())
        self.module.setParameterValue("collect_crossfall", collect_crossfall)
        
        if self.ui.w_collectlane_med_check.isChecked() == 1:
            w_collectlane_med = 1
        else:
            w_collectlane_med = 0
        self.module.setParameterValue("w_collectlane_med", str(w_collectlane_med))
        
        #--> Arterials/District Distributors/Dual Carriageways
        w_artlane_min = str(self.ui.w_arterial_min_box.text())
        self.module.setParameterValue("w_artlane_min", w_artlane_min)
        
        w_artlane_max = str(self.ui.w_arterial_max_box.text())
        self.module.setParameterValue("w_artlane_max", w_artlane_max)
        
        w_artmedian = str(self.ui.w_arterialmed_box.text())
        self.module.setParameterValue("w_artmedian", w_artmedian)
        
        art_crossfall = str(self.ui.arterial_crossfall_box.text())
        self.module.setParameterValue("art_crossfall", art_crossfall)
        
        if self.ui.w_arterial_med_check.isChecked() == 1:
            w_artlane_med = 1
        else:
            w_artlane_med = 0
        self.module.setParameterValue("w_artlane_med", str(w_artlane_med))
        
        if self.ui.w_arterialmed_nodev_check.isChecked() == 1:
            artmedian_reserved = 1
        else:
            artmedian_reserved = 0
        self.module.setParameterValue("artmedian_reserved", str(artmedian_reserved))
        
        #--> Highways/Freeways/Motorways
        w_hwylane_avg = str(self.ui.w_highwaylane_box.text())
        self.module.setParameterValue("w_hwylane_avg", w_hwylane_avg)
        
        w_hwymedian = str(self.ui.w_highwaymed_box.text())
        self.module.setParameterValue("w_hwymedian", w_hwymedian)
        
        hwy_crossfall = str(self.ui.highway_crossfall_box.text())
        self.module.setParameterValue("hwy_crossfall", hwy_crossfall)
        
        if self.ui.highway_buffer_check.isChecked() == 1:
            hwy_buffered = 1
        else:
            hwy_buffered = 0
        self.module.setParameterValue("hwy_buffered", str(hwy_buffered))
        
        if self.ui.w_highwaymed_nodev_check.isChecked() == 1:
            hwymedian_reserved = 1
        else:
            hwymedian_reserved = 0
        self.module.setParameterValue("hwymedian_reserved", str(hwymedian_reserved))
        
        #--> Other Transportation
        if self.ui.trans_on_off_check.isChecked() == 1:
            trans_explicit = 1
        else:
            trans_explicit = 0
        self.module.setParameterValue("trans_explicit", str(trans_explicit))
        
        if self.ui.trans_airport_box.isChecked() == 1:
            trans_airport = 1
        else:
            trans_airport = 0
        self.module.setParameterValue("trans_airport", str(trans_airport))
        
        if self.ui.trans_comseaport_box.isChecked() == 1:
            trans_comseaport = 1
        else:
            trans_comseaport = 0
        self.module.setParameterValue("trans_comseaport", str(trans_comseaport))
        
        if self.ui.trans_indseaport_box.isChecked() == 1:
            trans_indseaport = 1
        else:
            trans_indseaport = 0
        self.module.setParameterValue("trans_indseaport", str(trans_indseaport))
        
        if self.ui.trans_busdepot_box.isChecked() == 1:
            trans_busdepot = 1
        else:
            trans_busdepot = 0
        self.module.setParameterValue("trans_busdepot", str(trans_busdepot))
        
        if self.ui.trans_rail_box.isChecked() == 1:
            trans_railterminal = 1
        else:
            trans_railterminal = 0
        self.module.setParameterValue("trans_railterminal", str(trans_railterminal))
        
        
        ##########################
        #Open Space Tab
        ##########################
        #--> General Information
        pg_clustering_degree = str(self.ui.pg_clustering_slide.value())
        self.module.setParameterValue("pg_clustering_degree", pg_clustering_degree)
        
        pg_greengrey_ratio = str(self.ui.pg_ggratio_slide.value())
        self.module.setParameterValue("pg_greengrey_ratio", pg_greengrey_ratio)
        
        pg_linear_threshold = str(self.ui.pg_aspectratio_spin.value())
        self.module.setParameterValue("pg_linear_threshold", pg_linear_threshold)
        
        #--> Green Space Config
        if self.ui.pg_fpathcross_check.isChecked() == 1:
            pg_footpath_cross = 1
        else:
            pg_footpath_cross = 0
        self.module.setParameterValue("pg_footpath_cross", str(pg_footpath_cross))
        
        if self.ui.pg_fpathcirc_check.isChecked() == 1:
            pg_footpath_circle = 1
        else:
            pg_footpath_circle = 0
        self.module.setParameterValue("pg_footpath_circle", str(pg_footpath_circle))
        
        if self.ui.pg_fpathper_check.isChecked() == 1:
            pg_footpath_perimeter = 1
        else:
            pg_footpath_perimeter = 0
        self.module.setParameterValue("pg_footpath_perimeter", str(pg_footpath_perimeter))
        
        pg_circle_radius = str(self.ui.pg_fpathcirc_rad_spin.value())
        self.module.setParameterValue("pg_circle_radius", pg_circle_radius)
        
        pg_circle_accesses = str(self.ui.pg_fpathcirc_acc_spin.value())
        self.module.setParameterValue("pg_circle_accesses", pg_circle_accesses)
        
        pg_perimeter_setback = str(self.ui.pg_fpathper_sb_spin.value())
        self.module.setParameterValue("pg_perimeter_setback", pg_perimeter_setback)
        
        pg_perimeter_accesses = str(self.ui.pg_fpathper_acc_spin.value())
        self.module.setParameterValue("pg_perimeter_accesses", pg_perimeter_accesses)
        
        pg_footpath_avgW = str(self.ui.pg_fpath_width_box.text())
        self.module.setParameterValue("pg_footpath_avgW", pg_footpath_avgW)
        
        pg_footpath_impdced = str(self.ui.pg_impdced_box.text())
        self.module.setParameterValue("pg_footpath_impdced", pg_footpath_impdced)
        
        if self.ui.pg_fpath_width_check.isChecked() == 1:
            pg_footpath_varyW = 1
        else:
            pg_footpath_varyW = 0
        self.module.setParameterValue("pg_footpath_varyW", str(pg_footpath_varyW))
        
        if self.ui.pg_fpathmultiply_check.isChecked() == 1:
            pg_footpath_multiply = 1
        else:
            pg_footpath_multiply = 0
        self.module.setParameterValue("pg_footpath_multiply", str(pg_footpath_multiply))
        
        #--> Reserves & Floodways
        if self.ui.rfw_partimp_check.isChecked() == 1:
            rfw_partialimp_check = 1
        else:
            rfw_partialimp_check = 0
        self.module.setParameterValue("rfw_partialimp_check", str(rfw_partialimp_check))
        
        if self.ui.rfw_restrict_check.isChecked() == 1:
            rfw_areausable_check = 1
        else:
            rfw_areausable_check = 0
        self.module.setParameterValue("rfw_areausable_check", str(rfw_areausable_check))
        
        rfw_partialimp = str(self.ui.rfw_partimp_spin.value())
        self.module.setParameterValue("rfw_partialimp", rfw_partialimp)
        
        rfw_areausable = str(self.ui.rfw_restrict_spin.value())
        self.module.setParameterValue("rfw_areausable", rfw_areausable)
        
        ##########################
        #Others Tab
        ##########################
        #--> Unclassified
        if self.ui.unc_merge_check.isChecked() == 1:
            unc_merge = 1
        else:
            unc_merge = 0
        self.module.setParameterValue("unc_merge", str(unc_merge))
        
        if self.ui.unc_merge2imp_check.isChecked() == 1:
            unc_unc2square = 1
        else:
            unc_unc2square = 0
        self.module.setParameterValue("unc_unc2square", str(unc_unc2square))
        
        if self.ui.unc_merge2pg_check.isChecked() == 1:
            unc_unc2park = 1
        else:
            unc_unc2park = 0
        self.module.setParameterValue("unc_unc2park", str(unc_unc2park))
        
        if self.ui.unc_merge2trans_check.isChecked() == 1:
            unc_unc2road = 1
        else:
            unc_unc2road = 0
        self.module.setParameterValue("unc_unc2road", str(unc_unc2road))
        
        unc_unc2square_weight = str(self.ui.unc_merge2imp_spin.value())
        self.module.setParameterValue("unc_unc2square_weight", unc_unc2square_weight)
        
        unc_unc2park_weight = str(self.ui.unc_merge2pg_spin.value())
        self.module.setParameterValue("unc_unc2park_weight", unc_unc2park_weight)
        
        unc_unc2road_weight = str(self.ui.unc_merge2trans_spin.value())
        self.module.setParameterValue("unc_unc2road_weight", unc_unc2road_weight)
        
        if self.ui.unc_landmark_check.isChecked() == 1:
            unc_landmark = 1
        else:
            unc_landmark = 0
        self.module.setParameterValue("unc_landmark", str(unc_landmark))
        
        unc_landmark_threshold = str(self.ui.unc_landmarkthresh_spin.value())
        self.module.setParameterValue("unc_landmark_threshold", unc_landmark_threshold)
        
        unc_landmark_avgimp = str(self.ui.unc_landmarkimp_spin.value())
        self.module.setParameterValue("unc_landmark_avgimp", unc_landmark_avgimp)
        
        if self.ui.unc_landmarkwater_check.isChecked() == 1:
            unc_landmark_otherwater = 1
        else:
            unc_landmark_otherwater = 0
        self.module.setParameterValue("unc_landmark_otherwater", str(unc_landmark_otherwater))
        
        #--> Undeveloped
        if self.ui.und_notouch_radio.isChecked() == True:
            und_whattodo = "N"
        if self.ui.und_allowdev_radio.isChecked() == True:
            und_whattodo = "Y"
        self.module.setParameterValue("und_whattodo", und_whattodo)
        
        und_allowspace = str(self.ui.und_allowdev_spin.value())
        self.module.setParameterValue("und_allowspace", und_allowspace)
        
        if self.ui.und_typeget_check.isChecked() == 1:
            und_autodeterminetype = 1
        else:
            und_autodeterminetype = 0
        self.module.setParameterValue("und_autodeterminetype", str(und_autodeterminetype))
        
        #----------------END OF SAVE VALUES------------------------------------#
    
    def create_c1InputDialog(self):
        self.save_values()
        self.close()
        print "done"    
        form = activateurbplanbbc1GUI(self, QApplication.activeWindow())
        form.show()
#        c1Dialog.exec_()
        print "ok"
        return True
    
class activateurbplanbbc1GUI(QtGui.QDialog):
    def __init__(self, m, parent=None):  
        print "ah ok"
        self.module = Module
        self.module = m
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_c1_subDialog()
        self.ui.setupUi(self)
        
        print "hello world"
#       self.module = Module
#       self.module = m
        
        #------------------------#--------------------#------------------------#
        #                            SUB DIALOG C1                             #
        #------------------------#--------------------#------------------------#
        
        
        self.ui.lineEdit.setText(self.module.getParameterAsString("min_trad_cc"))
        #------------------------#END OF SUB DIALOG C1#------------------------#        
        QtCore.QObject.connect(self.ui.c1buttonBox, QtCore.SIGNAL("accepted()"), self.c1save_values)

    def c1save_values(self):
        min_trad_cc = str(self.ui.lineEdit.text())
        self.module.setParameterValue("min_trad_cc", min_trad_cc)
        pass
    
        