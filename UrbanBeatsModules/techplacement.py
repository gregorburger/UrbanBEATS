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
#import technology as tech
#import techdesign as td
#from techplacementguic import *
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from pydynamind import *
#from pyvibe import *

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

        self.technames = ["ASHP", "AQ", "ASR", "BF", "GR", "GT", "GPT", "IS", "PPL", "PB", "PP", "RT", "SF", "ST", "IRR", "WSUB", "WSUR", "SW", "TPS", "UT", "WWRR", "WT", "WEF"]
        
        
        #---DESIGN CRITERIA INPUTS-----------------------------------------------
        
        #DESIGN RATIONALE SETTINGS
        self.ration_runoff = True                #Design for flood mitigation?
        self.ration_pollute = True               #Design for pollution management?
        self.runoff_pri = 1                      #Priority of flood mitigation?
        self.pollute_pri = 1                     #Priority of pollution management?
        self.ration_harvest = False              #Design for harvesting & reuse? Adds storage-sizing to certain systems
        self.harvest_pri = 1                     #Priority for harvesting & reuse
        self.createParameter( "ration_runoff", BOOL,"")
        self.createParameter( "ration_pollute", BOOL,"")
        self.createParameter( "runoff_pri", DOUBLE,"")
        self.createParameter( "pollute_pri", DOUBLE,"")
        self.createParameter( "ration_harvest",BOOL,"")
        self.createParameter( "harvest_pri",DOUBLE,"")
        
        #WATER MANAGEMENT TARGETS
        self.targets_runoff = 80                 #Runoff reduction target [%]
        self.targets_TSS = 70                      #TSS Load reduction target [%]
        self.targets_TN = 30                       #TN Load reduction target [%]
        self.targets_TP = 30                       #TP Load reduction target [%]
        self.targets_harvest = 50                #required reliability of harvesting systems
        self.runoff_auto = False
        self.TSS_auto = False
        self.TN_auto = False
        self.TP_auto = False
        self.harvest_auto = False
        self.createParameter( "targets_runoff", DOUBLE,"")
        self.createParameter( "targets_TSS", DOUBLE,"")
        self.createParameter( "targets_TN", DOUBLE,"")
        self.createParameter( "targets_TP", DOUBLE,"")
        self.createParameter( "targets_harvest", DOUBLE,"")
        self.createParameter( "runoff_auto", BOOL,"")
        self.createParameter( "TSS_auto", BOOL,"")
        self.createParameter( "TN_auto", BOOL,"")
        self.createParameter( "TP_auto", BOOL,"")
        self.createParameter( "harvest_auto", BOOL,"")
        
        #STRATEGY CUSTOMIZE
        self.strategy_lot_check = True
        self.strategy_street_check = True
        self.strategy_neigh_check = True
        self.strategy_prec_check = True
        self.lot_increment = 4
        self.street_increment = 4
        self.neigh_increment = 4
        self.prec_increment = 4
        self.basin_target_min = 20
        self.basin_target_max = 100
        self.createParameter( "strategy_lot_check", BOOL,"")
        self.createParameter( "strategy_street_check", BOOL,"")
        self.createParameter( "strategy_neigh_check", BOOL,"")
        self.createParameter( "strategy_prec_check", BOOL,"")
        self.createParameter( "lot_increment", DOUBLE,"")
        self.createParameter( "street_increment", DOUBLE,"")
        self.createParameter( "neigh_increment", DOUBLE,"")
        self.createParameter( "prec_increment", DOUBLE,"")
        self.createParameter( "basin_target_min", DOUBLE,"")
        self.createParameter( "basin_target_max", DOUBLE,"")
        
        #ADDITIONAL STRATEGIES
        self.strategy_specific1 = False
        self.strategy_specific2 = False
        self.strategy_specific3 = False
        self.strategy_specific4 = False
        self.strategy_specific5 = False
        self.strategy_specific6 = False
        self.createParameter( "strategy_specific1", BOOL,"")
        self.createParameter( "strategy_specific2", BOOL,"")
        self.createParameter( "strategy_specific3", BOOL,"")
        self.createParameter( "strategy_specific4", BOOL,"")
        self.createParameter( "strategy_specific5", BOOL,"")
        self.createParameter( "strategy_specific6", BOOL,"")
        
        #---RETROFIT CONDITIONS INPUTS------------------------------------------
        self.retrofit_scenario = "N"    #N = Do Nothing, R = With Renewal, F = Forced
        self.renewal_cycle_def = 1      #Defined renewal cycle?
        self.renewal_lot_years = 10         #number of years to apply renewal rate
        self.renewal_street_years = 20      #cycle of years for street-scale renewal
        self.renewal_neigh_years = 40       #cycle of years for neighbourhood-precinct renewal
        self.renewal_lot_perc = 5           #renewal percentage
        self.force_street = 0              #forced renewal on lot?
        self.force_neigh = 0           #forced renewal on street?
        self.force_prec = 0            #forced renewal on neighbourhood and precinct?
        self.createParameter( "retrofit_scenario", STRING,"")
        self.createParameter( "renewal_cycle_def", BOOL,"")
        self.createParameter( "renewal_lot_years", DOUBLE,"")
        self.createParameter( "renewal_street_years", DOUBLE,"")
        self.createParameter( "renewal_neigh_years", DOUBLE,"")
        self.createParameter( "renewal_lot_perc", DOUBLE,"")
        self.createParameter( "force_street", BOOL,"")
        self.createParameter( "force_neigh", BOOL,"")
        self.createParameter( "force_prec", BOOL,"")
        
        self.lot_renew = 0
        self.lot_decom = 0
        self.street_renew = 0
        self.street_decom = 0
        self.neigh_renew = 0
        self.neigh_decom = 0
        self.prec_renew = 0
        self.prec_decom = 0
	self.decom_thresh = 40
        self.renewal_thresh = 30
        self.renewal_alternative = "K"          #if renewal cannot be done, what to do then? K=Keep, D=Decommission
        self.createParameter( "lot_renew", BOOL,"")
        self.createParameter( "lot_decom", BOOL,"")
        self.createParameter( "street_renew", BOOL,"")
        self.createParameter( "street_decom", BOOL,"")
        self.createParameter( "neigh_renew", BOOL,"")
        self.createParameter( "neigh_decom", BOOL,"")
        self.createParameter( "prec_renew", BOOL,"")
        self.createParameter( "prec_decom", BOOL,"")
        self.createParameter( "decom_thresh", DOUBLE,"")
        self.createParameter( "renewal_thresh", DOUBLE,"")
        self.createParameter( "renewal_alternative", STRING,"")
        
        
        #---GENERAL DESIGN CRITERIA---------------------------------------------
        #followed by vibe inputs
        #self.input_parameter = default value
        #self.createParameter( "input_parameter", DOUBLE)
        
        #---ADVANCED STORMWATER HARVESTING PLANT [ASHP]---###TBA###-------------
        self.ASHPstatus = 0
        self.createParameter( "ASHPstatus", BOOL,"")
        self.ASHPlevel = 0
        self.createParameter( "ASHPlevel", DOUBLE,"")
        self.ASHPgroup = 0
        self.createParameter( "ASHPgroup", DOUBLE,"")
        
        #---AQUACULTURE/LIVING SYSTEMS [AQ]---###TBA###-------------------------
        self.AQstatus = 0
        self.createParameter( "AQstatus", BOOL,"")
        self.AQlevel = 0
        self.createParameter( "AQlevel", DOUBLE,"")
        self.AQgroup = 0
        self.createParameter( "AQgroup", DOUBLE,"")
        
        #---AQUIFER STORAGE & RECOVERY SYSTEM [ASR]---###TBA###-----------------
        self.ASRstatus = 0
        self.createParameter( "ASRstatus", BOOL,"")
        self.ASRlevel = 0
        self.createParameter( "ASRlevel", DOUBLE,"")
        self.ASRgroup = 0
        self.createParameter( "ASRgroup", DOUBLE,"")
        
        
        #---BIOFILTRATION SYSTEM/RAINGARDEN [BF]--------------------------------
        self.BFstatus = 1
        self.createParameter( "BFstatus", BOOL,"")
        self.BFlevel = 0
        self.createParameter( "BFlevel", DOUBLE,"")
        self.BFgroup = 0
        self.createParameter( "BFgroup", DOUBLE,"")
        
        #Available Scales
        self.BFlot = True
        self.BFstreet = True
        self.BFneigh = True
        self.BFprec = True
        self.createParameter( "BFlot", BOOL,"")
        self.createParameter( "BFstreet", BOOL,"")
        self.createParameter( "BFneigh", BOOL,"")
        self.createParameter( "BFprec", BOOL,"")
        
        #Available Applications
        self.BFflow = False
	self.BFpollute = True
	self.createParameter( "BFflow", BOOL, "")        
	self.createParameter( "BFpollute", BOOL,"")
        
        #Design Curves
        self.BFdesignUB = True          #use DAnCE4Water's default curves to design system?
        self.BFdescur_path = "no file"  #path for design curve
        self.createParameter( "BFdesignUB", BOOL,"")
        self.createParameter( "BFdescur_path", STRING,"")
        
        #Design Information
        self.BFspec_EDD = 0.3
        self.BFspec_FD = 0.6
        self.createParameter( "BFspec_EDD", DOUBLE,"")
        self.createParameter( "BFspec_FD", DOUBLE,"")
        self.BFmaxsize = 999999         #maximum surface area of system in sqm
        self.createParameter( "BFmaxsize", DOUBLE,"")
	self.BFavglife = 20             #average life span of a biofilter
        self.createParameter("BFavglife", DOUBLE,"")
        

        self.BFlined = True
        self.createParameter( "BFlined", BOOL,"")
        
        
        #---GREEN ROOF [GR]---###TBA###-----------------------------------------
        self.GRstatus = 0
        self.createParameter( "GRstatus", BOOL,"")
        self.GRlevel = 0
        self.createParameter( "GRlevel", DOUBLE,"")
        self.GRgroup = 0
        self.createParameter( "GRgroup", DOUBLE,"")
                
        #---INFILTRATION SYSTEM [IS]--------------------------------------------
        self.ISstatus = 1
        self.createParameter( "ISstatus", BOOL,"")
        self.ISlevel = 0
        self.createParameter( "ISlevel", DOUBLE,"")
        self.ISgroup = 0
        self.createParameter( "ISgroup", DOUBLE,"")
        
        #Available Scales
        self.ISlot = True
        self.ISstreet = True
        self.ISneigh = True
        self.createParameter( "ISlot", BOOL,"")
        self.createParameter( "ISstreet", BOOL,"")
        self.createParameter( "ISneigh", BOOL,"")
        
        #Available Applications
        self.ISflow = True
        self.ISpollute = True
        self.createParameter( "ISflow", BOOL,"")
        self.createParameter( "ISpollute", BOOL,"")
        
        #Design Curves
        self.ISdesignUB = True          #use DAnCE4Water's default curves to design system?
        self.ISdescur_path = "no file"  #path for design curve
        self.createParameter( "ISdesignUB", BOOL,"")
        self.createParameter( "ISdescur_path", STRING,"")
        
        #Design Information
        self.ISspec_EDD = 0.2
        self.ISspec_FD = 0.8
        self.createParameter( "ISspec_EDD", DOUBLE,"")
        self.createParameter( "ISspec_FD", DOUBLE,"")
        self.ISmaxsize = 5000          #maximum surface area of system in sqm
        self.createParameter( "ISmaxsize", DOUBLE,"")
	self.ISavglife = 20             #average life span of an infiltration system
	self.createParameter( "ISavglife", DOUBLE,"")



        self.IS_2Dmodel = True
        self.createParameter( "IS_2Dmodel", BOOL,"")
        
        #---GROSS POLLUTANT TRAP [GPT]------------------------------------------
        self.GPTstatus = 0
        self.createParameter( "GPTstatus", BOOL,"")
        self.GPTlevel = 0
        self.createParameter( "GPTlevel", DOUBLE,"")
        self.GPTgroup = 0
        self.createParameter( "GPTgroup", DOUBLE,"")
        
        #self.input_parameter = default value
        #self.createParameter( "input_parameter", DOUBLE)
        
        #---GREYWATER TREATMENT & DIVERSION SYSTEM [GT]-------------------------
        self.GTstatus = 0
        self.createParameter( "GTstatus", BOOL,"")
        self.GTlevel = 0
        self.createParameter( "GTlevel", DOUBLE,"")
        self.GTgroup = 0
        self.createParameter( "GTgroup", DOUBLE,"")
        
        #followed by vibe inputs
        #self.input_parameter = default value
        #self.addParameter(self , "input_parameter", DOUBLE)
        
        #---PACKAGED PLANT [PPL]---###TBA###------------------------------------
        self.PPLstatus = 0
        self.createParameter( "PPLstatus", BOOL,"")
        self.PPLlevel = 0
        self.createParameter( "PPLlevel", DOUBLE,"")
        self.PPLgroup = 0
        self.createParameter( "PPLgroup", DOUBLE,"")
        
        #---PONDS & SEDIMENTATION BASIN [PB]------------------------------------
        self.PBstatus = 1
        self.createParameter( "PBstatus", BOOL,"")
        self.PBlevel = 0
        self.createParameter( "PBlevel", DOUBLE,"")
        self.PBgroup = 0
        self.createParameter( "PBgroup", DOUBLE,"")
        
        #Available Scales
        self.PBneigh = True
        self.PBprec = True
        self.createParameter( "PBneigh", BOOL,"")
        self.createParameter( "PBprec", BOOL,"")
        
        #Available Applications
        self.PBflow = True
        self.PBpollute = True
        self.createParameter( "PBflow", BOOL,"")
        self.createParameter( "PBpollute", BOOL,"")
        
        #Design Curves
        self.PBdesignUB = True          #use DAnCE4Water's default curves to design system?
        self.PBdescur_path = "no file"  #path for design curve
        self.createParameter( "PBdesignUB", BOOL,"")
        self.createParameter( "PBdescur_path", STRING,"")
        
        #Design Information
        self.PBspec_MD = "1.25" 	#need a string for the combo box
        self.createParameter( "PBspec_MD", STRING,"")
        self.PBmaxsize = 9999999           #maximum surface area of system in sqm
        self.createParameter( "PBmaxsize", DOUBLE,"")
	self.PBavglife = 20             #average life span of a pond/basin
	self.createParameter( "PBavglife", DOUBLE,"")

        
        #---POROUS/PERVIOUS PAVEMENT [PP]---###TBA###---------------------------
        self.PPstatus = 0
        self.createParameter( "PPstatus", BOOL,"")
        self.PPlevel = 0
        self.createParameter( "PPlevel", DOUBLE,"")
        self.PPgroup = 0
        self.createParameter( "PPgroup", DOUBLE,"")
        
        #---RAINWATER TANK [RT]-------------------------------------------------
        self.RTstatus = 0
        self.createParameter( "RTstatus", BOOL,"")
        self.RTlevel = 0
        self.createParameter( "RTlevel", DOUBLE,"")
        self.RTgroup = 0
        self.createParameter( "RTgroup", DOUBLE,"")
        
        self.RTscale_lot = True
        self.RTscale_street = True
        self.RTpurp_flood = True
        self.RTpurp_recyc = False
        self.createParameter( "RTscale_lot", BOOL,"")
        self.createParameter( "RTscale_street", BOOL,"")
        self.createParameter( "RTpurp_flood", BOOL,"")
        self.createParameter( "RTpurp_recyc", BOOL,"")
        
        self.RT_firstflush = 2          #first flush volume [mm]
        self.RT_maxdepth = 2            #max tank depth [m]
        self.RT_mindead = 0.1           #minimum dead storage level [m]
        self.RT_shape_circ = True       #consider circular tanks
        self.RT_shape_rect = True       #consider rectangular tanks
        self.RT_sbmodel = "ybs"         #storage-behaviour model settings
        self.RTdesignD4W = True         #use DAnCE4Water's default curves to design system?
        self.RTdescur_path = "no file"  #path for design curve
        self.createParameter( "RT_firstflush", DOUBLE,"")
        self.createParameter( "RT_maxdepth", DOUBLE,"")
        self.createParameter( "RT_mindead", DOUBLE,"")
        self.createParameter( "RT_shape_circ", BOOL,"")
        self.createParameter( "RT_shape_rect", BOOL,"")
        self.createParameter( "RT_sbmodel", STRING,"")
        self.createParameter( "RTdesignD4W", BOOL,"")
        self.createParameter( "RTdescur_path", STRING,"")
        self.RTavglife = 20             #average life span of a raintank
	self.createParameter( "RTavglife", DOUBLE,"")

        #---SAND/PEAT/GRAVEL FILTER [SF]----------------------------------------
        self.SFstatus = 0
        self.createParameter( "SFstatus", BOOL,"")
        self.SFlevel = 0
        self.createParameter( "SFlevel", DOUBLE,"")
        self.SFgroup = 0
        self.createParameter( "SFgroup", DOUBLE,"")
        
        #---SEPTIC TANK [ST]---###TBA###----------------------------------------
        self.STstatus = 0
        self.createParameter( "STstatus", BOOL,"")
        self.STlevel = 0
        self.createParameter( "STlevel", DOUBLE,"")
        self.STgroup = 0
        self.createParameter( "STgroup", DOUBLE,"")
        
        #---SUBSURFACE IRRIGATION SYSTEM [IRR]---###TBA###----------------------
        self.IRRstatus = 0
        self.createParameter( "IRRstatus", BOOL,"")
        self.IRRlevel = 0
        self.createParameter( "IRRlevel", DOUBLE,"")
        self.IRRgroup = 0
        self.createParameter( "IRRgroup", DOUBLE,"")
        
        #---SUBSURFACE WETLAND/REED BED [WSUB]----------------------------------
        self.WSUBstatus = 0
        self.createParameter( "WSUBstatus", BOOL,"")
        self.WSUBlevel = 0
        self.createParameter( "WSUBlevel", DOUBLE,"")
        self.WSUBgroup = 0
        self.createParameter( "WSUBgroup", DOUBLE,"")
        
        #---SURFACE WETLAND [WSUR]----------------------------------------------
        self.WSURstatus = 1
        self.createParameter( "WSURstatus", BOOL,"")
        self.WSURlevel = 0
        self.createParameter( "WSURlevel", DOUBLE,"")
        self.WSURgroup = 0
        self.createParameter( "WSURgroup", DOUBLE,"")
        
        #Available Scales
        self.WSURneigh = True
        self.WSURprec = True
        self.createParameter( "WSURneigh", BOOL,"")
        self.createParameter( "WSURprec", BOOL,"")
        
        #Available Applications
        self.WSURflow = True
        self.WSURpollute = True
        self.createParameter( "WSURflow", BOOL,"")
        self.createParameter( "WSURpollute", BOOL,"")
        
        #Design Curves
        self.WSURdesignUB = True          #use DAnCE4Water's default curves to design system?
        self.WSURdescur_path = "no file"  #path for design curve
        self.createParameter( "WSURdesignUB", BOOL,"")
        self.createParameter( "WSURdescur_path", STRING,"")
        
        #Design Information
        self.WSURspec_EDD = 0.75
        self.createParameter( "WSURspec_EDD", DOUBLE,"")
        self.WSURmaxsize = 9999999           #maximum surface area of system in sqm
        self.createParameter( "WSURmaxsize", DOUBLE,"")
	self.WSURavglife = 20             #average life span of a wetland
	self.createParameter( "WSURavglife", DOUBLE,"")

        
        #---SWALES & BUFFER STRIPS [SW]-----------------------------------------
        self.SWstatus = 1
        self.createParameter( "SWstatus", BOOL,"")
        self.SWlevel = 0
        self.createParameter( "SWlevel", DOUBLE,"")
        self.SWgroup = 0
        self.createParameter( "SWgroup", DOUBLE,"")
        
        #Available Scales
        self.SWstreet = True
        self.createParameter( "SWstreet", BOOL,"")
        
        #Available Applications
        self.SWflow = True
        self.SWpollute = True
        self.createParameter( "SWflow", BOOL,"")
        self.createParameter( "SWpollute", BOOL,"")
        
        #Design Curves
        self.SWdesignUB = True          #use DAnCE4Water's default curves to design system?
        self.SWdescur_path = "no file"  #path for design curve
        self.createParameter( "SWdesignUB", BOOL,"")
        self.createParameter( "SWdescur_path", STRING,"")
        
        #Design Information
        self.SWspec = 0
        self.createParameter( "SWspec", DOUBLE,"")
        self.SWmaxsize = 9999           #maximum surface area of system in sqm
        self.createParameter( "SWmaxsize", DOUBLE,"")
	self.SWavglife = 20             #average life span of a swale
	self.createParameter( "SWavglife", DOUBLE,"")


        #---TREE PITS [TPS]---###TBA###-----------------------------------------
        self.TPSstatus = 0
        self.createParameter( "TPSstatus", BOOL,"")
        self.TPSlevel = 0
        self.createParameter( "TPSlevel", DOUBLE,"")
        self.TPSgroup = 0
        self.createParameter( "TPSgroup", DOUBLE,"")
        
        
        #---URINE-SEPARATING TOILET [UT]---###TBA###----------------------------
        self.UTstatus = 0
        self.createParameter( "UTstatus", BOOL,"")
        self.UTlevel = 0
        self.createParameter( "UTlevel", DOUBLE,"")
        self.UTgroup = 0
        self.createParameter( "UTgroup", DOUBLE,"")
        
        #---WASTEWATER RECOVERY & RECYCLING PLANT [WWRR]---###TBA###------------
        self.WWRRstatus = 0
        self.createParameter( "WWRRstatus", BOOL,"")
        self.WWRRlevel = 0
        self.createParameter( "WWRRlevel", DOUBLE,"")
        self.WWRRgroup = 0
        self.createParameter( "WWRRgroup", DOUBLE,"")
        
        #---WATERLESS/COMPOSTING TOILETS [WT]---###TBA###-----------------------
        self.WTstatus = 0
        self.createParameter( "WTstatus", BOOL,"")
        self.WTlevel = 0
        self.createParameter( "WTlevel", DOUBLE,"")
        self.WTgroup = 0
        self.createParameter( "WTgroup", DOUBLE,"")
        
        #---WATER EFFICIENT APPLIANCES [WEF]------------------------------------
        self.WEFstatus = 0
        self.createParameter( "WEFstatus", BOOL,"")
        self.WEFlevel = 0
        self.createParameter( "WEFlevel", DOUBLE,"")
        self.WEFgroup = 0
        self.createParameter( "WEFgroup", DOUBLE,"")
        
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
        self.createParameter( "WEF_implement_method", STRING,"")
        self.createParameter( "LEG_force", BOOL,"")
        self.createParameter( "LEG_minrate", DOUBLE,"")
        self.createParameter( "PPP_force", BOOL,"")
        self.createParameter( "PPP_likelihood", DOUBLE,"")
        self.createParameter( "SEC_force", BOOL,"")
        self.createParameter( "SEC_urbansim", BOOL,"")
        self.createParameter( "D4W_UDMactive", BOOL,"")
        self.createParameter( "D4W_STMactive", BOOL,"")
        self.createParameter( "D4W_EVMactive", BOOL,"")
        
        self.WEF_rating_system = "AS"
        self.WEF_loc_famhouse = True
        self.WEF_loc_apart = True
        self.WEF_loc_nonres = True
        self.WEF_flow_method = "M"
        self.createParameter( "WEF_rating_system", STRING,"")
        self.createParameter( "WEF_loc_famhouse", BOOL,"")
        self.createParameter( "WEF_loc_apart", BOOL,"")
        self.createParameter( "WEF_loc_nonres", BOOL,"")
        self.createParameter( "WEF_flow_method", STRING,"")
        
        #---<Add a new system - Name> [abbrev.]---------------------------------
        #self.<abbrev>status = 1
        #self.addParameter(self , "<abbrev>status", BOOL)
        #followed by vibe inputs
        #self.input_parameter = default value
        #self.addParameter(self , "input_parameter", DOUBLE)
        
        #---REGIONAL INFORMATION -----------------------------------------------
        self.regioncity = "Melbourne"
        self.createParameter( "regioncity", STRING,"")
        
        
        #---MULTI-CRITERIA INPUTS-----------------------------------------------
        #SELECT EVALUATION METRICS
        self.scoringmatrix_path = "DaywaterMCA.csv"
        self.scoringmatrix_default = False
        self.scoring_include_all = True
        self.createParameter( "scoringmatrix_path", STRING,"")
        self.createParameter( "scoringmatrix_default", BOOL,"")
        self.createParameter( "scoring_include_all", BOOL,"")
        
        #CUSTOMIZE EVALUATION CRITERIA
        self.bottomlines_tech = True   #Include criteria? Yes/No
        self.bottomlines_env = True
        self.bottomlines_ecn = True
        self.bottomlines_soc = True
        self.bottomlines_tech_n = 4     #Metric numbers
        self.bottomlines_env_n = 5
        self.bottomlines_ecn_n = 2
        self.bottomlines_soc_n = 4
        
        self.eval_mode = "W"            #Evaluation Mode: W = Single weightings, P = Pareto Exploration (refer to parameter suffix)
        self.bottomlines_tech_p = 0     #Pareto Exploration increments
        self.bottomlines_env_p = 0
        self.bottomlines_ecn_p = 0
        self.bottomlines_soc_p = 0
        self.bottomlines_tech_w = 1     #Single weighting weights
        self.bottomlines_env_w = 1
        self.bottomlines_ecn_w = 1
        self.bottomlines_soc_w = 1
        self.createParameter( "bottomlines_tech", BOOL,"")
        self.createParameter( "bottomlines_env", BOOL,"")
        self.createParameter( "bottomlines_ecn",BOOL,"")
        self.createParameter( "bottomlines_soc", BOOL,"")
        self.createParameter( "bottomlines_tech_n", DOUBLE,"")
        self.createParameter( "bottomlines_env_n", DOUBLE,"")
        self.createParameter( "bottomlines_ecn_n", DOUBLE,"")
        self.createParameter( "bottomlines_soc_n", DOUBLE,"")
        self.createParameter( "eval_mode", STRING,"")
        self.createParameter( "bottomlines_tech_p", DOUBLE,"")
        self.createParameter( "bottomlines_env_p", DOUBLE,"")
        self.createParameter( "bottomlines_ecn_p", DOUBLE,"")
        self.createParameter( "bottomlines_soc_p", DOUBLE,"")
        self.createParameter( "bottomlines_tech_w", DOUBLE,"")
        self.createParameter( "bottomlines_env_w", DOUBLE,"")
        self.createParameter( "bottomlines_ecn_w", DOUBLE,"")
        self.createParameter( "bottomlines_soc_w", DOUBLE,"")
        
        #SCORING OF STRATEGIES
        self.scope_stoch = False
        self.score_method = "AHP"       #MCA scoring method
        self.tech2strat_method = "EqW"  #How to merge technology scores into strategy score
        self.createParameter( "scope_stoch", BOOL,"")
        self.createParameter( "score_method", STRING,"")
        self.createParameter( "tech2strat_method", STRING,"")
        
        #RANKING OF STRATEGIES
        self.ranktype = "RK"            #CI = Confidence Interval, RK = ranking
        self.topranklimit = 10
        self.conf_int = 95
        self.ingroup_scoring = "Avg"
        self.createParameter( "ranktype", STRING,"")
        self.createParameter( "topranklimit", DOUBLE,"")
        self.createParameter( "conf_int", DOUBLE,"")
        self.createParameter( "ingroup_scoring", STRING,"")
        

	#Views
	self.blocks = View("Block", FACE,WRITE)
	self.blocks.getAttribute("Status")
	self.blocks.getAttribute("ResTIArea")
	self.blocks.addAttribute("HasLotS")
	self.blocks.addAttribute("HasNeighS")
	self.blocks.addAttribute("HasStreetS")
	self.blocks.addAttribute("HasPrecS")
	self.blocks.addAttribute("MaxLotDeg")
	self.blocks.addAttribute("IAServiced")
	self.blocks.addAttribute("IADeficit")
	self.blocks.addAttribute("UpstrImpTreat")

	self.mapattributes = View("Mapattributes", COMPONENT,READ)
	self.mapattributes.getAttribute("NumBlocks")
	self.mapattributes.getAttribute("WidthBlocks")
	self.mapattributes.getAttribute("HeightBlocks")
	self.mapattributes.getAttribute("InputReso")
	self.mapattributes.getAttribute("TotalBasins")

	self.desAttr = View("DesAttr", COMPONENT,WRITE)
	self.desAttr.addAttribute("ration_runoff")
        self.desAttr.addAttribute("ration_pollute")
        self.desAttr.addAttribute("runoff_pri")
        self.desAttr.addAttribute("pollute_pri")
        self.desAttr.addAttribute("targets_runoff")
        self.desAttr.addAttribute("targets_TSS")
        self.desAttr.addAttribute("targets_TN")
        self.desAttr.addAttribute("targets_TP")
        self.desAttr.addAttribute("runoff_auto")
        self.desAttr.addAttribute("TSS_auto")
        self.desAttr.addAttribute("TN_auto")
        self.desAttr.addAttribute("TP_auto")
        self.desAttr.addAttribute("strategy_lot_check")
        self.desAttr.addAttribute("strategy_street_check")
        self.desAttr.addAttribute("strategy_neigh_check")
        self.desAttr.addAttribute("strategy_prec_check")
        self.desAttr.addAttribute("lot_increment")
        self.desAttr.addAttribute("street_increment")
        self.desAttr.addAttribute("neigh_increment")
        self.desAttr.addAttribute("prec_increment")
        self.desAttr.addAttribute("basin_target_min")
        self.desAttr.addAttribute("basin_target_max")
        self.desAttr.addAttribute("strategy_specific1")
        self.desAttr.addAttribute("strategy_specific2")
        self.desAttr.addAttribute("strategy_specific3")
        self.desAttr.addAttribute("strategy_specific4")
        self.desAttr.addAttribute("strategy_specific5")
        self.desAttr.addAttribute("strategy_specific6")
	self.desAttr.addAttribute("Status_ASHP")   
        self.desAttr.addAttribute("ASHPlevel")                              
        self.desAttr.addAttribute("Status_AQ") 
        self.desAttr.addAttribute("AQlevel")        
        self.desAttr.addAttribute("Status_ASR")
        self.desAttr.addAttribute("ASRlevel")
        self.desAttr.addAttribute("Status_BF")
        self.desAttr.addAttribute("BFlevel")
        self.desAttr.addAttribute("BFlot")
        self.desAttr.addAttribute("BFstreet")
        self.desAttr.addAttribute("BFneigh")
        self.desAttr.addAttribute("BFprec")
	self.desAttr.addAttribute("BFflow")        
	self.desAttr.addAttribute("BFpollute")
        self.desAttr.addAttribute("BFdesignUB")
        self.desAttr.addAttribute("BFdescur_path")
        self.desAttr.addAttribute("BFspec_EDD")
        self.desAttr.addAttribute("BFspec_FD")
        self.desAttr.addAttribute("BFmaxsize")
        self.desAttr.addAttribute("BFlined")
	self.desAttr.addAttribute("BFavglife")     
        self.desAttr.addAttribute("Status_GR")
        self.desAttr.addAttribute("GRlevel")     
        self.desAttr.addAttribute("Status_GT")
        self.desAttr.addAttribute("GTlevel")
        self.desAttr.addAttribute("Status_GPT")
        self.desAttr.addAttribute("GPTlevel")
        self.desAttr.addAttribute("Status_IS")
        self.desAttr.addAttribute("ISlevel")
        self.desAttr.addAttribute("ISlot")
        self.desAttr.addAttribute("ISstreet")
        self.desAttr.addAttribute("ISneigh")
        self.desAttr.addAttribute("ISflow")
        self.desAttr.addAttribute("ISpollute")
        self.desAttr.addAttribute("ISdesignUB")
        self.desAttr.addAttribute("ISdescur_path")
        self.desAttr.addAttribute("ISspec_EDD")
        self.desAttr.addAttribute("ISspec_FD")
        self.desAttr.addAttribute("ISmaxsize")
        self.desAttr.addAttribute("IS_2Dmodel")
	self.desAttr.addAttribute("ISavglife")     
        self.desAttr.addAttribute("Status_PPL")    
        self.desAttr.addAttribute("PPLlevel")
        self.desAttr.addAttribute("Status_PB")      
        self.desAttr.addAttribute("PBlevel")
        self.desAttr.addAttribute("PBneigh")
        self.desAttr.addAttribute("PBprec")
        self.desAttr.addAttribute("PBflow")
        self.desAttr.addAttribute("PBpollute")
        self.desAttr.addAttribute("PBdesignUB")
        self.desAttr.addAttribute("PBdescur_path")
        self.desAttr.addAttribute("PBspec_MD")
        self.desAttr.addAttribute("PBmaxsize")
	self.desAttr.addAttribute("PBavglife")
        self.desAttr.addAttribute("Status_PP")    
        self.desAttr.addAttribute("PPlevel")       
        self.desAttr.addAttribute("Status_RT")    
        self.desAttr.addAttribute("RTlevel")    
        self.desAttr.addAttribute("Status_SF")    
        self.desAttr.addAttribute("SFlevel")    
        self.desAttr.addAttribute("Status_ST")       
        self.desAttr.addAttribute("STlevel")   
        self.desAttr.addAttribute("Status_IRR")     
        self.desAttr.addAttribute("IRRlevel")
        self.desAttr.addAttribute("Status_WSUB")   
        self.desAttr.addAttribute("WSUBlevel")
        self.desAttr.addAttribute("Status_WSUR")   
        self.desAttr.addAttribute("WSURlevel")
        self.desAttr.addAttribute("WSURneigh")
        self.desAttr.addAttribute("WSURprec")
        self.desAttr.addAttribute("WSURflow")
        self.desAttr.addAttribute("WSURpollute")
        self.desAttr.addAttribute("WSURdesignUB")
        self.desAttr.addAttribute("WSURdescur_path")
        self.desAttr.addAttribute("WSURspec_EDD")
        self.desAttr.addAttribute("WSURmaxsize")
	self.desAttr.addAttribute("WSURavglife")
        self.desAttr.addAttribute("Status_SW")       
        self.desAttr.addAttribute("SWlevel")
        self.desAttr.addAttribute("SWstreet")
        self.desAttr.addAttribute("SWflow")
        self.desAttr.addAttribute("SWpollute")
        self.desAttr.addAttribute("SWdesignUB")
        self.desAttr.addAttribute("SWdescur_path")
        self.desAttr.addAttribute("SWspec")
        self.desAttr.addAttribute("SWmaxsize")
	self.desAttr.addAttribute("SWavglife")
        self.desAttr.addAttribute("Status_TPS") 
        self.desAttr.addAttribute("TPSlevel")
        self.desAttr.addAttribute("Status_UT")   
        self.desAttr.addAttribute("UTlevel")
        self.desAttr.addAttribute("Status_WWRR")
        self.desAttr.addAttribute("WWRRlevel")
        self.desAttr.addAttribute("Status_WT") 
        self.desAttr.addAttribute("WTlevel")
        self.desAttr.addAttribute("Status_WEF")
        self.desAttr.addAttribute("WEFlevel")
        self.desAttr.addAttribute("regioncity")
        self.desAttr.addAttribute("scoringmatrix_path")
        self.desAttr.addAttribute("scoringmatrix_default")
        self.desAttr.addAttribute("scoring_include_all")
        self.desAttr.addAttribute("eval_mode")
        self.desAttr.addAttribute("bottomlines_tech_p")
        self.desAttr.addAttribute("bottomlines_env_p")
        self.desAttr.addAttribute("bottomlines_ecn_p")
        self.desAttr.addAttribute("bottomlines_soc_p")
        self.desAttr.addAttribute("bottomlines_tech")
        self.desAttr.addAttribute("bottomlines_env")
        self.desAttr.addAttribute("bottomlines_ecn")
        self.desAttr.addAttribute("bottomlines_soc")
        self.desAttr.addAttribute("bottomlines_tech_n")
        self.desAttr.addAttribute("bottomlines_env_n")
        self.desAttr.addAttribute("bottomlines_ecn_n")
        self.desAttr.addAttribute("bottomlines_soc_n")
        self.desAttr.addAttribute("bottomlines_tech_w")
        self.desAttr.addAttribute("bottomlines_env_w")
        self.desAttr.addAttribute("bottomlines_ecn_w")
        self.desAttr.addAttribute("bottomlines_soc_w")
        self.desAttr.addAttribute("scope_stoch")
        self.desAttr.addAttribute("score_method")
        self.desAttr.addAttribute("tech2strat_method")
        self.desAttr.addAttribute("ranktype")
        self.desAttr.addAttribute("topranklimit")
        self.desAttr.addAttribute("conf_int")
        self.desAttr.addAttribute("ingroup_scoring")
        self.desAttr.addAttribute("techcheckedlot")
        self.desAttr.addAttribute("techcheckedstreet")
        self.desAttr.addAttribute("techcheckedneigh")
        self.desAttr.addAttribute("techcheckedprec")

	#Datastream
	datastream = []
	datastream.append(self.desAttr)
	datastream.append(self.mapattributes)
	datastream.append(self.blocks)
	self.addData("City", datastream)
	self.BLOCKIDtoUUID = {}

    def getBlockUUID(self, blockid,city):
	try:
		key = self.BLOCKIDtoUUID[blockid]
	except KeyError:
		key = ""
	return city.getFace(key)


    def initBLOCKIDtoUUID(self, city):
	blockuuids = city.getUUIDsOfComponentsInView(self.blocks)
        for blockuuid in blockuuids:
            block = city.getFace(blockuuid)
            ID = int(round(block.getAttribute("BlockID").getDouble()))
	    self.BLOCKIDtoUUID[ID] = blockuuid

	
    
    def run(self):
	homeDir = os.environ['HOME']
	dcvdirectory = homeDir + '/Documents/UrbanBEATS/UrbanBeatsModules/wsuddcurves/'
	print dcvdirectory
	#dcvdirectory = "C:\\Users\\Peter M Bach\\Documents\\UrbanBEATS Development\\__urbanBEATS\\wsuddcurves\\"
	city = self.getData("City")
	self.initBLOCKIDtoUUID(city)

	strvec = city.getUUIDsOfComponentsInView(self.mapattributes)
        map_attr = city.getComponent(strvec[0])
        
        
        #get data needed to being for loop analysis
        blocks_num = map_attr.getAttribute("NumBlocks").getDouble()     #number of blocks to loop through
        blocks_size = map_attr.getAttribute("BlockSize").getDouble()    #size of block
        map_w = map_attr.getAttribute("WidthBlocks").getDouble()        #num of blocks wide
        map_h = map_attr.getAttribute("HeightBlocks").getDouble()       #num of blocks tall
        input_res = map_attr.getAttribute("InputReso").getDouble()      #resolution of input data
        
        basins = map_attr.getAttribute("TotalBasins").getDouble()
        
        #--------------------------------------------------------------------------------#
        #       TRANSFER ALL DESIGN CRITERIA AND STRATEGY SETUP INPUTS TO DES_ATTR       #
        #--------------------------------------------------------------------------------#
        #write all technologies checked/unchecked statuses to output vector attribute list
        des_attr = Component()                              #technology status are saved to this attribute list
        city.addComponent(des_attr, self.desAttr)
        des_attr.addAttribute("ration_runoff", self.ration_runoff)
        des_attr.addAttribute("ration_pollute", self.ration_pollute)
        des_attr.addAttribute("runoff_pri", self.runoff_pri)
        des_attr.addAttribute("pollute_pri", self.pollute_pri)
        des_attr.addAttribute("targets_runoff", self.targets_runoff)
        des_attr.addAttribute("targets_TSS", self.targets_TSS)
        des_attr.addAttribute("targets_TN", self.targets_TN)
        des_attr.addAttribute("targets_TP", self.targets_TP)
        des_attr.addAttribute("runoff_auto", self.runoff_auto)
        des_attr.addAttribute("TSS_auto", self.TSS_auto)
        des_attr.addAttribute("TN_auto", self.TN_auto)
        des_attr.addAttribute("TP_auto", self.TP_auto)
        des_attr.addAttribute("strategy_lot_check", self.strategy_lot_check)
        des_attr.addAttribute("strategy_street_check", self.strategy_street_check)
        des_attr.addAttribute("strategy_neigh_check", self.strategy_neigh_check)
        des_attr.addAttribute("strategy_prec_check", self.strategy_prec_check)
        des_attr.addAttribute("lot_increment", self.lot_increment)
        des_attr.addAttribute("street_increment", self.street_increment)
        des_attr.addAttribute("neigh_increment", self.neigh_increment)
        des_attr.addAttribute("prec_increment", self.prec_increment)
        des_attr.addAttribute("basin_target_min", self.basin_target_min)
        des_attr.addAttribute("basin_target_max", self.basin_target_max)
        des_attr.addAttribute("strategy_specific1", self.strategy_specific1)
        des_attr.addAttribute("strategy_specific2", self.strategy_specific2)
        des_attr.addAttribute("strategy_specific3", self.strategy_specific3)
        des_attr.addAttribute("strategy_specific4", self.strategy_specific4)
        des_attr.addAttribute("strategy_specific5", self.strategy_specific5)
        des_attr.addAttribute("strategy_specific6", self.strategy_specific6)
        


	#--------------------------------------------------------------------------------#
        #       TRANSFER ALL RETROFIT INPUTS TO TO DES_ATTR                            #
        #--------------------------------------------------------------------------------#
        des_attr.addAttribute("retrofit_scenario", self.retrofit_scenario)
        des_attr.addAttribute("renewal_cycle_def", self.renewal_cycle_def)
        des_attr.addAttribute("renewal_lot_years", self.renewal_lot_years)
        des_attr.addAttribute("renewal_street_years", self.renewal_street_years)
        des_attr.addAttribute("renewal_neigh_years", self.renewal_neigh_years)
        des_attr.addAttribute("renewal_lot_perc", self.renewal_lot_perc)
        des_attr.addAttribute("force_street", self.force_street)
        des_attr.addAttribute("force_neigh", self.force_neigh)
        des_attr.addAttribute("force_prec", self.force_prec)
        des_attr.addAttribute("lot_renew", self.lot_renew)
        des_attr.addAttribute("lot_decom", self.lot_decom)
        des_attr.addAttribute("street_renew", self.street_renew)
        des_attr.addAttribute("street_decom", self.street_decom)
        des_attr.addAttribute("neigh_renew", self.neigh_renew)
        des_attr.addAttribute("neigh_decom", self.neigh_decom)
        des_attr.addAttribute("prec_renew", self.prec_renew)
        des_attr.addAttribute("prec_decom", self.prec_decom)
        des_attr.addAttribute("decom_thresh", self.decom_thresh)
        des_attr.addAttribute("renewal_thresh", self.renewal_thresh)
        des_attr.addAttribute("renewal_alternative", self.renewal_alternative)


        #--------------------------------------------------------------------------------#
        #       TRANSFER ALL TECHNOLOGY STATUSES TO DES_ATTR                             #
        #--------------------------------------------------------------------------------#
        
        des_attr.addAttribute("Status_ASHP", self.ASHPstatus)   #ADVANCED STORMWATERHARVESTING PLANT
        des_attr.addAttribute("ASHPlevel", self.ASHPlevel)
        #des_attr.addAttribute("ASHPgroup", self.ASHPgroup)
                              
        des_attr.addAttribute("Status_AQ", self.AQstatus)       #AQUACULTURE
        des_attr.addAttribute("AQlevel", self.AQlevel)
        #des_attr.addAttribute("AQgroup", self.AQgroup)
        
        des_attr.addAttribute("Status_ASR", self.ASRstatus)     #AQUIFER STORAGE & RECOVERY SYSTEM
        des_attr.addAttribute("ASRlevel", self.ASRlevel)
        #des_attr.addAttribute("ASRgroup", self.ASRgroup)
        
        #====================---------------------------------------------------------------
        des_attr.addAttribute("Status_BF", self.BFstatus)       #BIOFILTRATION SYSTEM
        des_attr.addAttribute("BFlevel", self.BFlevel)
        #des_attr.addAttribute("BFgroup", self.BFgroup)
        des_attr.addAttribute("BFlot", self.BFlot)
        des_attr.addAttribute("BFstreet", self.BFstreet)
        des_attr.addAttribute("BFneigh", self.BFneigh)
        des_attr.addAttribute("BFprec", self.BFprec)
        des_attr.addAttribute("BFflow", self.BFflow)
	des_attr.addAttribute("BFpollute", self.BFpollute)
        des_attr.addAttribute("BFspec_EDD", self.BFspec_EDD)
        des_attr.addAttribute("BFspec_FD", self.BFspec_FD)
        des_attr.addAttribute("BFmaxsize", self.BFmaxsize)
        des_attr.addAttribute("BFlined", self.BFlined)
	des_attr.addAttribute("BFavglife", self.BFavglife)

	#Designcurve
        #str(dcvdirectory)+BF-EDDx.xm-FDx.xm-DC.dcv
        BFdcvpath = str(dcvdirectory)+"BF-EDD"+str(self.BFspec_EDD)+"m-FD"+str(self.BFspec_FD)+"m-DC.dcv"
        print BFdcvpath
        des_attr.addAttribute("BFdesignUB", self.BFdesignUB)
        if self.BFdesignUB == True:
            des_attr.addAttribute("BFdescur_path", BFdcvpath)
        else:
            des_attr.addAttribute("BFdescur_path", self.BFdescur_path)
        #====================---------------------------------------------------------------
        
        des_attr.addAttribute("Status_GR", self.GRstatus)       #GREEN ROOF
        des_attr.addAttribute("GRlevel", self.GRlevel)
        #des_attr.addAttribute("GRgroup", self.GRgroup)
        
        des_attr.addAttribute("Status_GT", self.GTstatus)       #GREYWATER TANK
        des_attr.addAttribute("GTlevel", self.GTlevel)
        #des_attr.addAttribute("GTgroup", self.GTgroup)
        
        des_attr.addAttribute("Status_GPT", self.GPTstatus)     #GROSS POLLUTANT TRAP
        des_attr.addAttribute("GPTlevel", self.GPTlevel)
        #des_attr.addAttribute("GPTgroup", self.GPTgroup)
        
        #====================---------------------------------------------------------------
        des_attr.addAttribute("Status_IS", self.ISstatus)       #INFILTRATION SYSTEM
        des_attr.addAttribute("ISlevel", self.ISlevel)
        #des_attr.addAttribute("ISgroup", self.ISgroup)
        des_attr.addAttribute("ISlot", self.ISlot)
        des_attr.addAttribute("ISstreet", self.ISstreet)
        des_attr.addAttribute("ISneigh", self.ISneigh)
        des_attr.addAttribute("ISflow", self.ISflow)
        des_attr.addAttribute("ISpollute", self.ISpollute)
        des_attr.addAttribute("ISspec_EDD", self.ISspec_EDD)
        des_attr.addAttribute("ISspec_FD", self.ISspec_FD)
        des_attr.addAttribute("ISmaxsize", self.ISmaxsize)
        des_attr.addAttribute("IS_2Dmodel", self.IS_2Dmodel)
	des_attr.addAttribute("ISavglife", self.ISavglife)

        ISdcvpath = str(dcvdirectory)+"IS-EDD"+str(self.BFspec_EDD)+"m-FD"+str(self.BFspec_FD)+"m-DC.dcv"
        print ISdcvpath
        des_attr.addAttribute("ISdesignUB", self.ISdesignUB)
        if self.ISdesignUB == True:
            des_attr.addAttribute("ISdescur_path", ISdcvpath)
        else:
            des_attr.addAttribute("ISdescur_path", self.ISdescur_path)

        #====================---------------------------------------------------------------
        
        des_attr.addAttribute("Status_PPL", self.PPLstatus)     #PACKAGED PLANT
        des_attr.addAttribute("PPLlevel", self.PPLlevel)
        #des_attr.addAttribute("PPLgroup", self.PPLgroup)
        
        #====================---------------------------------------------------------------
        des_attr.addAttribute("Status_PB", self.PBstatus)       #PONDS & BASINS
        des_attr.addAttribute("PBlevel", self.PBlevel)
        #des_attr.addAttribute("PBgroup", self.PBgroup)
        des_attr.addAttribute("PBneigh", self.PBneigh)
        des_attr.addAttribute("PBprec", self.PBprec)
        des_attr.addAttribute("PBflow", self.PBflow)
        des_attr.addAttribute("PBpollute", self.PBpollute)
        des_attr.addAttribute("PBspec_MD", self.PBspec_MD)
        des_attr.addAttribute("PBmaxsize", self.PBmaxsize)
	des_attr.addAttribute("PBavglife", self.PBavglife)

        PBdcvpath = str(dcvdirectory)+"PB-MD"+str(self.PBspec_MD)+"m-DC.dcv"
        print PBdcvpath
        des_attr.addAttribute("PBdesignUB", self.PBdesignUB)
        if self.PBdesignUB == True:
            des_attr.addAttribute("PBdescur_path", PBdcvpath)
        else:
            des_attr.addAttribute("PBdescur_path", self.PBdescur_path)

        #====================---------------------------------------------------------------
        
        des_attr.addAttribute("Status_PP", self.PPstatus)       #POROUS PAVEMENTS
        des_attr.addAttribute("PPlevel", self.PPlevel)
        #des_attr.addAttribute("PPgroup", self.PPgroup)
        
        des_attr.addAttribute("Status_RT", self.RTstatus)       #RAINTANKS
        des_attr.addAttribute("RTlevel", self.RTlevel)
        #des_attr.addAttribute("RTgroup", self.RTgroup)
        
        des_attr.addAttribute("Status_SF", self.SFstatus)       #SAND/PEAT/GRAVEL FILTERS
        des_attr.addAttribute("SFlevel", self.SFlevel)
        #des_attr.addAttribute("SFgroup", self.SFgroup)
        
        des_attr.addAttribute("Status_ST", self.STstatus)       #SEPTIC TANKS
        des_attr.addAttribute("STlevel", self.STlevel)
        #des_attr.addAttribute("STgroup", self.STgroup)
        
        des_attr.addAttribute("Status_IRR", self.IRRstatus)     #SUBSURFACE IRRIGATION SYSTEM
        des_attr.addAttribute("IRRlevel", self.IRRlevel)
        #des_attr.addAttribute("IRRgroup", self.IRRgroup)
        
        des_attr.addAttribute("Status_WSUB", self.WSUBstatus)   #SUBSURFACE WETLAND
        des_attr.addAttribute("WSUBlevel", self.WSUBlevel)
        #des_attr.addAttribute("WSUBgroup", self.WSUBgroup)
        
        #====================---------------------------------------------------------------
        des_attr.addAttribute("Status_WSUR", self.WSURstatus)   #SURFACE WETLAND
        des_attr.addAttribute("WSURlevel", self.WSURlevel)
        #des_attr.addAttribute("WSURgroup", self.WSURgroup)
        des_attr.addAttribute("WSURneigh", self.WSURneigh)
        des_attr.addAttribute("WSURprec", self.WSURprec)
        des_attr.addAttribute("WSURflow", self.WSURflow)
        des_attr.addAttribute("WSURpollute", self.WSURpollute)
        des_attr.addAttribute("WSURspec_EDD", self.WSURspec_EDD)
        des_attr.addAttribute("WSURmaxsize", self.WSURmaxsize)
	des_attr.addAttribute("WSURavglife", self.WSURavglife)

        WSURdcvpath = str(dcvdirectory)+"WSUR-EDD"+str(self.WSURspec_EDD)+"m-DC.dcv"
        print WSURdcvpath
        des_attr.addAttribute("WSURdesignUB", self.WSURdesignUB)
        if self.WSURdesignUB == True:
            des_attr.addAttribute("WSURdescur_path", WSURdcvpath)
        else:
            des_attr.addAttribute("WSURdescur_path", self.WSURdescur_path)

        #====================---------------------------------------------------------------
        des_attr.addAttribute("Status_SW", self.SWstatus)       #SWALES & BUFFER STRIPS
        des_attr.addAttribute("SWlevel", self.SWlevel)
        #des_attr.addAttribute("SWgroup", self.SWgroup)
        des_attr.addAttribute("SWstreet", self.SWstreet)
        des_attr.addAttribute("SWflow", self.SWflow)
        des_attr.addAttribute("SWpollute", self.SWpollute)
        des_attr.addAttribute("SWdesignUB", self.SWdesignUB)
        des_attr.addAttribute("SWdescur_path", self.SWdescur_path)
        des_attr.addAttribute("SWspec", self.SWspec)
        des_attr.addAttribute("SWmaxsize", self.SWmaxsize)
	des_attr.addAttribute("SWavglife", self.SWavglife)

	#Design curves coming soon

	
        #====================---------------------------------------------------------------
        des_attr.addAttribute("Status_TPS", self.TPSstatus)     #TREE PITS
        des_attr.addAttribute("TPSlevel", self.TPSlevel)
        #des_attr.addAttribute("TPSgroup", self.TPSgroup)
        
        des_attr.addAttribute("Status_UT", self.UTstatus)       #URINE-SEPARATING TOILETS
        des_attr.addAttribute("UTlevel", self.UTlevel)
        #des_attr.addAttribute("UTgroup", self.UTgroup)
        
        des_attr.addAttribute("Status_WWRR", self.WWRRstatus)   #WASTEWATER RECOVERY & RECYCLING PLANT
        des_attr.addAttribute("WWRRlevel", self.WWRRlevel)
        #des_attr.addAttribute("WWRRgroup", self.WWRRgroup)
        
        des_attr.addAttribute("Status_WT", self.WTstatus)       #WATERLESS TOILETS
        des_attr.addAttribute("WTlevel", self.WTlevel)
        #des_attr.addAttribute("WTgroup", self.WTgroup)
        
        des_attr.addAttribute("Status_WEF", self.WEFstatus)     #WATER EFFICIENT APPLIANCES
        des_attr.addAttribute("WEFlevel", self.WEFlevel)
        #des_attr.addAttribute("WEFgroup", self.WEFgroup)
        
        #GET REGIONAL INPUTS
        des_attr.addAttribute("regioncity", self.regioncity)
        
        #--------------------------------------------------------------------------------#
        #       TRANSFER ALL EVALUATION INPUTS TO TO DES_ATTR                            #
        #--------------------------------------------------------------------------------#
        des_attr.addAttribute("scoringmatrix_path", self.scoringmatrix_path)
        des_attr.addAttribute("scoringmatrix_default", self.scoringmatrix_default)
        des_attr.addAttribute("scoring_include_all", self.scoring_include_all)
        
        des_attr.addAttribute("eval_mode", self.eval_mode)
        des_attr.addAttribute("bottomlines_tech_p", self.bottomlines_tech_p)
        des_attr.addAttribute("bottomlines_env_p", self.bottomlines_env_p)
        des_attr.addAttribute("bottomlines_ecn_p", self.bottomlines_ecn_p)
        des_attr.addAttribute("bottomlines_soc_p", self.bottomlines_soc_p)
        
        des_attr.addAttribute("bottomlines_tech", self.bottomlines_tech)
        des_attr.addAttribute("bottomlines_env", self.bottomlines_env)
        des_attr.addAttribute("bottomlines_ecn", self.bottomlines_ecn)
        des_attr.addAttribute("bottomlines_soc", self.bottomlines_soc)
        des_attr.addAttribute("bottomlines_tech_n", self.bottomlines_tech_n)
        des_attr.addAttribute("bottomlines_env_n", self.bottomlines_env_n)
        des_attr.addAttribute("bottomlines_ecn_n", self.bottomlines_ecn_n)
        des_attr.addAttribute("bottomlines_soc_n", self.bottomlines_soc_n)
        des_attr.addAttribute("bottomlines_tech_w", self.bottomlines_tech_w)
        des_attr.addAttribute("bottomlines_env_w", self.bottomlines_env_w)
        des_attr.addAttribute("bottomlines_ecn_w", self.bottomlines_ecn_w)
        des_attr.addAttribute("bottomlines_soc_w", self.bottomlines_soc_w)
        
        des_attr.addAttribute("scope_stoch", self.scope_stoch)
        des_attr.addAttribute("score_method", self.score_method)
        des_attr.addAttribute("tech2strat_method", self.tech2strat_method)
        
        des_attr.addAttribute("ranktype", self.ranktype)
        des_attr.addAttribute("topranklimit", self.topranklimit)
        des_attr.addAttribute("conf_int", self.conf_int)
        des_attr.addAttribute("ingroup_scoring", self.ingroup_scoring)
        
        
        #create technology list - THIS IS THE USER'S CUSTOMISED SHORTLIST
        techchecked = []                #holds the active technologies selected by user for simulation
        for j in self.technames:        #sifts through all tech names to pick out the right ones
            if int(des_attr.getAttribute("Status_"+j).getDouble()) == 1:  ####'!!!!!!!!
                techchecked.append(j)
            else:
                pass
        
        #create technology list for scales
        techcheckedlot = ""
        techcheckedstreet = ""
        techcheckedneigh = ""
        techcheckedprec = ""
        
        for j in techchecked:
            if int(des_attr.getAttribute(str(j)+"lot").getDouble()) == 1:
                techcheckedlot += str(j) + ","
            if int(des_attr.getAttribute(str(j)+"street").getDouble()) == 1:
                techcheckedstreet += str(j) + ","
            if int(des_attr.getAttribute(str(j)+"neigh").getDouble()) == 1:
                techcheckedneigh += str(j) + ","
            if int(des_attr.getAttribute(str(j)+"prec").getDouble()) == 1:
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
        
        des_attr.addAttribute("techcheckedlot", str(techcheckedlot))
        des_attr.addAttribute("techcheckedstreet", str(techcheckedstreet))
        des_attr.addAttribute("techcheckedneigh", str(techcheckedneigh))
        des_attr.addAttribute("techcheckedprec", str(techcheckedprec))
        
