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
import random
import math

class ubp_nonres(Module):
    """Description of class
	
    Description of Inputs & Outputs 
	- <description of inputs/outputs>
    
    Log of Updates made at each version:
    
    v0.80 (March 2012):
        - Created ubp_nonres.py
        - Contains the code that used to be in urbplanbb.py for Trade, Industries & Offices
        - Now handles the these districts that urbplanbb.py initially did for more modularity
        
	@ingroup DAnCE4Water
	@author Peter M Bach
	"""
    def __init__(self):
        Module.__init__(self)
        #input/output data - each planning module has as input BLOCKS, PATCHES, RULES
        #                  - each planning module has as output: updated BLOCKS
        #                  - PATCHES are passed on from UrbplanBB straight through (not modified)
        self.blockcityin = VectorDataIn
        self.nonresidential = VectorDataIn
        self.patchcityin = VectorDataIn
        self.planningrules = VectorDataIn
        self.addParameter(self, "blockcityin", VIBe2.VECTORDATA_IN)
        self.addParameter(self, "nonresidential", VIBe2.VECTORDATA_OUT)
        self.addParameter(self, "patchcityin", VIBe2.VECTORDATA_IN)
        self.addParameter(self, "planningrules", VIBe2.VECTORDATA_IN)
        
    def run(self):
        #Get Vector Data
        blockcityin = self.blockcityin.getItem()
        nonresidential = self.nonresidential.getItem()
        patchcityin = self.patchcityin.getItem()
        planningrules = self.planningrules.getItem()
        
        map_attr = blockcityin.getAttributes("MapAttributes")   #GET map attributes
        
        #Get some Parameters
        blocks_num = map_attr.getAttribute("NumBlocks")     #number of blocks to loop through
        blocks_size = map_attr.getAttribute("BlockSize")    #size of block
        map_w = map_attr.getAttribute("WidthBlocks")        #num of blocks wide
        map_h = map_attr.getAttribute("HeightBlocks")       #num of blocks tall
        input_res = map_attr.getAttribute("InputReso")      #resolution of input data
        urbansimdata = map_attr.getStringAttribute("UrbanSimData")
        
        
        #--------------------------------------------------------------------------------#
        #       DISASSEMBLE PLANNING RULES INTO USABLE FORMAT FROM PREVIOUS MODULE       #
        #--------------------------------------------------------------------------------#
        plan_gen = planningrules.getAttributes("GeneralRules")
        
        maximperv = plan_gen.getAttribute("maximperv")                          #DOUBLE -- maximum site imperviousness [%]
        maxsitecover = plan_gen.getAttribute("maxsitecover")                    #DOUBLE -- maximum site cover [%]
        lcality_mun_trans = plan_gen.getAttribute("locality_mun_trans")         #BOOL -- locality map for municipal & transport?
        
        #===-----------------
        
        plan_nonres = planningrules.getAttributes("NonResRules")
        
        employment_data = plan_nonres.getStringAttribute("employment_data")     #STRING -- 'D' = direct input, 'P' = population-derived
        employment_rad = plan_nonres.getAttribute("employment_rad")             #DOUBLE -- consider employment radius of 1km
        employment_rate = plan_nonres.getAttribute("employment_rate")           #DOUBLE -- employment rate for region in %
        employment_adjust = plan_nonres.getAttribute("employment_adjust")       #DOUBLE -- employment adjustment factor for future growth
        com_spacevary_check = plan_nonres.getAttribute("com_spacevary_check")   #BOOL -- True/False checkbox to vary required floor space
        
        Atrad_cc = plan_nonres.getAttribute("Atrad_cc")                         #DOUBLE -- Trade sqm/employee at city centre
        Atrad_uf = plan_nonres.getAttribute("Atrad_uf")                         #DOUBLE -- Trade sqm/employee at urban fringe
        Aoff_cc = plan_nonres.getAttribute("Aoff_cc")                           #DOUBLE -- Offices sqm/employee at city centre
        Aoff_uf = plan_nonres.getAttribute("Aoff_uf")                           #DOUBLE -- Offices sqm/employee at urban fringe
        Alind_cc = plan_nonres.getAttribute("Alind_cc")                         #DOUBLE -- Light industry sqm/employee at city centre
        Alind_uf = plan_nonres.getAttribute("Alind_uf")                         #DOUBLE -- Light industry sqm/employee at urban fringe
        Ahind_cc = plan_nonres.getAttribute("Ahind_cc")                         #DOUBLE -- Heavy industry sqm/employee at city centre
        Ahind_uf = plan_nonres.getAttribute("Ahind_uf")                         #DOUBLE -- Heavy industry sqm/employee at urban fringe
        ddecay_type = plan_nonres.getStringAttribute("ddecay_type")                   #STRING -- distance decay relationship
        
        com_fsetback_min = plan_nonres.getAttribute("com_fsetback_min")         #DOUBLE -- minimum front setback [m]
        com_setback_auto = plan_nonres.getAttribute("com_setback_auto")         #BOOL -- determine setback automatically?
        com_floors_max = plan_nonres.getAttribute("com_floors_max")             #DOUBLE -- maximum allowable floors
        
        com_carpark_dmin = plan_nonres.getAttribute("com_carpark_dmin")         #DOUBLE -- minimum depth of frontage parking area [m]
        com_carparkW = plan_nonres.getAttribute("com_carparkW")                 #DOUBLE -- minimum width of one parking lot
        com_carparkD = plan_nonres.getAttribute("com_carparkD")                 #DOUBLE -- minimum depth of one parking lot
        com_carpark_avgimp = plan_nonres.getAttribute("com_carpark_avgimp")     #DOUBLE -- avg. imperviousness of parking area
        com_carpark_share = plan_nonres.getAttribute("com_carpark_share")       #BOOL -- share carparks if multiple zones?
        com_service_dmin = plan_nonres.getAttribute("com_service_dmin")         #DOUBLE -- minimum depth of service area
        
        access_perp = plan_nonres.getAttribute("access_perp")                   #BOOL -- access road aligned perpendicular
        access_parall = plan_nonres.getAttribute("access_parall")               #BOOL -- access road aligned parallel
        access_cds = plan_nonres.getAttribute("access_cds")                     #BOOL -- access road cul-de sacs
        access_parall_medwidth = plan_nonres.getAttribute("access_parall_medwidth")   #DOUBLE -- median width if access rd aligned parallel
        access_cds_circlerad = plan_nonres.getAttribute("access_cds_circlerad") #DOUBLE -- turning circle radius in cul-de-sac
        access_ped_include = plan_nonres.getAttribute("access_ped_include")     #BOOL -- include pedestrian paths along service roads?
        
        lscape_hsbal = plan_nonres.getAttribute("lscape_hsbal")                 #DOUBLE -- balance between hard & soft landscapes
        lscape_avgimp_dced = plan_nonres.getAttribute("lscape_avgimp_dced")     #DOUBLE -- avg. imperviousness disconnected
        
        #===-----------------
        
        plan_space = planningrules.getAttributes("SpacesRules")
        
        w_comfootpath_min = plan_space.getAttribute("w_comfootpath_min")        #DOUBLE
        w_comfootpath_max = plan_space.getAttribute("w_comfootpath_max")        #DOUBLE
        w_comnaturestrip_min = plan_space.getAttribute("w_comnaturestrip_min")  #DOUBLE
        w_comnaturestrip_max = plan_space.getAttribute("w_comnaturestrip_max")  #DOUBLE
        w_comfootpath_med = plan_space.getAttribute("w_comfootpath_med")        #BOOL -- to simplify things, just use median footpath width?
        w_comnaturestrip_med = plan_space.getAttribute("w_comnaturestrip_med")  #BOOL -- to simplify things, just use median naturestrip width?
        
        w_collectlane_min = plan_space.getAttribute("w_collectlane_min")        #DOUBLE
        w_collectlane_max = plan_space.getAttribute("w_collectlane_max")        #DOUBLE
        w_collectlane_med = plan_space.getAttribute("w_collectlane_med")        #BOOL
        collect_crossfall = plan_space.getAttribute("collect_crossfall")        #DOUBLE
        
        
        #--------------------------------------------------------------------------------#
        #       BEGIN LOOPING ACROSS ALL BLOCKS IN MAP                                   #
        #--------------------------------------------------------------------------------#
        
        for i in range(int(blocks_num)):
            currentID = i + 1
            currentAttList = blockcityin.getAttributes("BlockID"+str(currentID))        #attribute list of current block structure
            currentPatchList = patchcityin.getAttributes("PatchDataID"+str(currentID))
            nonres_attr = Attribute()
            nonres_attr.setAttribute("BlockID", currentID)
            block_AActive = blocks_size * blocks_size * (currentAttList.getAttribute("Activity")/100)

            #--------------------------------------------------------------------------------#
            #            CONDITIONAL CHECK TO SEE IF CURRENT BLOCK IS RELEVANT               #
            #--------------------------------------------------------------------------------#
            #2 conditions to skip: (1) status = 0, (2) no industrial/trade area
            block_status = currentAttList.getAttribute("Status")
            tot_nonres_area = currentAttList.getAttribute("ALUC_Trad") + currentAttList.getAttribute("ALUC_ORC") \
                + currentAttList.getAttribute("ALUC_LI") + currentAttList.getAttribute("ALUC_HI")
            if block_status == 0 or tot_nonres_area == 0:
                print "BlockID"+str(currentID)+" not active or no relevant non-res area"
                continue
            #IF NOT SKIPPED, PLAN URBAN FORM
            nonres_attr.setAttribute("HasNonRes", 1)
            
            #--------------------------------------------------------------------------------#
            #            SETUP DATA - RETRIEVE FROM BLOCKCITY AND SAMPLE VALUES              #
            #--------------------------------------------------------------------------------#
            
            trad_area_tot = float(currentAttList.getAttribute("ALUC_Trad"))     #Total Trade Area
            ORC_area_tot = float(currentAttList.getAttribute("ALUC_ORC"))       #Total ORC Area
            LI_area_tot = float(currentAttList.getAttribute("ALUC_LI"))         #Total Light Industry Area
            HI_area_tot = float(currentAttList.getAttribute("ALUC_HI"))         #Total Heavy Industry Area
            total_industrial_area = LI_area_tot + HI_area_tot
            total_commercial_area = trad_area_tot + ORC_area_tot
            if total_industrial_area != 0:
                nonres_attr.setAttribute("HasIndustry", 1)
            if total_commercial_area != 0:
                nonres_attr.setAttribute("HasCommercial", 1)
                
                
            #--------------------------------------------------------------------------------#
            #            PLAN OUT URBAN FORM                                                 #
            #--------------------------------------------------------------------------------#
            
            #Get Employment information
            #Get all areas of different non-residential land zones           
            #Calculate Construction Area
            #Calculate number of allotments
            #Calculate building footprint
            #Calculate car park space
            #Calculate service area space
            #Tally up areas
            #Check remaining area with landscaping requirements (Hard vs. Soft)
            #Tally up impervious areas, etc.
            
            ### COMMERCIAL >> TRADE - URBAN PLANNING =========================================#
            
            
            
            
            
            ### COMMERCIAL >> ORC - URBAN PLANNING ===========================================#
            
            
            
            
            
            ### INDUSTRIAL >> LIGHT - URBAN PLANNING =========================================#
            
            
            
            
            
            ### INDUSTRIAL >> HEAVY - URBAN PLANNING =========================================#
            
            
            
            
            #--------------------------------------------------------------------------------#
            #            TALLY UP INFO AND WRITE TO OUTPUT                                   #
            #--------------------------------------------------------------------------------#
            
            #ASSUME FOR NOW Industrial Areas are 90% impervious and Commercial 80%
            Aimp_ind = 0.9*total_industrial_area
            Aimp_com = 0.8*total_commercial_area
            
            
            nonres_attr.setAttribute("AIndustry", total_industrial_area)
            nonres_attr.setAttribute("ACommercial", total_commercial_area)
            nonres_attr.setAttribute("AImp_Ind", Aimp_ind)
            nonres_attr.setAttribute("AImp_Com", Aimp_com)
            
            #-----------------------------------------------------------------#
            #        Write all updated Attribute Lists to the output          #
            #-----------------------------------------------------------------#
                
            nonresidential.setAttributes("BlockID"+str(currentID),nonres_attr)
            
            #FOR LOOP END (Repeat for next BlockID)
            
        #END OF MODULE
    
            
            
            
            