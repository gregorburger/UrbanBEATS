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

class ubp_residential(Module):
    """Description of class
	
    Description of Inputs & Outputs 
	- <description of inputs/outputs>
    
    Log of Updates made at each version:
    
    v0.80 update (October 2011):
        - Created ubp_residential.py
        - Contains the code that used to be in urbplanbb.py for residential
        - Now handles the residential districts that urbplanbb.py initially did for more modularity
        
	@ingroup DAnCE4Water
	@author Peter M Bach
	"""
    def __init__(self):
        Module.__init__(self)
        #input/output data - each planning module has as input BLOCKS, PATCHES, RULES
        #                  - each planning module has as output: updated BLOCKS
        #                  - PATCHES are passed on from UrbplanBB straight through (not modified)
        self.blockcityin = VectorDataIn
        self.residential = VectorDataIn
        self.patchcityin = VectorDataIn
        self.planningrules = VectorDataIn
        self.addParameter(self, "blockcityin", VIBe2.VECTORDATA_IN)
        self.addParameter(self, "residential", VIBe2.VECTORDATA_OUT)
        self.addParameter(self, "patchcityin", VIBe2.VECTORDATA_IN)
        self.addParameter(self, "planningrules", VIBe2.VECTORDATA_IN)
    
    
    def run(self):
        #Get Vector Data
        blockcityin = self.blockcityin.getItem()
        residential = self.residential.getItem()
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
        
        plan_res = planningrules.getAttributes("ResidentialRules")
        
        occup_avg = plan_res.getAttribute("occup_avg")                          #DOUBLE -- average occupancy (house)
        occup_max = plan_res.getAttribute("occup_max")                          #DOUBLE -- maximum occupancy (house)
        person_space = plan_res.getAttribute("person_space")                    #DOUBLE -- space per person [sqm]
        extra_comm_area = plan_res.getAttribute("extra_comm_area")              #DOUBLE -- extra space for communal area
        
        setback_f_min = plan_res.getAttribute("setback_f_min")                  #DOUBLE -- minimum front setback
        setback_f_max = plan_res.getAttribute("setback_f_max")                  #DOUBLE -- maximum front setback
        setback_s_min = plan_res.getAttribute("setback_s_min")                  #DOUBLE -- minimum side setback (applies to rear as well)
        setback_s_max = plan_res.getAttribute("setback_s_max")                  #DOUBLE -- maximum side setback (applies to rear as well)
        
        carports_max = plan_res.getAttribute("carports_max")                    #DOUBLE -- max number of carports
        garage_incl = plan_res.getAttribute("garage_incl")                      #BOOL -- include garage? YES/NO
        w_driveway_min = plan_res.getAttribute("w_driveway_min")                #DOUBLE -- minimum driveway width [m]
        patio_area_max = plan_res.getAttribute("patio_area_max")                #DOUBLE -- maximum patio area [sqm]
        patio_covered = plan_res.getAttribute("patio_covered")                  #BOOL -- is patio covered by roof?
        floor_num_max = plan_res.getAttribute("floor_num_max")                  #DOUBLE -- maximum number of floors
        floor_autobuild = plan_res.getAttribute("floor_autobuild")              #BOOL -- autobuild floors?
        
        occup_flat_avg = plan_res.getAttribute("occup_flat_avg")                #DOUBLE -- average occupancy of apartment
        commspace_indoor = plan_res.getAttribute("commspace_indoor")            #DOUBLE -- communal space % indoor
        commspace_outdoor = plan_res.getAttribute("commspace_outdoor")          #DOUBLE -- communal space % outdoor
        flat_area_max = plan_res.getAttribute("flat_area_max")                  #DOUBLE -- maximum apartment size [sqm]
        setback_HDR_avg = plan_res.getAttribute("setback_HDR_avg")              #DOUBLE -- average setback for HDR site
        setback_HDR_auto = plan_res.getAttribute("setback_HDR_auto")            #BOOL -- determine setback for HDR automatically?
                
        roof_connected = plan_res.getStringAttribute("roof_connected")          #STRING -- how is the roof connected to drainage? Direct/Disconnected/Varied?
        imperv_prop_dced = plan_res.getAttribute("imperv_prop_dced")            #DOUBLE -- proportion of impervious area disconnected
        
        #===-----------------
        
        plan_space = planningrules.getAttributes("SpacesRules")
        
        w_resfootpath_min = plan_space.getAttribute("w_resfootpath_min")        #DOUBLE
        w_resfootpath_max = plan_space.getAttribute("w_resfootpath_max")        #DOUBLE
        w_resnaturestrip_min = plan_space.getAttribute("w_resnaturestrip_min")  #DOUBLE
        w_resnaturestrip_max = plan_space.getAttribute("w_resnaturestrip_max")  #DOUBLE
        w_resfootpath_med = plan_space.getAttribute("w_resfootpath_med")        #BOOL -- to simplify things, just use median footpath width?
        w_resnaturestrip_med = plan_space.getAttribute("w_resnaturestrip_med")  #BOOL -- to simplify things, just use median naturestrip width?
        
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
            res_attr = Attribute()
            res_attr.setAttribute("BlockID", currentID)
            block_AActive = blocks_size * blocks_size * (currentAttList.getAttribute("Activity")/100)
    
            #--------------------------------------------------------------------------------#
            #            CONDITIONAL CHECK TO SEE IF CURRENT BLOCK IS RELEVANT               #
            #--------------------------------------------------------------------------------#
            
            block_status = currentAttList.getAttribute("Status")
            tot_res_area = currentAttList.getAttribute("ALUC_Res") 
            if block_status == 0 or tot_res_area == 0:          #2 conditions to skip: (1) block status = 0, (2) area of residential = 0
                print "BlockID"+str(currentID)+" is not active or has no residential area"
                continue
            #IF NOT SKIPPED, PLAN URBAN FORM
            res_attr.setAttribute("HasResidential", 1)
            
            #--------------------------------------------------------------------------------#
            #            SETUP DATA - RETRIEVE FROM BLOCKCITY AND SAMPLE VALUES              #
            #--------------------------------------------------------------------------------#
            
            #GET AREAS AND POPULATION
            #Total Residential Area - planning MUST balance with this area by the end of the module!
            res_area_tot = float(currentAttList.getAttribute("ALUC_Res"))
            print "Total Residential Area for Block "+str(currentID)+"= "+str(res_area_tot)+"sqm"
            
            res_pop_dens = currentAttList.getAttribute("POP_Res")
            
            ### RANDOM SAMPLING FOR FRONTAGE WIDTHS ###
            footpath_w = float(random.randint(w_resfootpath_min, w_resfootpath_max))
            naturestrip_w = float(random.randint(w_resnaturestrip_min, w_resnaturestrip_max))
            collectlane_w = float(random.randint(w_collectlane_min, w_collectlane_max))
            
            res_frontage = float(footpath_w + naturestrip_w + collectlane_w)
            frontage_impness = (float(footpath_w) + float(collectlane_w))/float(res_frontage)
            
            
            #--------------------------------------------------------------------------------#
            #            URBANSIM FORK                                                       #
            # - check the data to see if entire block is residential, if yes, set total area #
            #   to block size, to avoid area conflict. if not, do nothing and just assign    #
            #   population density from UrbanSim data.
            #--------------------------------------------------------------------------------#
            
            if str(urbansimdata) == "Yes":
                res_area_tot = res_pop_dens * person_space
                if res_area_tot > blocks_size*blocks_size:
                    print "entire block is residential"
                    res_area_tot = blocks_size*blocks_size
                    res_pop_dens = currentAttList.getAttribute("DwellDens")
                else:
                    print "entire block is not residential"
                    res_pop_dens = currentAttList.getAttribute("DwellDens")
            
            ### --- --- --- --- --- URBAN SIM DATA PROCESSING - END --- --- --- --- --- --- ###
            
            
            #--------------------------------------------------------------------------------#
            # STEP -1- CALCULATE DISTRICT AND LOT INFO (TOP DOWN MASTERPLANNING              #
            #--------------------------------------------------------------------------------#
           
            ###DISTRICT INFO###
            district_length = res_area_tot/100  #treats res as one long district of x by 100m
            district_divisions = int(district_length/200)
            
            ###LOT INFO###
            res_lot_depth = (100-res_frontage*2)/2
            res_length_reserve = district_length*2+(2+district_divisions*2)*(100-res_frontage*2)
            res_area_reserve = res_length_reserve * res_frontage            #need to adjust for footpaths and nstrips at edges
            res_area_ca = res_area_tot - res_area_reserve
            res_allotments = int(res_area_ca/10000 * res_pop_dens)
            
            if res_allotments < 1:
                extra_area = res_area_tot
                pass
            else:
                res_lot_area = res_area_ca / res_allotments
                res_lot_width = res_lot_area / res_lot_depth
            
                ###CONDITION required to determine whether we use HDR design rules or just normal Res design rules
                #if condition == True/False:
                res_type = "Houses"
                #else:
                #       res_type = "Apartments"
                #######
                
                    
                #--------------------------------------------------------------------------------#
                # STEP -2- CALCULATE DETAILS ON A SINGLE LOT BASED ON PLANNING INPUTS            #
                #--------------------------------------------------------------------------------#
                
                ###SURFACE INFO ON LOT###
                setback_f = float(random.randint(setback_f_min, setback_f_max))
                setback_s = float(random.randint(setback_s_min, setback_s_max))
                if (setback_s * 2) > (res_lot_width/2):
                    print "going semi-detached!"
                
                res_private_dw_area = setback_f * w_driveway_min
                res_public_dw_area = (naturestrip_w + collectlane_w)*w_driveway_min        #PER HOUSE
                
                res_parking_area = carports_max * 2.6 * 4.9     ########NOTE! LOOK UP VALUE FOR CARPORTS!
                if garage_incl == True:                         ########FUTURE VERSION: PUT IN PROPER GARAGE DIMENSIONS
                    res_garage_area = carports * 2.6 * 4.9
                    res_parking_area = 0.5*res_parking_area
                else:
                    res_garage_area = 0
                if patio_covered == False:
                    res_other_surface = patio_area_max
                    res_other_roof = 0
                else:
                    res_other_surface = 0
                    res_other_roof = patio_area_max
                
                occupancy = random.normalvariate(occup_avg,occup_avg/10)
                if occupancy > occup_max:      #if it exceeds maximum indicated, then make it max!
                    occupancy = occup_max      
                if occupancy < 1:                   #if it is below 1 then make it 1
                    occupancy = 1
                
                #evaluate building footprint, site cover and impervious area limits
                res_livingspace = (person_space*occupancy)*(1+extra_comm_area/100)
                res_roofarea_tot = res_livingspace + res_garage_area + res_other_roof
                if res_roofarea_tot > (maxsitecover/100*res_lot_area):
                    print "warning, maximum site cover limit exceeded"
                res_surfimparea_tot = res_private_dw_area + res_parking_area + res_other_surface
                res_totimparea = res_roofarea_tot + res_surfimparea_tot
                res_totpervarea = res_lot_area - res_totimparea
                if res_totimparea > (maximperv/100*res_lot_area):
                    print "warning, maximum imperviousness limit exceeded"        
            
                #evaluate effective impervious area
                roof_connected = roof_connected
                if roof_connected == "Direct":
                    imp_connected = res_surfimparea_tot*(1-imperv_prop_dced/100) + res_roofarea_tot
                    imp_disconnected = res_surfimparea_tot*(imperv_prop_dced/100)
                else: 
                    if roof_connected == "Disconnect":
                        imp_connected = res_surfimparea_tot*(1-imperv_prop_dced/100)
                        imp_disconnected = res_surfimparea_tot*(imperv_prop_dced/100) + res_roofarea_tot
                    else:
                        vary = random.randint(0, 1)
                        if vary == 0:
                            roof_connected = "Direct"
                            imp_connected = res_surfimparea_tot*(1-imperv_prop_dced/100) + res_roofarea_tot
                            imp_disconnected = res_surfimparea_tot*(imperv_prop_dced/100)
                        else:
                            roof_connected = "Disconnect"
                            imp_connected = res_surfimparea_tot*(1-imperv_prop_dced/100)
                            imp_disconnected = res_surfimparea_tot*(imperv_prop_dced/100) + res_roofarea_tot
                
                #evaluate some broader details
                print "RES FRONTAGE", str(frontage_impness)
                print "RES_AREA_RESERVE", str(res_area_reserve)
                res_district_imparea = (res_allotments * res_totimparea) + (res_area_reserve * frontage_impness)
                res_district_pervarea = (res_allotments * res_totpervarea) + (res_area_reserve * (1-frontage_impness))
                res_district_impareaconnected = (res_allotments * imp_connected) + (res_area_reserve * frontage_impness)
                res_district_impareadisconnect = (res_allotments * imp_disconnected)
                res_district_impprop = res_district_imparea / res_area_tot
                res_district_impeffprop = res_district_impareaconnected / res_area_tot
                res_district_pervarea = res_area_tot - res_district_imparea
                
                res_district_BU_area = res_district_imparea + res_district_pervarea
                print "Total bottom up area evaluated for res areas = "+str(res_district_BU_area)
                
                #--------------------------------------------------------------------------------#
                #       WRITE OUTPUTS TO VECTOR DATA TO BE TRANSFERRED INTO SUMMARY MODULE       #
                #--------------------------------------------------------------------------------#
                
                res_attr.setAttribute("ResAllots", res_allotments)
                res_attr.setAttribute("ResType", res_type)
                res_attr.setAttribute("ResLotOccup", occupancy)
                res_attr.setAttribute("AvgAllot_A", res_lot_area)
                res_attr.setAttribute("AvgAllot_W", res_lot_width)
                res_attr.setAttribute("AvgAllot_D", res_lot_depth)
                res_attr.setAttribute("ResLotPubDW_A", res_public_dw_area)
                res_attr.setAttribute("ResLotPrivDW_A", res_private_dw_area)
                res_attr.setAttribute("Collect_WLane", collectlane_w)
                res_attr.setAttribute("Foot_W", footpath_w)
                res_attr.setAttribute("NStrip_W", naturestrip_w)
                res_attr.setAttribute("ResLotRoofA", res_roofarea_tot)
                res_attr.setAttribute("ResLotImpA", res_totimparea)
                res_attr.setAttribute("ResLotConImpA", imp_connected)
                res_attr.setAttribute("ResLotDscImpA", imp_disconnected)
                res_attr.setAttribute("ResLotRoofConnect", roof_connected)
                res_attr.setAttribute("ResTIArea", res_district_imparea)
                res_attr.setAttribute("ResEIArea", res_district_impareaconnected)
                res_attr.setAttribute("ResTIF", res_district_impprop)
                res_attr.setAttribute("ResEIF", res_district_impeffprop)
                res_attr.setAttribute("ResPVArea", res_district_pervarea)
                res_attr.setAttribute("ResDCIArea", res_district_impareadisconnect)
                res_attr.setAttribute("AvlResLot", (res_lot_area - res_totimparea))                   #available space on lot
                res_attr.setAttribute("TotStreetA", (res_area_tot - res_allotments*res_lot_area))     #total street Area
                res_attr.setAttribute("AvlStreet", (res_district_pervarea - res_allotments*(res_lot_area-res_totimparea)))    #available street space
                    
            #-----------------------------------------------------------------#
            #        Write all updated Attribute Lists to the output          #
            #-----------------------------------------------------------------#
            
            residential.setAttributes("BlockID"+str(currentID),res_attr)
            
            #FOR LOOP END (Repeat for next BlockID)
            
        #END OF MODULE
    