#        #work out combinations
#        combos = []
#        for i in range(len(lot_increment)):
#            for j in range(len(street_increment)):
#                for k in range(len(neigh_increment)):
#                    if street_increment[j] + neigh_increment[k] <= 1:
#                        combos.append([lot_increment[i],street_increment[j],neigh_increment[k]])
#                    else:
#                        pass
        
        for i in range(int(blocks_num)):
            currentID = i + 1
            currentAttList = self.getBlockUUID(currentID,city)        #attribute list of current block structure
            #plist = blockcityin.getPoints("BlockID"+str(currentID))
            #flist = blockcityin.getFaces("BlockID"+str(currentID))
            #pnetlist = blockcityin.getPoints("NetworkID"+str(currentID))
            #enetlist = blockcityin.getEdges("NetworkID"+str(currentID))
            #network_attr = blockcityin.getAttributes("NetworkID"+str(currentID))
            #currentPatchList = patchcityin.getAttributes("PatchDataID"+str(currentID))
            
            #-----------------------------------------------------------------#
            #        DETERMINE WHETHER TO UPDATE CURRENT BLOCK AT ALL         #
            #-----------------------------------------------------------------#
            
            block_status = currentAttList.getAttribute("Status").getDouble()
            if block_status == 0 or currentAttList.getAttribute("ResTIArea").getDouble() == 0:
                continue
            
            currentAttList.addAttribute("HasLotS", 0)
            currentAttList.addAttribute("HasStreetS", 0)
            currentAttList.addAttribute("HasNeighS", 0)
            currentAttList.addAttribute("HasPrecS", 0)
            currentAttList.addAttribute("MaxLotDeg", 1.1)
            currentAttList.addAttribute("IAServiced", 0)
            totimparea = currentAttList.getAttribute("ResTIArea").getDouble()
            currentAttList.addAttribute("IADeficit", totimparea)
            currentAttList.addAttribute("UpstrImpTreat", 0)

            
        #Output vector update
        #blockcityout.setAttributes("MapAttributes", map_attr)
        #design_details.setAttributes("DesignAttributes", des_attr)
    
    ########################################################
    #LINK WITH GUI                                         #
    ########################################################
    
    def createInputDialog(self):
        form = activatetechplacementGUI(self, QApplication.activeWindow())
        form.show()
        return True  
