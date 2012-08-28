# -*- coding: utf-8 -*-
"""
@file
@author  Peter M Bach <peterbach@gmail.com>
@version 0.5
@section LICENSE

This file is part of DynaMind
Copyright (C) 2011  Peter M Bach
Copyright (C) 2012  HydroIT
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
#import pyvibe
from pydynamind import *
import math

class delinbasin(Module):
    """Uses the flowpaths from delinblocks output to find the upstream basin of
        blocks that drain into each of the blocks. Sets up an upstream matrix
        and write the information in string format. This can be splitted in the
        following modules into vectors of blocks that can then be scanned for
        relevant information.
	
    
    Log of Updates made at each version:
    
    v0.75 (March 2012):
        - Created file
        
	@ingroup UrbanBEATS & DAnCE4Water
	@author Peter M Bach
	"""

    def __init__(self):
        Module.__init__(self)  

	self.mapattributes = View("Mapattributes", COMPONENT, WRITE)
	self.mapattributes.getAttribute("NumBlocks")
	self.mapattributes.getAttribute("BlockSize")
	self.mapattributes.getAttribute("WidthBlocks")
	self.mapattributes.getAttribute("HeightBlocks")
	self.mapattributes.getAttribute("InputReso")
	self.mapattributes.addAttribute("TotalBasins")

	self.blocks = View("Block", FACE, WRITE)
	self.blocks.addAttribute("BasinBlocks")
	self.blocks.addAttribute("BasinDownBlocks")
	self.blocks.addAttribute("BasinArea")
	self.blocks.addAttribute("BasinCount")
	self.blocks.addAttribute("BasinMaxDisp")
	self.blocks.addAttribute("BasinID")
	self.blocks.addAttribute("BasinUUID")
  
	self.basin = View("Basin", COMPONENT, WRITE)
	self.basin.addAttribute("BasinID")
	self.basin.addAttribute("Blocks")
	self.basin.addAttribute("DownBlockID")
	self.basin.addAttribute("UpStr")
	    

	datastream = []
	datastream.append(self.mapattributes)
	datastream.append(self.blocks)
	datastream.append(self.basin)
        self.addData("City", datastream)
	self.BLOCKIDtoUUID = {}

    def getBlockUUID(self, blockid,city):
	try:
		key = self.BLOCKIDtoUUID[blockid]
	except KeyError:
		key = ""
	return city.getFace(key)

        '''blockuuids = city.getUUIDsOfComponentsInView(self.block)
        for blockuuid in blockuuids:
            block = city.getFace(blockuuid)
            ID = int(round(block.getAttribute("BlockID").getDouble()))
            if ID == blockid:
                return blockuuid
        return ""'''

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
	uuid = strvec[0]
        map_attr = city.getComponent(uuid)		#blockcityin.getAttributes("MapAttributes")   #Get map attributes
	
        blocks_num = map_attr.getAttribute("NumBlocks").getDouble()
        block_size = map_attr.getAttribute("BlockSize").getDouble()
 	map_w = map_attr.getAttribute("WidthBlocks").getDouble()
        map_h = map_attr.getAttribute("HeightBlocks").getDouble()       #num of blocks tall
        input_res = map_attr.getAttribute("InputReso").getDouble()      #resolution of input data
 	
        upstreamIDs = []
	track_vectorID = []
        for i in range(int(blocks_num)):
	    currentID = i+1
            
	    currentAttList = self.getBlockUUID(currentID,city)

            #currentAttList = blockcityin.getAttributes("BlockID"+str(currentID))
            track_vectorID.append(0)
            #check activity
            upstreamIDs.append([])
            if int(round(currentAttList.getAttribute("Status").getDouble())) == 0:
                track_vectorID[i] = 1
                continue
            for j in range(int(blocks_num)):

		block = self.getBlockUUID(j+1,city)

                if int(round(currentAttList.getAttribute("Status").getDouble())) == 0:
                    continue
                if int(round(block.getAttribute("downstrID").getDouble())) == currentID:
                    upstreamIDs[i].append(j+1)
                if int(round(block.getAttribute("downstrID").getDouble())) == -1:
                    if int(round(block.getAttribute("drainto_ID").getDouble())) == currentID:
                        upstreamIDs[i].append(j+1)


        for i in range(int(blocks_num)):              #now loop over each block

	    block = self.getBlockUUID(i+1,city)
            if int(round(block.getAttribute("Status").getDouble())) == 0:
                continue
            if len(upstreamIDs[i]) == 0:        #if the matrix for that block ID is zero, skip
                continue
            for j in upstreamIDs[i]:            #otherwise loop over the elements of this expanding vector
                currentSID = j                  #j takes value of the next immediate upstream block
                
                for k in range(int(blocks_num)):      #repeat the scanning process now across all blocks for ID j
		    block = self.getBlockUUID(k+1,city)
                    if int(round(block.getAttribute("Status").getDouble())) == 0:
                        continue
                    if int(round(block.getAttribute("BlockID").getDouble())) == currentSID:
                        continue
                    if int(round(block.getAttribute("downstrID").getDouble())) == currentSID:
                        if k+1 in upstreamIDs[i]:
                            continue
                        else:
                            upstreamIDs[i].append(k+1)
                    if int(round(block.getAttribute("downstrID").getDouble())) == -1:
                        if int(round(block.getAttribute("drainto_ID").getDouble())) == currentSID:
                            if k+1 in upstreamIDs[i]:
                                continue
                            else:
                                upstreamIDs[i].append(k+1)
                print upstreamIDs[i]
                      
        #upstream IDs is a 2D matrix with following: [ Block ID ][ Comma-separated list of upstream blocks ]    
        basin_count = 0
        basins = []     #vector to hold all the groups of basins found
        while sum(track_vectorID) != len(track_vectorID):
            basin_count += 1
            currentbasinID = basin_count
            currentLength = 0    
            for i in range(int(blocks_num)):
                #find the longest flow path
                if track_vectorID[i] == 1:       #if the current blockID has been checked, skip
                    continue
                if len(upstreamIDs[i]) > currentLength:
                    currentLength = len(upstreamIDs[i])
                    currentIndex = i
            print "Current Length: "+str(currentLength)
            print "Current ID: "+str(currentIndex+1)
            basinBlocks = upstreamIDs[currentIndex]
            basinBlocks.append(currentIndex+1)
            print basinBlocks
            basins.append(basinBlocks)
            
            #mark all blockIDs in track_vectorID
            for j in basinBlocks:
                track_vectorID[j-1] = 1
            
            print track_vectorID
                
        print "total basins = "+str(basin_count)
        

        downstreamIDs = []
        #Write code to transfer information into vector
        for i in range(int(blocks_num)):
            currentID = i+1
		#self.getBlockUUID(j+1,city)
            currentAttList = self.getBlockUUID(currentID,city) #blockcityin.getAttributes("BlockID"+str(currentID))
            #network_attr = blockcityin.getAttributes("NetworkID"+str(currentID))
            
            print "Block: "+str(currentID)
            downstreamIDs.append([])
            #Check if status is zero, if yes, then transfer info and continue
            if currentAttList.getAttribute("Status") == 0:
                continue
            
            #Get current upstream blocks vector
            upstreamBlocks = upstreamIDs[i]
            if len(upstreamBlocks) == 0:        #if there are no upstream blocks, write info and skip
                continue

            upstream_string = ""
            for j in upstreamBlocks:
                upstream_string += str(j)+","

	    upstream_attr = Attribute("BasinBlocks")
	    upstream_attr.setString(str(upstream_string))
            currentAttList.addAttribute(upstream_attr)

            #Get current Basin Vector and determine downstream blocks
            currentBasin = 0                    #FIND THE BASIN THIS BLOCK IS SITUATED IN
            for j in range(int(basin_count)):
                currentBasin = basins[j]
                if not currentID in currentBasin:
                    continue
            
            downstreamBlocks = []
            for j in currentBasin:
                if j == currentID:
                    continue
                if not j in upstreamBlocks:
                    downstreamBlocks.append(j)
            downstreamIDs[i] = downstreamBlocks
            downstream_string = ""
            for j in downstreamBlocks:
                downstream_string += str(j)+","
	    downstream_attr = Attribute("BasinDownBlocks")
	    downstream_attr.setString(str(downstream_string))
            currentAttList.addAttribute(downstream_attr)
            print "Downstream: "+downstream_string
            
            #Calculate total upstream basin area
            upstream_tot = len(upstreamBlocks)
            upstream_basin_area = block_size*block_size*upstream_tot/10000      #total upstream basin area [ha]
            currentAttList.addAttribute("BasinArea", upstream_basin_area)
            currentAttList.addAttribute("BasinBCount", upstream_tot)
            print "UpstreamArea"
            print upstream_tot
            print upstream_basin_area
            
            #Calculate longest distance between blocks in a basin
            current_x = currentAttList.getAttribute("Centre_x").getDouble()
            current_y = currentAttList.getAttribute("Centre_y").getDouble()
            disp_matrix = []    #displacement matrix, holds the distance between blocks
            for j in upstreamBlocks:
		block = self.getBlockUUID(j,city)
                compare_x = block.getAttribute("Centre_x").getDouble()
                compare_y = block.getAttribute("Centre_y").getDouble()
                disp = math.sqrt(pow((current_x - compare_x),2)+pow((current_y - compare_y),2))
                disp_matrix.append(disp)
            max_disp = max(disp_matrix)
            print "max displacement "+str(max_disp)
            currentAttList.addAttribute("BasinMaxDisp", max_disp)
            
        for i in range(int(basin_count)):
	    block = self.getBlockUUID(i+1,city)
            currentID = i+1
	    block.addAttribute("BasinID",currentID)
            basinAttList = Component()
	    city.addComponent(basinAttList, self.basin)
            basinAttList.addAttribute("BasinID", currentID)
            basinAttList.addAttribute("Blocks", len(basins[i]))
	    block.addAttribute("BasinUUID", basinAttList.getUUID())
            
            catchment = 0
            currentBlock = 0
            for j in basins[i]:
		block = self.getBlockUUID(j,city)
                if block.getAttribute("BasinArea").getDouble() > catchment:
                    currentBlock = j
                    catchment = block.getAttribute("BasinArea").getDouble()
            downstream_mostBlock = currentBlock
            
            basinAttList.addAttribute("DownBlockID", downstream_mostBlock)
            
            upstream_string = ""
            for j in basins[i]:
                upstream_string += str(j)+","
	    upstr_attr = Attribute("UpStr")
	    upstr_attr.setString(str(upstream_string))
            basinAttList.addAttribute(upstr_attr)
            
            print "Basin No. "+str(currentID)
            print "Blocks Total Number: "+str(len(basins[i]))
            print "Downstream Most Block: "+str(downstream_mostBlock)
            print "Upstream String of Blocks: "+upstream_string
        
        
        map_attr.addAttribute("TotalBasins", basin_count)
    #NEED TO WRITE SOMETHING THAT CAN SPECIFY THE MAXIMUM BASIN SIZE OF THE SEARCH ALGORITHM!
