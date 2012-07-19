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
        
        self.driver_people = 0
        self.driver_legal = 0
        self.driver_establish = 0
        self.addParameter(self, "driver_people", VIBe2.BOOL)
        self.addParameter(self, "driver_legal", VIBe2.BOOL)
        self.addParameter(self, "driver_establish", VIBe2.BOOL)
        
        self.lot_rule = "G"             #G = gradual, I = immediate, D = delayed
        self.street_rule = "G"
        self.neigh_rule = "G"
        self.prec_rule = "G"
        self.neigh_zone_ignore = 0
        self.prec_zone_ignore = 0
        self.prec_dev_threshold = 0
        self.prec_dev_percent = 50
        self.addParameter(self, "lot_rule", VIBe2.STRING)
        self.addParameter(self, "street_rule", VIBe2.STRING)
        self.addParameter(self, "neigh_rule", VIBe2.STRING)
        self.addParameter(self, "prec_rule", VIBe2.STRING)
        self.addParameter(self, "neigh_zone_ignore", VIBe2.BOOL)
        self.addParameter(self, "prec_zone_ignore", VIBe2.BOOL)
        self.addParameter(self, "prec_dev_threshold", VIBe2.BOOL)
        self.addParameter(self, "prec_dev_percent", VIBe2.DOUBLE)
        
    
    def run(self):
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
        
        #Get block number, etc.
        blocks_num = map_attr.getAttribute("NumBlocks")     #number of blocks to loop through
        blocks_size = map_attr.getAttribute("BlockSize")    #size of block
        map_w = map_attr.getAttribute("WidthBlocks")        #num of blocks wide
        map_h = map_attr.getAttribute("HeightBlocks")       #num of blocks tall
        input_res = map_attr.getAttribute("InputReso")      #resolution of input data
        urbansimdata = map_attr.getStringAttribute("UrbanSimData")
        
        basins = map_attr.getAttribute("TotalBasins")
        for i in range(int(basins)):
            currentID = i+1
            basin_attr = blockcityin.getAttributes("BasinID"+str(currentID))
            blockcityout.setAttributes("BasinID"+str(currentID), basin_attr)
        
        #CONVERSIONS
        #convert percentages to proportions and proportions to percentages and adjust other necessary
        #parameters
        prec_dev_percent = float(self.prec_dev_percent/100)
        
        
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
                
                patchcityout.setPoints("PatchDataID"+str(currentID), plist)
                patchcityout.setFaces("PatchDataID"+str(currentID),flist)
                patchcityout.setAttributes("PatchDataID"+str(currentID), currentPatchList)
            
                #skips the for loop iteration to the next block, not more needs to be done
                continue
            
            print currentID
            
        
            #-----------------------------------------------------------------#
            #        Write all updated Attribute Lists to the output          #
            #-----------------------------------------------------------------#
            
            blockcityout.setPoints("BlockID"+str(currentID),plist)
            blockcityout.setFaces("BlockID"+str(currentID),flist)
            blockcityout.setAttributes("BlockID"+str(currentID),currentAttList)
            blockcityout.setPoints("NetworkID"+str(currentID), pnetlist)
            blockcityout.setEdges("NetworkID"+str(currentID), enetlist)
            blockcityout.setAttributes("NetworkID"+str(currentID), network_attr)
            
            patchcityout.setPoints("PatchDataID"+str(currentID), plist)
            patchcityout.setFaces("PatchDataID"+str(currentID),flist)
            patchcityout.setAttributes("PatchDataID"+str(currentID), currentPatchList)
            
            #FOR LOOP END (Repeat for next BlockID)
            
        #Output vector update
        blockcityout.setAttributes("MapAttributes", map_attr)
    
    
    ########################################################
    #LINK WITH GUI                                         #
    ########################################################        
                        
    def createInputDialog(self):
        form = activatetechimplementGUI(self, QApplication.activeWindow())
        form.show()
        return True             