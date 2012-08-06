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
from osgeo import ogr, osr
import sys

class GetPreviousBlocks(Module):
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
        - Can import both blocks and patches shapefiles and transfer every attribute across to a VIBe2.VectorDataOut port. This port can be connected
        to a subsequent module and the attributes recalled. Currently no geometric information is transferred as it is believed that it will not be
        relevant so long as all subsequent maps in the simulation are aligned with each other.
        
        @ingroup UrbanBEATS
	@author Peter M Bach
	"""

    def __init__(self):
        Module.__init__(self)
        self.ongoing_sim = 0            #Is this module part of an ongoing simulation?
        self.path_name = "C:/UBEATS/"          #specify C-drive as default value
        self.block_path_name = "C:/UBEATS/0_UrbanBEATS-SCreek-500m_faces.shp"
        self.patch_path_name = "C:/UBEATS/0_UrbanBEATS-SCreek-500mp_faces.shp"    
        self.previousblocksout = VectorDataIn
        self.previouspatchout = VectorDataIn
        self.addParameter(self, "ongoing_sim", VIBe2.BOOL)
        self.addParameter(self, "path_name", VIBe2.STRING)
        self.addParameter(self, "block_path_name", VIBe2.STRING)
        self.addParameter(self, "patch_path_name", VIBe2.STRING)
        self.addParameter(self, "previousblocksout", VIBe2.VECTORDATA_OUT)
        self.addParameter(self, "previouspatchout", VIBe2.VECTORDATA_OUT)
        
    def run(self):
        #Prepare VectorData Output Formats
        previousblocksout = self.previousblocksout.getItem()
        previouspatchout = self.previouspatchout.getItem()
        map_attr = Attribute()
        
        #Get the correct driver (we are working with ESRI Shapefiles)
        driver = ogr.GetDriverByName('ESRI Shapefile')
        
        #Use the following file for testing: C:/UBEATS/0_UrbanBEATS-SC-500m_faces.shp
        blocksave_file = "ubeats_out.shp"
        patchsave_file = "ubeats_outp.shp"
        
        if self.ongoing_sim == True:
            blockfile_name = self.path_name + blocksave_file
            patchfile_name = self.path_name + patchsave_file
        else:
            blockfile_name = self.block_path_name
            patchfile_name = self.patch_path_name
        
        #open data source, check if it exists otherwise quit.
        blockdataSource = driver.Open(blockfile_name, 0)
        patchdataSource = driver.Open(patchfile_name, 0)
        if blockdataSource is None:
            print "Error, could not open Blocks "+blockfile_name
            sys.exit(1)
        if patchdataSource is None:
            print "Error, could not open Patches "+patchfile_name
            sys.exit(1)
        
        blocklayer = blockdataSource.GetLayer()
        patchlayer = patchdataSource.GetLayer()
        total_blocks = blocklayer.GetFeatureCount()
        blockspatialRef = blocklayer.GetSpatialRef()
        patchspatialRef = patchlayer.GetSpatialRef()
        print "Spatial Reference (Proj4): " + str(blockspatialRef.ExportToProj4())
        print "Total Blocks in map: " + str(total_blocks)
        
        #Perform some comparison to make sure that the projection of the loaded file is identical to that of the final desired format
        #Code...
        #...
        
        #Get extents of the layer
        extents = blocklayer.GetExtent()     #returns as xmin, xmax, ymin, ymax
        xmin = extents[0]
        ymin = extents[2]
        print str(xmin) + ", " + str(ymin)
        
        #Get some dimensions of the map
        map_width = extents[1] - xmin
        map_height = extents[3] - ymin
        
        #Get block size and number of blocks wide and tall from first block in the shape file
        firstBlock = blocklayer.GetFeature(0)
        centrex = firstBlock.GetField("Centre_x")
        block_size = 2*centrex
        blocks_wide = map_width/block_size
        blocks_tall = map_height/block_size
        
        print firstBlock.GetFieldCount()
        #print firstBlock.GetFieldIndex("")
        
        #Set some global attributes
        map_attr.setAttribute("Xmin", xmin)
        map_attr.setAttribute("Ymin", ymin)
        map_attr.setAttribute("Width", map_width)
        map_attr.setAttribute("Height", map_height)
        map_attr.setAttribute("BlockSize", block_size)
        map_attr.setAttribute("BlocksWidth", blocks_wide)
        map_attr.setAttribute("BlocksHeight", blocks_tall)
        map_attr.setAttribute("TotalBlocks", total_blocks)
        
        #Loop through each Block and obtain all attributes
        for i in range(int(total_blocks)):
            currentID = i+1
            currentBlock = blocklayer.GetFeature(i)          #obtains feature with FID = i
            currentPatches = patchlayer.GetFeature(i)        #obtains patches from patch file
            
            #Transfer all Block Attributes to Block Output
            block_attr = Attribute()                    #declares Attribute() vector for VIBe
            total_attrs = currentBlock.GetFieldCount()  #gets total number of attributes
            for j in range(int(total_attrs)):           
                name = str(currentBlock.GetFieldDefnRef(j).GetName())        #Obtain attribute name from FieldDefn object
                value = currentBlock.GetField(j)                        #get the value from the field using the same index
                if value == None:
                    pass
                else:
                    block_attr.setAttribute(str(name), value)                    #assign to block_attr vector
            previousblocksout.setAttributes("BlockID"+str(currentID), block_attr)       #save these attributes to the output vector
            currentBlock.Destroy()      #destroy to save memory
            
            #Transfer all Patch Attributes to Patch Output
            patch_attr = Attribute()
            total_patchattr = currentPatches.GetFieldCount()
            for j in range(int(total_patchattr)):
                name = str(currentPatches.GetFieldDefnRef(j).GetName())
                value = currentPatches.GetField(j)
                if value == None:
                    pass
                else:
                    patch_attr.setAttribute(str(name), value)
            previouspatchout.setAttributes("BlockID"+str(currentID), patch_attr)
            currentPatches.Destroy()    #destroy to save memory
        
        #Destroy the shapefile
        blockdataSource.Destroy()
        patchdataSource.Destroy()
        
        #Write Global Attributes to Vector Data output before finishing module
        previousblocksout.setAttributes("MapAttributes", map_attr)
        previouspatchout.setAttributes("MapAttributes", map_attr)        
        #END OF MODULE