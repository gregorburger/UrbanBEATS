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
#from pyvibe import *
from pydynamind import *
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


	self.blocks = View("Block",FACE,READ)
	self.blocks.getAttribute("BlockID")
	self.blocks.addAttribute("NonResidentialID")

	self.mapattributes = View("Mapattributes", COMPONENT,READ)
    	self.mapattributes.getAttribute("NumBlocks")
	self.mapattributes.getAttribute("BlockSize")
	self.mapattributes.getAttribute("WidthBlocks")
	self.mapattributes.getAttribute("HeightBlocks")
	self.mapattributes.getAttribute("InputReso")

	self.planGen = View("PlanGen",COMPONENT,READ)
	self.planGen.getAttribute("maximperv")
	self.planGen.getAttribute("maxsitecover")
	self.planGen.getAttribute("locality_mun_trans")

	self.planNonres = View("PlanNonres",COMPONENT,READ)
	self.planNonres.getAttribute("employment_data")     
        self.planNonres.getAttribute("employment_rad")             
        self.planNonres.getAttribute("employment_rate")           
        self.planNonres.getAttribute("employment_adjust")       
        self.planNonres.getAttribute("com_spacevary_check")   
        
        self.planNonres.getAttribute("Atrad_cc")                         
        self.planNonres.getAttribute("Atrad_uf")                         
        self.planNonres.getAttribute("Aoff_cc")                           
        self.planNonres.getAttribute("Aoff_uf")                           
        self.planNonres.getAttribute("Alind_cc")                         
        self.planNonres.getAttribute("Alind_uf")                         
        self.planNonres.getAttribute("Ahind_cc")                         
        self.planNonres.getAttribute("Ahind_uf")                         
        self.planNonres.getAttribute("ddecay_type")             
        
        self.planNonres.getAttribute("com_fsetback_min")         
        self.planNonres.getAttribute("com_setback_auto")         
        self.planNonres.getAttribute("com_floors_max")             
        
        self.planNonres.getAttribute("com_carpark_dmin")         
        self.planNonres.getAttribute("com_carparkW")                 
        self.planNonres.getAttribute("com_carparkD")                 
        self.planNonres.getAttribute("com_carpark_avgimp")     
        self.planNonres.getAttribute("com_carpark_share")       
        self.planNonres.getAttribute("com_service_dmin")         
        
        self.planNonres.getAttribute("access_perp")                   
        self.planNonres.getAttribute("access_parall")               
        self.planNonres.getAttribute("access_cds")                     
        self.planNonres.getAttribute("access_parall_medwidth")   
        self.planNonres.getAttribute("access_cds_circlerad") 
        self.planNonres.getAttribute("access_ped_include")     
        
        self.planNonres.getAttribute("lscape_hsbal")                 
        self.planNonres.getAttribute("lscape_avgimp_dced")


	self.planSpaces = View("PlanSpaces", COMPONENT,READ)
	self.planSpaces.getAttribute("w_comfootpath_min")
        self.planSpaces.getAttribute("w_comfootpath_max")
        self.planSpaces.getAttribute("w_comnaturestrip_min")
        self.planSpaces.getAttribute("w_comnaturestrip_max")
        self.planSpaces.getAttribute("w_comfootpath_med")
        self.planSpaces.getAttribute("w_comnaturestrip_med")
        
        self.planSpaces.getAttribute("w_collectlane_min")
        self.planSpaces.getAttribute("w_collectlane_max")
        self.planSpaces.getAttribute("w_collectlane_med")
        self.planSpaces.getAttribute("collect_crossfall")
     	
	self.nonResidential = View("NonResidential",COMPONENT,WRITE)
	self.nonResidential.addAttribute("BlockID")
	self.nonResidential.addAttribute("HasNonRes")
	self.nonResidential.addAttribute("HasIndustry")
	self.nonResidential.addAttribute("HasCommerical")
	self.nonResidential.addAttribute("AIndustry")
	self.nonResidential.addAttribute("ACommercial")
	self.nonResidential.addAttribute("AImp_Com")
	self.nonResidential.addAttribute("AImp_Ind")

	#Datastream
	datastream = []
	datastream.append(self.blocks)
	datastream.append(self.mapattributes)
	datastream.append(self.planGen)
	datastream.append(self.planNonres)
	datastream.append(self.planSpaces)
	datastream.append(self.nonResidential)
	
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
        city = self.getData("City")
	self.initBLOCKIDtoUUID(city)
        

	#Get Vector Data
	strvec = city.getUUIDsOfComponentsInView(self.mapattributes)
        map_attr = city.getComponent(strvec[0])   #GET map attributes

       
        #Get some Parameters
        blocks_num = map_attr.getAttribute("NumBlocks").getDouble()     #number of blocks to loop through
        blocks_size = map_attr.getAttribute("BlockSize").getDouble()    #size of block
        map_w = map_attr.getAttribute("WidthBlocks").getDouble()        #num of blocks wide
        map_h = map_attr.getAttribute("HeightBlocks").getDouble()       #num of blocks tall
        input_res = map_attr.getAttribute("InputReso").getDouble()      #resolution of input data

        
        
        #--------------------------------------------------------------------------------#
        #       DISASSEMBLE PLANNING RULES INTO USABLE FORMAT FROM PREVIOUS MODULE       #
        #--------------------------------------------------------------------------------#
	strvec = city.getUUIDsOfComponentsInView(self.planGen)        
	plan_gen = city.getComponent(strvec[0])
        
        maximperv = plan_gen.getAttribute("maximperv").getDouble()                          #DOUBLE -- maximum site imperviousness [%]
        maxsitecover = plan_gen.getAttribute("maxsitecover").getDouble()                    #DOUBLE -- maximum site cover [%]
        lcality_mun_trans = plan_gen.getAttribute("locality_mun_trans").getDouble()         #BOOL -- locality map for municipal & transport?
        
        #===-----------------
        strvec = city.getUUIDsOfComponentsInView(self.planNonres)
        plan_nonres = city.getComponent(strvec[0])
        
        employment_data = plan_nonres.getAttribute("employment_data").getString()     #STRING -- 'D' = direct input, 'P' = population-derived
        employment_rad = plan_nonres.getAttribute("employment_rad").getDouble()             #DOUBLE -- consider employment radius of 1km
        employment_rate = plan_nonres.getAttribute("employment_rate").getDouble()           #DOUBLE -- employment rate for region in %
        employment_adjust = plan_nonres.getAttribute("employment_adjust").getDouble()       #DOUBLE -- employment adjustment factor for future growth
        com_spacevary_check = bool(plan_nonres.getAttribute("com_spacevary_check"))   #BOOL -- True/False checkbox to vary required floor space
        
        Atrad_cc = plan_nonres.getAttribute("Atrad_cc").getDouble()                         #DOUBLE -- Trade sqm/employee at city centre
        Atrad_uf = plan_nonres.getAttribute("Atrad_uf").getDouble()                         #DOUBLE -- Trade sqm/employee at urban fringe
        Aoff_cc = plan_nonres.getAttribute("Aoff_cc").getDouble()                           #DOUBLE -- Offices sqm/employee at city centre
        Aoff_uf = plan_nonres.getAttribute("Aoff_uf").getDouble()                           #DOUBLE -- Offices sqm/employee at urban fringe
        Alind_cc = plan_nonres.getAttribute("Alind_cc").getDouble()                         #DOUBLE -- Light industry sqm/employee at city centre
        Alind_uf = plan_nonres.getAttribute("Alind_uf").getDouble()                         #DOUBLE -- Light industry sqm/employee at urban fringe
        Ahind_cc = plan_nonres.getAttribute("Ahind_cc").getDouble()                         #DOUBLE -- Heavy industry sqm/employee at city centre
        Ahind_uf = plan_nonres.getAttribute("Ahind_uf").getDouble()                         #DOUBLE -- Heavy industry sqm/employee at urban fringe
        ddecay_type = plan_nonres.getAttribute("ddecay_type").getString()                   #STRING -- distance decay relationship
        
        com_fsetback_min = plan_nonres.getAttribute("com_fsetback_min").getDouble()         #DOUBLE -- minimum front setback [m]
        com_setback_auto = bool(plan_nonres.getAttribute("com_setback_auto"))         #BOOL -- determine setback automatically?
        com_floors_max = plan_nonres.getAttribute("com_floors_max").getDouble()             #DOUBLE -- maximum allowable floors
        
        com_carpark_dmin = plan_nonres.getAttribute("com_carpark_dmin").getDouble()          #DOUBLE -- minimum depth of frontage parking area [m]
        com_carparkW = plan_nonres.getAttribute("com_carparkW").getDouble()                  #DOUBLE -- minimum width of one parking lot
        com_carparkD = plan_nonres.getAttribute("com_carparkD").getDouble()                  #DOUBLE -- minimum depth of one parking lot
        com_carpark_avgimp = plan_nonres.getAttribute("com_carpark_avgimp").getDouble()      #DOUBLE -- avg. imperviousness of parking area
        com_carpark_share = bool(plan_nonres.getAttribute("com_carpark_share"))       #BOOL -- share carparks if multiple zones?
        com_service_dmin = plan_nonres.getAttribute("com_service_dmin").getDouble()          #DOUBLE -- minimum depth of service area
        
        access_perp = bool(plan_nonres.getAttribute("access_perp"))                   #BOOL -- access road aligned perpendicular
        access_parall = bool(plan_nonres.getAttribute("access_parall"))               #BOOL -- access road aligned parallel
        access_cds = bool(plan_nonres.getAttribute("access_cds"))                     #BOOL -- access road cul-de sacs
        access_parall_medwidth = plan_nonres.getAttribute("access_parall_medwidth").getDouble()   #DOUBLE -- median width if access rd aligned parallel
        access_cds_circlerad = plan_nonres.getAttribute("access_cds_circlerad").getDouble() #DOUBLE -- turning circle radius in cul-de-sac
        access_ped_include = bool(plan_nonres.getAttribute("access_ped_include"))     #BOOL -- include pedestrian paths along service roads?
        
        lscape_hsbal = plan_nonres.getAttribute("lscape_hsbal").getDouble()                 #DOUBLE -- balance between hard & soft landscapes
        lscape_avgimp_dced = plan_nonres.getAttribute("lscape_avgimp_dced").getDouble()     #DOUBLE -- avg. imperviousness disconnected
        
        #===-----------------
        strvec = city.getUUIDsOfComponentsInView(self.planSpaces)
        plan_space = city.getComponent(strvec[0])
        
        w_comfootpath_min = plan_space.getAttribute("w_comfootpath_min").getDouble()        #DOUBLE
        w_comfootpath_max = plan_space.getAttribute("w_comfootpath_max").getDouble()        #DOUBLE
        w_comnaturestrip_min = plan_space.getAttribute("w_comnaturestrip_min").getDouble()  #DOUBLE
        w_comnaturestrip_max = plan_space.getAttribute("w_comnaturestrip_max").getDouble()  #DOUBLE
        w_comfootpath_med = bool(plan_space.getAttribute("w_comfootpath_med"))        #BOOL -- to simplify things, just use median footpath width?
        w_comnaturestrip_med = bool(plan_space.getAttribute("w_comnaturestrip_med"))  #BOOL -- to simplify things, just use median naturestrip width?
        
        w_collectlane_min = plan_space.getAttribute("w_collectlane_min").getDouble()        #DOUBLE
        w_collectlane_max = plan_space.getAttribute("w_collectlane_max").getDouble()        #DOUBLE
        w_collectlane_med = bool(plan_space.getAttribute("w_collectlane_med"))        #BOOL
        collect_crossfall = plan_space.getAttribute("collect_crossfall").getDouble()        #DOUBLE
        
        
        #--------------------------------------------------------------------------------#
        #       BEGIN LOOPING ACROSS ALL BLOCKS IN MAP                                   #
        #--------------------------------------------------------------------------------#
        
        for i in range(int(blocks_num)):
            currentID = i + 1
            currentAttList = self.getBlockUUID(currentID,city)#blockcityin.getAttributes("BlockID"+str(currentID))        #attribute list of current block structure
            #currentPatchList = patchcityin.getAttributes("PatchDataID"+str(currentID))
            nonres_attr = Component()
	    city.addComponent(nonres_attr,self.nonResidential)
            nonres_attr.addAttribute("BlockID", currentID)
	    currentAttList.addAttribute("NonResidentialID", nonres_attr.getUUID())
            block_AActive = blocks_size * blocks_size * (currentAttList.getAttribute("Activity").getDouble()/100)

            #--------------------------------------------------------------------------------#
            #            CONDITIONAL CHECK TO SEE IF CURRENT BLOCK IS RELEVANT               #
            #--------------------------------------------------------------------------------#
            #2 conditions to skip: (1) status = 0, (2) no industrial/trade area
	    block_status = currentAttList.getAttribute("Status").getDouble()
	    landclassvec = currentAttList.getAttribute("Area_Landclass").getDoubleVector()

            tot_nonres_area = landclassvec[1] + landclassvec[2] \
		+ landclassvec[3] + landclassvec[4]
            if block_status == 0 or tot_nonres_area == 0:
                print "BlockID"+str(currentID)+" not active or no relevant non-res area"
		nonres_attr.addAttribute("HasNonRes", 0)
                continue
            #IF NOT SKIPPED, PLAN URBAN FORM
            nonres_attr.addAttribute("HasNonRes", 1)
            
            #--------------------------------------------------------------------------------#
            #            SETUP DATA - RETRIEVE FROM BLOCKCITY AND SAMPLE VALUES              #
            #--------------------------------------------------------------------------------#
            
            trad_area_tot = float(landclassvec[1])     #Total Trade Area
            ORC_area_tot = float(landclassvec[2])       #Total ORC Area
            LI_area_tot = float(landclassvec[3])         #Total Light Industry Area
            HI_area_tot = float(landclassvec[4])         #Total Heavy Industry Area
            total_industrial_area = LI_area_tot + HI_area_tot
            total_commercial_area = trad_area_tot + ORC_area_tot
            if total_industrial_area != 0:
                nonres_attr.addAttribute("HasIndustry", 1)
            if total_commercial_area != 0:
                nonres_attr.addAttribute("HasCommercial", 1)
                
                
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
            
            
            nonres_attr.addAttribute("AIndustry", total_industrial_area)
            nonres_attr.addAttribute("ACommercial", total_commercial_area)
            nonres_attr.addAttribute("AImp_Ind", Aimp_ind)
            nonres_attr.addAttribute("AImp_Com", Aimp_com)
            
            #-----------------------------------------------------------------#
            #        Write all updated Attribute Lists to the output          #
            #-----------------------------------------------------------------#
                
            #nonresidential.setAttributes("BlockID"+str(currentID),nonres_attr)
            
            #FOR LOOP END (Repeat for next BlockID)
            
        #END OF MODULE
    
            
            
            
            
