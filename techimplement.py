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

from techimplementguic import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from pyvibe import *
import pyvibe
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
        self.blockcityin = VectorDataIn         #current map of blocks based on present time
        self.patchdatain = VectorDataIn         #current patch information for present day
        self.techconfigin = VectorDataIn        #masterplan suggested tech configuration
        self.previousblocksin = VectorDataIn    #masterplan map of blocks
        self.previouspatchin = VectorDataIn         #masterplan map of patches
        self.blockcityout = VectorDataIn        #current map of blocks based on present time
        self.techinplace = VectorDataIn         #technologies implement into present day blocks
        self.addParameter(self, "blockcityin", VIBe2.VECTORDATA_IN)
        self.addParameter(self, "patchdatain", VIBe2.VECTORDATA_IN)
        self.addParameter(self, "techconfigin", VIBe2.VECTORDATA_IN)
        self.addParameter(self, "previousblocksin", VIBe2.VECTORDATA_IN)
        self.addParameter(self, "previouspatchin", VIBe2.VECTORDATA_IN)
        self.addParameter(self, "blockcityout", VIBe2.VECTORDATA_OUT)
        self.addParameter(self, "techinplace", VIBe2.VECTORDATA_OUT)
        
        self.scale_matrix = ["L", "S", "N", "P"] 
        
        #IMPLEMENTATION RULES TAB
        self.dynamic_rule = "B"         #B = Block-based, P = Parcel-based
        self.addParameter(self, "dynamic_rule", VIBe2.STRING)
        
        #Block-based Rules
        self.block_based_thresh = 30    #Threshold for implementation, % exceeded
        self.bb_lot_rule = "AMAP"       #AMAP = as many as possible, STRICT = strictly abide by %
        self.bb_street_zone = 1         #implement even if area hasn't been zoned yet
        self.bb_neigh_zone = 1          #implement even if neigh area hasn't been zoned yet
        self.addParameter(self, "block_based_thresh", VIBe2.DOUBLE)
        self.addParameter(self, "bb_lot_rule", VIBe2.STRING)
        self.addParameter(self, "bb_street_zone", VIBe2.BOOL)
        self.addParameter(self, "bb_neigh_zone", VIBe2.BOOL)
        
        self.pb_lot_rule = "G"             #G = gradual, I = immediate, D = delayed
        self.pb_street_rule = "G"
        self.pb_neigh_rule = "G"
        self.pb_neigh_zone_ignore = 0
        self.addParameter(self, "pb_lot_rule", VIBe2.STRING)
        self.addParameter(self, "pb_street_rule", VIBe2.STRING)
        self.addParameter(self, "pb_neigh_rule", VIBe2.STRING)
        self.addParameter(self, "pb_neigh_zone_ignore", VIBe2.BOOL)
        
        self.prec_rule = "G"
        self.prec_zone_ignore = 0
        self.prec_dev_threshold = 0
        self.prec_dev_percent = 50
        self.addParameter(self, "prec_rule", VIBe2.STRING)
        self.addParameter(self, "prec_zone_ignore", VIBe2.BOOL)
        self.addParameter(self, "prec_dev_threshold", VIBe2.BOOL)
        self.addParameter(self, "prec_dev_percent", VIBe2.DOUBLE)
        
        #DRIVERS TAB - NOT ACTIVE YET, BUT PARAMETER LIST IS DEFINED FOR NOW
        self.driver_people = 0
        self.driver_legal = 0
        self.driver_establish = 0
        self.addParameter(self, "driver_people", VIBe2.BOOL)
        self.addParameter(self, "driver_legal", VIBe2.BOOL)
        self.addParameter(self, "driver_establish", VIBe2.BOOL)
    
    def run(self):
        currentyear = 2000
        #Get vector data
        blockcityin = self.blockcityin.getItem()
        patchdatain = self.patchdatain.getItem()
        techconfigin = self.techconfigin.getItem()
        previousblocksin = self.previousblocksin.getItem()
        previouspatchin = self.previouspatchin.getItem()
        blockcityout = self.blockcityout.getItem()
        techinplace = self.techinplace.getItem()
        
        #Get global map attributes
        map_attr = blockcityin.getAttributes("MapAttributes")
        totsystems = techconfigin.getAttributes("GlobalSystemAttributes").getAttribute("TotalSystems")
        print "Total Systems in map: "+str(totsystems)
        
        #Get block number, etc.
        blocks_num = map_attr.getAttribute("NumBlocks")     #number of blocks to loop through
        blocks_size = map_attr.getAttribute("BlockSize")    #size of block
        map_w = map_attr.getAttribute("WidthBlocks")        #num of blocks wide
        map_h = map_attr.getAttribute("HeightBlocks")       #num of blocks tall
        input_res = map_attr.getAttribute("InputReso")      #resolution of input data
        urbansimdata = map_attr.getStringAttribute("UrbanSimData")
        
        
        basins = map_attr.getAttribute("TotalBasins")
        for i in range(int(basins)):
            #Purpose of this loop is to transfer the basin attributes across to the outport of this module
            currentID = i+1
            basin_attr = blockcityin.getAttributes("BasinID"+str(currentID))
            blockcount = basin_attr.getAttribute("Blocks")
            downstreammostblock = basin_attr.getAttribute("DownBlockID")
            basinblockIDs = basin_attr.getStringAttribute("UpStr")
            
            blockcityout.setAttributes("BasinID"+str(currentID), basin_attr)
        
        #Get all systems for current block
        system_list = []
        for i in range(int(blocks_num)):
            system_list.append([])
        
        for j in range(int(totsystems)):
            locate = techconfigin.getAttributes("System"+str(j)).getAttribute("Location")
            system_list[int(locate-1)].append(j)             #matrix contains all systemIDs (attribute list name) across all blocks
        
        print system_list
        
        #Begin looping across blocks
        for i in range(int(blocks_num)):
            currentID = i + 1
            currentAttList = blockcityin.getAttributes("BlockID"+str(currentID))        #attribute list of current block structure
            currentPatchList = patchdatain.getAttributes("PatchDataID"+str(currentID))
            #existingAttList = existingblock.getAttributes("BlockID"+str(currentID))    #attribute list of the existing block structure
            plist = blockcityin.getPoints("BlockID"+str(currentID))
            flist = blockcityin.getFaces("BlockID"+str(currentID))
            pnetlist = blockcityin.getPoints("NetworkID"+str(currentID))
            enetlist = blockcityin.getEdges("NetworkID"+str(currentID))
            network_attr = blockcityin.getAttributes("NetworkID"+str(currentID))
            
            #-----------------------------------------------------------------#
            #        DETERMINE WHETHER TO UPDATE CURRENT BLOCK AT ALL         #
            #-----------------------------------------------------------------#
            
            ### QUIT CONDITION #1 - BLOCK STATUS = 0 ###
            if self.skipIfStatusZero(currentID, plist, flist, pnetlist, enetlist, network_attr):
                continue
            
            ### QUIT CONDITION #2 - NO SYSTEMS PLANNED FOR BLOCK AT ALL ###
            sys_implement = system_list[i]
            if self.skipIfNoSystems(currentID, sys_implement, plist, flist, pnetlist, enetlist, network_attr):
                continue
 
            #GRAB ALL DETAILS FROM MASTERPLAN FOR USE WHEREVER
            mpdata = self.getMasterPlanData(currentID)
            
            ### QUIT CONDITION #3 - DYNAMIC-MODE = Block-based and DEVELOPMENT < Threshold ###
            if self.dynamic_rule == "B":
                block_skip = self.skipIfBelowBlockThreshold(currentID, float(self.block_based_thresh/100), plist, flist, pnetlist, enetlist, network_attr)
                #use block_skip to determine whether to skip the next few steps
 
            #DECLARE ATTRIBUTE LIST FOR SAVING IMPLEMENTED TECHNOLOGIES LIST
            centreX = currentAttList.getAttribute("Centre_x")
            centreY = currentAttList.getAttribute("Centre_y")
            
            ### LOT IMPLEMENTATION ###
            ### Condition 1: block_skip=False, Condtion 2: there are systems at that scale, Condition 3: there are allotments in the block
            #Get Lot Systems Details
            lot_details = [0, 0]        #[0] - total lot treated, [1] - lot degree
            if block_skip == False:
                sys_implement_lot = self.locatePlannedSystems(sys_implement, "L")
                if sys_implement_lot == None:
                    print "No Lot Systems planned for Block "+str(currentID)
                else:
                    new_lot_details = self.implementLot(currentID, sys_implement_lot, mpdata, [centreX, centreY], currentyear)
                    if new_lot_details != 0:
                        lot_details[0] += new_lot_details[0]        #update total impervious area treated at lot
                        lot_details[1] = new_lot_details[1]         #update the % implementation at lot scale
            
            ### STREET IMPLEMENTATION ###
            ### Condition 1: block_skip=False, Condition 2: there are street systems planned
            streetdeg = 0
            if block_skip == False:
                sys_implement_street = self.locatePlannedSystems(sys_implement, "S")
                if sys_implement_street == None:
                    print "No Street Systems planned for Block "+str(currentID)
                else:
                    self.implementStreet(currentID, sys_implement_street, mpdata, [centreX, centreY], currentyear, lot_details)
                    
            ### NEIGHBOURHOOD IMPLEMENTATION ###
            neighdeg = 0
            if block_skip == False:
                sys_implement_neigh = self.locatePlannedSystems(sys_implement, "N")
                if sys_implement_neigh == None:
                    print "No Neighbourhood Systems planned for Block "+str(currentID)
                else:
                    self.implementNeighbourhood(currentID, sys_implement_neigh, mpdata, [centreX, centreY], currentyear, lot_details)
        
            ### PRECINCT IMPLEMENTATION ###
            precdeg = 0
            sys_implement_prec = self.locatePlannedSystems(sys_implement, "P")
            if sys_implement_prec == None:
                print "No Precinct Systems planned for Block "+str(currentID)
            else:
                self.implementPrecinct(currentID, sys_implement_prec, mpdata, [centreX, centreY], currentyear)
            
            #-----------------------------------------------------------------#
            #        Write all updated Attribute Lists to the output          #
            #-----------------------------------------------------------------#
            
            blockcityout.setPoints("BlockID"+str(currentID),plist)
            blockcityout.setFaces("BlockID"+str(currentID),flist)
            blockcityout.setAttributes("BlockID"+str(currentID),currentAttList)
            blockcityout.setPoints("NetworkID"+str(currentID), pnetlist)
            blockcityout.setEdges("NetworkID"+str(currentID), enetlist)
            blockcityout.setAttributes("NetworkID"+str(currentID), network_attr)
            
            #FOR LOOP END (Repeat for next BlockID)
            
        #Output vector update
        blockcityout.setAttributes("MapAttributes", map_attr)
        
    def getBlockCityVectors(self):
        blockcityin = self.blockcityin.getItem()
        blockcityout = self.blockcityout.getItem()
        return [blockcityin, blockcityout]
    
    def skipIfStatusZero(self, ID, plist, flist, pnetlist, enetlist, network_attr):
        #Determines if the current BlockID's status is 1 or 0, if 0 transfers all its data
        #to the output vector and returns true. If main function receives true
        blockcityin, blockcityout = self.getBlockCityVectors()
        if blockcityin.getAttributes("BlockID"+str(ID)).getAttribute("Status") == 0:
            print "BlockID"+str(ID)+" is not active in simulation"
            blockcityout.setPoints("BlockID"+str(ID), plist)
            blockcityout.setFaces("BlockID"+str(ID),flist)
            blockcityout.setAttributes("BlockID"+str(ID),blockcityin.getAttributes("BlockID"+str(ID)))
            blockcityout.setPoints("NetworkID"+str(ID), pnetlist)
            blockcityout.setEdges("NetworkID"+str(ID), enetlist)
            blockcityout.setAttributes("NetworkID"+str(ID), network_attr)
            return True
        else:
            return False

    def skipIfNoSystems(self, ID, sys_implement, plist, flist, pnetlist, enetlist, network_attr):
        blockcityin, blockcityout = self.getBlockCityVectors()
        if len(sys_implement) == 0:
            print "No Systems planned for Block "+str(ID)+", skipping..."
            #even if block isn't active at all, attributes from previous module are passed on
            blockcityout.setPoints("BlockID"+str(ID),plist)
            blockcityout.setFaces("BlockID"+str(ID),flist)
            blockcityout.setAttributes("BlockID"+str(ID),blockcityin.getAttributes("BlockID"+str(ID)))
            blockcityout.setPoints("NetworkID"+str(ID), pnetlist)
            blockcityout.setEdges("NetworkID"+str(ID), enetlist)
            blockcityout.setAttributes("NetworkID"+str(ID), network_attr)
            return True
        else:
            return False
    
    def getMasterPlanData(self, ID):
        #Gets data for the current block from the simulated masterplan, parameters are saved into
        #an array, which is returned with following index reference:
        #   0 - total allotments in block
        #   1 - total residential impervious area of district
        #   2 - impervious area of one lot
        #   3 - Available space on the street scape
        #   4 - Available space in open areas for neighbourhood systems
        previousblocksin = self.previousblocksin.getItem()
        allots = previousblocksin.getAttributes("BlockID"+str(ID)).getAttribute("ResAllots")         
        resTIarea = previousblocksin.getAttributes("BlockID"+str(ID)).getAttribute("ResTIArea")      
        LotImpArea = previousblocksin.getAttributes("BlockID"+str(ID)).getAttribute("ResLotImpA")    
        AvlStreet = previousblocksin.getAttributes("BlockID"+str(ID)).getAttribute("AvlStreet")      
        AvlNeigh = previousblocksin.getAttributes("BlockID"+str(ID)).getAttribute("ALUC_PG")
        masterplan_array = [allots, resTIarea, LotImpArea, AvlStreet, AvlNeigh]
        return masterplan_array
    
    def skipIfBelowBlockThreshold(self, ID, threshold, plist, flist, pnetlist, enetlist, network_attr):
        blockcityin, blockcityout = self.getBlockCityVectors()
        prop_undev = blockcityin.getAttributes("BlockID"+str(ID)).getAttribute("pLUC_Und")
        if (1-prop_undev) < threshold:
            blockcityout.setPoints("BlockID"+str(ID),plist)
            blockcityout.setFaces("BlockID"+str(ID),flist)
            blockcityout.setAttributes("BlockID"+str(ID),blockcityin.getAttributes("BlockID"+str(ID)))
            blockcityout.setPoints("NetworkID"+str(ID), pnetlist)
            blockcityout.setEdges("NetworkID"+str(ID), enetlist)
            blockcityout.setAttributes("NetworkID"+str(ID), network_attr)
            return True
        else:
            return False
    
    def locatePlannedSystems(self, system_list, scale):
        #Searches the input planned technologies list for a system that fits the scale in the block
        #Returns the system attribute list
        techconfigin = self.techconfigin.getItem()
        system_object = None
        for i in system_list:
            if str(techconfigin.getAttributes("System"+str(i)).getStringAttribute("Scale")) == scale:
                system_object = techconfigin.getAttributes("System"+str(i))
        return system_object

    def implementLot(self, ID, sys_descr, mpdata, centrePoints, currentyear):
        #Implements lot-scale technologies into current Block ID, takes several inputs
        #Calls the function drawTechnologyDataPoint() to output geometry and attribute data
        #   ID = BlockID
        #   sys_descr = AttributeList of the system found with locatePlannedSystem()
        #   mpdata = Masterplan data found with getMasterPlanData()
        #   centrePoints = [centreX, centreY]
        #   currentyear = current building year to be added to implemented system
        blockcityin, blockcityout = self.getBlockCityVectors()
        currentAttList = blockcityin.getAttributes("BlockID"+str(ID))
        lotcount = sys_descr.getAttribute("TotSystems")
        system_type_matrix = ['BF', 'SW', 'WSUR', 'PB', 'IS']               
        system_type_numeric = [2463, 7925, 9787, 7663, 4635]                #Think Telephone Buttons :) ('Biof', 'Swal', 'WSUR', 'Pond', 'Infl')
            
        #Check if block has allotments, if not, do nothing
        if currentAttList.getAttribute("ResAllots") == 0:
            print "Current Block "+str(ID)+" has no residential allotments"
            return 0     #break function here
    
        #Get Details
        allotments = currentAttList.getAttribute("ResAllots")
        lotimparea = currentAttList.getAttribute("ResLotImpA")
        roofarea = currentAttList.getAttribute("ResLotRoofA")
        openspace = currentAttList.getAttribute("rfw_Adev")
        
        lottype = sys_descr.getStringAttribute("Type1")
        lotdeg = sys_descr.getAttribute("Service1")
        lotsysarea = sys_descr.getAttribute("Area1")
        lotsysstatus = sys_descr.getAttribute("Status1")
        lotsysbuildyr = sys_descr.getAttribute("YearConst1")
        loteafact = sys_descr.getAttribute("AreaFactor1")
        lotqty = sys_descr.getAttribute("Quantity1")
        lotimpT = sys_descr.getAttribute("ImpTreated1")
        
        print lottype, lotdeg, lotsysarea, lotsysstatus, lotsysbuildyr
        
        if lotsysbuildyr == 9999:               #if the system is already implemented, then skip
            goallots = int(lotdeg*mpdata[0])        #final number of houses with systems (masterplan)
            print "Goal Lots: ", str(goallots)
            
            #calculate how many to implement based on allotment rules
            if self.bb_lot_rule == "AMAP":
                #AMAP = as many as possible
                #lesser of: how many we ultimately want or how many have been built
                num_systems_impl = min(goallots, allotments)
                print num_systems_impl
            elif self.bb_lot_rule == "STRICT":
                #STRICT = strictly follow %
                #number of allotments built * %
                num_systems_impl = int(allotments * lotdeg)
                print num_systems_impl
                lotqty = num_systems_impl
            
            tot_system_area = num_systems_impl * lotsysarea
            tot_lot_treated = num_systems_impl * lotimparea
            lotimpT = tot_lot_treated
            print tot_system_area
            print tot_lot_treated
        
        #Write to outputs
        techimpl_attr = Attribute()
        techimpl_attr.setAttribute("Location", ID)
        techimpl_attr.setAttribute("Scale", self.scale_matrix.index("L"))
        techimpl_attr.setAttribute("TotSystems", lotcount)
        for j in range(int(lotcount)):
            techimpl_attr.setAttribute("Sys"+str(j+1)+"Type", lottype)
            techimpl_attr.setAttribute("Sys"+str(j+1)+"TypeN", system_type_numeric[system_type_matrix.index(lottype)])
            techimpl_attr.setAttribute("Sys"+str(j+1)+"Qty", lotqty)
            #techimpl_attr.setAttribute("Sys"+str(j+1)+"TotA", tot_system_area)
            techimpl_attr.setAttribute("Sys"+str(j+1)+"ImpT", lotimpT)
            techimpl_attr.setAttribute("Sys"+str(j+1)+"Area", lotsysarea)
            techimpl_attr.setAttribute("Sys"+str(j+1)+"Status", 1)
            techimpl_attr.setAttribute("Sys"+str(j+1)+"Year", min(lotsysbuildyr, currentyear))
            techimpl_attr.setAttribute("Sys"+str(j+1)+"Degree", lotdeg)
            techimpl_attr.setAttribute("Sys"+str(j+1)+"EAFact", loteafact)
            
        self.drawTechnologyDataPoint(ID, centrePoints[0], centrePoints[1], "L", techimpl_attr)
        if lotsysbuildyr < currentyear:               #if the system is already implemented, then skip
            return [lotimpT, lotdeg]
        return [tot_lot_treated, lotdeg]
    
    def implementStreet(self, ID, sys_descr, mpdata, centrePoints, currentyear, lot_details):
        #Implements street-scale technologies into current Block ID, takes several inputs
            #Calls the function drawTechnologyDataPoint() to output geometry and attribute data
            #   ID = BlockID
            #   sys_descr = AttributeList of the system found with locatePlannedSystem()
            #   mpdata = Masterplan data found with getMasterPlanData()
            #   centrePoints = [centreX, centreY]
            #   currentyear = current building year to be added to implemented system
            #   lot_details = [total lot impervious treated, lot % implementation]
        blockcityin, blockcityout = self.getBlockCityVectors()
        currentAttList = blockcityin.getAttributes("BlockID"+str(ID))
        streetcount = sys_descr.getAttribute("TotSystems")
        system_type_matrix = ['BF', 'SW', 'WSUR', 'PB', 'IS']               
        system_type_numeric = [2463, 7925, 9787, 7663, 4635]                #Think Telephone Buttons :) ('Biof', 'Swal', 'WSUR', 'Pond', 'Infl')
           
            
        #Grab data
        streettype = sys_descr.getStringAttribute("Type1")
        streetdeg = sys_descr.getAttribute("Service1")
        streetsysarea = sys_descr.getAttribute("Area1")
        streetsysstatus = sys_descr.getAttribute("Status1")
        streetsysbuildyr = sys_descr.getAttribute("YearConst1")
        streeteafact = sys_descr.getAttribute("AreaFactor1")
        streetqty = sys_descr.getAttribute("Quantity1")
        streetimpT = sys_descr.getAttribute("ImpTreated1")
        
        print streettype, streetdeg, streetsysarea, streetsysstatus, streetsysbuildyr
        
        if streetsysbuildyr == 9999:               #if the system is already implemented, then skip
            #GET CURRENT DETAILS
            resimparea = currentAttList.getAttribute("ResTIArea")
            street_neigh_imp_area = resimparea - lot_details[0]        #if there was no lot implementation, then tot_lot_treated = 0
            street_avl_space = currentAttList.getAttribute("AvlStreet")
            print "Street Areas:"
            print resimparea, street_neigh_imp_area, street_avl_space
            
            #Masterplan details
            street_neigh_masterplan = mpdata[1] - (mpdata[2]*lot_details[1]*mpdata[0])
            print "Masterplan: "
            print mpdata[1], street_neigh_masterplan, mpdata[3]
            
            #Compare impervious areas
            imp_developed = float(resimparea)/float(mpdata[1])
            if imp_developed < float(self.block_based_thresh/100):              #QUIT CONDITION 1: developed imp area less than threshold
                return True
            if self.bb_street_zone == 0 and street_avl_space < streetsysarea:   #QUIT CONDITION 2: no space and model was restrained to available space
                return True
            
            #else implement the system
            tot_street_treated = streetdeg * street_neigh_imp_area
            streetimpT = tot_street_treated
            print "Street Area treated: ", str(tot_street_treated)
            
        techimpl_attr = Attribute()
        techimpl_attr.setAttribute("Location", ID)
        techimpl_attr.setAttribute("Scale", self.scale_matrix.index("S"))
        techimpl_attr.setAttribute("TotSystems", streetcount)
        for j in range(int(streetcount)):
            techimpl_attr.setAttribute("Sys"+str(j+1)+"Type", streettype)
            techimpl_attr.setAttribute("Sys"+str(j+1)+"TypeN", system_type_numeric[system_type_matrix.index(streettype)])
            techimpl_attr.setAttribute("Sys"+str(j+1)+"Qty", streetqty)
            techimpl_attr.setAttribute("Sys"+str(j+1)+"Area", streetsysarea)
            techimpl_attr.setAttribute("Sys"+str(j+1)+"ImpT", streetimpT)
            techimpl_attr.setAttribute("Sys"+str(j+1)+"Status", 1)
            techimpl_attr.setAttribute("Sys"+str(j+1)+"Year", min(streetsysbuildyr, currentyear))
            techimpl_attr.setAttribute("Sys"+str(j+1)+"Degree", streetdeg)
            techimpl_attr.setAttribute("Sys"+str(j+1)+"EAFact", streeteafact)
            
        self.drawTechnologyDataPoint(ID, centrePoints[0], centrePoints[1], "S", techimpl_attr)
        return True
    
    def implementNeighbourhood(self, ID, sys_descr, mpdata, centrePoints, currentyear, lot_details):
        #Implements neighbourhood-scale technologies into current Block ID, takes several inputs
        #Calls the function drawTechnologyDataPoint() to output geometry and attribute data
        #   ID = BlockID
        #   sys_descr = AttributeList of the system found with locatePlannedSystem()
        #   mpdata = Masterplan data found with getMasterPlanData()
        #   centrePoints = [centreX, centreY]
        #   currentyear = current building year to be added to implemented system
        #   lot_details = [total lot impervious treated, lot % implementation]
        blockcityin, blockcityout = self.getBlockCityVectors()
        currentAttList = blockcityin.getAttributes("BlockID"+str(ID))
        neighcount = sys_descr.getAttribute("TotSystems")
        system_type_matrix = ['BF', 'SW', 'WSUR', 'PB', 'IS']               
        system_type_numeric = [2463, 7925, 9787, 7663, 4635]                #Think Telephone Buttons :) ('Biof', 'Swal', 'WSUR', 'Pond', 'Infl')
            
        #Grab Data
        neightype = sys_descr.getStringAttribute("Type1")
        neighdeg = sys_descr.getAttribute("Service1")
        neighsysarea = sys_descr.getAttribute("Area1")
        neighsysstatus = sys_descr.getAttribute("Status1")
        neighsysbuildyr = sys_descr.getAttribute("YearConst1")
        neigheafact = sys_descr.getAttribute("AreaFactor1")
        neighqty = sys_descr.getAttribute("Quantity1")
        neighimpT = sys_descr.getAttribute("ImpTreated1")
        
        print neightype, neighdeg, neighsysarea, neighsysstatus, neighsysbuildyr
        #Follow the same as street, but check the open space first
        
        if neighsysbuildyr == 9999:               #if the system is already implemented, then skip
            #Current Year Details
            resimparea = currentAttList.getAttribute("ResTIArea")
            street_neigh_imp_area = resimparea - lot_details[0]        #if there was no lot implementation, then tot_lot_treated = 0
            neigh_avail_sp = currentAttList.getAttribute("ALUC_PG")
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
            neighimpT = tot_neigh_treated
            print "Neigh Area treated: ", str(tot_neigh_treated)
        
        techimpl_attr = Attribute()
        techimpl_attr.setAttribute("Location", ID)
        techimpl_attr.setAttribute("Scale", self.scale_matrix.index("N"))
        techimpl_attr.setAttribute("TotSystems", neighcount)
        for j in range(int(neighcount)):
            techimpl_attr.setAttribute("Sys"+str(j+1)+"Type", neightype)
            techimpl_attr.setAttribute("Sys"+str(j+1)+"TypeN", system_type_numeric[system_type_matrix.index(neightype)])
            techimpl_attr.setAttribute("Sys"+str(j+1)+"Qty", neighqty)
            techimpl_attr.setAttribute("Sys"+str(j+1)+"Area", neighsysarea)
            techimpl_attr.setAttribute("Sys"+str(j+1)+"ImpT", neighimpT)
            techimpl_attr.setAttribute("Sys"+str(j+1)+"Status", 1)
            techimpl_attr.setAttribute("Sys"+str(j+1)+"Year", min(neighsysbuildyr, currentyear))
            techimpl_attr.setAttribute("Sys"+str(j+1)+"Degree", neighdeg) 
            techimpl_attr.setAttribute("Sys"+str(j+1)+"EAFact", neigheafact)
            
        self.drawTechnologyDataPoint(ID, centrePoints[0], centrePoints[1], "N", techimpl_attr)
        return True
    
    def drawTechnologyDataPoint(self, ID, centreX, centreY, scale, techimpl_attr):
        #Grab data
        techinplace = self.techinplace.getItem()
        blocks_size = self.blockcityin.getItem().getAttributes("MapAttributes").getAttribute("BlockSize")    
        
        #Use an offsets_matrix and the scale to locate the proper coordinates
        offsets_matrix = [[centreX+blocks_size/8, centreY+blocks_size/4],[centreX+blocks_size/4, centreY-blocks_size/8],[centreX-blocks_size/8, centreY-blocks_size/4],[centreX-blocks_size/4, centreY+blocks_size/8]]
        scale_matrix = ["L", "S", "N", "P"]
        scale_index = scale_matrix.index(scale)
        coordinates = offsets_matrix[scale_index]
        
        #Draw the point and assign attributes
        plist = pyvibe.PointList()
        plist.append(Point(coordinates[0], coordinates[1], 0))
        techinplace.setPoints("BlockID"+str(ID)+str(scale), plist)
        techinplace.setAttributes("BlockID"+str(ID)+str(scale), techimpl_attr)
        return True

    
    def getUpstreamIDs(self, ID):
        blockcityin = self.blockcityin.getItem()
        currentAttList = blockcityin.getAttributes("BlockID"+str(ID))
        upstr_string = currentAttList.getStringAttribute("BasinBlocks") #does not include current ID itself
        upstreamIDs = upstr_string.split(',')
        upstreamIDs.remove('')
        for i in range(len(upstreamIDs)):
            upstreamIDs[i] = int(upstreamIDs[i])
        return upstreamIDs

    def calculateUpstreamDevelopment(self, ID, upstreamIDs):
        blockcityin = self.blockcityin.getItem()
        currentAttList = blockcityin.getAttributes("BlockID"+str(ID))
        block_size = blockcityin.getAttributes("MapAttributes").getAttribute("BlockSize")
        #grab total developed area
        upstreamArea = currentAttList.getAttribute("BasinArea")*10000 + (block_size * block_size)
        undeveloped_area = currentAttList.getAttribute("ALUC_Und")
        for i in upstreamIDs:
            undeveloped_area += blockcityin.getAttributes("BlockID"+str(i)).getAttribute("ALUC_Und")
        percentage_dev = 1-(undeveloped_area/upstreamArea)
        return percentage_dev
    
    def getUpstreamImpArea(self, ID, upstreamIDs):
        #This function scans the database of blockIDs and tallies up the total 
        #upstream impervious area returning it to the main run function of the
        #module.
        blockcityin = self.blockcityin.getItem()
        currentAttList = blockcityin.getAttributes("BlockID"+str(ID))
        Aimptotal = currentAttList.getAttribute("ResTIArea")   #tally for total upstream impervious area
        for i in upstreamIDs:
            Aimptotal += blockcityin.getAttributes("BlockID"+str(i)).getAttribute("ResTIArea")
        return Aimptotal        #in sqm units
    
    def implementPrecinct(self, ID, sys_descr, mpdata, centrePoints, currentyear):
        #Implements precinct-scale technologies into current Block ID, takes several inputs
        #Calls the function drawTechnologyDataPoint() to output geometry and attribute data
        #   ID = BlockID
        #   sys_descr = AttributeList of the system found with locatePlannedSystem()
        #   mpdata = Masterplan data found with getMasterPlanData()
        #   centrePoints = [centreX, centreY]
        #   currentyear = current building year to be added to implemented system
        blockcityin, blockcityout = self.getBlockCityVectors()
        currentAttList = blockcityin.getAttributes("BlockID"+str(ID))
        preccount = sys_descr.getAttribute("TotSystems")
        system_type_matrix = ['BF', 'SW', 'WSUR', 'PB', 'IS']               
        system_type_numeric = [2463, 7925, 9787, 7663, 4635]                #Think Telephone Buttons :) ('Biof', 'Swal', 'WSUR', 'Pond', 'Infl')
            
        upstreamIDs = self.getUpstreamIDs(ID)
        
        #Calculate total development upstream of block
        if self.prec_dev_threshold == True:
            #if this is selected as part of the simulation then calculate upstream development
            percentage_dev = self.calculateUpstreamDevelopment(ID, upstreamIDs)
            if percentage_dev < float(self.prec_dev_percent/100):
                print "Upstream precinct not developed enough, skipping..."
                return True
        #Otherwise force implement precinct systems
        
        #Grab Data    
        prectype = sys_descr.getStringAttribute("Type1")
        precdeg = sys_descr.getAttribute("Service1")
        precsysarea = sys_descr.getAttribute("Area1")
        precsysstatus = sys_descr.getAttribute("Status1")
        precsysbuildyr = sys_descr.getAttribute("YearConst1")
        preceafact = sys_descr.getAttribute("AreaFactor1")
        precqty = sys_descr.getAttribute("Quantity1")
        precimpT = sys_descr.getAttribute("ImpTreated1")
        
        print prectype, precdeg, precsysarea, precsysstatus, precsysbuildyr
        #Follow the same as street, but check the open space first
        
        if precsysbuildyr == 9999:               #if the system is already implemented, then skip
            neigh_avail_sp = currentAttList.getAttribute("ALUC_PG") 
            
            #check if space
            if self.prec_zone_ignore == False and precsysarea > neigh_avail_sp:
                print "Not enough space yet"
                return True
            
            imp_area_tot = self.getUpstreamImpArea(ID, upstreamIDs)
            tot_prec_treated = precdeg * imp_area_tot
            precimpT = tot_prec_treated
            
        techimpl_attr = Attribute()
        techimpl_attr.setAttribute("Location", ID)
        techimpl_attr.setAttribute("Scale", self.scale_matrix.index("P"))
        techimpl_attr.setAttribute("TotSystems", preccount)
        for j in range(int(preccount)):
            techimpl_attr.setAttribute("Sys"+str(j+1)+"Type", prectype)
            techimpl_attr.setAttribute("Sys"+str(j+1)+"TypeN", system_type_numeric[system_type_matrix.index(prectype)])
            techimpl_attr.setAttribute("Sys"+str(j+1)+"Qty", precqty)
            techimpl_attr.setAttribute("Sys"+str(j+1)+"Area", precsysarea)
            techimpl_attr.setAttribute("Sys"+str(j+1)+"ImpT", precimpT)
            techimpl_attr.setAttribute("Sys"+str(j+1)+"Status", 1)
            techimpl_attr.setAttribute("Sys"+str(j+1)+"Year", min(precsysbuildyr, currentyear))
            techimpl_attr.setAttribute("Sys"+str(j+1)+"Degree", precdeg) 
            techimpl_attr.setAttribute("Sys"+str(j+1)+"EAFact", preceafact)
        
        self.drawTechnologyDataPoint(ID, centrePoints[0], centrePoints[1], "P", techimpl_attr)
        return True
    
    
    ########################################################
    #LINK WITH GUI                                         #
    ########################################################
                        
    def createInputDialog(self):
        form = activatetechimplementGUI(self, QApplication.activeWindow())
        form.show()
        return True             