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

from pyvibe import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from urbwatersettings_guic import *


class urbwatersettings(Module):
    """Description
    
    Log of Updates made at each version:
    
    v0.8 first:
        - 
        Future work:
            - 
            - 
	@author Peter M Bach
	"""

    def __init__(self):
        Module.__init__(self)
        self.urbanwatersetup_out = VectorDataIn
        self.addParameter(self, "design_settings", VIBe2.VECTORDATA_OUT)
        
        ### Input time series data
        self.rain_ts = 6        #time step of rainfall data (default: 6-min = 360 secs)
        self.evap_ts = 1440     #time step of evap data (default: daily)
        self.solar_ts = 1440
        self.rain_fname = "none"
        self.evap_fname = "none"
        self.solar_fname = "none"
        self.addParameter(self, "rain_ts", VIBe2.DOUBLE)
        self.addParameter(self, "evap_ts", VIBe2.DOUBLE)
        self.addParameter(self, "solar_ts", VIBe2.DOUBLE)
        self.addParameter(self, "rain_fname", VIBe2.STRING)
        self.addParameter(self, "evap_fname", VIBe2.STRING)
        self.addParameter(self, "solar_fname", VIBe2.STRING)
        
        ### Climate Scaling Factors
        self.rain_scale = False
        self.evap_scale = False
        self.solar_scale = False
        self.addParameter(self, "rain_scale", VIBe2.BOOL)
        self.addParameter(self, "evap_scale", VIBe2.BOOL)
        self.addParameter(self, "solar_scale", VIBe2.BOOL)
        self.rsf_01 = 1.00
        self.rsf_02 = 1.00
        self.rsf_03 = 1.00
        self.rsf_04 = 1.00
        self.rsf_05 = 1.00
        self.rsf_06 = 1.00
        self.rsf_07 = 1.00
        self.rsf_08 = 1.00
        self.rsf_09 = 1.00
        self.rsf_10 = 1.00
        self.rsf_11 = 1.00
        self.rsf_12 = 1.00
        self.addParameter(self, "rsf_01", VIBe2.DOUBLE)
        self.addParameter(self, "rsf_02", VIBe2.DOUBLE)
        self.addParameter(self, "rsf_03", VIBe2.DOUBLE)
        self.addParameter(self, "rsf_04", VIBe2.DOUBLE)
        self.addParameter(self, "rsf_05", VIBe2.DOUBLE)
        self.addParameter(self, "rsf_06", VIBe2.DOUBLE)
        self.addParameter(self, "rsf_07", VIBe2.DOUBLE)
        self.addParameter(self, "rsf_08", VIBe2.DOUBLE)
        self.addParameter(self, "rsf_09", VIBe2.DOUBLE)
        self.addParameter(self, "rsf_10", VIBe2.DOUBLE)
        self.addParameter(self, "rsf_11", VIBe2.DOUBLE)
        self.addParameter(self, "rsf_12", VIBe2.DOUBLE)
        self.esf_01 = 1.00
        self.esf_02 = 1.00
        self.esf_03 = 1.00
        self.esf_04 = 1.00
        self.esf_05 = 1.00
        self.esf_06 = 1.00
        self.esf_07 = 1.00
        self.esf_08 = 1.00
        self.esf_09 = 1.00
        self.esf_10 = 1.00
        self.esf_11 = 1.00
        self.esf_12 = 1.00
        self.addParameter(self, "esf_01", VIBe2.DOUBLE)
        self.addParameter(self, "esf_02", VIBe2.DOUBLE)
        self.addParameter(self, "esf_03", VIBe2.DOUBLE)
        self.addParameter(self, "esf_04", VIBe2.DOUBLE)
        self.addParameter(self, "esf_05", VIBe2.DOUBLE)
        self.addParameter(self, "esf_06", VIBe2.DOUBLE)
        self.addParameter(self, "esf_07", VIBe2.DOUBLE)
        self.addParameter(self, "esf_08", VIBe2.DOUBLE)
        self.addParameter(self, "esf_09", VIBe2.DOUBLE)
        self.addParameter(self, "esf_10", VIBe2.DOUBLE)
        self.addParameter(self, "esf_11", VIBe2.DOUBLE)
        self.addParameter(self, "esf_12", VIBe2.DOUBLE)
        self.ssf_01 = 1.00
        self.ssf_02 = 1.00
        self.ssf_03 = 1.00
        self.ssf_04 = 1.00
        self.ssf_05 = 1.00
        self.ssf_06 = 1.00
        self.ssf_07 = 1.00
        self.ssf_08 = 1.00
        self.ssf_09 = 1.00
        self.ssf_10 = 1.00
        self.ssf_11 = 1.00
        self.ssf_12 = 1.00
        self.addParameter(self, "ssf_01", VIBe2.DOUBLE)
        self.addParameter(self, "ssf_02", VIBe2.DOUBLE)
        self.addParameter(self, "ssf_03", VIBe2.DOUBLE)
        self.addParameter(self, "ssf_04", VIBe2.DOUBLE)
        self.addParameter(self, "ssf_05", VIBe2.DOUBLE)
        self.addParameter(self, "ssf_06", VIBe2.DOUBLE)
        self.addParameter(self, "ssf_07", VIBe2.DOUBLE)
        self.addParameter(self, "ssf_08", VIBe2.DOUBLE)
        self.addParameter(self, "ssf_09", VIBe2.DOUBLE)
        self.addParameter(self, "ssf_10", VIBe2.DOUBLE)
        self.addParameter(self, "ssf_11", VIBe2.DOUBLE)
        self.addParameter(self, "ssf_12", VIBe2.DOUBLE)
        
        ### Input, hydrology parameters
        self.Simpmax = 1        #MOPUS RnR parameter - max impervious surface store
        self.Spervmax = 100     #MOPUS RnR parameter - max pervious soil store
        self.muskK = 30         #Muskingum-Cunge routing parameter
        self.muskTheta = 0.25   #Muskingum-Cunge routing parameter
        self.route_method = 1   #Routing method: 1=Muskingum, 2=K-wave
            #KINEMATIC WAVE PARAMETERS
        self.addParameter(self, "Simpmax", VIBe2.DOUBLE)
        self.addParameter(self, "Spervmax", VIBe2.DOUBLE)
        self.addParameter(self, "muskK", VIBe2.DOUBLE)
        self.addParameter(self, "muskTheta", VIBe2.DOUBLE)
        self.addParameter(self, "route_method", VIBe2.DOUBLE)
        
        ### Input, pollution & treatment parameters
        #coming soon...
        
        
        
        ### Input, demand patterns parameters
        self.freq_kitchen = 2                   #Household Demands START
        self.freq_shower = 2
        self.freq_toilet = 2
        self.freq_laundry = 2
        self.dur_kitchen = 10
        self.dur_shower = 5
        self.demandvary_kitchen = 0.00
        self.demandvary_shower = 0.00
        self.demandvary_toilet = 0.00
        self.demandvary_laundry = 0.00
        self.ffp_kitchen = "PO"
        self.ffp_shower = "PO"
        self.ffp_toilet = "PO"
        self.ffp_laundry = "PO"
        self.t2t_household = 0.5
        self.ffp_garden = "PO"
        self.addParameter(self, "freq_kitchen", VIBe2.DOUBLE)
        self.addParameter(self, "freq_shower", VIBe2.DOUBLE)
        self.addParameter(self, "freq_toilet", VIBe2.DOUBLE)
        self.addParameter(self, "freq_laundry", VIBe2.DOUBLE)
        self.addParameter(self, "dur_kitchen", VIBe2.DOUBLE)
        self.addParameter(self, "dur_shower", VIBe2.DOUBLE)
        self.addParameter(self, "demandvary_kitchen", VIBe2.DOUBLE)
        self.addParameter(self, "demandvary_shower", VIBe2.DOUBLE)
        self.addParameter(self, "demandvary_toilet", VIBe2.DOUBLE)
        self.addParameter(self, "demandvary_laundry", VIBe2.DOUBLE)
        self.addParameter(self, "ffp_kitchen", VIBe2.STRING)
        self.addParameter(self, "ffp_shower", VIBe2.STRING)
        self.addParameter(self, "ffp_toilet", VIBe2.STRING)
        self.addParameter(self, "ffp_laundry", VIBe2.STRING)
        self.addParameter(self, "t2t_household", VIBe2.DOUBLE)
        self.addParameter(self, "ffp_garden", VIBe2.STRING)
        self.other_demand = 10                  #Other Demand START
        self.t2t_public = 0.5
        self.ffp_public = "PO"
        self.irrigate_commun = False
        self.irrigate_pg = False
        self.irrigate_resflood = False
        self.addParameter(self, "other_demand", VIBe2.DOUBLE)
        self.addParameter(self, "t2t_public", VIBe2.DOUBLE)
        self.addParameter(self, "ffp_public", VIBe2.STRING)
        self.addParameter(self, "irrigate_commun", VIBe2.BOOL)
        self.addParameter(self, "irrigate_pg", VIBe2.BOOL)
        self.addParameter(self, "irrigate_resflood", VIBe2.BOOL)
        self.start_efficiency = 0
        self.initial_irrigate = "PET"           #obtain initial irrigation demand from "TSS","PET","NON"
        self.irrigatesim_dur = 1                #1 year
        self.irrigatepet_perc = 125             #% of PET
        self.addParameter(self, "start_efficiency", VIBe2.DOUBLE)
        self.addParameter(self, "initial_irrigate", VIBe2.STRING)
        self.addParameter(self, "irrigatesim_dur", VIBe2.DOUBLE)
        self.addParameter(self, "irrigatepet_perc", VIBe2.DOUBLE)
        self.dagg_method = "LD"                 #disaggregation method: LD (linear downscaling), DP (diurnal pattern)
        self.daggld_subprop = False             #simple linear disaggregation parameters
        self.daggld_dayprop = 80
        self.daggdp_predef = False
        self.daggdp_method = "GJ"               #predefined method
        self.daggdp_custom = False
        self.daggdp_morning = 0.4               #sub-daily factors
        self.daggdp_noon = 0.2
        self.daggdp_evening = 0.3
        self.daggdp_night = 0.1
        self.addParameter(self, "dagg_method", VIBe2.STRING)
        self.addParameter(self, "daggld_subprop", VIBe2.BOOL)
        self.addParameter(self, "daggld_dayprop", VIBe2.DOUBLE)
        self.addParameter(self, "daggdp_predef", VIBe2.BOOL)
        self.addParameter(self, "daggdp_method", VIBe2.STRING)
        self.addParameter(self, "daggdp_custom", VIBe2.BOOL)
        self.addParameter(self, "daggdp_morning", VIBe2.DOUBLE)
        self.addParameter(self, "daggdp_noon", VIBe2.DOUBLE)
        self.addParameter(self, "daggdp_evening", VIBe2.DOUBLE)
        self.addParameter(self, "daggdp_night", VIBe2.DOUBLE)
        
        
        #Input, supply & wastewater parameters
        #coming soon...
        
        #Input, energy parameters
        #coming soon...
        
        #Input, economic parameters
        #coming soon...
        
    
    def run(self):
        urbanwatersetup_out = self.urbanwatersetup_out.getItem()
        
        #Transfer scaling factors as a string and convert it to an array in next module
        rsf_matrix = str(self.rsf_01)+"*|*"+str(self.rsf_02)+"*|*"+str(self.rsf_03)+"*|*"+ \
            str(self.rsf_04)+"*|*"+str(self.rsf_05)+"*|*"+str(self.rsf_06)+"*|*"+ \
            str(self.rsf_07)+"*|*"+str(self.rsf_08)+"*|*"+str(self.rsf_09)+"*|*"+\
            str(self.rsf_10)+"*|*"+str(self.rsf_11)+"*|*"+str(self.rsf_12)
        CD3simulation_config.setAttribute("rsf_matrix", rsf_matrix)
        
        esf_matrix = str(self.esf_01)+"*|*"+str(self.esf_02)+"*|*"+str(self.esf_03)+"*|*"+ \
            str(self.esf_04)+"*|*"+str(self.esf_05)+"*|*"+str(self.esf_06)+"*|*"+ \
            str(self.esf_07)+"*|*"+str(self.esf_08)+"*|*"+str(self.esf_09)+"*|*"+\
            str(self.esf_10)+"*|*"+str(self.esf_11)+"*|*"+str(self.esf_12)
        CD3simulation_config.setAttribute("esf_matrix", esf_matrix)
        
        ssf_matrix = str(self.ssf_01)+"*|*"+str(self.ssf_02)+"*|*"+str(self.ssf_03)+"*|*"+ \
            str(self.ssf_04)+"*|*"+str(self.ssf_05)+"*|*"+str(self.ssf_06)+"*|*"+ \
            str(self.ssf_07)+"*|*"+str(self.ssf_08)+"*|*"+str(self.ssf_09)+"*|*"+\
            str(self.ssf_10)+"*|*"+str(self.ssf_11)+"*|*"+str(self.ssf_12)
        CD3simulation_config.setAttribute("ssf_matrix", ssf_matrix)
        
        #TRANSFER ALL INPUTS TO THE OUTPUT VECTOR
        design_attr = Attribute()
        design_attr.setAttribute("rsf_matrix", rsf_matrix)
        design_attr.setAttribute("esf_matrix", esf_matrix)
        design_attr.setAttribute("ssf_matrix", ssf_matrix)
        design_attr.setAttribute("rain_ts", self.rain_ts)
        design_attr.setAttribute("evap_ts", self.evap_ts)
        design_attr.setAttribute("solar_ts", self.solar_ts)
        design_attr.setAttribute("rain_fname", self.rain_fname)
        design_attr.setAttribute("evap_fname", self.evap_fname)
        design_attr.setAttribute("solar_fname", self.solar_fname)
        design_attr.setAttribute("rain_scale", self.rain_scale)
        design_attr.setAttribute("evap_scale", self.evap_scale)
        design_attr.setAttribute("solar_scale", self.solar_scale)
        design_attr.setAttribute("Simpmax", self.Simpmax)
        design_attr.setAttribute("Spervmax", self.Spervmax)
        design_attr.setAttribute("muskK", self.muskK)
        design_attr.setAttribute("muskK", self.muskK)
        design_attr.setAttribute("muskK", self.muskK)
        design_attr.setAttribute("muskK", self.muskK)
        
        #Output vector update
        urbanwatersetup_out.setAttributes("UrbanWaterSettings", design_attr)
        

    
    ########################################################
    #LINK WITH GUI                                         #
    ########################################################   
    
    def createInputDialog(self):
        form = activateurbwatersettings_GUI(self, QApplication.activeWindow())
        form.show()
        return True  