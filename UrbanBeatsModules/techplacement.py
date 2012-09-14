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
	self.setParameterValue("ration_runoff",str(self.ration_runoff))
        self.createParameter( "ration_pollute", BOOL,"")
	self.setParameterValue("ration_pollute",str(self.ration_runoff))
        self.createParameter( "runoff_pri", DOUBLE,"")
	self.setParameterValue("runoff_pri",str(self.runoff_pri))
	
        self.createParameter( "pollute_pri", DOUBLE,"")
	self.setParameterValue("pollute_pri",str(self.pollute_pri))
        self.createParameter( "ration_harvest",BOOL,"")
	self.setParameterValue("ration_harvest",str(self.ration_harvest))
	self.createParameter( "harvest_pri",DOUBLE,"")
	self.setParameterValue("harvest_pri",str(self.harvest_pri))
        
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
	self.setParameterValue("targets_runoff",str(self.targets_runoff))
        self.createParameter( "targets_TSS", DOUBLE,"")
	self.setParameterValue("targets_TSS",str(self.targets_TSS))
        self.createParameter( "targets_TN", DOUBLE,"")
	self.setParameterValue("targets_TN",str(self.targets_TN))
        self.createParameter( "targets_TP", DOUBLE,"")
	self.setParameterValue("targets_TP",str(self.targets_TN))
        self.createParameter( "targets_harvest", DOUBLE,"")
	self.setParameterValue("targets_harvest",str(self.targets_harvest))
        self.createParameter( "runoff_auto", BOOL,"")
	self.setParameterValue("runoff_auto",str(self.runoff_auto))
        self.createParameter( "TSS_auto", BOOL,"")
	self.setParameterValue("TSS_auto",str(self.TSS_auto))
        self.createParameter( "TN_auto", BOOL,"")
	self.setParameterValue("TN_auto",str(self.TN_auto))
        self.createParameter( "TP_auto", BOOL,"")
	self.setParameterValue("TP_auto",str(self.TP_auto))
        self.createParameter( "harvest_auto", BOOL,"")
	self.setParameterValue("harvest_auto",str(self.harvest_auto))
        
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
	self.setParameterValue("strategy_lot_check",str(self.strategy_lot_check))
        self.createParameter( "strategy_street_check", BOOL,"")
	self.setParameterValue("strategy_street_check",str(self.strategy_street_check))
        self.createParameter( "strategy_neigh_check", BOOL,"")
	self.setParameterValue("strategy_neigh_check",str(self.strategy_neigh_check))
        self.createParameter( "strategy_prec_check", BOOL,"")
	self.setParameterValue("strategy_prec_check",str(self.strategy_prec))
        self.createParameter( "lot_increment", DOUBLE,"")
	self.setParameterValue("lot_increment",str(self.lot_increment))
        self.createParameter( "street_increment", DOUBLE,"")
	self.setParameterValue("street_increment",str(self.street_increment))
        self.createParameter( "neigh_increment", DOUBLE,"")
	self.setParameterValue("neigh_increment",str(self.neigh_increment))
        self.createParameter( "prec_increment", DOUBLE,"")
	self.setParameterValue("prec_increment",str(self.prec_increment))
        self.createParameter( "basin_target_min", DOUBLE,"")
	self.setParameterValue("basin_target_min",str(self.basin_target_min))
        self.createParameter( "basin_target_max", DOUBLE,"")
	self.setParameterValue("basin_target_max",str(self.basin_target_max))
        
        #ADDITIONAL STRATEGIES
        self.strategy_specific1 = False
        self.strategy_specific2 = False
        self.strategy_specific3 = False
        self.strategy_specific4 = False
        self.strategy_specific5 = False
        self.strategy_specific6 = False
        self.createParameter( "strategy_specific1", BOOL,"")
	self.setParameterValue("strategy_specific1",str(self.strategy_specific1))
        self.createParameter( "strategy_specific2", BOOL,"")
	self.setParameterValue("strategy_specific2",str(self.strategy_specific2))
        self.createParameter( "strategy_specific3", BOOL,"")
	self.setParameterValue("strategy_specific3",str(self.strategy_specific3))
        self.createParameter( "strategy_specific4", BOOL,"")
	self.setParameterValue("strategy_specific4",str(self.strategy_specific4))
        self.createParameter( "strategy_specific5", BOOL,"")
	self.setParameterValue("strategy_specific5",str(self.strategy_specific5))
        self.createParameter( "strategy_specific6", BOOL,"")
	self.setParameterValue("strategy_specific6",str(self.strategy_specific6))
        
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
	self.setParameterValue("retrofit_scenario",self.retrofit_scenario)
        self.createParameter( "renewal_cycle_def", BOOL,"")
        self.createParameter( "renewal_lot_years", DOUBLE,"")
	self.setParameterValue("renewal_lot_years",str(self.renewal_lot_years))
        self.createParameter( "renewal_street_years", DOUBLE,"")
	self.setParameterValue("renewal_street_years",str(self.renewal_street_years))
        self.createParameter( "renewal_neigh_years", DOUBLE,"")
	self.setParameterValue("renewal_neigh_years",str(self.renewal_neigh_years))
        self.createParameter( "renewal_lot_perc", DOUBLE,"")
	self.setParameterValue("renewal_lot_perc",str(self.renewal_lot_perc))
        self.createParameter( "force_street", BOOL,"")
	self.setParameterValue("force_street",str(self.force_street))
        self.createParameter( "force_neigh", BOOL,"")
	self.setParameterValue("force_neigh",str(self.force_neigh))
        self.createParameter( "force_prec", BOOL,"")
	self.setParameterValue("force_prec",str(self.force_prec))
        
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
	self.setParameterValue("lot_renew",str(self.lot_renew))
        self.createParameter( "lot_decom", BOOL,"")
	self.setParameterValue("lot_decom",str(self.lot_decom))
        self.createParameter( "street_renew", BOOL,"")
	self.setParameterValue("street_renew",str(self.street_renew))
        self.createParameter( "street_decom", BOOL,"")
	self.setParameterValue("street_decom",str(self.street_decom))
        self.createParameter( "neigh_renew", BOOL,"")
	self.setParameterValue("neigh_renew",str(self.neigh_renew))
        self.createParameter( "neigh_decom", BOOL,"")
	self.setParameterValue("neigh_decom",str(self.neigh_decom))
        self.createParameter( "prec_renew", BOOL,"")
	self.setParameterValue("prec_renew",str(self.prec_renew))
        self.createParameter( "prec_decom", BOOL,"")
        self.createParameter( "decom_thresh", DOUBLE,"")
	self.setParameterValue("decom_thresh",str(self.decom_thres))
        self.createParameter( "renewal_thresh", DOUBLE,"")
	self.setParameterValue("renewal_thresh",str(self.renewal_thresh))
        self.createParameter( "renewal_alternative", STRING,"")
	self.setParameterValue("renewal_alternative",self.renewal_alternative)
        
        
        #---GENERAL DESIGN CRITERIA---------------------------------------------
        #followed by vibe inputs
        #self.input_parameter = default value
        #self.createParameter( "input_parameter", DOUBLE)
        
        #---ADVANCED STORMWATER HARVESTING PLANT [ASHP]---###TBA###-------------
        self.ASHPstatus = 0
        self.createParameter( "ASHPstatus", BOOL,"")
	self.setParameterValue("ASHPstatus",str(self.ASHPstatus))
        self.ASHPlevel = 0
        self.createParameter( "ASHPlevel", DOUBLE,"")
	self.setParameterValue("ASHPlevel",str(self.ASHPlevel))
        self.ASHPgroup = 0
        self.createParameter( "ASHPgroup", DOUBLE,"")
	self.setParameterValue("ASHPgroup",str(self.ASHPgroup))
        
        #---AQUACULTURE/LIVING SYSTEMS [AQ]---###TBA###-------------------------
        self.AQstatus = 0
        self.createParameter( "AQstatus", BOOL,"")
	self.setParameterValue("AQstatus",str(self.AQstatus))
        self.AQlevel = 0
        self.createParameter( "AQlevel", DOUBLE,"")
	self.setParameterValue("AQlevel",str(self.AQlevel))
        self.AQgroup = 0
        self.createParameter( "AQgroup", DOUBLE,"")
	self.setParameterValue("AQgroup",str(self.AQgroup))
        
        #---AQUIFER STORAGE & RECOVERY SYSTEM [ASR]---###TBA###-----------------
        self.ASRstatus = 0
        self.createParameter( "ASRstatus", BOOL,"")
	self.setParameterValue("ASRstatus",str(self.ASRstatus))
        self.ASRlevel = 0
        self.createParameter( "ASRlevel", DOUBLE,"")
	self.setParameterValue("ASRlevel",str(self.ASRlevel))
        self.ASRgroup = 0
        self.createParameter( "ASRgroup", DOUBLE,"")
	self.setParameterValue("ASRgroup",str(self.ASRgroup))
        
        
        #---BIOFILTRATION SYSTEM/RAINGARDEN [BF]--------------------------------
        self.BFstatus = 1
        self.createParameter( "BFstatus", BOOL,"")
	self.setParameterValue("BFstatus",str(self.BFstatus))
        self.BFlevel = 0
        self.createParameter( "BFlevel", DOUBLE,"")
	self.setParameterValue("BFlevel",str(self.BFlevel))
        self.BFgroup = 0
        self.createParameter( "BFgroup", DOUBLE,"")
	self.setParameterValue("BFgroup",str(self.BFgroup))
        
        #Available Scales
        self.BFlot = True
        self.BFstreet = True
        self.BFneigh = True
        self.BFprec = True
        self.createParameter( "BFlot", BOOL,"")
	self.setParameterValue("BFlot",str(self.BFlot))
        self.createParameter( "BFstreet", BOOL,"")
	self.setParameterValue("BFstreet",str(self.BFstreet))
        self.createParameter( "BFneigh", BOOL,"")
	self.setParameterValue("BFneigh",str(self.BFneigh))
        self.createParameter( "BFprec", BOOL,"")
	self.setParameterValue("BFprec",str(self.BFprec))
        
        #Available Applications
        self.BFflow = False
	self.BFpollute = True
	self.createParameter( "BFflow", BOOL, "")
	self.setParameterValue("BFflow",str(self.BFflow))        
	self.createParameter( "BFpollute", BOOL,"")
	self.setParameterValue("BFpullute",str(self.BFflow))
        
        #Design Curves
        self.BFdesignUB = True          #use DAnCE4Water's default curves to design system?
        self.BFdescur_path = "no file"  #path for design curve
        self.createParameter( "BFdesignUB", BOOL,"")
	self.setParameterValue("BFdesignUB",str(self.BFdesignUB))
        self.createParameter( "BFdescur_path", STRING,"")
	self.setParameterValue("BFdescur_path",self.BFdescur_path)
        
        #Design Information
        self.BFspec_EDD = 0.3
        self.BFspec_FD = 0.6
        self.createParameter( "BFspec_EDD", DOUBLE,"")
	self.setParameterValue("BFspec_EDD",str(self.BFspec_EDD))
        self.createParameter( "BFspec_FD", DOUBLE,"")
	self.setParameterValue("BFspec_FD",str(self.BFspec_FD))
        self.BFmaxsize = 999999         #maximum surface area of system in sqm
        self.createParameter( "BFmaxsize", DOUBLE,"")
	self.setParameterValue("BFmaxsize",str(self.BFmaxsize))
	self.BFavglife = 20             #average life span of a biofilter
        self.createParameter("BFavglife", DOUBLE,"")
	self.setParameterValue("BFavglife",str(self.BFavglife))
        

        self.BFlined = True
        self.createParameter( "BFlined", BOOL,"")
	self.setParameterValue("BFlined",str(self.BFlined))
        
        
        #---GREEN ROOF [GR]---###TBA###-----------------------------------------
        self.GRstatus = 0
        self.createParameter( "GRstatus", BOOL,"")
	self.setParameterValue("GRstatus",str(self.GRstatus))
        self.GRlevel = 0
        self.createParameter( "GRlevel", DOUBLE,"")
	self.setParameterValue("GRlevel",str(self.GRlevel))
        self.GRgroup = 0
        self.createParameter( "GRgroup", DOUBLE,"")
	self.setParameterValue("GRgroup",str(self.GRgroup))
                
        #---INFILTRATION SYSTEM [IS]--------------------------------------------
        self.ISstatus = 1
        self.createParameter( "ISstatus", BOOL,"")
	self.setParameterValue("ISstatus",str(self.ISstatus))
        self.ISlevel = 0
        self.createParameter( "ISlevel", DOUBLE,"")
	self.setParameterValue("ISlevel",str(self.ISlevel))
        self.ISgroup = 0
        self.createParameter( "ISgroup", DOUBLE,"")
	self.setParameterValue("ISgroup",str(self.ISgroup))
        
        #Available Scales
        self.ISlot = True
        self.ISstreet = True
        self.ISneigh = True
        self.createParameter( "ISlot", BOOL,"")
	self.setParameterValue("ISlot",str(self.ISlot))
        self.createParameter( "ISstreet", BOOL,"")
	self.setParameterValue("ISstreet",str(self.ISstreet))
        self.createParameter( "ISneigh", BOOL,"")
	self.setParameterValue("ISneigh",str(self.ISneigh))
        
        #Available Applications
        self.ISflow = True
        self.ISpollute = True
        self.createParameter( "ISflow", BOOL,"")
	self.setParameterValue("ISflow",str(self.ISflow))
        self.createParameter( "ISpollute", BOOL,"")
	self.setParameterValue("ISpollute",str(self.ISpollute))
        
        #Design Curves
        self.ISdesignUB = True          #use DAnCE4Water's default curves to design system?
        self.ISdescur_path = "no file"  #path for design curve
        self.createParameter( "ISdesignUB", BOOL,"")
	self.setParameterValue("ISdesignUB",str(self.ISdesignUB))
        self.createParameter( "ISdescur_path", STRING,"")
	self.setParameterValue("ISdescur_path",self.ISdescur_path)
        
        #Design Information
        self.ISspec_EDD = 0.2
        self.ISspec_FD = 0.8
        self.createParameter( "ISspec_EDD", DOUBLE,"")
	self.setParameterValue("ISspec_EDD",str(self.ISspec_EDD))
        self.createParameter( "ISspec_FD", DOUBLE,"")
	self.setParameterValue("ISspec_FD",str(self.ISspec_FD))
        self.ISmaxsize = 5000          #maximum surface area of system in sqm
        self.createParameter( "ISmaxsize", DOUBLE,"")
	self.setParameterValue("ISmaxsize",str(self.ISmaxsize))
	self.ISavglife = 20             #average life span of an infiltration system
	self.createParameter( "ISavglife", DOUBLE,"")
	self.setParameterValue("ISavglife",str(self.ISavglife))



        self.IS_2Dmodel = True
        self.createParameter( "IS_2Dmodel", BOOL,"")
	self.setParameterValue("IS_2Dmodel",str(self.IS_2Dmodel))
        
        #---GROSS POLLUTANT TRAP [GPT]------------------------------------------
        self.GPTstatus = 0
        self.createParameter( "GPTstatus", BOOL,"")
	self.setParameterValue("GPTstatus",str(self.GPTstatus))
        self.GPTlevel = 0
        self.createParameter( "GPTlevel", DOUBLE,"")
	self.setParameterValue("GPTlevel",str(self.GPTlevel))
        self.GPTgroup = 0
        self.createParameter( "GPTgroup", DOUBLE,"")
	self.setParameterValue("GPTgroup",str(self.GPTgroup))
        
        #self.input_parameter = default value
        #self.createParameter( "input_parameter", DOUBLE)
        
        #---GREYWATER TREATMENT & DIVERSION SYSTEM [GT]-------------------------
        self.GTstatus = 0
        self.createParameter( "GTstatus", BOOL,"")
	self.setParameterValue("Gtstatus",str(self.GTstatus))
        self.GTlevel = 0
        self.createParameter( "GTlevel", DOUBLE,"")
	self.setParameterValue("GTlevel",str(self.GTlevel))
        self.GTgroup = 0
        self.createParameter( "GTgroup", DOUBLE,"")
	self.setParameterValue("GTgroup",str(self.GTgroup))
        
        #followed by vibe inputs
        #self.input_parameter = default value
        #self.addParameter(self , "input_parameter", DOUBLE)
        
        #---PACKAGED PLANT [PPL]---###TBA###------------------------------------
        self.PPLstatus = 0
        self.createParameter( "PPLstatus", BOOL,"")
	self.setParameterValue("PPLstatus",str(self.PPLstatus))
        self.PPLlevel = 0
        self.createParameter( "PPLlevel", DOUBLE,"")
	self.setParameterValue("PPLlevel",str(self.PPLlevel))
        self.PPLgroup = 0
        self.createParameter( "PPLgroup", DOUBLE,"")
	self.setParameterValue("PPLgroup",str(self.PPLgroup))
        
        #---PONDS & SEDIMENTATION BASIN [PB]------------------------------------
        self.PBstatus = 1
        self.createParameter( "PBstatus", BOOL,"")
	self.setParameterValue("PBstatus",str(self.PBstatus))
        self.PBlevel = 0
        self.createParameter( "PBlevel", DOUBLE,"")
	self.setParameterValue("PVlevel",str(self.PVlevel))
        self.PBgroup = 0
        self.createParameter( "PBgroup", DOUBLE,"")
	self.setParameterValue("PBgroup",str(self.PBgroup))
        
        #Available Scales
        self.PBneigh = True
        self.PBprec = True
        self.createParameter( "PBneigh", BOOL,"")
	self.setParameterValue("PBneigh",str(self.PBneigh))
        self.createParameter( "PBprec", BOOL,"")
	self.setParameterValue("PBprec",str(self.PBprec))
        
        #Available Applications
        self.PBflow = True
        self.PBpollute = True
        self.createParameter( "PBflow", BOOL,"")
	self.setParameterValue("PBflow",str(self.PBflow))
        self.createParameter( "PBpollute", BOOL,"")
	self.setParameterValue("PBpollute",str(self.PBpollute))
        
        #Design Curves
        self.PBdesignUB = True          #use DAnCE4Water's default curves to design system?
        self.PBdescur_path = "no file"  #path for design curve
        self.createParameter( "PBdesignUB", BOOL,"")
	self.setParameterValue("PBdesignUB",str(self.PBdesignUB))
        self.createParameter( "PBdescur_path", STRING,"")
	self.setParameterValue("PBdescur_path",self.PBdescur_path)
        
        #Design Information
        self.PBspec_MD = "1.25" 	#need a string for the combo box
        self.createParameter( "PBspec_MD", STRING,"")
	self.setParameterValue("PBspec_MD",self.PBspec_MD)
        self.PBmaxsize = 9999999           #maximum surface area of system in sqm
        self.createParameter( "PBmaxsize", DOUBLE,"")
	self.setParameterValue("PBmaxsize",str(self.PBmaxsize))
	self.PBavglife = 20             #average life span of a pond/basin
	self.createParameter( "PBavglife", DOUBLE,"")
	self.setParameterValue("PBavglife",str(self.PBavglife))

        
        #---POROUS/PERVIOUS PAVEMENT [PP]---###TBA###---------------------------
        self.PPstatus = 0
        self.createParameter( "PPstatus", BOOL,"")
	self.setParameterValue("PPstatus",str(self.PPstatus))
        self.PPlevel = 0
        self.createParameter( "PPlevel", DOUBLE,"")
	self.setParameterValue("PPlevel",str(self.PPlevel))
        self.PPgroup = 0
        self.createParameter( "PPgroup", DOUBLE,"")
	self.setParameterValue("PPgroup",str(self.PPgroup))
        
        #---RAINWATER TANK [RT]-------------------------------------------------
        self.RTstatus = 0
        self.createParameter( "RTstatus", BOOL,"")
	self.setParameterValue("RTstatus",str(self.RTstatus))
        self.RTlevel = 0
        self.createParameter( "RTlevel", DOUBLE,"")
	self.setParameterValue("RTlevel",str(self.RTlevel))
        self.RTgroup = 0
        self.createParameter( "RTgroup", DOUBLE,"")
	self.setParameterValue("RTgroup",str(self.RTgroup))
        
        self.RTscale_lot = True
        self.RTscale_street = True
        self.RTpurp_flood = True
        self.RTpurp_recyc = False
        self.createParameter( "RTscale_lot", BOOL,"")
	self.setParameterValue("RTscale_lot",str(self.RTscale_lot))
        self.createParameter( "RTscale_street", BOOL,"")
	self.setParameterValue("RTscale_street",str(self.RTscale))
        self.createParameter( "RTpurp_flood", BOOL,"")
	self.setParameterValue("RTpurp_flood",str(self.RTpurp_flood))
        self.createParameter( "RTpurp_recyc", BOOL,"")
	self.setParameterValue("RTpurp_recyc",str(self.RTpurp_recyc))
        
        self.RT_firstflush = 2          #first flush volume [mm]
        self.RT_maxdepth = 2            #max tank depth [m]
        self.RT_mindead = 0.1           #minimum dead storage level [m]
        self.RT_shape_circ = True       #consider circular tanks
        self.RT_shape_rect = True       #consider rectangular tanks
        self.RT_sbmodel = "ybs"         #storage-behaviour model settings
        self.RTdesignD4W = True         #use DAnCE4Water's default curves to design system?
        self.RTdescur_path = "no file"  #path for design curve
        self.createParameter( "RT_firstflush", DOUBLE,"")
	self.setParameterValue("RT_firstflush",str(self.RT_firstflush))
        self.createParameter( "RT_maxdepth", DOUBLE,"")
	self.setParameterValue("RT_maxdepth",str(self.RT_maxdepth))
        self.createParameter( "RT_mindead", DOUBLE,"")
	self.setParameterValue("RT_mindead",str(self.RT_mindead))
        self.createParameter( "RT_shape_circ", BOOL,"")
	self.setParameterValue("RT_shape_circ",str(self.RT_shape_circ))
        self.createParameter( "RT_shape_rect", BOOL,"")
	self.setParameterValue("RT_shape_rect",str(self.RT_shape_rect))
        self.createParameter( "RT_sbmodel", STRING,"")
	self.setParameterValue("RT_sbmodel",self.RT_sbmodel)
        self.createParameter( "RTdesignD4W", BOOL,"")
	self.setParameterValue("RTdesignD4W",str(self.RT_sbmodel))
        self.createParameter( "RTdescur_path", STRING,"")
	self.setParameterValue("RT_descur_path",self.RTdescur_path)
        self.RTavglife = 20             #average life span of a raintank
	self.createParameter( "RTavglife", DOUBLE,"")
	self.setParameterValue("RTavglife",str(self.RTavglife))

        #---SAND/PEAT/GRAVEL FILTER [SF]----------------------------------------
        self.SFstatus = 0
        self.createParameter( "SFstatus", BOOL,"")
	self.setParameterValue("SFstatus",str(self.SFstatus))
        self.SFlevel = 0
        self.createParameter( "SFlevel", DOUBLE,"")
	self.setParameterValue("SFlevel",str(self.SFlevel))
        self.SFgroup = 0
        self.createParameter( "SFgroup", DOUBLE,"")
	self.setParameterValue("SFgroup",str(self.SFgroup))
        
        #---SEPTIC TANK [ST]---###TBA###----------------------------------------
        self.STstatus = 0
        self.createParameter( "STstatus", BOOL,"")
	self.setParameterValue("STstatus",str(self.STstatus))
        self.STlevel = 0
        self.createParameter( "STlevel", DOUBLE,"")
	self.setParameterValue("STlevel",str(self.STlevel))
        self.STgroup = 0
        self.createParameter( "STgroup", DOUBLE,"")
	self.setParameterValue("STgroup",str(self.STgroup))
        
        #---SUBSURFACE IRRIGATION SYSTEM [IRR]---###TBA###----------------------
        self.IRRstatus = 0
        self.createParameter( "IRRstatus", BOOL,"")
	self.setParameterValue("IRRstatus",str(self.IRRstatus))
        self.IRRlevel = 0
        self.createParameter( "IRRlevel", DOUBLE,"")
	self.setParameterValue("IRRlevel",str(self.IRRlevel))
        self.IRRgroup = 0
        self.createParameter( "IRRgroup", DOUBLE,"")
	self.setParameterValue("IRRgroup",str(self.IRRgroup))
        
        #---SUBSURFACE WETLAND/REED BED [WSUB]----------------------------------
        self.WSUBstatus = 0
        self.createParameter( "WSUBstatus", BOOL,"")
	self.setParameterValue("WSUBstatus",str(self.WSUBstatus))
        self.WSUBlevel = 0
        self.createParameter( "WSUBlevel", DOUBLE,"")
	self.setParameterValue("WSUBlevel",str(self.WSUBlevel))
        self.WSUBgroup = 0
        self.createParameter( "WSUBgroup", DOUBLE,"")
	self.setParameterValue("WSUBgroup",str(self.WSUBgroup))
        
        #---SURFACE WETLAND [WSUR]----------------------------------------------
        self.WSURstatus = 1
        self.createParameter( "WSURstatus", BOOL,"")
	self.setParameterValue("WSURstatus",str(self.WSURstatus))
        self.WSURlevel = 0
        self.createParameter( "WSURlevel", DOUBLE,"")
	self.setParameterValue("WSURlevel",str(self.WSURlevel))
        self.WSURgroup = 0
        self.createParameter( "WSURgroup", DOUBLE,"")
	self.setParameterValue("WSURgroup",str(self.WSURgroup))
        
        #Available Scales
        self.WSURneigh = True
        self.WSURprec = True
        self.createParameter( "WSURneigh", BOOL,"")
	self.setParameterValue("WSURneigh",str(self.WSURneigh))
        self.createParameter( "WSURprec", BOOL,"")
	self.setParameterValue("WSURprec",str(self.WSURprec))
        
        #Available Applications
        self.WSURflow = True
        self.WSURpollute = True
        self.createParameter( "WSURflow", BOOL,"")
	self.setParameterValue("WSURflow",str(self.WSURflow))
        self.createParameter( "WSURpollute", BOOL,"")
	self.setParameterValue("WSURpollute",str(self.WSURpollute))
        
        #Design Curves
        self.WSURdesignUB = True          #use DAnCE4Water's default curves to design system?
        self.WSURdescur_path = "no file"  #path for design curve
        self.createParameter( "WSURdesignUB", BOOL,"")
	self.setParameterValue("WSURdesignUB",str(self.WSURdesignUB))
        self.createParameter( "WSURdescur_path", STRING,"")
	self.setParameterValue("WSURdescur_path",self.WSURdescur_path)
        
        #Design Information
        self.WSURspec_EDD = 0.75
        self.createParameter( "WSURspec_EDD", DOUBLE,"")
	self.setParameterValue("WSURspec_EDD",str(self.WSURspec_EDD))
        self.WSURmaxsize = 9999999           #maximum surface area of system in sqm
        self.createParameter( "WSURmaxsize", DOUBLE,"")
	self.setParameterValue("WSURmaxsize",str(self.WSURmaxsize))
	self.WSURavglife = 20             #average life span of a wetland
	self.createParameter( "WSURavglife", DOUBLE,"")
	self.setParameterValue("WSURavglife",str(self.WSURavglife))

        
        #---SWALES & BUFFER STRIPS [SW]-----------------------------------------
        self.SWstatus = 1
        self.createParameter( "SWstatus", BOOL,"")
	self.setParameterValue("SWstatus",str(self.SWstatus))
        self.SWlevel = 0
        self.createParameter( "SWlevel", DOUBLE,"")
	self.setParameterValue("SWlevel",str(self.SWlevel))
        self.SWgroup = 0
        self.createParameter( "SWgroup", DOUBLE,"")
	self.setParameterValue("SWgroup",str(self.SWgroup))
        
        #Available Scales
        self.SWstreet = True
        self.createParameter( "SWstreet", BOOL,"")
	self.setParameterValue("SWstreet",str(self.SWstreet))
        
        #Available Applications
        self.SWflow = True
        self.SWpollute = True
        self.createParameter( "SWflow", BOOL,"")
	self.setParameterValue("SWflow",str(self.SWflow))
        self.createParameter( "SWpollute", BOOL,"")
	self.setParameterValue("SWpollute",str(self.SWpollute))
        
        #Design Curves
        self.SWdesignUB = True          #use DAnCE4Water's default curves to design system?
        self.SWdescur_path = "no file"  #path for design curve
        self.createParameter( "SWdesignUB", BOOL,"")
	self.setParameterValue("SWdesignUB",str(self.SWdesignUB))
        self.createParameter( "SWdescur_path", STRING,"")
	self.setParameterValue("SWdescur_path",self.SWdescur_path)
        
        #Design Information
        self.SWspec = 0
        self.createParameter( "SWspec", DOUBLE,"")
	self.setParameterValue("SWspec",str(self.SWspec))
        self.SWmaxsize = 9999           #maximum surface area of system in sqm
        self.createParameter( "SWmaxsize", DOUBLE,"")
	self.setParameterValue("SWmaxsize",str(self.SWmaxsize))
	self.SWavglife = 20             #average life span of a swale
	self.createParameter( "SWavglife", DOUBLE,"")
	self.setParameterValue("SWavglie",str(self.SWavglife))


        #---TREE PITS [TPS]---###TBA###-----------------------------------------
        self.TPSstatus = 0
        self.createParameter( "TPSstatus", BOOL,"")
	self.setParameterValue("TPSstatus",str(self.TPSstatus))
        self.TPSlevel = 0
        self.createParameter( "TPSlevel", DOUBLE,"")
	self.setParameterValue("TPSlevel",str(self.TPSlevel))
        self.TPSgroup = 0
        self.createParameter( "TPSgroup", DOUBLE,"")
	self.setParameterValue("TPSgroup",str(self.TPSgroup))
        
        
        #---URINE-SEPARATING TOILET [UT]---###TBA###----------------------------
        self.UTstatus = 0
        self.createParameter( "UTstatus", BOOL,"")
	self.setParameterValue("UTstatus",str(self.UTstatus))
        self.UTlevel = 0
        self.createParameter( "UTlevel", DOUBLE,"")
	self.setParameterValue("UTlevel",str(self.UTlevel))
        self.UTgroup = 0
        self.createParameter( "UTgroup", DOUBLE,"")
	self.setParameterValue("UTgroup",str(self.UTgroup))
        
        #---WASTEWATER RECOVERY & RECYCLING PLANT [WWRR]---###TBA###------------
        self.WWRRstatus = 0
        self.createParameter( "WWRRstatus", BOOL,"")
	self.setParameterValue("WWRRstatus",str(self.WWRRstatus))
        self.WWRRlevel = 0
        self.createParameter( "WWRRlevel", DOUBLE,"")
	self.setParameterValue("WWRRlevel",str(self.WWRRlevel))
        self.WWRRgroup = 0
        self.createParameter( "WWRRgroup", DOUBLE,"")
	self.setParameterValue("WWRRgroup",str(self.WWRRlevel))
        
        #---WATERLESS/COMPOSTING TOILETS [WT]---###TBA###-----------------------
        self.WTstatus = 0
        self.createParameter( "WTstatus", BOOL,"")
	self.setParameterValue("WTstatus",str(self.WTstatus))
        self.WTlevel = 0
        self.createParameter( "WTlevel", DOUBLE,"")
	self.setParameterValue("WTlevel",str(self.WTlevel))
        self.WTgroup = 0
        self.createParameter( "WTgroup", DOUBLE,"")
	self.setParameterValue("WTgroup",str(self.WTgroup))
        
        #---WATER EFFICIENT APPLIANCES [WEF]------------------------------------
        self.WEFstatus = 0
        self.createParameter( "WEFstatus", BOOL,"")
	self.setParameterValue("WEFstatus",str(self.WEFstatus))
        self.WEFlevel = 0
        self.createParameter( "WEFlevel", DOUBLE,"")
	self.setParameterValue("WEFlevel",str(self.WEFlevel))
        self.WEFgroup = 0
        self.createParameter( "WEFgroup", DOUBLE,"")
	self.setParameterValue("WEFgroup",str(self.WEFgroup))
        
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
	self.setParameterValue("WEF_implement_method",self.WEF_implement_method)
        self.createParameter( "LEG_force", BOOL,"")
	self.setParameterValue("LEG_force",str(self.LEG_force))
        self.createParameter( "LEG_minrate", DOUBLE,"")
	self.setParameterValue("LEG_minrate",str(self.LEG_minrate))
        self.createParameter( "PPP_force", BOOL,"")
	self.setParameterValue("PPP_force",str(self.PPP_force))
        self.createParameter( "PPP_likelihood", DOUBLE,"")
	self.setParameterValue("PPP_likelihood",str(self.PPP_likelihood))
        self.createParameter( "SEC_force", BOOL,"")
	self.setParameterValue("SEC_force",str(self.SEC_force))
        self.createParameter( "SEC_urbansim", BOOL,"")
	self.setParameterValue("SEC_urbansim",str(self.SEC_urbansim))
        self.createParameter( "D4W_UDMactive", BOOL,"")
	self.setParameterValue("D4W_UDMactive",str(self.D4W_UDMacitve))
        self.createParameter( "D4W_STMactive", BOOL,"")
	self.setParameterValue("D4W_STMactive",str(self.D4W_STMactive))
        self.createParameter( "D4W_EVMactive", BOOL,"")
	self.setParameterValue("D4W_EVMactive",str(self.D4W_EVMactive))
        
        self.WEF_rating_system = "AS"
        self.WEF_loc_famhouse = True
        self.WEF_loc_apart = True
        self.WEF_loc_nonres = True
        self.WEF_flow_method = "M"
        self.createParameter( "WEF_rating_system", STRING,"")
	self.setParameterValue("WEF_rating_system",self.WEF_rating_system)
        self.createParameter( "WEF_loc_famhouse", BOOL,"")
	self.setParameterValue("WEF_loc_famhouse",str(self.WEF_loc_famhouse))
        self.createParameter( "WEF_loc_apart", BOOL,"")
	self.setParameterValue("WEF_loc_apart",str(self.WEF_loc_famhouse))
        self.createParameter( "WEF_loc_nonres", BOOL,"")
	self.setParameterValue("WEF_loc_nonres",str(self.WEF_loc_nonres))
        self.createParameter( "WEF_flow_method", STRING,"")
	self.setParameterValue("WEF_flow_method", self.WEF_flow_method)
        
        #---<Add a new system - Name> [abbrev.]---------------------------------
        #self.<abbrev>status = 1
        #self.addParameter(self , "<abbrev>status", BOOL)
        #followed by vibe inputs
        #self.input_parameter = default value
        #self.addParameter(self , "input_parameter", DOUBLE)
        
        #---REGIONAL INFORMATION -----------------------------------------------
        self.regioncity = "Melbourne"
        self.createParameter( "regioncity", STRING,"")
	self.setParameterValue("Melbourne",self.regioncity)
        
        
        #---MULTI-CRITERIA INPUTS-----------------------------------------------
        #SELECT EVALUATION METRICS
        self.scoringmatrix_path = "DaywaterMCA.csv"
        self.scoringmatrix_default = False
        self.scoring_include_all = True
        self.createParameter( "scoringmatrix_path", STRING,"")
	self.setParameterValue("scoringmatrix_path",self.scoringmatrix_path)
        self.createParameter( "scoringmatrix_default", BOOL,"")
	self.setParameterValue("scoringmatrix_default",str(self.scoringmatrix_default))
        self.createParameter( "scoring_include_all", BOOL,"")
	self.setParameterValue("scoring_include_all",str(self.scoring_unclude_all))
        
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
	self.setParameterValue("bottomlines_tech",str(self.bottomlines_tech))
        self.createParameter( "bottomlines_env", BOOL,"")
	self.setParameterValue("bottomlines_env",str(self.bottomlines_env))
        self.createParameter( "bottomlines_ecn",BOOL,"")
	self.setParameterValue("bottomlines_ecn",str(self.bottomlines_ecn))
        self.createParameter( "bottomlines_soc", BOOL,"")
	self.setParameterValue("bottomlines_soc",str(self.bottomlines_soc))
        self.createParameter( "bottomlines_tech_n", DOUBLE,"")
	self.setParameterValue("bottomlines_tech_n", str(self.bottomlines_tech_n))
        self.createParameter( "bottomlines_env_n", DOUBLE,"")
	self.setParameterValue("bottomlines_env_n",str(self.bottomlines_env_n))
        self.createParameter( "bottomlines_ecn_n", DOUBLE,"")
	self.setParameterValue("bottomlines_ecn_n",str(self.bottomlines_ecn_n))
        self.createParameter( "bottomlines_soc_n", DOUBLE,"")
	self.setParameterValue("bottomlines_soc_n",str(self.bottomlines_soc_n))
        self.createParameter( "eval_mode", STRING,"")
	self.setParameterValue("eval_mode",self.eval_mode)
        self.createParameter( "bottomlines_tech_p", DOUBLE,"")
	self.setParameterValue("bottomlines_tech_p",str(self.bottomlines_tech_p))
        self.createParameter( "bottomlines_env_p", DOUBLE,"")
	self.setParameterValue("bottomlines_env_p",str(self.bottomlines_env_p))
        self.createParameter( "bottomlines_ecn_p", DOUBLE,"")
	self.setParameterValue("bottomlines_ecn_p",str(self.bottomlines_ecn_p))
        self.createParameter( "bottomlines_soc_p", DOUBLE,"")
	self.setParameterValue("bottomlines_soc_p",str(self.bottomlines_soc_p))
        self.createParameter( "bottomlines_tech_w", DOUBLE,"")
	self.setParameterValue("bottomlines_tech_w",str(self.bottomlines_tech_w))
        self.createParameter( "bottomlines_env_w", DOUBLE,"")
	self.setParameterValue("bottomlines_env_w",str(self.bottomlines_env_w))
        self.createParameter( "bottomlines_ecn_w", DOUBLE,"")
	self.setParameterValue("bottomlines_ecn_w",str(self.bottomlines_ecn_w))
        self.createParameter( "bottomlines_soc_w", DOUBLE,"")
	self.setParameterValue("bottomlines_soc_w",str(self.bottomlines_ecn_w))
        
        #SCORING OF STRATEGIES
        self.scope_stoch = False
        self.score_method = "AHP"       #MCA scoring method
        self.tech2strat_method = "EqW"  #How to merge technology scores into strategy score
        self.createParameter( "scope_stoch", BOOL,"")
	self.setParameterValue("scope_stoch",str(self.scope_stoch))
        self.createParameter( "score_method", STRING,"")
	self.setParameterValue("score_method",self.score_method)
        self.createParameter( "tech2strat_method", STRING,"")
	self.setParameterValue("tech2strat_method",self.tech2strat_method)
        
        #RANKING OF STRATEGIES
        self.ranktype = "RK"            #CI = Confidence Interval, RK = ranking
        self.topranklimit = 10
        self.conf_int = 95
        self.ingroup_scoring = "Avg"
        self.createParameter( "ranktype", STRING,"")
	self.setParameterValue("ranktype",self.ranktype)
        self.createParameter( "topranklimit", DOUBLE,"")
	self.setParameterValue("topranklimit",str(self.topranklimit))
        self.createParameter( "conf_int", DOUBLE,"")
	self.setParameterValue("conf_int",str(self.conf_int))
        self.createParameter( "ingroup_scoring", STRING,"")
	self.setParameterValue("ingroup_scoring", self.ingroup_scoring)
        

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
	self.desAttr.addAttribute("retrofit_scenario")
	self.desAttr.addAttribute("force_street")
	self.desAttr.addAttribute("force_neigh")
	self.desAttr.addAttribute("force_prec")
	self.desAttr.addAttribute("renewal_alternative")
	self.desAttr.addAttribute("renewal_cycle_def")
	self.desAttr.addAttribute("renewal_lot_years")
	self.desAttr.addAttribute("renewal_street_years")
	self.desAttr.addAttribute("renewal_neigh_years")
	self.desAttr.addAttribute("renewal_lot_perc")
	self.desAttr.addAttribute("lot_renew")
	self.desAttr.addAttribute("lot_decom")
	self.desAttr.addAttribute("street_renew")
	self.desAttr.addAttribute("street_decom")
	self.desAttr.addAttribute("neigh_renew")
	self.desAttr.addAttribute("neigh_decom")
	self.desAttr.addAttribute("prec_renew")
	self.desAttr.addAttribute("prec_decom")
	self.desAttr.addAttribute("decom_thresh")
	self.desAttr.addAttribute("renewal_thresh")

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
#	homeDir = os.environ['HOME']
#	dcvdirectory = homeDir + '/Documents/UrbanBEATS/UrbanBeatsModules/wsuddcurves/'
#	print dcvdirectory
	#dcvdirectory = "C:\\Users\\Peter M Bach\\Documents\\UrbanBEATS Development\\__urbanBEATS\\wsuddcurves\\"
	dcvdirectory = "./UrbanBEATS/UrbanBeatsModules/wsuddcurves/"
	#dcvdirectory = "C:\\Heiko\\WSC\\data\\wsuddcurves\\"
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
	        currentAttList.addAttribute("HasLotS", 0)
	        currentAttList.addAttribute("HasStreetS", 0)
		currentAttList.addAttribute("HasNeighS", 0)
	        currentAttList.addAttribute("HasPrecS", 0)
	        currentAttList.addAttribute("MaxLotDeg", 0)
	        currentAttList.addAttribute("IAServiced", 0)
	        currentAttList.addAttribute("IADeficit", 0)
	        currentAttList.addAttribute("UpstrImpTreat", 0)
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
