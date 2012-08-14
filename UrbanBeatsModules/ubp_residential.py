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
	
	self.blocks = View("Block",FACE,READ)
	self.blocks.getAttribute("BlockID")

	self.mapattributes = View("Mapattributes", COMPONENT,READ)
    	self.mapattributes.getAttribute("NumBlocks")
	self.mapattributes.getAttribute("BlockSize")
	self.mapattributes.getAttribute("WidthBlocks")
	self.mapattributes.getAttribute("HeightBlocks")
	self.mapattributes.getAttribute("InputReso")
    	
	self.planGen = View("PlanGen", COMPONENT, READ)
        self.planGen.getAttribute("maximperv")
        self.planGen.getAttribute("maxsitecover")
        self.planGen.getAttribute("locality_mun_trans")

	self.planRes = View("PlanRes", COMPONENT, READ)
	self.planRes.getAttribute("occup_avg")
        self.planRes.getAttribute("occup_max")
        self.planRes.getAttribute("person_space")
        self.planRes.getAttribute("extra_comm_area")
        
        self.planRes.getAttribute("setback_f_min")
        self.planRes.getAttribute("setback_f_max")
        self.planRes.getAttribute("setback_s_min")
        self.planRes.getAttribute("setback_s_max")
        
        self.planRes.getAttribute("carports_max")
        self.planRes.getAttribute("garage_incl")
        self.planRes.getAttribute("w_driveway_min")
        self.planRes.getAttribute("patio_area_max")
        self.planRes.getAttribute("patio_covered")
        self.planRes.getAttribute("floor_num_max")
        self.planRes.getAttribute("floor_autobuild")
        
        self.planRes.getAttribute("occup_flat_avg")
        self.planRes.getAttribute("commspace_indoor")
        self.planRes.getAttribute("commspace_outdoor")
        self.planRes.getAttribute("flat_area_max")
        self.planRes.getAttribute("setback_HDR_avg")
        self.planRes.getAttribute("setback_HDR_auto")
        self.planRes.getAttribute("roof_connected")
        self.planRes.getAttribute("imperv_prop_dced")

	self.planSpaces = View("PlanSpaces",COMPONENT,WRITE)

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

	self.residential = View("Residential",COMPONENT,WRITE)
	self.residential.addAttribute("BlockID")
	self.residential.addAttribute("HasResidential")
	self.residential.addAttribute("ResAllots")
        self.residential.addAttribute("ResType")
        self.residential.addAttribute("ResLotOccup")
        self.residential.addAttribute("AvgAllot_A")
        self.residential.addAttribute("AvgAllot_W")
        self.residential.addAttribute("AvgAllot_D")
        self.residential.addAttribute("ResLotPubDW_A")
        self.residential.addAttribute("ResLotPrivDW_A",)
        self.residential.addAttribute("Collect_WLane")
        self.residential.addAttribute("Foot_W")
        self.residential.addAttribute("NStrip_W")
        self.residential.addAttribute("ResLotRoofA")
        self.residential.addAttribute("ResLotImpA")
        self.residential.addAttribute("ResLotConImpA")
        self.residential.addAttribute("ResLotDscImpA")
        self.residential.addAttribute("ResLotRoofConnect")
        self.residential.addAttribute("ResTIArea")
        self.residential.addAttribute("ResEIArea")
        self.residential.addAttribute("ResTIF")
        self.residential.addAttribute("ResEIF")
        self.residential.addAttribute("ResPVArea")
        self.residential.addAttribute("ResDCIArea")
        self.residential.addAttribute("AvlResLot")
        self.residential.addAttribute("TotStreetA")
        self.residential.addAttribute("AvlStreet")	


	#Datastream
	datastream = []
	datastream.append(self.blocks)
	datastream.append(self.mapattributes)
	datastream.append(self.planGen)
	datastream.append(self.planRes)
	datastream.append(self.planSpaces)
	datastream.append(self.residential)
	
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
        lcality_mun_trans = bool(plan_gen.getAttribute("locality_mun_trans"))	            #BOOL -- locality map for municipal & transport?
        #===-----------------
        
        strvec = city.getUUIDsOfComponentsInView(self.planRes)
        plan_res = city.getComponent(strvec[0])
        occup_avg = plan_res.getAttribute("occup_avg").getDouble()                          #DOUBLE -- average occupancy (house)
        occup_max = plan_res.getAttribute("occup_max").getDouble()                          #DOUBLE -- maximum occupancy (house)
        person_space = plan_res.getAttribute("person_space").getDouble()                    #DOUBLE -- space per person [sqm]
        extra_comm_area = plan_res.getAttribute("extra_comm_area").getDouble()              #DOUBLE -- extra space for communal area
        
        setback_f_min = plan_res.getAttribute("setback_f_min").getDouble()                    #DOUBLE -- minimum front setback
        setback_f_max = plan_res.getAttribute("setback_f_max").getDouble()                    #DOUBLE -- maximum front setback
        setback_s_min = plan_res.getAttribute("setback_s_min").getDouble()                    #DOUBLE -- minimum side setback (applies to rear as well)
        setback_s_max = plan_res.getAttribute("setback_s_max").getDouble()                    #DOUBLE -- maximum side setback (applies to rear as well)
        
        carports_max = plan_res.getAttribute("carports_max").getDouble()                      #DOUBLE -- max number of carports
        garage_incl = bool(plan_res.getAttribute("garage_incl"))                              #BOOL -- include garage? YES/NO
        w_driveway_min = plan_res.getAttribute("w_driveway_min").getDouble()                  #DOUBLE -- minimum driveway width [m]
        patio_area_max = plan_res.getAttribute("patio_area_max").getDouble()                  #DOUBLE -- maximum patio area [sqm]
        patio_covered = bool(plan_res.getAttribute("patio_covered"))                          #BOOL -- is patio covered by roof?
        floor_num_max = plan_res.getAttribute("floor_num_max").getDouble()                    #DOUBLE -- maximum number of floors
        floor_autobuild = bool(plan_res.getAttribute("floor_autobuild"))                      #BOOL -- autobuild floors?
        
        occup_flat_avg = plan_res.getAttribute("occup_flat_avg").getDouble()                  #DOUBLE -- average occupancy of apartment
        commspace_indoor = plan_res.getAttribute("commspace_indoor").getDouble()              #DOUBLE -- communal space % indoor
        commspace_outdoor = plan_res.getAttribute("commspace_outdoor").getDouble()            #DOUBLE -- communal space % outdoor
        flat_area_max = plan_res.getAttribute("flat_area_max").getDouble()                    #DOUBLE -- maximum apartment size [sqm]
        setback_HDR_avg = plan_res.getAttribute("setback_HDR_avg").getDouble()                #DOUBLE -- average setback for HDR site
        setback_HDR_auto = bool(plan_res.getAttribute("setback_HDR_auto"))                    #BOOL -- determine setback for HDR automatically?
                
        roof_connected = plan_res.getAttribute("roof_connected").getString()	                      #STRING -- how is the roof connected to drainage? Direct/Disconnected/Varied?
	imperv_prop_dced = plan_res.getAttribute("imperv_prop_dced").getDouble()              #DOUBLE -- proportion of impervious area disconnected
        
        #===-----------------
        
	strvec = city.getUUIDsOfComponentsInView(self.planSpaces)
        plan_space = city.getComponent(strvec[0])
        w_resfootpath_min = plan_space.getAttribute("w_resfootpath_min").getDouble()        #DOUBLE
        w_resfootpath_max = plan_space.getAttribute("w_resfootpath_max").getDouble()        #DOUBLE
        w_resnaturestrip_min = plan_space.getAttribute("w_resnaturestrip_min").getDouble()  #DOUBLE
        w_resnaturestrip_max = plan_space.getAttribute("w_resnaturestrip_max").getDouble()  #DOUBLE
        w_resfootpath_med = bool(plan_space.getAttribute("w_resfootpath_med"))              #BOOL -- to simplify things, just use median footpath width?
        w_resnaturestrip_med = bool(plan_space.getAttribute("w_resnaturestrip_med"))        #BOOL -- to simplify things, just use median naturestrip width?
        
        w_collectlane_min = plan_space.getAttribute("w_collectlane_min").getDouble()        #DOUBLE
        w_collectlane_max = plan_space.getAttribute("w_collectlane_max").getDouble()        #DOUBLE
        w_collectlane_med = bool(plan_space.getAttribute("w_collectlane_med"))              #BOOL
        collect_crossfall = plan_space.getAttribute("collect_crossfall").getDouble()        #DOUBLE
        
        
        #--------------------------------------------------------------------------------#
        #       BEGIN LOOPING ACROSS ALL BLOCKS IN MAP                                   #
        #--------------------------------------------------------------------------------#
        
        for i in range(int(blocks_num)):
            currentID = i + 1
            currentAttList = self.getBlockUUID(currentID,city)#blockcityin.getAttributes("BlockID"+str(currentID))        #attribute list of current block structure
            #currentPatchList = patchcityin.getAttributes("PatchDataID"+str(currentID))
            res_attr = Component()
	    city.addComponent(res_attr,self.residential)
            res_attr.addAttribute("BlockID", currentID)
            block_AActive = blocks_size * blocks_size * (currentAttList.getAttribute("Activity").getDouble()/100)
    
            #--------------------------------------------------------------------------------#
            #            CONDITIONAL CHECK TO SEE IF CURRENT BLOCK IS RELEVANT               #
            #--------------------------------------------------------------------------------#
            
            block_status = currentAttList.getAttribute("Status").getDouble()
	    tot_res_area = currentAttList.getAttribute("ALUC_Res").getDouble()
            if block_status == 0 or tot_res_area == 0:          #2 conditions to skip: (1) block status = 0, (2) area of residential = 0
                print "BlockID"+str(currentID)+" is not active or has no residential area"
                continue
            #IF NOT SKIPPED, PLAN URBAN FORM
            res_attr.addAttribute("HasResidential", 1)
            
            #--------------------------------------------------------------------------------#
            #            SETUP DATA - RETRIEVE FROM BLOCKCITY AND SAMPLE VALUES              #
            #--------------------------------------------------------------------------------#
            
            #GET AREAS AND POPULATION
            #Total Residential Area - planning MUST balance with this area by the end of the module!
            
	    res_area_tot = currentAttList.getAttribute("ALUC_Res").getDouble()
            print "Total Residential Area for Block "+str(currentID)+"= "+str(res_area_tot)+"sqm"
            
            res_pop_dens = currentAttList.getAttribute("POP_Res").getDouble()
            
            ### RANDOM SAMPLING FOR FRONTAGE WIDTHS ###
            footpath_w = random.randint(w_resfootpath_min, w_resfootpath_max)
            naturestrip_w = random.randint(w_resnaturestrip_min, w_resnaturestrip_max)
            collectlane_w = random.randint(w_collectlane_min, w_collectlane_max)
            
            res_frontage = footpath_w + naturestrip_w + collectlane_w
            frontage_impness = (footpath_w + collectlane_w)/res_frontage
            
            
            #--------------------------------------------------------------------------------#
            #            URBANSIM FORK                                                       #
            # - check the data to see if entire block is residential, if yes, set total area #
            #   to block size, to avoid area conflict. if not, do nothing and just assign    #
            #   population density from UrbanSim data.
            #--------------------------------------------------------------------------------#
            '''
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
            '''
            
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
                setback_f = random.randint(setback_f_min, setback_f_max)
                setback_s = random.randint(setback_s_min, setback_s_max)
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
                
                res_attr.addAttribute("ResAllots", res_allotments)
                res_attr.addAttribute("ResType", res_type)
                res_attr.addAttribute("ResLotOccup", occupancy)
                res_attr.addAttribute("AvgAllot_A", res_lot_area)
                res_attr.addAttribute("AvgAllot_W", res_lot_width)
                res_attr.addAttribute("AvgAllot_D", res_lot_depth)
                res_attr.addAttribute("ResLotPubDW_A", res_public_dw_area)
                res_attr.addAttribute("ResLotPrivDW_A", res_private_dw_area)
                res_attr.addAttribute("Collect_WLane", collectlane_w)
                res_attr.addAttribute("Foot_W", footpath_w)
                res_attr.addAttribute("NStrip_W", naturestrip_w)
                res_attr.addAttribute("ResLotRoofA", res_roofarea_tot)
                res_attr.addAttribute("ResLotImpA", res_totimparea)
                res_attr.addAttribute("ResLotConImpA", imp_connected)
                res_attr.addAttribute("ResLotDscImpA", imp_disconnected)
                res_attr.addAttribute("ResLotRoofConnect", roof_connected)
                res_attr.addAttribute("ResTIArea", res_district_imparea)
                res_attr.addAttribute("ResEIArea", res_district_impareaconnected)
                res_attr.addAttribute("ResTIF", res_district_impprop)
                res_attr.addAttribute("ResEIF", res_district_impeffprop)
                res_attr.addAttribute("ResPVArea", res_district_pervarea)
                res_attr.addAttribute("ResDCIArea", res_district_impareadisconnect)
                res_attr.addAttribute("AvlResLot", (res_lot_area - res_totimparea))                   #available space on lot
                res_attr.addAttribute("TotStreetA", (res_area_tot - res_allotments*res_lot_area))     #total street Area
                res_attr.addAttribute("AvlStreet", (res_district_pervarea - res_allotments*(res_lot_area-res_totimparea)))    #available street space
                    
            #-----------------------------------------------------------------#
            #        Write all updated Attribute Lists to the output          #
            #-----------------------------------------------------------------#
            

            
            #FOR LOOP END (Repeat for next BlockID)
            
        #END OF MODULE
    
