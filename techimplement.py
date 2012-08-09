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
        currentyear = 1960
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
        
        #CONVERSIONS
        #convert percentages to proportions and proportions to percentages and adjust other necessary
        #parameters
        prec_dev_percent = float(self.prec_dev_percent/100)
        
        
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
        system_indices = []
        for i in range(int(blocks_num)):
            system_indices.append([])
        
        for j in range(int(totsystems)):
            locate = techconfigin.getAttributes("System"+str(j)).getAttribute("Location")
            system_indices[int(locate-1)].append(j)             #matrix contains all systemIDs (attribute list name) across all blocks
        
        print system_indices
        
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
            block_status = currentAttList.getAttribute("Status")
            if block_status == 0:
                print "BlockID"+str(currentID)+" is not active in simulation"
                #even if block isn't active at all, attributes from previous module are passed on
                blockcityout.setPoints("BlockID"+str(currentID),plist)
                blockcityout.setFaces("BlockID"+str(currentID),flist)
                blockcityout.setAttributes("BlockID"+str(currentID),currentAttList)
                blockcityout.setPoints("NetworkID"+str(currentID), pnetlist)
                blockcityout.setEdges("NetworkID"+str(currentID), enetlist)
                blockcityout.setAttributes("NetworkID"+str(currentID), network_attr)
                
                #skips the for loop iteration to the next block, not more needs to be done
                continue
            
            ### QUIT CONDITION #2 - NO SYSTEMS PLANNED FOR BLOCK AT ALL ###
            sys_implement = system_indices[i]
            print sys_implement
            if len(sys_implement) == 0:
                print "No Systems planned for Block "+str(currentID)+", skipping..."
                #even if block isn't active at all, attributes from previous module are passed on
                blockcityout.setPoints("BlockID"+str(currentID),plist)
                blockcityout.setFaces("BlockID"+str(currentID),flist)
                blockcityout.setAttributes("BlockID"+str(currentID),currentAttList)
                blockcityout.setPoints("NetworkID"+str(currentID), pnetlist)
                blockcityout.setEdges("NetworkID"+str(currentID), enetlist)
                blockcityout.setAttributes("NetworkID"+str(currentID), network_attr)
                #skip the block
                continue
            
            #GRAB ALL DETAILS FROM MASTERPLAN FOR USE WHEREVER
            mastplanallots = previousblocksin.getAttributes("BlockID"+str(currentID)).getAttribute("ResAllots")         #total allotments planned for block
            mastplanresTIarea = previousblocksin.getAttributes("BlockID"+str(currentID)).getAttribute("ResTIArea")      #total impervious area of district
            mastplanLotImpArea = previousblocksin.getAttributes("BlockID"+str(currentID)).getAttribute("ResLotImpA")    #impervious area of one lot
            mastplanAvlStreet = previousblocksin.getAttributes("BlockID"+str(currentID)).getAttribute("AvlStreet")      #Available street area
            mastplanAvlNeigh = previousblocksin.getAttributes("BlockID"+str(currentID)).getAttribute("ALUC_PG")         #Available neighbourhood area
            
            ### QUIT CONDITION #3 - DYNAMIC-MODE = Block-based and DEVELOPMENT < Threshold ###
            #Get Block Data
            block_skip = False
            if self.dynamic_rule == "B" and (1-currentAttList.getAttribute("pLUC_Und")) < float(self.block_based_thresh/100):
                print "BlockID"+str(currentID)+" is not developed enough yet, skipping..."
                #even if block isn't active at all, attributes from previous module are passed on
                blockcityout.setPoints("BlockID"+str(currentID),plist)
                blockcityout.setFaces("BlockID"+str(currentID),flist)
                blockcityout.setAttributes("BlockID"+str(currentID),currentAttList)
                blockcityout.setPoints("NetworkID"+str(currentID), pnetlist)
                blockcityout.setEdges("NetworkID"+str(currentID), enetlist)
                blockcityout.setAttributes("NetworkID"+str(currentID), network_attr)
                #skip the block
                block_skip = True
            
            #DECLARE ATTRIBUTE LIST FOR SAVING IMPLEMENTED TECHNOLOGIES LIST
            techimpl_attr = Attribute()
            centreX = currentAttList.getAttribute("Centre_x")
            centreY = currentAttList.getAttribute("Centre_y")
            offsets_matrix = [[centreX+blocks_size/8, centreY+blocks_size/4],[centreX+blocks_size/4, centreY-blocks_size/8],[centreX-blocks_size/8, centreY-blocks_size/4],[centreX-blocks_size/4, centreY+blocks_size/8]]
            
            ### LOT IMPLEMENTATION ###
            ### Condition 1: block_skip=False, Condtion 2: there are systems at that scale, Condition 3: there are allotments in the block
            #Get Lot Systems Details
            tot_lot_treated = 0
            lotdeg = 0
            if block_skip == False:
                systemfound = 0
                for j in sys_implement:
                    if str(techconfigin.getAttributes("System"+str(j)).getStringAttribute("Scale")) == "L":
                        sys_implement_lot = techconfigin.getAttributes("System"+str(j))
                        systemfound = 1
                if systemfound == 0:                #IF THERE ARE NO LOT SYSTEMS, CONTINUE ON TO STREET
                    print "No Lot Systems planned for Block "+str(currentID)
                else:
                    lotcount = sys_implement_lot.getAttribute("TotSystems")
                    if currentAttList.getAttribute("ResAllots") == 0:
                        print "Current Block "+str(currentID)+" has no residential allotments"
                        pass
                    else:
                        #Get Residential Details
                        allotments = currentAttList.getAttribute("ResAllots")
                        lotimparea = currentAttList.getAttribute("ResLotImpA")
                        roofarea = currentAttList.getAttribute("ResLotRoofA")
                        openspace = currentAttList.getAttribute("rfw_Adev")
                        
                        lottype = sys_implement_lot.getStringAttribute("Type1")
                        lotdeg = sys_implement_lot.getAttribute("Service1")
                        lotsysarea = sys_implement_lot.getAttribute("Area1")
                        lotsysstatus = sys_implement_lot.getAttribute("Status1")
                        lotsysbuildyr = sys_implement_lot.getAttribute("YearConst1")
                        
                        print lottype, lotdeg, lotsysarea, lotsysstatus, lotsysbuildyr
                        
                        goallots = int(lotdeg*mastplanallots)
                        
                        #lot implementation rule - as many as possible or strictly follow planning
                        if self.bb_lot_rule == "AMAP":
                            num_systems_impl = min(goallots, allotments)            #if as many as possible: either the desired number of allotments (goallots) or however many have been built (allotments)
                        elif self.bb_lot_rule == "STRICT":
                            num_systems_impl = int(allotments * lotdeg)             #if strictly follow planning %, then current number of allotments * %
                        print num_systems_impl
                        
                        tot_system_area = num_systems_impl * lotsysarea
                        tot_lot_treated = num_systems_impl * lotimparea
                        
                        print tot_system_area
                        print tot_lot_treated
                        
                        #Write out lot systems information
                        techimpl_attr.setAttribute("Location", currentID)
                        techimpl_attr.setAttribute("Scale", "L")
                        techimpl_attr.setAttribute("TotSystems", lotcount)
                        for j in range(int(lotcount)):
                            techimpl_attr.setAttribute("Sys"+str(j+1)+"Type", lottype)
                            techimpl_attr.setAttribute("Sys"+str(j+1)+"Qty", num_systems_impl)
                            techimpl_attr.setAttribute("Sys"+str(j+1)+"TotA", tot_system_area)
                            techimpl_attr.setAttribute("Sys"+str(j+1)+"ImpT", tot_lot_treated)
                            techimpl_attr.setAttribute("Sys"+str(j+1)+"Area", lotsysarea)
                            techimpl_attr.setAttribute("Sys"+str(j+1)+"Status", 1)
                            techimpl_attr.setAttribute("Sys"+str(j+1)+"Buildyr", currentyear)
                        
                        coordinates = offsets_matrix[0]
                        plist = pyvibe.PointList()
                        plist.append(Point(coordinates[0],coordinates[1],0))
                        techinplace.setPoints("BlockID"+str(currentID)+"L", plist)
                        techinplace.setAttributes("BlockID"+str(currentID)+"L", techimpl_attr)
                         
            ### STREET IMPLEMENTATION ###
            ### Condition 1: block_skip=False, Condition 2: there are street systems planned
            streetdeg = 0
            if block_skip == False:
                systemfound = 0             #see if there are systems
                for j in sys_implement:
                    if str(techconfigin.getAttributes("System"+str(j)).getStringAttribute("Scale")) == "S":
                        sys_implement_street = techconfigin.getAttributes("System"+str(j))
                        systemfound = 1
                        
                if systemfound == 0:                #IF THERE ARE NO LOT SYSTEMS, CONTINUE ON TO NEIGHBOURHOOD
                    print "No Street Systems planned for Block "+str(currentID)
                else:
                    #implement street system
                    streettype = sys_implement_street.getStringAttribute("Type1")
                    streetdeg = sys_implement_street.getAttribute("Service1")
                    streetsysarea = sys_implement_street.getAttribute("Area1")
                    streetsysstatus = sys_implement_street.getAttribute("Status1")
                    streetsysbuildyr = sys_implement_street.getAttribute("YearConst1")
                    
                    print streettype, streetdeg, streetsysarea, streetsysstatus, streetsysbuildyr
                    
                    #Get curent impervious area, get impervious area to treat of the whole thing, if current is within reason of 'to be treated area', implement entire street system if available space is there
                    
                    #GET CURRENT DETAILS
                    resimparea = currentAttList.getAttribute("ResTIArea")
                    street_neigh_imp_area = resimparea - tot_lot_treated        #if there was no lot implementation, then tot_lot_treated = 0
                    print "Street Areas:"
                    print resimparea
                    print street_neigh_imp_area
                    street_avl_space = currentAttList.getAttribute("AvlStreet")
                    print street_avl_space
                    
                    #Masterplan details
                    street_neigh_masterplan = mastplanresTIarea - (mastplanLotImpArea*lotdeg*mastplanallots)
                    print "Masterplan: "
                    print mastplanresTIarea
                    print street_neigh_masterplan
                    print mastplanAvlStreet
                    
                
            ### NEIGHBOURHOOD IMPLEMENTATION ###
            neighdeg = 0
            if block_skip == False:
                systemfound = 0             #see if there are systems
                for j in sys_implement:
                    if str(techconfigin.getAttributes("System"+str(j)).getStringAttribute("Scale")) == "N":
                        sys_implement_street = techconfigin.getAttributes("System"+str(j))
                        systemfound = 1
                        
                if systemfound == 0:                #IF THERE ARE NO LOT SYSTEMS, CONTINUE ON TO PRECINCT
                    print "No Neighbourhood Systems planned for Block "+str(currentID)
                else:
                    #implement neighbourhood system
                    neightype = sys_implement_street.getStringAttribute("Type1")
                    neighdeg = sys_implement_street.getAttribute("Service1")
                    neighsysarea = sys_implement_street.getAttribute("Area1")
                    neighsysstatus = sys_implement_street.getAttribute("Status1")
                    neighsysbuildyr = sys_implement_street.getAttribute("YearConst1")
                    
                    print neightype, neighdeg, neighsysarea, neighsysstatus, neighsysbuildyr
                    #Follow the same as street, but check the open space first
                    
                    #Current Year Details
                    resimparea = currentAttList.getAttribute("ResTIArea")
                    street_neigh_imp_area = resimparea - tot_lot_treated        #if there was no lot implementation, then tot_lot_treated = 0
                    print "Neigh Areas:"
                    print "District Imp", str(resimparea)
                    print "Imp to treat at st and n:", str(street_neigh_imp_area)
                    neigh_avail_sp = currentAttList.getAttribute("ALUC_PG")
                    print "Available space: ", str(neigh_avail_sp)
                    
                    #Masterplan details
                    street_neigh_masterplan = mastplanresTIarea - (mastplanLotImpArea*lotdeg*mastplanallots)
                    print "Masterplan: "
                    print "District imp: ", str(mastplanresTIarea)
                    print "Imp to treat at st and n:", str(street_neigh_masterplan)
                    print "Availble space: ", str(mastplanAvlNeigh)
                    
            ### PRECINCT IMPLEMENTATION ###
            systemfound = 0             #see if there are systems
            for j in sys_implement:
                if str(techconfigin.getAttributes("System"+str(j)).getStringAttribute("Scale")) == "P":
                    sys_implement_street = techconfigin.getAttributes("System"+str(j))
                    systemfound = 1
                    
            if systemfound == 0:                #IF THERE ARE NO PRECINCT SYSTEMS, PASS
                print "No Precinct Systems planned for Block "+str(currentID)
            else:
                
                
                pass
                #BASIN CHECK DEVELOPMENT %
            
            
            
            
        
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
        
    
    ########################################################
    #LINK WITH GUI                                         #
    ########################################################        
    def calculateUpstreamDeveloped(self, ID):
        #determines the total upstream area % that has been developed
        pass
    
                        
    def createInputDialog(self):
        form = activatetechimplementGUI(self, QApplication.activeWindow())
        form.show()
        return True             