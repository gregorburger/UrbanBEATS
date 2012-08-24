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

class ubp_spaces(Module):
    """Description of class
	
    Description of Inputs & Outputs 
	- <description of inputs/outputs>
    
    Log of Updates made at each version:
    
    v0.80 (March 2012):
        - Created ubp_spaces.py
        - Contains the code that used to be in urbplanbb.py for "Open Spaces", i.e. roads, parks, reserves, undeveloped, unclassified
        - Now handles the these districts that urbplanbb.py initially did for more modularity
    
	@ingroup DAnCE4Water
	@author Peter M Bach
	"""
    def __init__(self):
        Module.__init__(self)
        #input/output data - each planning module has as input BLOCKS, PATCHES, RULES
        #                  - each planning module has as output: updated BLOCKS
        #                  - PATCHES are passed on from UrbplanBB straight through (not modified)
	self.blocks = View("Block",FACE,WRITE)
	self.blocks.getAttribute("BlockID")
	self.blocks.addAttribute("Landmark")

	self.mapattributes = View("Mapattributes",COMPONENT,READ)
    	self.mapattributes.getAttribute("NumBlocks")
	self.mapattributes.getAttribute("BlockSize")
	self.mapattributes.getAttribute("WidthBlocks")
	self.mapattributes.getAttribute("HeightBlocks")
	self.mapattributes.getAttribute("InputReso")

	self.planGen = View("PlanGen", COMPONENT, READ)
        self.planGen.getAttribute("maximperv")
        self.planGen.getAttribute("maxsitecover")
        self.planGen.getAttribute("locality_mun_trans")

	self.planSpaces = View("PlanSpaces",COMPONENT,READ)
	self.planSpaces.getAttribute("pg_clustering_degree")
	self.planSpaces.getAttribute("pg_greengrey_ratio")
	self.planSpaces.getAttribute("pg_linear_threshold")
	self.planSpaces.getAttribute("pg_footpath_cross")
  	self.planSpaces.getAttribute("pg_footpath_circle")
	self.planSpaces.getAttribute("pg_footpath_perimeter") 
	self.planSpaces.getAttribute("pg_circle_radius") 
	self.planSpaces.getAttribute("pg_circle_accesses") 
	self.planSpaces.getAttribute("pg_perimeter_setback") 
	self.planSpaces.getAttribute("pg_perimeter_accesses")
	self.planSpaces.getAttribute("pg_footpath_avgW")  
	self.planSpaces.getAttribute("pg_footpath_impdced") 
	self.planSpaces.getAttribute("pg_footpath_varyW")  
	self.planSpaces.getAttribute("pg_footpath_multiply") 
	self.planSpaces.getAttribute("rfw_partialimp_check")  
	self.planSpaces.getAttribute("rfw_partialimp")    
	self.planSpaces.getAttribute("rfw_areausable_check") 
	self.planSpaces.getAttribute("rfw_areausable")     
	self.planSpaces.getAttribute("unc_merge") 
	self.planSpaces.getAttribute("unc_unc2square")    
	self.planSpaces.getAttribute("unc_unc2square_weight")
	self.planSpaces.getAttribute("unc_unc2park")
	self.planSpaces.getAttribute("unc_unc2park_weight")
	self.planSpaces.getAttribute("unc_unc2road") 
	self.planSpaces.getAttribute("unc_unc2road_weight")
	self.planSpaces.getAttribute("unc_landmark")
	self.planSpaces.getAttribute("unc_landmark_threshold")
	self.planSpaces.getAttribute("unc_landmark_avgimp")
	self.planSpaces.getAttribute("unc_landmark_otherwater") 
	self.planSpaces.getAttribute("und_whattodo")
	self.planSpaces.getAttribute("und_allowspace") 
	self.planSpaces.getAttribute("und_autodeterminetype")
	self.planSpaces.getAttribute("w_resfootpath_min") 
        self.planSpaces.getAttribute("w_resfootpath_max") 
        self.planSpaces.getAttribute("w_resnaturestrip_min") 
        self.planSpaces.getAttribute("w_resnaturestrip_max") 
        self.planSpaces.getAttribute("w_resfootpath_med") 
        self.planSpaces.getAttribute("w_resnaturestrip_med") 
        self.planSpaces.getAttribute("w_collectlane_min")
        self.planSpaces.getAttribute("w_collectlane_max")
        self.planSpaces.getAttribute("w_collectlane_med")
        self.planSpaces.getAttribute("collect_crossfall")
        self.planSpaces.getAttribute("w_artlane_min")
        self.planSpaces.getAttribute("w_artlane_max")
        self.planSpaces.getAttribute("w_artlane_med")
        self.planSpaces.getAttribute("w_artmedian")
        self.planSpaces.getAttribute("artmedian_reserved")
        self.planSpaces.getAttribute("art_crossfall")
        self.planSpaces.getAttribute("w_hwylane_avg")
        self.planSpaces.getAttribute("w_hwymedian")
        self.planSpaces.getAttribute("hwy_buffered")
        self.planSpaces.getAttribute("hwymedian_reserved")
        self.planSpaces.getAttribute("hwy_crossfall") 

	self.spacesAttr = View("Spaces",COMPONENT,WRITE)
	self.spacesAttr.addAttribute("BlockID")
	self.spacesAttr.addAttribute("HasSpaces")
	self.spacesAttr.addAttribute("rfw_Adev")
	

	#Datastream
	datastream = []
	datastream.append(self.blocks)
	datastream.append(self.mapattributes)
	datastream.append(self.planSpaces)
	datastream.append(self.spacesAttr)
	datastream.append(self.planGen)
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
        blocks_size = map_attr.getAttribute("BlockSize").getDouble()     #size of block
        map_w = map_attr.getAttribute("WidthBlocks").getDouble()         #num of blocks wide
        map_h = map_attr.getAttribute("HeightBlocks").getDouble()        #num of blocks tall
        input_res = map_attr.getAttribute("InputReso").getDouble()       #resolution of input data

        
        
        #--------------------------------------------------------------------------------#
        #       DISASSEMBLE PLANNING RULES INTO USABLE FORMAT FROM PREVIOUS MODULE       #
        #--------------------------------------------------------------------------------#
        strvec = city.getUUIDsOfComponentsInView(self.planGen)  
        plan_gen = city.getComponent(strvec[0])
        
        maximperv = plan_gen.getAttribute("maximperv").getDouble()                          #DOUBLE -- maximum site imperviousness [%]
        maxsitecover = plan_gen.getAttribute("maxsitecover").getDouble()                    #DOUBLE -- maximum site cover [%]
        lcality_mun_trans = bool(plan_gen.getAttribute("locality_mun_trans"))         #BOOL -- locality map for municipal & transport?
        
        #===-----------------
        strvec = city.getUUIDsOfComponentsInView(self.planSpaces)
        plan_spaces = city.getComponent(strvec[0])
        
        pg_clustering_degree = plan_spaces.getAttribute("pg_clustering_degree").getDouble()          #DOUBLE -- degree of clustering, 0=low, 1=medium, 2=high
        pg_greengrey_ratio = plan_spaces.getAttribute("pg_greengrey_ratio").getDouble()              #DOUBLE -- balance between green and grey spaces -10=fully grey, +10=fully green
        pg_linear_threshold = plan_spaces.getAttribute("pg_linear_threshold").getDouble()            #DOUBLE -- ratio threshold to consider open space as "linear"
        
        pg_footpath_cross = bool(plan_spaces.getAttribute("pg_footpath_cross"))               #BOOL
        pg_footpath_circle = bool(plan_spaces.getAttribute("pg_footpath_circle"))             #BOOL
        pg_footpath_perimeter = bool(plan_spaces.getAttribute("pg_footpath_perimeter"))       #BOOL
        pg_circle_radius = plan_spaces.getAttribute("pg_circle_radius").getDouble()                  #DOUBLE -- radius of circle footpath if chosen [% of park width]
        pg_circle_accesses = plan_spaces.getAttribute("pg_circle_accesses").getDouble()              #DOUBLE -- no. of access routes from boundary to circle
        pg_perimeter_setback = plan_spaces.getAttribute("pg_perimeter_setback").getDouble()          #DOUBLE -- setback of perimeter footpath if chosen [% of park width]
        pg_perimeter_accesses = plan_spaces.getAttribute("pg_perimeter_accesses").getDouble()        #DOUBLE -- no. of access routes from boundary to perimeter footpath
        pg_footpath_avgW = plan_spaces.getAttribute("pg_footpath_avgW").getDouble()                  #DOUBLE -- average width of the footpath
        pg_footpath_impdced = plan_spaces.getAttribute("pg_footpath_impdced").getDouble()            #DOUBLE -- avg. prop of imperviousness disconnected from footpath
        pg_footpath_varyW = bool(plan_spaces.getAttribute("pg_footpath_varyW"))                #BOOL -- vary the width of the footpath?
        pg_footpath_multiply = bool(plan_spaces.getAttribute("pg_footpath_multiply"))          #BOOL -- multiply footpaths if green space is classed as linear?
        
        rfw_partialimp_check = bool(plan_spaces.getAttribute("rfw_partialimp_check"))         #BOOL -- assume the area is partially impervious
        rfw_partialimp = plan_spaces.getAttribute("rfw_partialimp").getDouble()                      #DOUBLE -- set the partially impervious value [%]
        rfw_areausable_check = bool(plan_spaces.getAttribute("rfw_areausable_check"))         #BOOL -- restrict some of the usable area
        rfw_areausable = plan_spaces.getAttribute("rfw_areausable").getDouble()                      #DOUBLE -- set the amount of area that can be used [%]
        
        unc_merge = bool(plan_spaces.getAttribute("unc_merge"))                               #BOOL
        unc_unc2square = bool(plan_spaces.getAttribute("unc_unc2square"))                     #BOOL
        unc_unc2square_weight = plan_spaces.getAttribute("unc_unc2square_weight").getDouble()        #DOUBLE
        unc_unc2park = bool(plan_spaces.getAttribute("unc_unc2park"))                         #BOOL
        unc_unc2park_weight = plan_spaces.getAttribute("unc_unc2park_weight").getDouble()            #DOUBLE
        unc_unc2road = bool(plan_spaces.getAttribute("unc_unc2road"))                         #BOOL
        unc_unc2road_weight = plan_spaces.getAttribute("unc_unc2road_weight").getDouble()            #DOUBLE
        unc_landmark = bool(plan_spaces.getAttribute("unc_landmark"))                         #BOOL
        unc_landmark_threshold = plan_spaces.getAttribute("unc_landmark_threshold").getDouble()      #DOUBLE
        unc_landmark_avgimp = plan_spaces.getAttribute("unc_landmark_avgimp").getDouble()            #DOUBLE
        unc_landmark_otherwater = bool(plan_spaces.getAttribute("unc_landmark_otherwater"))   #BOOL
        
        und_whattodo = plan_spaces.getAttribute("und_whattodo").getString()                   #STRING -- what to do with this land? N= do not touch, Y = allow
        und_allowspace = plan_spaces.getAttribute("und_allowspace").getDouble()                      #DOUBLE -- allowable space to be used for technologies
        und_autodeterminetype = bool(plan_spaces.getAttribute("und_autodeterminetype"))       #BOOL -- automatically determine type based on distance from city centre
        
        #===-----------------
        
        w_resfootpath_min = plan_spaces.getAttribute("w_resfootpath_min").getDouble()         #DOUBLE
        w_resfootpath_max = plan_spaces.getAttribute("w_resfootpath_max").getDouble()         #DOUBLE
        w_resnaturestrip_min = plan_spaces.getAttribute("w_resnaturestrip_min").getDouble()   #DOUBLE
        w_resnaturestrip_max = plan_spaces.getAttribute("w_resnaturestrip_max").getDouble()   #DOUBLE
        w_resfootpath_med = bool(plan_spaces.getAttribute("w_resfootpath_med"))        #BOOL -- to simplify things, just use median footpath width?
        w_resnaturestrip_med = bool(plan_spaces.getAttribute("w_resnaturestrip_med"))  #BOOL -- to simplify things, just use median naturestrip width?
        
        w_collectlane_min = plan_spaces.getAttribute("w_collectlane_min").getDouble()         #DOUBLE
        w_collectlane_max = plan_spaces.getAttribute("w_collectlane_max").getDouble()         #DOUBLE
        w_collectlane_med = bool(plan_spaces.getAttribute("w_collectlane_med"))        #BOOL
        collect_crossfall = plan_spaces.getAttribute("collect_crossfall").getDouble()         #DOUBLE
        
        w_artlane_min = plan_spaces.getAttribute("w_artlane_min").getDouble()                 #DOUBLE
        w_artlane_max = plan_spaces.getAttribute("w_artlane_max").getDouble()                 #DOUBLE
        w_artlane_med = bool(plan_spaces.getAttribute("w_artlane_med"))                #BOOL
        w_artmedian = plan_spaces.getAttribute("w_artmedian").getDouble()                     #DOUBLE
        artmedian_reserved = bool(plan_spaces.getAttribute("artmedian_reserved"))      #BOOL
        art_crossfall = plan_spaces.getAttribute("art_crossfall").getDouble()                 #DOUBLE
        
        w_hwylane_avg = plan_spaces.getAttribute("w_hwylane_avg").getDouble()                 #DOUBLE
        w_hwymedian = plan_spaces.getAttribute("w_hwymedian").getDouble()                     #DOUBLE
        hwy_buffered = bool(plan_spaces.getAttribute("hwy_buffered"))                   #BOOL
        hwymedian_reserved = bool(plan_spaces.getAttribute("hwymedian_reserved"))      #BOOL
        hwy_crossfall = plan_spaces.getAttribute("hwy_crossfall").getDouble()                 #DOUBLE
        
        
        #--------------------------------------------------------------------------------#
        #       BEGIN LOOPING ACROSS ALL BLOCKS IN MAP                                   #
        #--------------------------------------------------------------------------------#
        
        for i in range(int(blocks_num)):
            currentID = i + 1
            currentAttList = self.getBlockUUID(currentID,city)        #attribute list of current block structure
            #currentPatchList = patchcityin.getAttributes("PatchDataID"+str(currentID))
            spaces_attr = Component()
	    city.addComponent(spaces_attr,self.spacesAttr)        
	    spaces_attr.addAttribute("BlockID", currentID)
            block_AActive = blocks_size * blocks_size * (currentAttList.getAttribute("Activity").getDouble()/100)

            #--------------------------------------------------------------------------------#
            #            CONDITIONAL CHECK TO SEE IF CURRENT BLOCK IS RELEVANT               #
            #--------------------------------------------------------------------------------#
            # THIS MODULE WILL RUN IF THE BLOCK HAS:
            #   - Road area: ALUC_Rd > 0
            #   - Parks & Gardens Area: ALUC_PG > 0
            #   - Reserves & Floodways Area: ALUC_RFlood > 0
            #   - Undeveloped Area: ALUC_Und > 0
            #   - Unclassified Area: ALUC_NA > 0
            #--------------------------------------------------------------------------------#
            
            block_status = currentAttList.getAttribute("Status").getDouble()
	    landclassvec = currentAttList.getAttribute("Area_Landclass").getDoubleVector()
            total_space_area = landclassvec[13] + landclassvec[8] \
                + landclassvec[10] + landclassvec[11] + landclassvec[12]
            if block_status == 0 or total_space_area == 0:              #2 conditions to skip: (1) status = 0, (2) no spaces areas
                print "BlockID"+str(currentID)+" is not active in simulation"
                continue
            #IF NOT SKIPPED, PLAN URBAN FORM
            spaces_attr.addAttribute("HasSpaces", 1)
              
            
            #--------------------------------------------------------------------------------#
            #            SETUP DATA - RETRIEVE FROM BLOCKCITY AND SAMPLE VALUES              #
            #--------------------------------------------------------------------------------#
  
            rd_area_map = float(landclassvec[8])
            pg_area_tot = float(landclassvec[10])
            RFlood_area_tot = float(landclassvec[11])
            und_area_tot = float(landclassvec[12])
            
            unc_area_total = float(landclassvec[13])
	    landclassvec = currentAttList.getAttribute("PopulationDensity_Landclass").getDoubleVector()
            unc_area_pop = landclassvec[13]
              
            #--------------------------------------------------------------------------------#
            #            DEAL WITH UNCLASSIFIED AREA FIRST                                   #
            #--------------------------------------------------------------------------------#
            
            ### REDISTRIBUTE UNCLASSIFIED AREA ==============================================#
            extra_road = 0	#compiler throws an error because there could be a case where this variable could no be declared and so in line 356 he wouldnt know "extra_road"
            if unc_area_total == 0:
                extra_square = 0
                extra_park = 0
                extra_road = 0
            else:
                ### LANDMARK CASE ###
                #Determine Conditions for treatment of unclassified land
                if unc_landmark == True:                              #if landmark? then all areas used for this
                    #commands: check size of unc first before considering as landmark
                    unc_thresh_area = unc_landmark_threshold/100 * block_AActive
                    if unc_area_total >= unc_thresh_area:
                        unc_Aimp = unc_landmark_avgimp/100 * unc_area_total   #calculates impervious area
                        unc_Aeimp = unc_Atimp * (1 - lscape_avgimp_dced)   #calculate effective impervious area using commercial value
                        unc_Aperv = unc_area_total - unc_Aimp
                        unc_EIF = unc_Aeipm/unc_area_total
                            
                        if unc_landmark_otherwater == True:                #!!!!!consider putting this in the ppa module
                            pass
                            #rules for other water demand
                        else:
                            pass
                            #tally up total green area for watering
                        
                        currentAttList.addAttribute("Landmark", "Yes")              #for now
    #                    currentAttList.setAttribute("LMark_TIF", unc_landmark_avgimp/100)     #Additional Landmark attributes if this is of interest
    #                    currentAttList.setAttribute("LMark_EIF", unc_EIF)
    #                    currentAttList.setAttribute("LMark_IA", unc_Atimp)
    #                    currentAttList.setAttribute("LMark_EIA", unc_Aeimp)
                else:
                    ### MERGE CASE ###
                    #if not a landmark, merge as square, park or road
                    total_weights = unc_unc2square_weight*unc_unc2square + \
                     unc_unc2park_weight*unc_unc2park + \
                     unc_unc2road_weight*unc_unc2road
                        
                    p_U2S = unc_unc2square*unc_unc2square_weight/total_weights        #proportions weighted against True/False again
                    extra_square = unc_area_total * p_U2S                                       #if not checked, no extra area because of 0 multiply
                    p_U2P = unc_unc2park*unc_unc2park_weight/total_weights
                    extra_park = unc_area_total * p_U2P
                    p_U2R = unc_unc2road*unc_unc2road_weight/total_weights
                    extra_road = unc_area_total * p_U2R
                    
                    if total_weights == 0:                      #if no option checked, total_weights is zero
                        extra_undev = unc_area_total            #if none of the options are ticked, area assumed completely open
                
                    
                #attributes are not written to the vector because this will be transferred to the next land zones
            
            ### ROAD AREAS ==============================================================================#
            
            rd_area_tot = rd_area_map + extra_road            #add unclassified land merged as road into total road area
            
            if rd_area_tot == 0:
                pass
            else:
                pass
            
            #get patch data
            
            
            ### OPEN SPACES >> PARKS & GARDENS =======================================================#
            
            if pg_area_tot == 0:
                pass
            else:
                pass
                #use clustering degree, green-grey ratio and linear threshold to determine park characteristics
                #in particular the number of grey to green spaces in this particular block
            
                #use for each park, pick a random footpath config from the list and go through the park desiging footpaths
                    #tally up the total green area, total footpath area
                    #tally up the total imperviousness, effective imperviousness
                    #make sure if green space is linear to multiply the footpaths
             
            #Get patch data 
             
             
            
            ### OPEN SPACES >> RESERVES & FLOODWAYS =======================================================#
            
            #DO THE RESERVES THING
            if RFlood_area_tot == 0:
                pass
            else:
                if rfw_partialimp_check == True:
                    #if reserve is partially impervious, calculate Aimp and Aeimp
                    rfw_Aimp = RFlood_area_tot * rfw_partialimp/100
                    rfw_Aeimp = rfw_Aimp * (1 - pg_footpath_impdced)
                    rfw_Aperv = RFlood_area_tot - rfw_Aimp
                else:
                    rfw_Aimp = 0
                    rfw_Aeimp = 0
                    rfw_Aperv = RFlood_area_tot
                if rfw_areausable_check == True:
                    #if the area is usable then calculate the amount of area that is usable
                    rfw_Adev = RFlood_area_tot * rfw_areausable/100
                else:
                    rfw_Adev = 0
            
            #get patch data
                    
                
            ### OPEN SPACES >> UNDEVELOPED AREAS =======================================================#
            
            if und_area_tot == 0:
                pass
            else:
                #determine type of undeveloped land based on distance from city centre
    #            urb_extent = map_attr.getAttribute("Sprawl_Extent")
    #            block_dist = currentAttList.getAttribute("CBD_Dist")
                
                #probability of a brownfield over a greenfield varies from definite one end to other as we move from CBD to 50% distance
                #therefore at 0% --> p_BF = 100%, 50% p_BF = 0%, p_GF = 0%, p_GF = 100%, decay on one only and calculate the other...
                
    #            p_BFoGF = -2*(block_dist/urb_extent) + 1            #Linear trend decay = -2x + 100, Exponential: 99e^-0.138x, Log: 
    #            p_AGoGF = -2*(1-block_dist/urb_extent) + 1          
                
                #probability of greenfield over agriculture varies from definite one end to other as we move from 50% to sprawl limit
                
    #            if block_dist/urb_extent < 0.5:
    #                if random.random() > p_BFoGF:           #if a random number between 0 and 1 is greater than probability of brownfield over greenfield
    #                    und_type = "GF"                     #then type is greenfield (if pBFoGF = 0.6 --> 60% chance of BF and 40% of GF)
    #                else:
    #                    und_type = "BF"
    #            else:
    #                if random.random() > p_AGoGF:
    #                    und_type = "GF"
    #                else:
    #                    und_type = "AG"
                
                #do something with the undeveloped space... decide based on inputs
                if und_whattodo == "Y":
                    und_Adev = und_allowance/100 * und_area_tot
                else:
                    und_Adev = 0
                
            #--------------------------------------------------------------------------------#
            #            TALLY UP INFO AND WRITE TO OUTPUT                                   #
            #--------------------------------------------------------------------------------#
            
            if RFlood_area_tot == 0:
                pass
            else:
                spaces_attr.addAttribute("rfw_Adev", rfw_Adev)
                
            
            #-----------------------------------------------------------------#
            #        Write all updated Attribute Lists to the output          #
            #-----------------------------------------------------------------#
                
            #spaces.setAttributes("BlockID"+str(currentID),spaces_attr)
            
            #FOR LOOP END (Repeat for next BlockID)
            
        #END OF MODULE
    
             
