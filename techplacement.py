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
import technology as tech
import techdesign as td
from techplacementguic import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from pyvibe import *

class techplacement(Module):
    """description of this module
        
    Describe the inputs and outputso f this module.
	- <description of inputs/outputs>
    
    Log of Updates made at each version:
    
    v0.80 update (March 2012):
        -
        -
        Future work:
            -
            -
    
    
    v0.75 update (October 2011):
        - 
        Future work:
            - 
            - 
    
    v0.5 update (August 2011):
        - 
        -
        
    v0.5 first (July 2011):
        - 
	
	@ingroup DAnCE4Water
	@author Peter M Bach
	"""

    def __init__(self):
        Module.__init__(self)
        self.blockcityin = VectorDataIn
        self.blockcityout = VectorDataIn
        self.patchcityin = VectorDataIn
        self.patchcityout = VectorDataIn
        self.design_details = VectorDataIn
        self.addParameter(self, "blockcityin", VIBe2.VECTORDATA_IN)
        self.addParameter(self, "blockcityout", VIBe2.VECTORDATA_OUT)
        self.addParameter(self, "patchcityin", VIBe2.VECTORDATA_IN)
        self.addParameter(self, "patchcityout", VIBe2.VECTORDATA_OUT)
        self.addParameter(self, "design_details", VIBe2.VECTORDATA_OUT)
        self.technames = ["ASHP", "AQ", "ASR", "BF", "GR", "GT", "GPT", "IS", "PPL", "PB", "PP", "RT", "SF", "ST", "IRR", "WSUB", "WSUR", "SW", "TPS", "UT", "WWRR", "WT", "WEF"]
        
        self.reportin = VectorDataIn
        self.reportout = VectorDataIn
        self.addParameter(self, "reportin", VIBe2.VECTORDATA_IN)
        self.addParameter(self, "reportout", VIBe2.VECTORDATA_OUT)
        
        #---DESIGN CRITERIA INPUTS-----------------------------------------------
        
        #DESIGN RATIONALE SETTINGS
        self.ration_runoff = True                #Design for flood mitigation?
        self.ration_pollute = True               #Design for pollution management?
        self.runoff_pri = 1                      #Priority of flood mitigation?
        self.pollute_pri = 1                      #Priority of pollution management?
        self.addParameter(self, "ration_runoff", VIBe2.BOOL)
        self.addParameter(self, "ration_pollute", VIBe2.BOOL)
        self.addParameter(self, "runoff_pri", VIBe2.DOUBLE)
        self.addParameter(self, "pollute_pri", VIBe2.DOUBLE)
        
        #WATER MANAGEMENT TARGETS
        self.targets_runoff = 80                 #Runoff reduction target [%]
        self.targets_TSS = 80                      #TSS Load reduction target [%]
        self.targets_TN = 30                       #TN Load reduction target [%]
        self.targets_TP = 30                       #TP Load reduction target [%]
        self.runoff_auto = False
        self.TSS_auto = False
        self.TN_auto = False
        self.TP_auto = False
        self.addParameter(self, "targets_runoff", VIBe2.DOUBLE)
        self.addParameter(self, "targets_TSS", VIBe2.DOUBLE)
        self.addParameter(self, "targets_TN", VIBe2.DOUBLE)
        self.addParameter(self, "targets_TP", VIBe2.DOUBLE)
        self.addParameter(self, "runoff_auto", VIBe2.BOOL)
        self.addParameter(self, "TSS_auto", VIBe2.BOOL)
        self.addParameter(self, "TN_auto", VIBe2.BOOL)
        self.addParameter(self, "TP_auto", VIBe2.BOOL)
        
        #STRATEGY CUSTOMIZE
        self.strategy_lot_check = True
        self.strategy_street_check = True
        self.strategy_neigh_check = True
        self.strategy_prec_check = True
        self.lot_increment = 4
        self.street_increment = 4
        self.neigh_increment = 4
        self.prec_increment = 4
        self.basin_target_min = 50
        self.basin_target_max = 100
        self.addParameter(self, "strategy_lot_check", VIBe2.BOOL)
        self.addParameter(self, "strategy_street_check", VIBe2.BOOL)
        self.addParameter(self, "strategy_neigh_check", VIBe2.BOOL)
        self.addParameter(self, "strategy_prec_check", VIBe2.BOOL)
        self.addParameter(self, "lot_increment", VIBe2.DOUBLE)
        self.addParameter(self, "street_increment", VIBe2.DOUBLE)
        self.addParameter(self, "neigh_increment", VIBe2.DOUBLE)
        self.addParameter(self, "prec_increment", VIBe2.DOUBLE)
        self.addParameter(self, "basin_target_min", VIBe2.DOUBLE)
        self.addParameter(self, "basin_target_max", VIBe2.DOUBLE)
        
        #ADDITIONAL STRATEGIES
        self.strategy_specific1 = False
        self.strategy_specific2 = False
        self.strategy_specific3 = False
        self.strategy_specific4 = False
        self.strategy_specific5 = False
        self.strategy_specific6 = False
        self.addParameter(self, "strategy_specific1", VIBe2.BOOL)
        self.addParameter(self, "strategy_specific2", VIBe2.BOOL)
        self.addParameter(self, "strategy_specific3", VIBe2.BOOL)
        self.addParameter(self, "strategy_specific4", VIBe2.BOOL)
        self.addParameter(self, "strategy_specific5", VIBe2.BOOL)
        self.addParameter(self, "strategy_specific6", VIBe2.BOOL)
        
        #---RETROFIT CONDITIONS INPUTS------------------------------------------
        self.retrofit_scenario = "N"    #N = Do Nothing, R = With Renewal, F = Forced
        self.renewal_cycle_def = 1      #Defined renewal cycle?
        self.renewal_years = 10         #number of years to apply renewal rate
        self.renewal_perc = 5           #renewal percentage
        self.force_street = 0              #forced renewal on lot?
        self.force_neigh = 0           #forced renewal on street?
        self.force_prec = 0            #forced renewal on neighbourhood and precinct?
        self.addParameter(self, "retrofit_scenario", VIBe2.STRING)
        self.addParameter(self, "renewal_cycle_def", VIBe2.BOOL)
        self.addParameter(self, "renewal_years", VIBe2.DOUBLE)
        self.addParameter(self, "renewal_perc", VIBe2.DOUBLE)
        self.addParameter(self, "force_street", VIBe2.BOOL)
        self.addParameter(self, "force_neigh", VIBe2.BOOL)
        self.addParameter(self, "force_prec", VIBe2.BOOL)
        
        self.lot_renew = 0
        self.lot_decom = 0
        self.street_renew = 0
        self.street_decom = 0
        self.neigh_renew = 0
        self.neigh_decom = 0
        self.prec_renew = 0
        self.prec_decom = 0
        self.addParameter(self, "lot_renew", VIBe2.BOOL)
        self.addParameter(self, "lot_decom", VIBe2.BOOL)
        self.addParameter(self, "street_renew", VIBe2.BOOL)
        self.addParameter(self, "street_decom", VIBe2.BOOL)
        self.addParameter(self, "neigh_renew", VIBe2.BOOL)
        self.addParameter(self, "neigh_decom", VIBe2.BOOL)
        self.addParameter(self, "prec_renew", VIBe2.BOOL)
        self.addParameter(self, "prec_decom", VIBe2.BOOL)
        
        
        #---GENERAL DESIGN CRITERIA---------------------------------------------
        #followed by vibe inputs
        #self.input_parameter = default value
        #self.addParameter(self, "input_parameter", VIBe2.DOUBLE)
        
        #---ADVANCED STORMWATER HARVESTING PLANT [ASHP]---###TBA###-------------
        self.ASHPstatus = 0
        self.addParameter(self, "ASHPstatus", VIBe2.BOOL)
        self.ASHPlevel = 0
        self.addParameter(self, "ASHPlevel", VIBe2.DOUBLE)
        self.ASHPgroup = 0
        self.addParameter(self, "ASHPgroup", VIBe2.DOUBLE)
        
        #---AQUACULTURE/LIVING SYSTEMS [AQ]---###TBA###-------------------------
        self.AQstatus = 0
        self.addParameter(self, "AQstatus", VIBe2.BOOL)
        self.AQlevel = 0
        self.addParameter(self, "AQlevel", VIBe2.DOUBLE)
        self.AQgroup = 0
        self.addParameter(self, "AQgroup", VIBe2.DOUBLE)
        
        #---AQUIFER STORAGE & RECOVERY SYSTEM [ASR]---###TBA###-----------------
        self.ASRstatus = 0
        self.addParameter(self, "ASRstatus", VIBe2.BOOL)
        self.ASRlevel = 0
        self.addParameter(self, "ASRlevel", VIBe2.DOUBLE)
        self.ASRgroup = 0
        self.addParameter(self, "ASRgroup", VIBe2.DOUBLE)
        
        
        #---BIOFILTRATION SYSTEM/RAINGARDEN [BF]--------------------------------
        self.BFstatus = 0
        self.addParameter(self, "BFstatus", VIBe2.BOOL)
        self.BFlevel = 0
        self.addParameter(self, "BFlevel", VIBe2.DOUBLE)
        self.BFgroup = 0
        self.addParameter(self, "BFgroup", VIBe2.DOUBLE)
        
        #Available Scales
        self.BFlot = True
        self.BFstreet = True
        self.BFneigh = True
        self.BFprec = True
        self.addParameter(self, "BFlot", VIBe2.BOOL)
        self.addParameter(self, "BFstreet", VIBe2.BOOL)
        self.addParameter(self, "BFneigh", VIBe2.BOOL)
        self.addParameter(self, "BFprec", VIBe2.BOOL)
        
        #Available Applications
        self.BFpollute = True
        self.addParameter(self, "BFpollute", VIBe2.BOOL)
        
        #Design Curves
        self.BFdesignUB = True          #use DAnCE4Water's default curves to design system?
        self.BFdescur_path = "no file"  #path for design curve
        self.addParameter(self, "BFdesignUB", VIBe2.BOOL)
        self.addParameter(self, "BFdescur_path", VIBe2.STRING)
        
        #Design Information
        self.BFspec_EDD = 0.3
        self.BFspec_FD = 0.6
        self.addParameter(self, "BFspec_EDD", VIBe2.DOUBLE)
        self.addParameter(self, "BFspec_FD", VIBe2.DOUBLE)
        self.BFmaxsize = 5000           #maximum surface area of system in sqm
        self.addParameter(self, "BFmaxsize", VIBe2.DOUBLE)
        
        self.BFlined = True
        self.addParameter(self, "BFlined", VIBe2.BOOL)
        
        
        #---GREEN ROOF [GR]---###TBA###-----------------------------------------
        self.GRstatus = 0
        self.addParameter(self, "GRstatus", VIBe2.BOOL)
        self.GRlevel = 0
        self.addParameter(self, "GRlevel", VIBe2.DOUBLE)
        self.GRgroup = 0
        self.addParameter(self, "GRgroup", VIBe2.DOUBLE)
                
        #---INFILTRATION SYSTEM [IS]--------------------------------------------
        self.ISstatus = 1
        self.addParameter(self, "ISstatus", VIBe2.BOOL)
        self.ISlevel = 0
        self.addParameter(self, "ISlevel", VIBe2.DOUBLE)
        self.ISgroup = 0
        self.addParameter(self, "ISgroup", VIBe2.DOUBLE)
        
        #Available Scales
        self.ISlot = True
        self.ISstreet = True
        self.ISneigh = True
        self.addParameter(self, "ISlot", VIBe2.BOOL)
        self.addParameter(self, "ISstreet", VIBe2.BOOL)
        self.addParameter(self, "ISneigh", VIBe2.BOOL)
        
        #Available Applications
        self.ISflow = True
        self.ISpollute = True
        self.addParameter(self, "ISflow", VIBe2.BOOL)
        self.addParameter(self, "ISpollute", VIBe2.BOOL)
        
        #Design Curves
        self.ISdesignUB = True          #use DAnCE4Water's default curves to design system?
        self.ISdescur_path = "no file"  #path for design curve
        self.addParameter(self, "ISdesignUB", VIBe2.BOOL)
        self.addParameter(self, "ISdescur_path", VIBe2.STRING)
        
        #Design Information
        self.ISspec_EDD = 0.2
        self.ISspec_FD = 0.8
        self.addParameter(self, "ISspec_EDD", VIBe2.DOUBLE)
        self.addParameter(self, "ISspec_FD", VIBe2.DOUBLE)
        self.ISmaxsize = 5000          #maximum surface area of system in sqm
        self.addParameter(self, "ISmaxsize", VIBe2.DOUBLE)

        self.IS_2Dmodel = True
        self.addParameter(self, "IS_2Dmodel", VIBe2.BOOL)
        
        #---GROSS POLLUTANT TRAP [GPT]------------------------------------------
        self.GPTstatus = 0
        self.addParameter(self, "GPTstatus", VIBe2.BOOL)
        self.GPTlevel = 0
        self.addParameter(self, "GPTlevel", VIBe2.DOUBLE)
        self.GPTgroup = 0
        self.addParameter(self, "GPTgroup", VIBe2.DOUBLE)
        
        #self.input_parameter = default value
        #self.addParameter(self, "input_parameter", VIBe2.DOUBLE)
        
        #---GREYWATER TREATMENT & DIVERSION SYSTEM [GT]-------------------------
        self.GTstatus = 0
        self.addParameter(self, "GTstatus", VIBe2.BOOL)
        self.GTlevel = 0
        self.addParameter(self, "GTlevel", VIBe2.DOUBLE)
        self.GTgroup = 0
        self.addParameter(self, "GTgroup", VIBe2.DOUBLE)
        
        #followed by vibe inputs
        #self.input_parameter = default value
        #self.addParameter(self, "input_parameter", VIBe2.DOUBLE)
        
        #---PACKAGED PLANT [PPL]---###TBA###------------------------------------
        self.PPLstatus = 0
        self.addParameter(self, "PPLstatus", VIBe2.BOOL)
        self.PPLlevel = 0
        self.addParameter(self, "PPLlevel", VIBe2.DOUBLE)
        self.PPLgroup = 0
        self.addParameter(self, "PPLgroup", VIBe2.DOUBLE)
        
        #---PONDS & SEDIMENTATION BASIN [PB]------------------------------------
        self.PBstatus = 0
        self.addParameter(self, "PBstatus", VIBe2.BOOL)
        self.PBlevel = 0
        self.addParameter(self, "PBlevel", VIBe2.DOUBLE)
        self.PBgroup = 0
        self.addParameter(self, "PBgroup", VIBe2.DOUBLE)
        
        #Available Scales
        self.PBneigh = True
        self.PBprec = True
        self.addParameter(self, "PBneigh", VIBe2.BOOL)
        self.addParameter(self, "PBprec", VIBe2.BOOL)
        
        #Available Applications
        self.PBflow = True
        self.PBpollute = True
        self.addParameter(self, "PBflow", VIBe2.BOOL)
        self.addParameter(self, "PBpollute", VIBe2.BOOL)
        
        #Design Curves
        self.PBdesignUB = True          #use DAnCE4Water's default curves to design system?
        self.PBdescur_path = "no file"  #path for design curve
        self.addParameter(self, "PBdesignUB", VIBe2.BOOL)
        self.addParameter(self, "PBdescur_path", VIBe2.STRING)
        
        #Design Information
        self.PBspec_MD = 1.25
        self.addParameter(self, "PBspec_MD", VIBe2.DOUBLE)
        self.PBmaxsize = 10000           #maximum surface area of system in sqm
        self.addParameter(self, "PBmaxsize", VIBe2.DOUBLE)

        
        #---POROUS/PERVIOUS PAVEMENT [PP]---###TBA###---------------------------
        self.PPstatus = 0
        self.addParameter(self, "PPstatus", VIBe2.BOOL)
        self.PPlevel = 0
        self.addParameter(self, "PPlevel", VIBe2.DOUBLE)
        self.PPgroup = 0
        self.addParameter(self, "PPgroup", VIBe2.DOUBLE)
        
        #---RAINWATER TANK [RT]-------------------------------------------------
        self.RTstatus = 0
        self.addParameter(self, "RTstatus", VIBe2.BOOL)
        self.RTlevel = 0
        self.addParameter(self, "RTlevel", VIBe2.DOUBLE)
        self.RTgroup = 0
        self.addParameter(self, "RTgroup", VIBe2.DOUBLE)
        
        self.RTscale_lot = True
        self.RTscale_street = True
        self.RTpurp_flood = True
        self.RTpurp_recyc = False
        self.addParameter(self, "RTscale_lot", VIBe2.BOOL)
        self.addParameter(self, "RTscale_street", VIBe2.BOOL)
        self.addParameter(self, "RTpurp_flood", VIBe2.BOOL)
        self.addParameter(self, "RTpurp_recyc", VIBe2.BOOL)
        
        self.RT_firstflush = 2          #first flush volume [mm]
        self.RT_maxdepth = 2            #max tank depth [m]
        self.RT_mindead = 0.1           #minimum dead storage level [m]
        self.RT_shape_circ = True       #consider circular tanks
        self.RT_shape_rect = True       #consider rectangular tanks
        self.RT_sbmodel = "ybs"         #storage-behaviour model settings
        self.RTdesignD4W = True         #use DAnCE4Water's default curves to design system?
        self.RTdescur_path = "no file"  #path for design curve
        self.addParameter(self, "RT_firstflush", VIBe2.DOUBLE)
        self.addParameter(self, "RT_maxdepth", VIBe2.DOUBLE)
        self.addParameter(self, "RT_mindead", VIBe2.DOUBLE)
        self.addParameter(self, "RT_shape_circ", VIBe2.BOOL)
        self.addParameter(self, "RT_shape_rect", VIBe2.BOOL)
        self.addParameter(self, "RT_sbmodel", VIBe2.STRING)
        self.addParameter(self, "RTdesignD4W", VIBe2.BOOL)
        self.addParameter(self, "RTdescur_path", VIBe2.STRING)
        
        #---SAND/PEAT/GRAVEL FILTER [SF]----------------------------------------
        self.SFstatus = 0
        self.addParameter(self, "SFstatus", VIBe2.BOOL)
        self.SFlevel = 0
        self.addParameter(self, "SFlevel", VIBe2.DOUBLE)
        self.SFgroup = 0
        self.addParameter(self, "SFgroup", VIBe2.DOUBLE)
        
        #---SEPTIC TANK [ST]---###TBA###----------------------------------------
        self.STstatus = 0
        self.addParameter(self, "STstatus", VIBe2.BOOL)
        self.STlevel = 0
        self.addParameter(self, "STlevel", VIBe2.DOUBLE)
        self.STgroup = 0
        self.addParameter(self, "STgroup", VIBe2.DOUBLE)
        
        #---SUBSURFACE IRRIGATION SYSTEM [IRR]---###TBA###----------------------
        self.IRRstatus = 0
        self.addParameter(self, "IRRstatus", VIBe2.BOOL)
        self.IRRlevel = 0
        self.addParameter(self, "IRRlevel", VIBe2.DOUBLE)
        self.IRRgroup = 0
        self.addParameter(self, "IRRgroup", VIBe2.DOUBLE)
        
        #---SUBSURFACE WETLAND/REED BED [WSUB]----------------------------------
        self.WSUBstatus = 0
        self.addParameter(self, "WSUBstatus", VIBe2.BOOL)
        self.WSUBlevel = 0
        self.addParameter(self, "WSUBlevel", VIBe2.DOUBLE)
        self.WSUBgroup = 0
        self.addParameter(self, "WSUBgroup", VIBe2.DOUBLE)
        
        #---SURFACE WETLAND [WSUR]----------------------------------------------
        self.WSURstatus = 0
        self.addParameter(self, "WSURstatus", VIBe2.BOOL)
        self.WSURlevel = 0
        self.addParameter(self, "WSURlevel", VIBe2.DOUBLE)
        self.WSURgroup = 0
        self.addParameter(self, "WSURgroup", VIBe2.DOUBLE)
        
        #Available Scales
        self.WSURneigh = True
        self.WSURprec = True
        self.addParameter(self, "WSURneigh", VIBe2.BOOL)
        self.addParameter(self, "WSURprec", VIBe2.BOOL)
        
        #Available Applications
        self.WSURflow = True
        self.WSURpollute = True
        self.addParameter(self, "WSURflow", VIBe2.BOOL)
        self.addParameter(self, "WSURpollute", VIBe2.BOOL)
        
        #Design Curves
        self.WSURdesignUB = True          #use DAnCE4Water's default curves to design system?
        self.WSURdescur_path = "no file"  #path for design curve
        self.addParameter(self, "WSURdesignUB", VIBe2.BOOL)
        self.addParameter(self, "WSURdescur_path", VIBe2.STRING)
        
        #Design Information
        self.WSURspec_EDD = 0.75
        self.addParameter(self, "WSURspec_EDD", VIBe2.DOUBLE)
        self.WSURmaxsize = 10000           #maximum surface area of system in sqm
        self.addParameter(self, "WSURmaxsize", VIBe2.DOUBLE)

        
        #---SWALES & BUFFER STRIPS [SW]-----------------------------------------
        self.SWstatus = 0
        self.addParameter(self, "SWstatus", VIBe2.BOOL)
        self.SWlevel = 0
        self.addParameter(self, "SWlevel", VIBe2.DOUBLE)
        self.SWgroup = 0
        self.addParameter(self, "SWgroup", VIBe2.DOUBLE)
        
        #Available Scales
        self.SWstreet = True
        self.addParameter(self, "SWstreet", VIBe2.BOOL)
        
        #Available Applications
        self.SWflow = True
        self.SWpollute = True
        self.addParameter(self, "SWflow", VIBe2.BOOL)
        self.addParameter(self, "SWpollute", VIBe2.BOOL)
        
        #Design Curves
        self.SWdesignUB = True          #use DAnCE4Water's default curves to design system?
        self.SWdescur_path = "no file"  #path for design curve
        self.addParameter(self, "SWdesignUB", VIBe2.BOOL)
        self.addParameter(self, "SWdescur_path", VIBe2.STRING)
        
        #Design Information
        self.SWspec = 0
        self.addParameter(self, "SWspec", VIBe2.DOUBLE)
        self.SWmaxsize = 600           #maximum surface area of system in sqm
        self.addParameter(self, "SWmaxsize", VIBe2.DOUBLE)


        #---TREE PITS [TPS]---###TBA###-----------------------------------------
        self.TPSstatus = 0
        self.addParameter(self, "TPSstatus", VIBe2.BOOL)
        self.TPSlevel = 0
        self.addParameter(self, "TPSlevel", VIBe2.DOUBLE)
        self.TPSgroup = 0
        self.addParameter(self, "TPSgroup", VIBe2.DOUBLE)
        
        
        #---URINE-SEPARATING TOILET [UT]---###TBA###----------------------------
        self.UTstatus = 0
        self.addParameter(self, "UTstatus", VIBe2.BOOL)
        self.UTlevel = 0
        self.addParameter(self, "UTlevel", VIBe2.DOUBLE)
        self.UTgroup = 0
        self.addParameter(self, "UTgroup", VIBe2.DOUBLE)
        
        #---WASTEWATER RECOVERY & RECYCLING PLANT [WWRR]---###TBA###------------
        self.WWRRstatus = 0
        self.addParameter(self, "WWRRstatus", VIBe2.BOOL)
        self.WWRRlevel = 0
        self.addParameter(self, "WWRRlevel", VIBe2.DOUBLE)
        self.WWRRgroup = 0
        self.addParameter(self, "WWRRgroup", VIBe2.DOUBLE)
        
        #---WATERLESS/COMPOSTING TOILETS [WT]---###TBA###-----------------------
        self.WTstatus = 0
        self.addParameter(self, "WTstatus", VIBe2.BOOL)
        self.WTlevel = 0
        self.addParameter(self, "WTlevel", VIBe2.DOUBLE)
        self.WTgroup = 0
        self.addParameter(self, "WTgroup", VIBe2.DOUBLE)
        
        #---WATER EFFICIENT APPLIANCES [WEF]------------------------------------
        self.WEFstatus = 0
        self.addParameter(self, "WEFstatus", VIBe2.BOOL)
        self.WEFlevel = 0
        self.addParameter(self, "WEFlevel", VIBe2.DOUBLE)
        self.WEFgroup = 0
        self.addParameter(self, "WEFgroup", VIBe2.DOUBLE)
        
        self.WEF_implement_method = "LEG"
        self.LEG_force = False
        self.LEG_minrate = 5
        self.PPP_force = False
        self.PPP_likelihood = 50
        self.SEC_force = False
        self.SEC_urbansim = False
        self.D4W_UDMactive = False
        self.D4W_STMactive = False
        self.D4W_EVMactive = False
        self.addParameter(self, "WEF_implement_method", VIBe2.STRING)
        self.addParameter(self, "LEG_force", VIBe2.BOOL)
        self.addParameter(self, "LEG_minrate", VIBe2.DOUBLE)
        self.addParameter(self, "PPP_force", VIBe2.BOOL)
        self.addParameter(self, "PPP_likelihood", VIBe2.DOUBLE)
        self.addParameter(self, "SEC_force", VIBe2.BOOL)
        self.addParameter(self, "SEC_urbansim", VIBe2.BOOL)
        self.addParameter(self, "D4W_UDMactive", VIBe2.BOOL)
        self.addParameter(self, "D4W_STMactive", VIBe2.BOOL)
        self.addParameter(self, "D4W_EVMactive", VIBe2.BOOL)
        
        self.WEF_rating_system = "AS"
        self.WEF_loc_famhouse = True
        self.WEF_loc_apart = True
        self.WEF_loc_nonres = True
        self.WEF_flow_method = "M"
        self.addParameter(self, "WEF_rating_system", VIBe2.STRING)
        self.addParameter(self, "WEF_loc_famhouse", VIBe2.BOOL)
        self.addParameter(self, "WEF_loc_apart", VIBe2.BOOL)
        self.addParameter(self, "WEF_loc_nonres", VIBe2.BOOL)
        self.addParameter(self, "WEF_flow_method", VIBe2.STRING)
        
        #---<Add a new system - Name> [abbrev.]---------------------------------
        #self.<abbrev>status = 1
        #self.addParameter(self, "<abbrev>status", VIBe2.BOOL)
        #followed by vibe inputs
        #self.input_parameter = default value
        #self.addParameter(self, "input_parameter", VIBe2.DOUBLE)
        
        #---REGIONAL INFORMATION -----------------------------------------------
        self.regioncity = "Melbourne"
        self.addParameter(self, "regioncity", VIBe2.STRING)
        
        
        #---MULTI-CRITERIA INPUTS-----------------------------------------------
        #SELECT EVALUATION METRICS
        self.scoringmatrix_path = "None"
        self.scoringmatrix_default = False
        self.scoring_include_all = True
        self.addParameter(self, "scoringmatrix_path", VIBe2.STRING)
        self.addParameter(self, "scoringmatrix_default", VIBe2.BOOL)
        self.addParameter(self, "scoring_include_all", VIBe2.BOOL)
        
        #CUSTOMIZE EVALUATION CRITERIA
        self.bottomlines_tech = False   #Include criteria? Yes/No
        self.bottomlines_env = False
        self.bottomlines_ecn = False
        self.bottomlines_soc = False
        self.bottomlines_tech_n = 0     #Metric numbers
        self.bottomlines_env_n = 0
        self.bottomlines_ecn_n = 0
        self.bottomlines_soc_n = 0
        
        self.eval_mode = "W"            #Evaluation Mode: W = Single weightings, P = Pareto Exploration (refer to parameter suffix)
        self.bottomlines_tech_p = 0     #Pareto Exploration increments
        self.bottomlines_env_p = 0
        self.bottomlines_ecn_p = 0
        self.bottomlines_soc_p = 0
        self.bottomlines_tech_w = 0     #Single weighting weights
        self.bottomlines_env_w = 0
        self.bottomlines_ecn_w = 0
        self.bottomlines_soc_w = 0
        self.addParameter(self, "bottomlines_tech", VIBe2.BOOL)
        self.addParameter(self, "bottomlines_env", VIBe2.BOOL)
        self.addParameter(self, "bottomlines_ecn", VIBe2.BOOL)
        self.addParameter(self, "bottomlines_soc", VIBe2.BOOL)
        self.addParameter(self, "bottomlines_tech_n", VIBe2.DOUBLE)
        self.addParameter(self, "bottomlines_env_n", VIBe2.DOUBLE)
        self.addParameter(self, "bottomlines_ecn_n", VIBe2.DOUBLE)
        self.addParameter(self, "bottomlines_soc_n", VIBe2.DOUBLE)
        self.addParameter(self, "eval_mode", VIBe2.STRING)
        self.addParameter(self, "bottomlines_tech_p", VIBe2.DOUBLE)
        self.addParameter(self, "bottomlines_env_p", VIBe2.DOUBLE)
        self.addParameter(self, "bottomlines_ecn_p", VIBe2.DOUBLE)
        self.addParameter(self, "bottomlines_soc_p", VIBe2.DOUBLE)
        self.addParameter(self, "bottomlines_tech_w", VIBe2.DOUBLE)
        self.addParameter(self, "bottomlines_env_w", VIBe2.DOUBLE)
        self.addParameter(self, "bottomlines_ecn_w", VIBe2.DOUBLE)
        self.addParameter(self, "bottomlines_soc_w", VIBe2.DOUBLE)
        
        #SCORING OF STRATEGIES
        self.scope_stoch = False
        self.score_method = "AHP"       #MCA scoring method
        self.tech2strat_method = "EqW"  #How to merge technology scores into strategy score
        self.addParameter(self, "scope_stoch", VIBe2.BOOL)
        self.addParameter(self, "score_method", VIBe2.STRING)
        self.addParameter(self, "tech2strat_method", VIBe2.STRING)
        
        #RANKING OF STRATEGIES
        self.ranktype = "CI"            #CI = Confidence Interval, RK = ranking
        self.topranklimit = 10
        self.conf_int = 95
        self.ingroup_scoring = "Avg"
        self.addParameter(self, "ranktype", VIBe2.STRING)
        self.addParameter(self, "topranklimit", VIBe2.DOUBLE)
        self.addParameter(self, "conf_int", VIBe2.DOUBLE)
        self.addParameter(self, "ingroup_scoring", VIBe2.STRING)
        
        
    def run(self):
        #Link input vectors with local variables
        blockcityin = self.blockcityin.getItem()
        blockcityout = self.blockcityout.getItem()
        patchcityin = self.patchcityin.getItem()
        patchcityout = self.patchcityout.getItem()
        map_attr = blockcityin.getAttributes("MapAttributes")
        design_details = self.design_details.getItem()
        
        #get data needed to being for loop analysis
        blocks_num = map_attr.getAttribute("NumBlocks")     #number of blocks to loop through
        blocks_size = map_attr.getAttribute("BlockSize")    #size of block
        map_w = map_attr.getAttribute("WidthBlocks")        #num of blocks wide
        map_h = map_attr.getAttribute("HeightBlocks")       #num of blocks tall
        input_res = map_attr.getAttribute("InputReso")      #resolution of input data
        
        basins = map_attr.getAttribute("TotalBasins")
        for i in range(int(basins)):
            currentID = i+1
            basin_attr = blockcityin.getAttributes("BasinID"+str(currentID))
            blockcityout.setAttributes("BasinID"+str(currentID), basin_attr)
        
        #--------------------------------------------------------------------------------#
        #       TRANSFER ALL DESIGN CRITERIA AND STRATEGY SETUP INPUTS TO DES_ATTR       #
        #--------------------------------------------------------------------------------#
        #write all technologies checked/unchecked statuses to output vector attribute list
        des_attr = Attribute()                              #technology status are saved to this attribute list
        
        des_attr.setAttribute("ration_runoff", self.ration_runoff)
        des_attr.setAttribute("ration_pollute", self.ration_pollute)
        des_attr.setAttribute("runoff_pri", self.runoff_pri)
        des_attr.setAttribute("pollute_pri", self.pollute_pri)
        des_attr.setAttribute("targets_runoff", self.targets_runoff)
        des_attr.setAttribute("targets_TSS", self.targets_TSS)
        des_attr.setAttribute("targets_TN", self.targets_TN)
        des_attr.setAttribute("targets_TP", self.targets_TP)
        des_attr.setAttribute("runoff_auto", self.runoff_auto)
        des_attr.setAttribute("TSS_auto", self.TSS_auto)
        des_attr.setAttribute("TN_auto", self.TN_auto)
        des_attr.setAttribute("TP_auto", self.TP_auto)
        des_attr.setAttribute("strategy_lot_check", self.strategy_lot_check)
        des_attr.setAttribute("strategy_street_check", self.strategy_street_check)
        des_attr.setAttribute("strategy_neigh_check", self.strategy_neigh_check)
        des_attr.setAttribute("strategy_prec_check", self.strategy_prec_check)
        des_attr.setAttribute("lot_increment", self.lot_increment)
        des_attr.setAttribute("street_increment", self.street_increment)
        des_attr.setAttribute("neigh_increment", self.neigh_increment)
        des_attr.setAttribute("prec_increment", self.prec_increment)
        des_attr.setAttribute("basin_target_min", self.basin_target_min)
        des_attr.setAttribute("basin_target_max", self.basin_target_max)
        des_attr.setAttribute("strategy_specific1", self.strategy_specific1)
        des_attr.setAttribute("strategy_specific2", self.strategy_specific2)
        des_attr.setAttribute("strategy_specific3", self.strategy_specific3)
        des_attr.setAttribute("strategy_specific4", self.strategy_specific4)
        des_attr.setAttribute("strategy_specific5", self.strategy_specific5)
        des_attr.setAttribute("strategy_specific6", self.strategy_specific6)
        
        #--------------------------------------------------------------------------------#
        #       TRANSFER ALL TECHNOLOGY STATUSES TO DES_ATTR                             #
        #--------------------------------------------------------------------------------#
        
        des_attr.setAttribute("Status_ASHP", self.ASHPstatus)   #ADVANCED STORMWATERHARVESTING PLANT
        des_attr.setAttribute("ASHPlevel", self.ASHPlevel)
        #des_attr.setAttribute("ASHPgroup", self.ASHPgroup)
                              
        des_attr.setAttribute("Status_AQ", self.AQstatus)       #AQUACULTURE
        des_attr.setAttribute("AQlevel", self.AQlevel)
        #des_attr.setAttribute("AQgroup", self.AQgroup)
        
        des_attr.setAttribute("Status_ASR", self.ASRstatus)     #AQUIFER STORAGE & RECOVERY SYSTEM
        des_attr.setAttribute("ASRlevel", self.ASRlevel)
        #des_attr.setAttribute("ASRgroup", self.ASRgroup)
        
        #====================---------------------------------------------------------------
        des_attr.setAttribute("Status_BF", self.BFstatus)       #BIOFILTRATION SYSTEM
        des_attr.setAttribute("BFlevel", self.BFlevel)
        #des_attr.setAttribute("BFgroup", self.BFgroup)
        des_attr.setAttribute("BFlot", self.BFlot)
        des_attr.setAttribute("BFstreet", self.BFstreet)
        des_attr.setAttribute("BFneigh", self.BFneigh)
        des_attr.setAttribute("BFprec", self.BFprec)
        des_attr.setAttribute("BFpollute", self.BFpollute)
        des_attr.setAttribute("BFdesignUB", self.BFdesignUB)
        des_attr.setAttribute("BFdescur_path", self.BFdescur_path)
        des_attr.setAttribute("BFspec_EDD", self.BFspec_EDD)
        des_attr.setAttribute("BFspec_FD", self.BFspec_FD)
        des_attr.setAttribute("BFmaxsize", self.BFmaxsize)
        des_attr.setAttribute("BFlined", self.BFlined)
        #====================---------------------------------------------------------------
        
        des_attr.setAttribute("Status_GR", self.GRstatus)       #GREEN ROOF
        des_attr.setAttribute("GRlevel", self.GRlevel)
        #des_attr.setAttribute("GRgroup", self.GRgroup)
        
        des_attr.setAttribute("Status_GT", self.GTstatus)       #GREYWATER TANK
        des_attr.setAttribute("GTlevel", self.GTlevel)
        #des_attr.setAttribute("GTgroup", self.GTgroup)
        
        des_attr.setAttribute("Status_GPT", self.GPTstatus)     #GROSS POLLUTANT TRAP
        des_attr.setAttribute("GPTlevel", self.GPTlevel)
        #des_attr.setAttribute("GPTgroup", self.GPTgroup)
        
        #====================---------------------------------------------------------------
        des_attr.setAttribute("Status_IS", self.ISstatus)       #INFILTRATION SYSTEM
        des_attr.setAttribute("ISlevel", self.ISlevel)
        #des_attr.setAttribute("ISgroup", self.ISgroup)
        des_attr.setAttribute("ISlot", self.ISlot)
        des_attr.setAttribute("ISstreet", self.ISstreet)
        des_attr.setAttribute("ISneigh", self.ISneigh)
        des_attr.setAttribute("ISflow", self.ISflow)
        des_attr.setAttribute("ISpollute", self.ISpollute)
        des_attr.setAttribute("ISdesignUB", self.ISdesignUB)
        des_attr.setAttribute("ISdescur_path", self.ISdescur_path)
        des_attr.setAttribute("ISspec_EDD", self.ISspec_EDD)
        des_attr.setAttribute("ISspec_FD", self.ISspec_FD)
        des_attr.setAttribute("ISmaxsize", self.ISmaxsize)
        des_attr.setAttribute("IS_2Dmodel", self.IS_2Dmodel)
        #====================---------------------------------------------------------------
        
        des_attr.setAttribute("Status_PPL", self.PPLstatus)     #PACKAGED PLANT
        des_attr.setAttribute("PPLlevel", self.PPLlevel)
        #des_attr.setAttribute("PPLgroup", self.PPLgroup)
        
        #====================---------------------------------------------------------------
        des_attr.setAttribute("Status_PB", self.PBstatus)       #PONDS & BASINS
        des_attr.setAttribute("PBlevel", self.PBlevel)
        #des_attr.setAttribute("PBgroup", self.PBgroup)
        des_attr.setAttribute("PBneigh", self.PBneigh)
        des_attr.setAttribute("PBprec", self.PBprec)
        des_attr.setAttribute("PBflow", self.PBflow)
        des_attr.setAttribute("PBpollute", self.PBpollute)
        des_attr.setAttribute("PBdesignUB", self.PBdesignUB)
        des_attr.setAttribute("PBdescur_path", self.PBdescur_path)
        des_attr.setAttribute("PBspec_MD", self.PBspec_MD)
        des_attr.setAttribute("PBmaxsize", self.PBmaxsize)
        #====================---------------------------------------------------------------
        
        des_attr.setAttribute("Status_PP", self.PPstatus)       #POROUS PAVEMENTS
        des_attr.setAttribute("PPlevel", self.PPlevel)
        #des_attr.setAttribute("PPgroup", self.PPgroup)
        
        des_attr.setAttribute("Status_RT", self.RTstatus)       #RAINTANKS
        des_attr.setAttribute("RTlevel", self.RTlevel)
        #des_attr.setAttribute("RTgroup", self.RTgroup)
        
        des_attr.setAttribute("Status_SF", self.SFstatus)       #SAND/PEAT/GRAVEL FILTERS
        des_attr.setAttribute("SFlevel", self.SFlevel)
        #des_attr.setAttribute("SFgroup", self.SFgroup)
        
        des_attr.setAttribute("Status_ST", self.STstatus)       #SEPTIC TANKS
        des_attr.setAttribute("STlevel", self.STlevel)
        #des_attr.setAttribute("STgroup", self.STgroup)
        
        des_attr.setAttribute("Status_IRR", self.IRRstatus)     #SUBSURFACE IRRIGATION SYSTEM
        des_attr.setAttribute("IRRlevel", self.IRRlevel)
        #des_attr.setAttribute("IRRgroup", self.IRRgroup)
        
        des_attr.setAttribute("Status_WSUB", self.WSUBstatus)   #SUBSURFACE WETLAND
        des_attr.setAttribute("WSUBlevel", self.WSUBlevel)
        #des_attr.setAttribute("WSUBgroup", self.WSUBgroup)
        
        #====================---------------------------------------------------------------
        des_attr.setAttribute("Status_WSUR", self.WSURstatus)   #SURFACE WETLAND
        des_attr.setAttribute("WSURlevel", self.WSURlevel)
        #des_attr.setAttribute("WSURgroup", self.WSURgroup)
        des_attr.setAttribute("WSURneigh", self.WSURneigh)
        des_attr.setAttribute("WSURprec", self.WSURprec)
        des_attr.setAttribute("WSURflow", self.WSURflow)
        des_attr.setAttribute("WSURpollute", self.WSURpollute)
        des_attr.setAttribute("WSURdesignUB", self.WSURdesignUB)
        des_attr.setAttribute("WSURdescur_path", self.WSURdescur_path)
        des_attr.setAttribute("WSURspec_EDD", self.WSURspec_EDD)
        des_attr.setAttribute("WSURmaxsize", self.WSURmaxsize)
        #====================---------------------------------------------------------------
        des_attr.setAttribute("Status_SW", self.SWstatus)       #SWALES & BUFFER STRIPS
        des_attr.setAttribute("SWlevel", self.SWlevel)
        #des_attr.setAttribute("SWgroup", self.SWgroup)
        des_attr.setAttribute("SWstreet", self.SWstreet)
        des_attr.setAttribute("SWflow", self.SWflow)
        des_attr.setAttribute("SWpollute", self.SWpollute)
        des_attr.setAttribute("SWdesignUB", self.SWdesignUB)
        des_attr.setAttribute("SWdescur_path", self.SWdescur_path)
        des_attr.setAttribute("SWspec", self.SWspec)
        des_attr.setAttribute("SWmaxsize", self.SWmaxsize)
        #====================---------------------------------------------------------------
        des_attr.setAttribute("Status_TPS", self.TPSstatus)     #TREE PITS
        des_attr.setAttribute("TPSlevel", self.TPSlevel)
        #des_attr.setAttribute("TPSgroup", self.TPSgroup)
        
        des_attr.setAttribute("Status_UT", self.UTstatus)       #URINE-SEPARATING TOILETS
        des_attr.setAttribute("UTlevel", self.UTlevel)
        #des_attr.setAttribute("UTgroup", self.UTgroup)
        
        des_attr.setAttribute("Status_WWRR", self.WWRRstatus)   #WASTEWATER RECOVERY & RECYCLING PLANT
        des_attr.setAttribute("WWRRlevel", self.WWRRlevel)
        #des_attr.setAttribute("WWRRgroup", self.WWRRgroup)
        
        des_attr.setAttribute("Status_WT", self.WTstatus)       #WATERLESS TOILETS
        des_attr.setAttribute("WTlevel", self.WTlevel)
        #des_attr.setAttribute("WTgroup", self.WTgroup)
        
        des_attr.setAttribute("Status_WEF", self.WEFstatus)     #WATER EFFICIENT APPLIANCES
        des_attr.setAttribute("WEFlevel", self.WEFlevel)
        #des_attr.setAttribute("WEFgroup", self.WEFgroup)
        
        #GET REGIONAL INPUTS
        des_attr.setAttribute("regioncity", self.regioncity)
        
        #--------------------------------------------------------------------------------#
        #       TRANSFER ALL EVALUATION INPUTS TO TO DES_ATTR                            #
        #--------------------------------------------------------------------------------#
        des_attr.setAttribute("scoringmatrix_path", self.scoringmatrix_path)
        des_attr.setAttribute("scoringmatrix_default", self.scoringmatrix_default)
        des_attr.setAttribute("scoring_include_all", self.scoring_include_all)
        
        des_attr.setAttribute("eval_mode", self.eval_mode)
        des_attr.setAttribute("bottomlines_tech_p", self.bottomlines_tech_p)
        des_attr.setAttribute("bottomlines_env_p", self.bottomlines_env_p)
        des_attr.setAttribute("bottomlines_ecn_p", self.bottomlines_ecn_p)
        des_attr.setAttribute("bottomlines_soc_p", self.bottomlines_soc_p)
        
        des_attr.setAttribute("bottomlines_tech", self.bottomlines_tech)
        des_attr.setAttribute("bottomlines_env", self.bottomlines_env)
        des_attr.setAttribute("bottomlines_ecn", self.bottomlines_ecn)
        des_attr.setAttribute("bottomlines_soc", self.bottomlines_soc)
        des_attr.setAttribute("bottomlines_tech_n", self.bottomlines_tech_n)
        des_attr.setAttribute("bottomlines_env_n", self.bottomlines_env_n)
        des_attr.setAttribute("bottomlines_ecn_n", self.bottomlines_ecn_n)
        des_attr.setAttribute("bottomlines_soc_n", self.bottomlines_soc_n)
        des_attr.setAttribute("bottomlines_tech_w", self.bottomlines_tech_w)
        des_attr.setAttribute("bottomlines_env_w", self.bottomlines_env_w)
        des_attr.setAttribute("bottomlines_ecn_w", self.bottomlines_ecn_w)
        des_attr.setAttribute("bottomlines_soc_w", self.bottomlines_soc_w)
        
        des_attr.setAttribute("scope_stoch", self.scope_stoch)
        des_attr.setAttribute("score_method", self.score_method)
        des_attr.setAttribute("tech2strat_method", self.tech2strat_method)
        
        des_attr.setAttribute("ranktype", self.ranktype)
        des_attr.setAttribute("topranklimit", self.topranklimit)
        des_attr.setAttribute("conf_int", self.conf_int)
        des_attr.setAttribute("ingroup_scoring", self.ingroup_scoring)
        
        
        #create technology list - THIS IS THE USER'S CUSTOMISED SHORTLIST
        techchecked = []                #holds the active technologies selected by user for simulation
        for j in self.technames:        #sifts through all tech names to pick out the right ones
            if int(des_attr.getAttribute("Status_"+j)) == 1:
                techchecked.append(j)
            else:
                pass
        
        #create technology list for scales
        techcheckedlot = ""
        techcheckedstreet = ""
        techcheckedneigh = ""
        techcheckedprec = ""
        
        for j in techchecked:
            if int(des_attr.getAttribute(str(j)+"lot")) == 1:
                techcheckedlot += str(j) + ","
            if int(des_attr.getAttribute(str(j)+"street")) == 1:
                techcheckedstreet += str(j) + ","
            if int(des_attr.getAttribute(str(j)+"neigh")) == 1:
                techcheckedneigh += str(j) + ","
            if int(des_attr.getAttribute(str(j)+"prec")) == 1:
                techcheckedprec += str(j) + ","
        
        if self.strategy_lot_check == False:
            print "Simulation not to include Lot-scale strategies, skipping analysis"
            techcheckedlot = ","
        if self.strategy_street_check == False:
            print "Simulation not to include Street-scale strategies, skipping analysis"
            techcheckedstreet = ","
        if self.strategy_neigh_check == False:
            print "Simulation not to include Neighbourhood-scale strategies, skipping analysis"
            techcheckedneigh = ","
        if self.strategy_prec_check == False:
            print "Simulation not to include Precinct-scale strategies, skipping analysis"
            techcheckedprec = ""
        
        print techcheckedlot
        print techcheckedstreet
        print techcheckedneigh
        print techcheckedprec
        
        des_attr.setAttribute("techcheckedlot", str(techcheckedlot))
        des_attr.setAttribute("techcheckedstreet", str(techcheckedstreet))
        des_attr.setAttribute("techcheckedneigh", str(techcheckedneigh))
        des_attr.setAttribute("techcheckedprec", str(techcheckedprec))
        
