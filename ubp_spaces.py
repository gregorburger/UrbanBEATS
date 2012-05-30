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
        self.blockcityin = VectorDataIn
        self.spaces = VectorDataIn
        self.patchcityin = VectorDataIn
        self.planningrules = VectorDataIn
        self.addParameter(self, "blockcityin", VIBe2.VECTORDATA_IN)
        self.addParameter(self, "spaces", VIBe2.VECTORDATA_OUT)
        self.addParameter(self, "patchcityin", VIBe2.VECTORDATA_IN)
        self.addParameter(self, "planningrules", VIBe2.VECTORDATA_IN)
    
    
    def run(self):
        #Get Vector Data
        blockcityin = self.blockcityin.getItem()
        spaces = self.spaces.getItem()
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
        
        plan_spaces = planningrules.getAttributes("SpacesRules")
        
        pg_clustering_degree = plan_spaces.getAttribute("pg_clustering_degree")         #DOUBLE -- degree of clustering, 0=low, 1=medium, 2=high
        pg_greengrey_ratio = plan_spaces.getAttribute("pg_greengrey_ratio")             #DOUBLE -- balance between green and grey spaces -10=fully grey, +10=fully green
        pg_linear_threshold = plan_spaces.getAttribute("pg_linear_threshold")           #DOUBLE -- ratio threshold to consider open space as "linear"
        
        pg_footpath_cross = plan_spaces.getAttribute("pg_footpath_cross")               #BOOL
        pg_footpath_circle = plan_spaces.getAttribute("pg_footpath_circle")             #BOOL
        pg_footpath_perimeter = plan_spaces.getAttribute("pg_footpath_perimeter")       #BOOL
        pg_circle_radius = plan_spaces.getAttribute("pg_circle_radius")                 #DOUBLE -- radius of circle footpath if chosen [% of park width]
        pg_circle_accesses = plan_spaces.getAttribute("pg_circle_accesses")             #DOUBLE -- no. of access routes from boundary to circle
        pg_perimeter_setback = plan_spaces.getAttribute("pg_perimeter_setback")         #DOUBLE -- setback of perimeter footpath if chosen [% of park width]
        pg_perimeter_accesses = plan_spaces.getAttribute("pg_perimeter_accesses")       #DOUBLE -- no. of access routes from boundary to perimeter footpath
        pg_footpath_avgW = plan_spaces.getAttribute("pg_footpath_avgW")                 #DOUBLE -- average width of the footpath
        pg_footpath_impdced = plan_spaces.getAttribute("pg_footpath_impdced")           #DOUBLE -- avg. prop of imperviousness disconnected from footpath
        pg_footpath_varyW = plan_spaces.getAttribute("pg_footpath_varyW")               #BOOL -- vary the width of the footpath?
        pg_footpath_multiply = plan_spaces.getAttribute("pg_footpath_multiply")         #BOOL -- multiply footpaths if green space is classed as linear?
        
        rfw_partialimp_check = plan_spaces.getAttribute("rfw_partialimp_check")         #BOOL -- assume the area is partially impervious
        rfw_partialimp = plan_spaces.getAttribute("rfw_partialimp")                     #DOUBLE -- set the partially impervious value [%]
        rfw_areausable_check = plan_spaces.getAttribute("rfw_areausable_check")         #BOOL -- restrict some of the usable area
        rfw_areausable = plan_spaces.getAttribute("rfw_areausable")                     #DOUBLE -- set the amount of area that can be used [%]
        
        unc_merge = plan_spaces.getAttribute("unc_merge")                               #BOOL
        unc_unc2square = plan_spaces.getAttribute("unc_unc2square")                     #BOOL
        unc_unc2square_weight = plan_spaces.getAttribute("unc_unc2square_weight")       #DOUBLE
        unc_unc2park = plan_spaces.getAttribute("unc_unc2park")                         #BOOL
        unc_unc2park_weight = plan_spaces.getAttribute("unc_unc2park_weight")           #DOUBLE
        unc_unc2road = plan_spaces.getAttribute("unc_unc2road")                         #BOOL
        unc_unc2road_weight = plan_spaces.getAttribute("unc_unc2road_weight")           #DOUBLE
        unc_landmark = plan_spaces.getAttribute("unc_landmark")                         #BOOL
        unc_landmark_threshold = plan_spaces.getAttribute("unc_landmark_threshold")     #DOUBLE
        unc_landmark_avgimp = plan_spaces.getAttribute("unc_landmark_avgimp")           #DOUBLE
        unc_landmark_otherwater = plan_spaces.getAttribute("unc_landmark_otherwater")   #BOOL
        
        und_whattodo = plan_spaces.getStringAttribute("und_whattodo")                   #STRING -- what to do with this land? N= do not touch, Y = allow
        und_allowspace = plan_spaces.getAttribute("und_allowspace")                     #DOUBLE -- allowable space to be used for technologies
        und_autodeterminetype = plan_spaces.getAttribute("und_autodeterminetype")       #BOOL -- automatically determine type based on distance from city centre
        
        #===-----------------
        
        w_resfootpath_min = plan_spaces.getAttribute("w_resfootpath_min")        #DOUBLE
        w_resfootpath_max = plan_spaces.getAttribute("w_resfootpath_max")        #DOUBLE
        w_resnaturestrip_min = plan_spaces.getAttribute("w_resnaturestrip_min")  #DOUBLE
        w_resnaturestrip_max = plan_spaces.getAttribute("w_resnaturestrip_max")  #DOUBLE
        w_resfootpath_med = plan_spaces.getAttribute("w_resfootpath_med")        #BOOL -- to simplify things, just use median footpath width?
        w_resnaturestrip_med = plan_spaces.getAttribute("w_resnaturestrip_med")  #BOOL -- to simplify things, just use median naturestrip width?
        
        w_collectlane_min = plan_spaces.getAttribute("w_collectlane_min")        #DOUBLE
        w_collectlane_max = plan_spaces.getAttribute("w_collectlane_max")        #DOUBLE
        w_collectlane_med = plan_spaces.getAttribute("w_collectlane_med")        #BOOL
        collect_crossfall = plan_spaces.getAttribute("collect_crossfall")        #DOUBLE
        
        w_artlane_min = plan_spaces.getAttribute("w_artlane_min")                #DOUBLE
        w_artlane_max = plan_spaces.getAttribute("w_artlane_max")                #DOUBLE
        w_artlane_med = plan_spaces.getAttribute("w_artlane_med")                #BOOL
        w_artmedian = plan_spaces.getAttribute("w_artmedian")                    #DOUBLE
        artmedian_reserved = plan_spaces.getAttribute("artmedian_reserved")      #BOOL
        art_crossfall = plan_spaces.getAttribute("art_crossfall")                #DOUBLE
        
        w_hwylane_avg = plan_spaces.getAttribute("w_hwylane_avg")                #DOUBLE
        w_hwymedian = plan_spaces.getAttribute("w_hwymedian")                    #DOUBLE
        hwy_buffered = plan_spaces.getAttribute("hwy_buffered")                  #BOOL
        hwymedian_reserved = plan_spaces.getAttribute("hwymedian_reserved")      #BOOL
        hwy_crossfall = plan_spaces.getAttribute("hwy_crossfall")                #DOUBLE
        
        
        #--------------------------------------------------------------------------------#
        #       BEGIN LOOPING ACROSS ALL BLOCKS IN MAP                                   #
        #--------------------------------------------------------------------------------#
        
        for i in range(int(blocks_num)):
            currentID = i + 1
            currentAttList = blockcityin.getAttributes("BlockID"+str(currentID))        #attribute list of current block structure
            currentPatchList = patchcityin.getAttributes("PatchDataID"+str(currentID))
            spaces_attr = Attribute()
            spaces_attr.setAttribute("BlockID", currentID)
            block_AActive = blocks_size * blocks_size * (currentAttList.getAttribute("Activity")/100)

            #--------------------------------------------------------------------------------#
            #            CONDITIONAL CHECK TO SEE IF CURRENT BLOCK IS RELEVANT               #
            #--------------------------------------------------------------------------------#
            
            block_status = currentAttList.getAttribute("Status")
            total_space_area = currentAttList.getAttribute("ALUC_NA") + currentAttList.getAttribute("ALUC_Rd") \
                + currentAttList.getAttribute("ALUC_PG") + currentAttList.getAttribute("ALUC_RFlood") + currentAttList.getAttribute("ALUC_Und")
            if block_status == 0 or total_space_area == 0:              #2 conditions to skip: (1) status = 0, (2) no spaces areas
                print "BlockID"+str(currentID)+" is not active in simulation"
                continue
            #IF NOT SKIPPED, PLAN URBAN FORM
            spaces_attr.setAttribute("HasSpaces", 1)
              
            
            #--------------------------------------------------------------------------------#
            #            SETUP DATA - RETRIEVE FROM BLOCKCITY AND SAMPLE VALUES              #
            #--------------------------------------------------------------------------------#
  
            rd_area_map = float(currentAttList.getAttribute("ALUC_Rd"))
            pg_area_tot = float(currentAttList.getAttribute("ALUC_PG"))
            RFlood_area_tot = float(currentAttList.getAttribute("ALUC_RFlood"))
            und_area_tot = float(currentAttList.getAttribute("ALUC_Und"))
            
            unc_area_total = float(currentAttList.getAttribute("ALUC_NA"))
            unc_area_pop = currentAttList.getAttribute("POP_NA")
              
            #--------------------------------------------------------------------------------#
            #            DEAL WITH UNCLASSIFIED AREA FIRST                                   #
            #--------------------------------------------------------------------------------#
            
            ### REDISTRIBUTE UNCLASSIFIED AREA ==============================================#
            
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
                        
                        currentAttList.setAttribute("Landmark", "Yes")              #for now
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
                spaces_attr.setAttribute("rfw_Adev", rfw_Adev)
                
            
            #-----------------------------------------------------------------#
            #        Write all updated Attribute Lists to the output          #
            #-----------------------------------------------------------------#
                
            spaces.setAttributes("BlockID"+str(currentID),spaces_attr)
            
            #FOR LOOP END (Repeat for next BlockID)
            
        #END OF MODULE
    
             