# -*- coding: utf-8 -*-
"""
@file
@author Peter M Bach <peterbach@gmail.com>
@version 0.5
@section LICENSE

This file is part of VIBe2
Copyright (C) 2011 Peter M Bach

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
"""

from techimplementguic import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
#from pyvibe import *
#import pyvibe
from pydynamind import *
import math
import numpy as np

class techimplement(Module):
    """Loads the Blocks and Patches Shapefile and transfers all relevant information into
a suitable data management structure for use in urbplanbb and other modules
Inputs: Either project path or exact filename
- Obtain file directly from a filename or from an ongoing simulation? - Boolean
Filename: specify path
Ongoing simulation: specify project path (it is likely the program will load a text file with information on how to grab the shapefile)
Outputs: Vector Data containing block attributes (these are used in later modules as a comparison with the newly entered data)
Log of Updates made at each version:
v0.80 (July 2012):
- First created.
-
@ingroup UrbanBEATS
@author Peter M Bach
"""

    def __init__(self):
        Module.__init__(self)

        self.currentyear = 1960
        self.startyear = 1960

        #self.addParameter(self, "startyear", VIBe2.DOUBLEDATA_IN)
        #self.addParameter(self, "currentyear", VIBe2.DOUBLEDATA_IN)
        
        self.scale_matrix = ["L", "S", "N", "P"]
        
        #IMPLEMENTATION RULES TAB
        self.dynamic_rule = "B" #B = Block-based, P = Parcel-based
        self.createParameter( "dynamic_rule", STRING,"")
        
        #Block-based Rules
        self.block_based_thresh = 30 #Threshold for implementation, % exceeded
        self.bb_lot_rule = "AMAP" #AMAP = as many as possible, STRICT = strictly abide by %
        self.bb_street_zone = 1 #implement even if area hasn't been zoned yet
        self.bb_neigh_zone = 1 #implement even if neigh area hasn't been zoned yet
        self.createParameter( "block_based_thresh",DOUBLE,"")
        self.createParameter( "bb_lot_rule", STRING,"")
        self.createParameter( "bb_street_zone",BOOL,"")
        self.createParameter( "bb_neigh_zone",BOOL,"")
        
        self.pb_lot_rule = "G" #G = gradual, I = immediate, D = delayed
        self.pb_street_rule = "G"
        self.pb_neigh_rule = "G"
        self.pb_neigh_zone_ignore = 0
        self.createParameter( "pb_lot_rule", STRING,"")
        self.createParameter( "pb_street_rule", STRING,"")
        self.createParameter( "pb_neigh_rule", STRING,"")
        self.createParameter( "pb_neigh_zone_ignore",BOOL,"")
        
        self.prec_rule = "G"
        self.prec_zone_ignore = 0
        self.prec_dev_threshold = 0
        self.prec_dev_percent = 50
        self.createParameter( "prec_rule", STRING,"")
        self.createParameter( "prec_zone_ignore", BOOL,"")
        self.createParameter( "prec_dev_threshold", BOOL,"")
        self.createParameter( "prec_dev_percent", DOUBLE,"")
        
        #DRIVERS TAB - NOT ACTIVE YET, BUT PARAMETER LIST IS DEFINED FOR NOW
        self.driver_people = 0
        self.driver_legal = 0
        self.driver_establish = 0
        self.createParameter( "driver_people", BOOL,"")
        self.createParameter( "driver_legal", BOOL,"")
        self.createParameter( "driver_establish", BOOL,"")
    
	#Views
	self.blocks = View("Block",FACE,READ)
	self.blocks.getAttribute("BlockID")
	self.blocks.getAttribute("BasinUUID")
	self.blocks.getAttribute("Percentage_Landclass")
	self.blocks.getAttribute("Area_Landclass")

	self.prevBlocks = View("PreviousBlock",COMPONENT,READ)
        #self.prevBlocks.getAttribute("ResAllots")
        #self.prevBlocks.getAttribute("ResTIArea")
        #self.prevBlocks.getAttribute("ResLotImpA")
        #self.prevBlocks.getAttribute("AvlStreet")
        #self.prevBlocks.getAttribute("ALUC_PG")
        self.patch = View("Patch Attributes", COMPONENT, WRITE)

	self.mastermapattributes = View("MasterMapattributes",COMPONENT,READ)
        self.mastermapattributes.getAttribute("Xmin")
        self.mastermapattributes.getAttribute("Ymin")
        self.mastermapattributes.getAttribute("Width")
        self.mastermapattributes.getAttribute("Height")
        self.mastermapattributes.getAttribute("BlockSize")
        self.mastermapattributes.getAttribute("BlocksWidth")
        self.mastermapattributes.getAttribute("BlocksHeight")
        self.mastermapattributes.getAttribute("TotalBlocks")

	self.mapattributes = View("Mapattributes", COMPONENT, WRITE)
	self.mapattributes.getAttribute("NumBlocks")
	self.mapattributes.getAttribute("BlockSize")
	self.mapattributes.getAttribute("WidthBlocks")
	self.mapattributes.getAttribute("HeightBlocks")
	self.mapattributes.getAttribute("InputReso")
	self.mapattributes.addAttribute("TotalBasins")

	self.sysGlobal = View("SystemGlobal",COMPONENT,READ)
	self.sysGlobal.getAttribute("TotalSystems")
	
	self.basin = View("Basin", COMPONENT, READ)
	self.basin.addAttribute("BasinID")
	self.basin.addAttribute("Blocks")
	self.basin.addAttribute("DownBlockID")
	self.basin.addAttribute("UpStr")

	self.sysAttr = View("SystemAttribute",COMPONENT,WRITE)
	self.sysAttr.addAttribute("SystemID")
	self.sysAttr.addAttribute("Location")
	self.sysAttr.addAttribute("Scale")
        
	self.techimplAttr = View("TechimplementAttribute",NODE,WRITE)	
	self.techimplAttr.addAttribute("Location")
        self.techimplAttr.addAttribute("ScaleN")
        self.techimplAttr.addAttribute("Scale")
        self.techimplAttr.addAttribute("Type")
        self.techimplAttr.addAttribute("TypeN")
        self.techimplAttr.addAttribute("Qty")
        self.techimplAttr.addAttribute("GoalQty")
        self.techimplAttr.addAttribute("ImpT")
        self.techimplAttr.addAttribute("SysArea")
        self.techimplAttr.addAttribute("Status")
        self.techimplAttr.addAttribute("Year")
        self.techimplAttr.addAttribute("Degree")
        self.techimplAttr.addAttribute("EAFact")
        self.techimplAttr.addAttribute("CurImpT")
        self.techimplAttr.addAttribute("Upgrades")
        self.techimplAttr.addAttribute("WDepth")
        self.techimplAttr.addAttribute("FDepth")


	datastream = []
	datastream.append(self.blocks)
	datastream.append(self.mapattributes)
	datastream.append(self.mastermapattributes)
        datastream.append(self.sysGlobal)
	datastream.append(self.basin)
	datastream.append(self.sysAttr)
	datastream.append(self.techimplAttr)
	datastream.append(self.prevBlocks)
        self.addData("City", datastream)
	self.BLOCKIDtoUUID = {}
	self.SYSTEMIDtoUUID = {}
	self.PATCHIDtoUUID = {}

    def initBLOCKIDtoUUID(self, city):
	blockuuids = city.getUUIDsOfComponentsInView(self.blocks)
        for blockuuid in blockuuids:
            block = city.getFace(blockuuid)
            ID = int(round(block.getAttribute("BlockID").getDouble()))
	    self.BLOCKIDtoUUID[ID] = blockuuid

    def initSYSIDtoUUID(self, city):
	sysuuids = city.getUUIDsOfComponentsInView(self.sysAttr)
        for sysuuid in sysuuids:
            sys = city.getComponent(sysuuid)
            ID = int(round(sys.getAttribute("SystemID").getDouble()))
	    self.SYSTEMIDtoUUID[ID] = sysuuid

    def initPATCHIDtoUUID(self, city):
	patchuuids = city.getUUIDsOfComponentsInView(self.patch)
        for patchuuid in patchuuids:
            patch = city.getComponent(patchuuid)
            ID = int(round(patch.getAttribute("Block_ID").getDouble()))
	    self.PATCHIDtoUUID[ID] = patchuuid

    def getBlockUUID(self, blockid,city):
	try:
		key = self.BLOCKIDtoUUID[blockid]
	except KeyError:
		key = ""
	return city.getFace(key)

    def getSysComp(self, sysID,city):
	try:
		key = self.SYSTEMIDtoUUID[sysID]
	except KeyError:
		key = ""
	return city.getComponent(key)

    def getPatchComp(self, patchID,city):
	try:
		key = self.PATCHIDtoUUID[patchID]
	except KeyError:
		key = ""
	return city.getComponent(key)

    def run(self):
	city = self.getData("City")
	self.initBLOCKIDtoUUID(city)
	self.initSYSIDtoUUID(city)
	self.initPATCHIDtoUUID(city)
        currentyear = self.currentyear
        startyear = self.startyear


        #Get global map attributes
	strvec = city.getUUIDsOfComponentsInView(self.mapattributes)
        map_attr = city.getComponent(strvec[0])

	strvec = city.getUUIDsOfComponentsInView(self.sysGlobal)
        totsystems = city.getComponent(strvec[0]).getAttribute("TotalSystems").getDouble()
        print "Total Systems in map: "+str(totsystems)
        
        #Get block number, etc.
        blocks_num = map_attr.getAttribute("NumBlocks").getDouble() #number of blocks to loop through   
	blocks_size = map_attr.getAttribute("BlockSize").getDouble() #size of block
        map_w = map_attr.getAttribute("WidthBlocks").getDouble() #num of blocks wide
        map_h = map_attr.getAttribute("HeightBlocks").getDouble() #num of blocks tall
        input_res = map_attr.getAttribute("InputReso").getDouble() #resolution of input data

        
        basins = map_attr.getAttribute("TotalBasins").getDouble()
        for i in range(int(basins)):
            #Purpose of this loop is to transfer the basin attributes across to the outport of this module
            currentID = i+1
	    basin_uuid = self.getBlockUUID(currentID,city).getAttribute("BasinUUID").getString()
	    basin_attr = city.getComponent(basin_uuid)
            blockcount = basin_attr.getAttribute("Blocks").getDouble()
            downstreammostblock = basin_attr.getAttribute("DownBlockID").getDouble()
            basinblockIDs = basin_attr.getAttribute("UpStr").getString()
            

        
        #Get all systems for current block
        system_list = []
        for i in range(int(blocks_num)):
            system_list.append([])
        
        for j in range(int(totsystems)):
	    print j	
            locate = self.getSysComp(j,city).getAttribute("Location").getDouble()
	    system_list[int(locate-1)].append(j) #matrix contains all systemIDs (attribute list name) across all blocks
        
        print system_list
        
        #Begin looping across blocks
        for i in range(int(blocks_num)):
            currentID = i + 1
            currentAttList = self.getBlockUUID(currentID,city) #attribute list of current block structure
            currentPatchList = self.getPatchComp(currentID,city)
            #existingAttList = existingblock.getAttributes("BlockID"+str(currentID)) #attribute list of the existing block structure
            #plist = blockcityin.getPoints("BlockID"+str(currentID))
            #flist = blockcityin.getFaces("BlockID"+str(currentID))
            #pnetlist = blockcityin.getPoints("NetworkID"+str(currentID))
            #enetlist = blockcityin.getEdges("NetworkID"+str(currentID))
            #network_attr = blockcityin.getAttributes("NetworkID"+str(currentID))
            
            #-----------------------------------------------------------------#
            # DETERMINE WHETHER TO UPDATE CURRENT BLOCK AT ALL #
            #-----------------------------------------------------------------#
            
            ### QUIT CONDITION #1 - BLOCK STATUS = 0 ###
            if self.skipIfStatusZero(currentID, city):
                continue
            
            ### QUIT CONDITION #2 - NO SYSTEMS PLANNED FOR BLOCK AT ALL ###
            sys_implement = system_list[i]
            if self.skipIfNoSystems(currentID, sys_implement ):
                continue
 
            #GRAB ALL DETAILS FROM MASTERPLAN FOR USE WHEREVER
            mpdata = self.getMasterPlanData(currentID,city)
            
            ### QUIT CONDITION #3 - DYNAMIC-MODE = Block-based and DEVELOPMENT < Threshold ###
            if self.dynamic_rule == "B":
                block_skip = self.skipIfBelowBlockThreshold(currentID, float(self.block_based_thresh/100), city)
                #use block_skip to determine whether to skip the next few steps
 
            #DECLARE ATTRIBUTE LIST FOR SAVING IMPLEMENTED TECHNOLOGIES LIST
            centreX = currentAttList.getAttribute("Centre_x").getDouble()
            centreY = currentAttList.getAttribute("Centre_y").getDouble()
            
            ### LOT IMPLEMENTATION ###
            ### Condition 1: block_skip=False, Condtion 2: there are systems at that scale, Condition 3: there are allotments in the block
            #Get Lot Systems Details
            lot_details = [0, 0] #[0] - total lot treated, [1] - lot degree
            if block_skip == False:
                sys_implement_lot = self.locatePlannedSystems(sys_implement, "L",city)
                if sys_implement_lot == None:
                    print "No Lot Systems planned for Block "+str(currentID)
                else:
                    new_lot_details = self.implementLot(currentID, sys_implement_lot, mpdata, [centreX, centreY], currentyear,city)
                    if new_lot_details != 0:
                        lot_details[0] += new_lot_details[0] #update total impervious area treated at lot
                        lot_details[1] = new_lot_details[1] #update the % implementation at lot scale
            
            ### STREET IMPLEMENTATION ###
            ### Condition 1: block_skip=False, Condition 2: there are street systems planned
            streetdeg = 0
            if block_skip == False:
                sys_implement_street = self.locatePlannedSystems(sys_implement, "S",city)
                if sys_implement_street == None:
                    print "No Street Systems planned for Block "+str(currentID)
                else:
                    self.implementStreet(currentID, sys_implement_street, mpdata, [centreX, centreY], currentyear, lot_details,city)
                    
            ### NEIGHBOURHOOD IMPLEMENTATION ###
            neighdeg = 0
            if block_skip == False:
                sys_implement_neigh = self.locatePlannedSystems(sys_implement, "N",city)
                if sys_implement_neigh == None:
                    print "No Neighbourhood Systems planned for Block "+str(currentID)
                else:
                    self.implementNeighbourhood(currentID, sys_implement_neigh, mpdata, [centreX, centreY], currentyear, lot_details,city)
        
            ### PRECINCT IMPLEMENTATION ###
            precdeg = 0
            sys_implement_prec = self.locatePlannedSystems(sys_implement, "P",city)
            if sys_implement_prec == None:
                print "No Precinct Systems planned for Block "+str(currentID)
            else:
                self.implementPrecinct(currentID, sys_implement_prec, mpdata, [centreX, centreY], currentyear,city)
            

            
            #FOR LOOP END (Repeat for next BlockID)
            
        #Output vector update

    
    def skipIfStatusZero(self, ID, city):
        #Determines if the current BlockID's status is 1 or 0, if 0 transfers all its data
        #to the output vector and returns true. If main function receives true

        if self.getBlockUUID(ID,city).getAttribute("Status").getDouble() == 0:
            print "BlockID"+str(ID)+" is not active in simulation"
            return True
        else:
            return False

    def skipIfNoSystems(self, ID, sys_implement):
        if len(sys_implement) == 0:
            print "No Systems planned for Block "+str(ID)+", skipping..."
            return True
        else:
            return False
    
    def getMasterPlanData(self, ID,city):
        #Gets data for the current block from the simulated masterplan, parameters are saved into
        #an array, which is returned with following index reference:
        # 0 - total allotments in block
        # 1 - total residential impervious area of district
        # 2 - impervious area of one lot
        # 3 - Available space on the street scape
        # 4 - Available space in open areas for neighbourhood systems
	
	##### get prev blocks

        allots = self.getBlockUUID(ID,city).getAttribute("ResAllots").getDouble()
        resTIarea = self.getBlockUUID(ID,city).getAttribute("ResTIArea").getDouble()
        LotImpArea = self.getBlockUUID(ID,city).getAttribute("ResLotImpA").getDouble()
        AvlStreet = self.getBlockUUID(ID,city).getAttribute("AvlStreet").getDouble()
	landclassvec = self.getBlockUUID(ID,city).getAttribute("Area_Landclass").getDoubleVector()
        AvlNeigh = landclassvec[10]
        masterplan_array = [allots, resTIarea, LotImpArea, AvlStreet, AvlNeigh]
        return masterplan_array
    
    def skipIfBelowBlockThreshold(self, ID, threshold,city):
	landclassvec = self.getBlockUUID(ID,city).getAttribute("Percentage_Landclass").getDoubleVector()
        prop_undev = landclassvec[13]
        if (1-prop_undev) < threshold:
            return True
        else:
            return False
    
    def locatePlannedSystems(self, system_list, scale,city):
        #Searches the input planned technologies list for a system that fits the scale in the block
        #Returns the system attribute list
        system_object = None
        for i in system_list:
            if str(self.getSysComp(i,city).getAttribute("Scale").getString()) == scale:
                system_object = self.getSysComp(i,city)
        return system_object

    def implementLot(self, ID, sys_descr, mpdata, centrePoints, currentyear,city):
        #Implements lot-scale technologies into current Block ID, takes several inputs
        #Calls the function drawTechnologyDataPoint() to output geometry and attribute data
        # ID = BlockID
        # sys_descr = AttributeList of the system found with locatePlannedSystem()
        # mpdata = Masterplan data found with getMasterPlanData()
        # centrePoints = [centreX, centreY]
        # currentyear = current building year to be added to implemented system
        currentAttList = self.getBlockUUID(ID,city)

        system_type_matrix = ['BF', 'SW', 'WSUR', 'PB', 'IS']
        system_type_numeric = [2463, 7925, 9787, 7663, 4635] #Think Telephone Buttons :) ('Biof', 'Swal', 'WSUR', 'Pond', 'Infl')
            
        #Check if block has allotments, if not, do nothing
        if currentAttList.getAttribute("ResAllots").getDouble() == 0:
            print "Current Block "+str(ID)+" has no residential allotments"
            return 0 #break function here
    
        #Get Details
        allotments = currentAttList.getAttribute("ResAllots").getDouble()
        lotimparea = currentAttList.getAttribute("ResLotImpA").getDouble()
        roofarea = currentAttList.getAttribute("ResLotRoofA").getDouble()
        openspace = currentAttList.getAttribute("rfw_Adev").getDouble()
        
        lottype = sys_descr.getAttribute("Type").getString()
        lotdeg = sys_descr.getAttribute("Degree").getDouble()
        lotsysarea = sys_descr.getAttribute("SysArea").getDouble()
        lotsysstatus = sys_descr.getAttribute("Status").getDouble()
        lotsysbuildyr = sys_descr.getAttribute("Year").getDouble()
        loteafact = sys_descr.getAttribute("EAFact").getDouble()
        lotqty = sys_descr.getAttribute("Qty").getDouble()
        goalqty = sys_descr.getAttribute("GoalQty").getDouble() #THIS IS RELEVANT HERE!
        lotimpT = sys_descr.getAttribute("ImpT").getDouble() #How much the lot system will treat in terms of TOTAL IMP AREA
        currentimpT = sys_descr.getAttribute("CurImpT").getDouble()
        upgrades = sys_descr.getAttribute("Upgrades").getDouble()
        
        wdepth = sys_descr.getAttribute("WDepth").getDouble()
        fdepth = sys_descr.getAttribute("FDepth").getDouble()
        
        print lottype, lotdeg, lotsysarea, lotsysstatus, lotsysbuildyr
        
        
        if lotsysbuildyr == 9999: #if the system is already implemented, then check if it has been fully implemented
            goallots = int(lotdeg*mpdata[0]) #final number of houses with systems (masterplan)
            print "Goal Lots: ", str(goallots)
            #calculate how many to implement based on allotment rules
            if self.bb_lot_rule == "AMAP":
                #AMAP = as many as possible, i.e. lesser of: how many we ultimately want or how many have been built
                goalqty = goallots #AT THE TIME OF IMPLEMENTATION, WHAT IS OUT DESIRED NUMBER OF ALLOTMENTS, define goalqty
                num_systems_impl = min(goallots, allotments)
                lotqty = num_systems_impl
                print num_systems_impl
            elif self.bb_lot_rule == "STRICT":
                #STRICT = strictly follow %, i.e. number of allotments built * %
                goalqty = goallots
                num_systems_impl = int(allotments * lotdeg)
                lotqty = num_systems_impl
                print num_systems_impl
                
            tot_system_area = num_systems_impl * lotsysarea #total area currently = how many were implemented
            tot_lot_treated_current = lotimparea * num_systems_impl
            tot_lot_treated = lotimparea * goalqty #total treated are = how many are planned * impervious area treated by one
            lotimpT = tot_lot_treated #This value is updated once the system has been implemented
            currentimpT = tot_lot_treated_current #current treated Aimp
            print tot_system_area
        elif lotsysbuildyr != 9999:
            #how many in the original plan? -- goallots
            #how many already in?
            remaining_lotqty = goalqty - lotqty #At any future implementation stage, we check the very first goal allotments!
            if self.bb_lot_rule == "AMAP" and remaining_lotqty > 0:
                #implement more lot systems
                pass
            elif self.bb_lot_rule == "STRICT" and remaining_lotqty > 0:
                #implement more lot systems according to rule
                pass
            
        #Write to outputs
        techimpl_attr = Node(0,0,0)
	city.addNode(techimpl_attr,self.techimplAttr) 
        techimpl_attr.addAttribute("Location", ID)
        techimpl_attr.addAttribute("ScaleN", self.scale_matrix.index("L"))
        techimpl_attr.addAttribute("Scale", "L")
        techimpl_attr.addAttribute("Type", lottype)
        techimpl_attr.addAttribute("TypeN", system_type_numeric[system_type_matrix.index(lottype)])
        techimpl_attr.addAttribute("Qty", lotqty)
        techimpl_attr.addAttribute("GoalQty", goalqty)
        techimpl_attr.addAttribute("ImpT", lotimpT)
        techimpl_attr.addAttribute("SysArea", lotsysarea)
        techimpl_attr.addAttribute("Status", 1)
        techimpl_attr.addAttribute("Year", min(lotsysbuildyr, currentyear))
        techimpl_attr.addAttribute("Degree", lotdeg)
        techimpl_attr.addAttribute("EAFact", loteafact)
        techimpl_attr.addAttribute("CurImpT", currentimpT)
        techimpl_attr.addAttribute("Upgrades", upgrades)
        techimpl_attr.addAttribute("WDepth", wdepth)
        techimpl_attr.addAttribute("FDepth", fdepth)
             
        self.drawTechnologyDataPoint(ID, centrePoints[0], centrePoints[1], "L", techimpl_attr,city)
        if lotsysbuildyr < currentyear: #if the system is already implemented, then skip
            return [lotimpT, lotdeg]
        return [currentimpT, lotdeg]
    
    def implementStreet(self, ID, sys_descr, mpdata, centrePoints, currentyear, lot_details,city):
        #Implements street-scale technologies into current Block ID, takes several inputs
            #Calls the function drawTechnologyDataPoint() to output geometry and attribute data
            # ID = BlockID
            # sys_descr = AttributeList of the system found with locatePlannedSystem()
            # mpdata = Masterplan data found with getMasterPlanData()
            # centrePoints = [centreX, centreY]
            # currentyear = current building year to be added to implemented system
            # lot_details = [total lot impervious treated, lot % implementation]

        currentAttList = self.getBlockUUID(ID,city)
        
        system_type_matrix = ['BF', 'SW', 'WSUR', 'PB', 'IS']
        system_type_numeric = [2463, 7925, 9787, 7663, 4635] #Think Telephone Buttons :) ('Biof', 'Swal', 'WSUR', 'Pond', 'Infl')
           
        #Grab data
        streettype = sys_descr.getAttribute("Type").getString()
        streetdeg = sys_descr.getAttribute("Degree").getDouble()
        streetsysarea = sys_descr.getAttribute("SysArea").getDouble()
        streetsysstatus = sys_descr.getAttribute("Status").getDouble()
        streetsysbuildyr = sys_descr.getAttribute("Year").getDouble()
        streeteafact = sys_descr.getAttribute("EAFact").getDouble()
        streetqty = sys_descr.getAttribute("Qty").getDouble()
        streetimpT = sys_descr.getAttribute("ImpT").getDouble()
        currentimpT = sys_descr.getAttribute("CurImpT").getDouble()
        goalqty = sys_descr.getAttribute("GoalQty").getDouble()
        upgrades = sys_descr.getAttribute("Upgrades").getDouble()
        
        wdepth = sys_descr.getAttribute("WDepth").getDouble()
        fdepth = sys_descr.getAttribute("FDepth").getDouble()
        
        print streettype, streetdeg, streetsysarea, streetsysstatus, streetsysbuildyr
        
        if streetsysbuildyr == 9999: #if the system is already implemented, then skip
            #GET CURRENT DETAILS
            resimparea = currentAttList.getAttribute("ResTIArea").getDouble()
            street_neigh_imp_area = resimparea - lot_details[0] #if there was no lot implementation, then tot_lot_treated = 0
            street_avl_space = currentAttList.getAttribute("AvlStreet").getDouble()
            print "Street Areas:"
            print resimparea, street_neigh_imp_area, street_avl_space
            
            #Masterplan details
            street_neigh_masterplan = mpdata[1] - (mpdata[2]*lot_details[1]*mpdata[0])
            print "Masterplan: "
            print mpdata[1], street_neigh_masterplan, mpdata[3]
            
            #Compare impervious areas
            imp_developed = float(resimparea)/float(mpdata[1])
            if imp_developed < float(self.block_based_thresh/100): #QUIT CONDITION 1: developed imp area less than threshold
                return True
            if self.bb_street_zone == 0 and street_avl_space < streetsysarea: #QUIT CONDITION 2: no space and model was restrained to available space
                return True
            
            #else implement the system
            tot_street_treated = streetdeg * street_neigh_imp_area
            currentimpT = tot_street_treated
            print "Street Area treated: ", str(tot_street_treated)
            
        techimpl_attr = Node(0,0,0)
	city.addNode(techimpl_attr,self.techimplAttr) 
        techimpl_attr.addAttribute("Location", ID)
        techimpl_attr.addAttribute("ScaleN", self.scale_matrix.index("S"))
        techimpl_attr.addAttribute("Scale", "S")
        techimpl_attr.addAttribute("Type", streettype)
        techimpl_attr.addAttribute("TypeN", system_type_numeric[system_type_matrix.index(streettype)])
        techimpl_attr.addAttribute("Qty", streetqty)
        techimpl_attr.addAttribute("GoalQty", goalqty)
        techimpl_attr.addAttribute("SysArea", streetsysarea)
        techimpl_attr.addAttribute("ImpT", streetimpT)
        techimpl_attr.addAttribute("Status", 1)
        techimpl_attr.addAttribute("Year", min(streetsysbuildyr, currentyear))
        techimpl_attr.addAttribute("Degree", streetdeg)
        techimpl_attr.addAttribute("EAFact", streeteafact)
        techimpl_attr.addAttribute("CurImpT", currentimpT)
        techimpl_attr.addAttribute("Upgrades", upgrades)
        techimpl_attr.addAttribute("WDepth", wdepth)
        techimpl_attr.addAttribute("FDepth", fdepth)
             
        self.drawTechnologyDataPoint(ID, centrePoints[0], centrePoints[1], "S", techimpl_attr,city)
        return True
    
    def implementNeighbourhood(self, ID, sys_descr, mpdata, centrePoints, currentyear, lot_details,city):
        #Implements neighbourhood-scale technologies into current Block ID, takes several inputs
        #Calls the function drawTechnologyDataPoint() to output geometry and attribute data
        # ID = BlockID
        # sys_descr = AttributeList of the system found with locatePlannedSystem()
        # mpdata = Masterplan data found with getMasterPlanData()
        # centrePoints = [centreX, centreY]
        # currentyear = current building year to be added to implemented system
        # lot_details = [total lot impervious treated, lot % implementation]

        currentAttList = self.getBlockUUID(ID,city)
        system_type_matrix = ['BF', 'SW', 'WSUR', 'PB', 'IS']
        system_type_numeric = [2463, 7925, 9787, 7663, 4635] #Think Telephone Buttons :) ('Biof', 'Swal', 'WSUR', 'Pond', 'Infl')
            
        #Grab Data
        neightype = sys_descr.getAttribute("Type").getString()
        neighdeg = sys_descr.getAttribute("Degree").getDouble()
        neighsysarea = sys_descr.getAttribute("SysArea").getDouble()
        neighsysstatus = sys_descr.getAttribute("Status").getDouble()
        neighsysbuildyr = sys_descr.getAttribute("Year").getDouble()
        neigheafact = sys_descr.getAttribute("EAFact").getDouble()
        neighqty = sys_descr.getAttribute("Qty").getDouble()
        neighimpT = sys_descr.getAttribute("ImpT").getDouble()
        currentimpT = sys_descr.getAttribute("CurImpT").getDouble()
        goalqty = sys_descr.getAttribute("GoalQty").getDouble()
        upgrades = sys_descr.getAttribute("Upgrades").getDouble()
        
        wdepth = sys_descr.getAttribute("WDepth").getDouble()
        fdepth = sys_descr.getAttribute("FDepth").getDouble()
        
        print neightype, neighdeg, neighsysarea, neighsysstatus, neighsysbuildyr
        #Follow the same as street, but check the open space first
        
        if neighsysbuildyr == 9999: #if the system is already implemented, then skip
            #Current Year Details
            resimparea = currentAttList.getAttribute("ResTIArea").getDouble()
            street_neigh_imp_area = resimparea - lot_details[0] #if there was no lot implementation, then tot_lot_treated = 0
            landclassvec = self.getBlockUUID(ID,city).getAttribute("Area_Landclass").getDoubleVector()
	    neigh_avail_sp = landclassvec[10]
            print "Neigh Areas:"
            print resimparea, street_neigh_imp_area, neigh_avail_sp
            
            #Masterplan details
            street_neigh_masterplan = mpdata[1] - (mpdata[2]*lot_details[1]*mpdata[0])
            print "Masterplan: "
            print mpdata[1], street_neigh_masterplan, mpdata[4]
            
            #Compare impervious areas
            imp_developed = float(resimparea)/float(mpdata[1])
            if imp_developed < float(self.block_based_thresh/100):
                return True
            if self.bb_street_zone == 0 and neigh_avl_space < streetsysarea:
                return True
            
            #else implement the system
            tot_neigh_treated = neighdeg * street_neigh_imp_area
            currentimpT = tot_neigh_treated
            print "Neigh Area treated: ", str(tot_neigh_treated)
        
        techimpl_attr = Node(0,0,0)
	city.addNode(techimpl_attr,self.techimplAttr) 
        techimpl_attr.addAttribute("Location", ID)
        techimpl_attr.addAttribute("ScaleN", self.scale_matrix.index("N"))
        techimpl_attr.addAttribute("Scale", "N")
        techimpl_attr.addAttribute("Type", neightype)
        techimpl_attr.addAttribute("TypeN", system_type_numeric[system_type_matrix.index(neightype)])
        techimpl_attr.addAttribute("Qty", neighqty)
        techimpl_attr.addAttribute("GoalQty", goalqty)
        techimpl_attr.addAttribute("SysArea", neighsysarea)
        techimpl_attr.addAttribute("ImpT", neighimpT)
        techimpl_attr.addAttribute("Status", 1)
        techimpl_attr.addAttribute("Year", min(neighsysbuildyr, currentyear))
        techimpl_attr.addAttribute("Degree", neighdeg)
        techimpl_attr.addAttribute("EAFact", neigheafact)
        techimpl_attr.addAttribute("CurImpT", currentimpT)
        techimpl_attr.addAttribute("Upgrades", upgrades)
        techimpl_attr.addAttribute("WDepth", wdepth)
        techimpl_attr.addAttribute("FDepth", fdepth)
            
        self.drawTechnologyDataPoint(ID, centrePoints[0], centrePoints[1], "N", techimpl_attr,city)
        return True
    
    def drawTechnologyDataPoint(self, ID, centreX, centreY, scale, techimpl_attr,city):
        #Grab data
	strvec = city.getUUIDsOfComponentsInView(self.mapattributes)
        blocks_size = city.getComponent(strvec[0]).getAttribute("BlockSize").getDouble()
        
        #Use an offsets_matrix and the scale to locate the proper coordinates
        offsets_matrix = [[centreX+blocks_size/8, centreY+blocks_size/4],[centreX+blocks_size/4, centreY-blocks_size/8],[centreX-blocks_size/8, centreY-blocks_size/4],[centreX-blocks_size/4, centreY+blocks_size/8]]
        scale_matrix = ["L", "S", "N", "P"]
        scale_index = scale_matrix.index(scale)
        coordinates = offsets_matrix[scale_index]
        
        #Draw the point and assign attributes

	techimpl_attr.setX(coordinates[0])
	techimpl_attr.setY(coordinates[1])
        return True

    def getUpstreamIDs(self, ID,city):

        currentAttList = self.getBlockUUID(ID,city)
        upstr_string = currentAttList.getAttribute("BasinBlocks").getString() #does not include current ID itself
        upstreamIDs = upstr_string.split(',')
        upstreamIDs.remove('')
        for i in range(len(upstreamIDs)):
            upstreamIDs[i] = int(upstreamIDs[i])
        return upstreamIDs

    def calculateUpstreamDevelopment(self, ID, upstreamIDs,city):

        currentAttList = self.getBlockUUID(ID,city)
        block_size = blockcityin.getAttributes("MapAttributes").getAttribute("BlockSize")
        #grab total developed area
        upstreamArea = currentAttList.getAttribute("BasinArea").getDouble()*10000 + (block_size * block_size)
	landclassvec = currentAttList.getAttribute("Percentage_Landclass").getDoubleVector()
        undeveloped_area = landclass[13]
        for i in upstreamIDs:
	    landclassvec = self.getBlockUUID(i,city).getAttribute("Percentage_Landclass").getDoubleVector()
            undeveloped_area += landclassvec[13]
        percentage_dev = 1-(undeveloped_area/upstreamArea)
        return percentage_dev
    
    def getUpstreamImpArea(self, ID, upstreamIDs,city):
        #This function scans the database of blockIDs and tallies up the total
        #upstream impervious area returning it to the main run function of the
        #module.

        Aimptotal = self.getBlockUUID(ID,city).getAttribute("ResTIArea").getDouble() #tally for total upstream impervious area
        for i in upstreamIDs:
            Aimptotal += self.getBlockUUID(i,city).getAttribute("ResTIArea").getDouble()
        return Aimptotal #in sqm units
    
    def implementPrecinct(self, ID, sys_descr, mpdata, centrePoints, currentyear,city):
        #Implements precinct-scale technologies into current Block ID, takes several inputs
        #Calls the function drawTechnologyDataPoint() to output geometry and attribute data
        # ID = BlockID
        # sys_descr = AttributeList of the system found with locatePlannedSystem()
        # mpdata = Masterplan data found with getMasterPlanData()
        # centrePoints = [centreX, centreY]
        # currentyear = current building year to be added to implemented system

        currentAttList = self.getBlockUUID(ID,city)
        
        system_type_matrix = ['BF', 'SW', 'WSUR', 'PB', 'IS']
        system_type_numeric = [2463, 7925, 9787, 7663, 4635] #Think Telephone Buttons :) ('Biof', 'Swal', 'WSUR', 'Pond', 'Infl')
            
        upstreamIDs = self.getUpstreamIDs(ID,city)
        
        #Calculate total development upstream of block
        if self.prec_dev_threshold == True:
            #if this is selected as part of the simulation then calculate upstream development
            percentage_dev = self.calculateUpstreamDevelopment(ID, upstreamIDs,city)
            if percentage_dev < float(self.prec_dev_percent/100):
                print "Upstream precinct not developed enough, skipping..."
                return True
        #Otherwise force implement precinct systems
        
        #Grab Data
        prectype = sys_descr.getAttribute("Type").getString()
        precdeg = sys_descr.getAttribute("Degree").getDouble()
        precsysarea = sys_descr.getAttribute("SysArea").getDouble()
        precsysstatus = sys_descr.getAttribute("Status").getDouble()
        precsysbuildyr = sys_descr.getAttribute("Year").getDouble()
        preceafact = sys_descr.getAttribute("EAFact").getDouble()
        precqty = sys_descr.getAttribute("Qty").getDouble()
        precimpT = sys_descr.getAttribute("ImpT").getDouble()
        currentimpT = sys_descr.getAttribute("CurImpT").getDouble()
        goalqty = sys_descr.getAttribute("GoalQty").getDouble()
        upgrades = sys_descr.getAttribute("Upgrades").getDouble()
        
        wdepth = sys_descr.getAttribute("WDepth").getDouble()
        fdepth = sys_descr.getAttribute("FDepth").getDouble()
        
        print prectype, precdeg, precsysarea, precsysstatus, precsysbuildyr
        #Follow the same as street, but check the open space first
        
        if precsysbuildyr == 9999: #if the system is already implemented, then skip
            landclassvec = self.getBlockUUID(ID,city).getAttribute("Area_Landclass").getDoubleVector()
            neigh_avail_sp = landclassvec[10]
            
            #check if space
            if self.prec_zone_ignore == False and precsysarea > neigh_avail_sp:
                print "Not enough space yet"
                return True
            
            imp_area_tot = self.getUpstreamImpArea(ID, upstreamIDs,city)
            tot_prec_treated = precdeg * imp_area_tot
            currentimpT= tot_prec_treated
            
        techimpl_attr = Node(0,0,0)
	city.addNode(techimpl_attr,self.techimplAttr) 
        techimpl_attr.addAttribute("Location", ID)
        techimpl_attr.addAttribute("Scale", self.scale_matrix.index("P"))
        techimpl_attr.addAttribute("ScaleN", "P")
        techimpl_attr.addAttribute("Type", prectype)
        techimpl_attr.addAttribute("TypeN", system_type_numeric[system_type_matrix.index(prectype)])
        techimpl_attr.addAttribute("Qty", precqty)
        techimpl_attr.addAttribute("GoalQty", goalqty)
        techimpl_attr.addAttribute("SysArea", precsysarea)
        techimpl_attr.addAttribute("ImpT", precimpT)
        techimpl_attr.addAttribute("Status", 1)
        techimpl_attr.addAttribute("Year", min(precsysbuildyr, currentyear))
        techimpl_attr.addAttribute("Degree", precdeg)
        techimpl_attr.addAttribute("EAFact", preceafact)
        techimpl_attr.addAttribute("CurImpT", currentimpT)
        techimpl_attr.addAttribute("Upgrades", upgrades)
        techimpl_attr.addAttribute("WDepth", wdepth)
        techimpl_attr.addAttribute("FDepth", fdepth)
        
        self.drawTechnologyDataPoint(ID, centrePoints[0], centrePoints[1], "P", techimpl_attr,city)
        return True
    
    
    ########################################################
    #LINK WITH GUI #
    ########################################################
                        
    def createInputDialog(self):
        form = activatetechimplementGUI(self, QApplication.activeWindow())
        form.show()
        return True 