#        #work out combinations
#        combos = []
#        for i in range(len(lot_increment)):
#            for j in range(len(street_increment)):
#                for k in range(len(neigh_increment)):
#                    if street_increment[j] + neigh_increment[k] <= 1:
#                        combos.append([lot_increment[i],street_increment[j],neigh_increment[k]])
#                    else:
#                        pass
        
        
        #begin algorithm for assessing system suitability in all blocks
        for i in range(int(blocks_num)):
            currentID = i + 1
            currentAttList = blockcityin.getAttributes("BlockID"+str(currentID))        #attribute list of current block structure
            plist = blockcityin.getPoints("BlockID"+str(currentID))
            flist = blockcityin.getFaces("BlockID"+str(currentID))
            pnetlist = blockcityin.getPoints("NetworkID"+str(currentID))
            enetlist = blockcityin.getEdges("NetworkID"+str(currentID))
            network_attr = blockcityin.getAttributes("NetworkID"+str(currentID))
            currentPatchList = patchcityin.getAttributes("PatchDataID"+str(currentID))
            
            #-----------------------------------------------------------------#
            #        DETERMINE WHETHER TO UPDATE CURRENT BLOCK AT ALL         #
            #-----------------------------------------------------------------#
            
            block_status = currentAttList.getAttribute("Status")
            if block_status == 0 or currentAttList.getAttribute("ResTIArea") == 0:
                print "BlockID"+str(currentID)+" is not active in simulation or has no residential area"
                #even if block isn't active at all, attributes from previous module are passed on
                blockcityout.setPoints("BlockID"+str(currentID),plist)
                blockcityout.setFaces("BlockID"+str(currentID),flist)
                blockcityout.setAttributes("BlockID"+str(currentID),currentAttList)
                blockcityout.setPoints("NetworkID"+str(currentID), pnetlist)
                blockcityout.setEdges("NetworkID"+str(currentID), enetlist)
                blockcityout.setAttributes("NetworkID"+str(currentID), network_attr)
                
                patchcityout.setPoints("PatchDataID"+str(currentID), plist)
                patchcityout.setFaces("PatchDataID"+str(currentID),flist)
                patchcityout.setAttributes("PatchDataID"+str(currentID), currentPatchList)
            
                #skips the for loop iteration to the next block, not more needs to be done
                continue
            
            blockcityout.setPoints("BlockID"+str(currentID),plist)
            blockcityout.setFaces("BlockID"+str(currentID),flist)
            blockcityout.setAttributes("BlockID"+str(currentID),currentAttList)
            blockcityout.setPoints("NetworkID"+str(currentID), pnetlist)
            blockcityout.setEdges("NetworkID"+str(currentID), enetlist)
            blockcityout.setAttributes("NetworkID"+str(currentID), network_attr)
            
            patchcityout.setPoints("PatchDataID"+str(currentID), plist)
            patchcityout.setFaces("PatchDataID"+str(currentID),flist)
            patchcityout.setAttributes("PatchDataID"+str(currentID), currentPatchList)
            
            #FOR LOOP END (Repeat for next BlockID)
            
        #Output vector update
        blockcityout.setAttributes("MapAttributes", map_attr)
        design_details.setAttributes("DesignAttributes", des_attr)
    
    ########################################################
    #LINK WITH GUI                                         #
    ########################################################
    
    def createInputDialog(self):
        form = activatetechplacementGUI(self, QApplication.activeWindow())
        form.show()
        return True  