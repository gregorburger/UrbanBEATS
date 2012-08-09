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
#import pyvibe
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
	self.blockcityin = View("BlockCityIn",RASTERDATA,READ)
	self.blockcityout = View("BlockCityOut",RASTERDATA,READ)
        #self.blockcityin = VectorDataIn
        #self.blockcityout = VectorDataIn
        self.addParameter(self, "blockcityin", VIBe2.VECTORDATA_IN)
        self.addParameter(self, "blockcityout", VIBe2.VECTORDATA_OUT)
    


	
    
    def run(self):
	
	blockcityin = self.getRasterData("City", self.blockcityin)
	blockcityout = self.getRasterData("City", self.blockcityout)
        #blockcityin = self.blockcityin.getItem()
        #blockcityout = self.blockcityout.getItem()
        
        map_attr = blockcityin.getAttributes("MapAttributes")   #Get map attributes
        blocks_num = map_attr.getAttribute("NumBlocks")
        block_size = map_attr.getAttribute("BlockSize")
        map_w = map_attr.getAttribute("WidthBlocks")
        map_h = map_attr.getAttribute("HeightBlocks")       #num of blocks tall
        input_res = map_attr.getAttribute("InputReso")      #resolution of input data
        
        upstreamIDs = []
        track_vectorID = []
        blocks_uuids = city.getUUIDs("BLOCK")
        for b_uuid in blocks_uuids:
        #for i in range(int(blocks_num)):
            block = city.getFace(b_uuid)
            '''currentID = i+1
            currentAttList = blockcityin.getAttributes("BlockID"+str(currentID))'''
            track_vectorID.append(0)
            #check activity
            upstreamIDs.append([])
            
            #if currentAttList.getAttribute("Status") == 0:
            if block.getAttribute("Status") == 0:
                track_vectorID[i] = 1
                continue
            for b_uuid_2 in blocks_uuids:
            #for j in range(int(blocks_num)):
                block2 = city.getFace(b_uuid2)
                if block2.getAttribute("Status") == 0:
                    continue
                    
                if block2.getAttribute("Status") == 0:
                    continue
                if block2.getAttribute.getAttribute("downstrID") == currentID:
                    upstreamIDs[block.getUUID].append(block2.getUUID())
                if block2.getAttribute.getAttribute("downstrID") == -1:
                    if block2.getAttribute.getAttribute("drainto_ID") == currentID:
                        upstreamIDs[block.getUUID].append(block2.getUUID())

        for b_uuid in blocks_uuids:
        #for i in range(int(blocks_num)):
            block = city.getFace(b_uuid)       
        #for i in range(int(blocks_num)):              #now loop over each block
            if blockcityin.getAttributes("BlockID"+str(i+1)).getAttribute("Status") == 0:
                continue
            if len(upstreamIDs[i]) == 0:        #if the matrix for that block ID is zero, skip
                continue
            for j in upstreamIDs[i]:            #otherwise loop over the elements of this expanding vector
                currentSID = j                  #j takes value of the next immediate upstream block
                
                for k in range(int(blocks_num)):      #repeat the scanning process now across all blocks for ID j
                    if blockcityin.getAttributes("BlockID"+str(k+1)).getAttribute("Status") == 0:
                        continue
                    if blockcityin.getAttributes("BlockID"+str(k+1)).getAttribute("BlockID") == currentSID:
                        continue
                    if blockcityin.getAttributes("BlockID"+str(k+1)).getAttribute("downstrID") == currentSID:
                        if k+1 in upstreamIDs[i]:
                            continue
                        else:
                            upstreamIDs[i].append(k+1)
                    if blockcityin.getAttributes("BlockID"+str(k+1)).getAttribute("downstrID") == -1:
                        if blockcityin.getAttributes("BlockID"+str(k+1)).getAttribute("drainto_ID") == currentSID:
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
            currentAttList = blockcityin.getAttributes("BlockID"+str(currentID))
            plist = blockcityin.getPoints("BlockID"+str(currentID))
            flist = blockcityin.getFaces("BlockID"+str(currentID))
            pnetlist = blockcityin.getPoints("NetworkID"+str(currentID))
            enetlist = blockcityin.getEdges("NetworkID"+str(currentID))
            network_attr = blockcityin.getAttributes("NetworkID"+str(currentID))
            
            print "Block: "+str(currentID)
            downstreamIDs.append([])
            #Check if status is zero, if yes, then transfer info and continue
            if currentAttList.getAttribute("Status") == 0:
                blockcityout.setPoints("BlockID"+str(currentID),plist)
                blockcityout.setFaces("BlockID"+str(currentID),flist)
                blockcityout.setAttributes("BlockID"+str(currentID), currentAttList)
                blockcityout.setPoints("NetworkID"+str(currentID), pnetlist)
                blockcityout.setEdges("NetworkID"+str(currentID), enetlist)
                blockcityout.setAttributes("NetworkID"+str(currentID), network_attr)
                continue
            
            #Get current upstream blocks vector
            upstreamBlocks = upstreamIDs[i]
            if len(upstreamBlocks) == 0:        #if there are no upstream blocks, write info and skip
                blockcityout.setPoints("BlockID"+str(currentID),plist)
                blockcityout.setFaces("BlockID"+str(currentID),flist)
                blockcityout.setAttributes("BlockID"+str(currentID), currentAttList)
                blockcityout.setPoints("NetworkID"+str(currentID), pnetlist)
                blockcityout.setEdges("NetworkID"+str(currentID), enetlist)
                blockcityout.setAttributes("NetworkID"+str(currentID), network_attr)
                continue
            upstream_string = ""
            for j in upstreamBlocks:
                upstream_string += str(j)+","
            currentAttList.setAttribute("BasinBlocks", str(upstream_string))
            print "Upstream: "+upstream_string
            
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
            currentAttList.setAttribute("BasinDownBlocks", str(downstream_string))
            print "Downstream: "+downstream_string
            
            #Calculate total upstream basin area
            upstream_tot = len(upstreamBlocks)
            upstream_basin_area = block_size*block_size*upstream_tot/10000      #total upstream basin area [ha]
            currentAttList.setAttribute("BasinArea", upstream_basin_area)
            currentAttList.setAttribute("BasinBCount", upstream_tot)
            print "UpstreamArea"
            print upstream_tot
            print upstream_basin_area
            
            #Calculate longest distance between blocks in a basin
            current_x = currentAttList.getAttribute("Centre_x")
            current_y = currentAttList.getAttribute("Centre_y")
            disp_matrix = []    #displacement matrix, holds the distance between blocks
            for j in upstreamBlocks:
                compare_x = blockcityin.getAttributes("BlockID"+str(j)).getAttribute("Centre_x")
                compare_y = blockcityin.getAttributes("BlockID"+str(j)).getAttribute("Centre_y")
                disp = math.sqrt(pow((current_x - compare_x),2)+pow((current_y - compare_y),2))
                disp_matrix.append(disp)
            max_disp = max(disp_matrix)
            print "max displacement "+str(max_disp)
            currentAttList.setAttribute("BasinMaxDisp", max_disp)
            
            #-----------------------------------------------------------------#
            #        Write all updated Attribute Lists to the output          #
            #-----------------------------------------------------------------#
            
            blockcityout.setPoints("BlockID"+str(currentID),plist)
            blockcityout.setFaces("BlockID"+str(currentID),flist)
            blockcityout.setAttributes("BlockID"+str(currentID), currentAttList)
            blockcityout.setPoints("NetworkID"+str(currentID), pnetlist)
            blockcityout.setEdges("NetworkID"+str(currentID), enetlist)
            blockcityout.setAttributes("NetworkID"+str(currentID), network_attr)
            
        for i in range(int(basin_count)):
            currentID = i+1
            basinAttList = Attribute()
            basinAttList.setAttribute("BasinID", currentID)
            basinAttList.setAttribute("Blocks", len(basins[i]))
            
            catchment = 0
            currentBlock = 0
            for j in basins[i]:
                if blockcityout.getAttributes("BlockID"+str(j)).getAttribute("BasinArea") > catchment:
                    currentBlock = j
                    catchment = blockcityout.getAttributes("BlockID"+str(j)).getAttribute("BasinArea")
            downstream_mostBlock = currentBlock
            
            basinAttList.setAttribute("DownBlockID", downstream_mostBlock)
            
            upstream_string = ""
            for j in basins[i]:
                upstream_string += str(j)+","
            basinAttList.setAttribute("UpStr", str(upstream_string))
            
            print "Basin No. "+str(currentID)
            print "Blocks Total Number: "+str(len(basins[i]))
            print "Downstream Most Block: "+str(downstream_mostBlock)
            print "Upstream String of Blocks: "+upstream_string
        
            blockcityout.setAttributes("BasinID"+str(currentID), basinAttList)          #BasinID+number is the basic Attributes Unit
        
        map_attr.setAttribute("TotalBasins", basin_count)    
        blockcityout.setAttributes("MapAttributes", map_attr)
    
    #NEED TO WRITE SOMETHING THAT CAN SPECIFY THE MAXIMUM BASIN SIZE OF THE SEARCH ALGORITHM!
