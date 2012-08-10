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

import ubeats_music_interface as umusic
from pyvibe import *
import sys, random, numpy, math

class WriteResults2MUSIC(Module):
    """Creates a fully functional MUSIC model file *.msf for the input map of blocks and systems
        
    Inputs: 
    
    Log of Updates made at each version:
    
    v0.80 (August 2012):
        - First created
        - Future work: To make sure the projection is adjusted if the file was not created by UrbanBEATS
        
    
	@ingroup UrbanBEATS
	@author Peter M Bach
	"""

    def __init__(self):
        Module.__init__(self)
        self.blockcityin = VectorDataIn
        self.patchcityin = VectorDataIn
        self.techconfigin = VectorDataIn
        self.designparameters = VectorDataIn
        self.addParameter(self, "blockcityin", VIBe2.VECTORDATA_IN)
        self.addParameter(self, "patchcityin", VIBe2.VECTORDATA_IN)
        self.addParameter(self, "techconfigin", VIBe2.VECTORDATA_IN)
        self.addParameter(self, "designparameters", VIBe2.VECTORDATA_IN)
        
    
    def run(self):
        blockcityin = self.blockcityin.getItem()
        patchcityin = self.patchcityin.getItem()
        techconfigin = self.techconfigin.getItem()
        designparameters = self.designparameters.getItem()
        
        map_attr = blockcityin.getAttributes("MapAttributes")
        #get data needed to being for loop analysis
        blocks_num = map_attr.getAttribute("NumBlocks")     #number of blocks to loop through
        blocks_size = map_attr.getAttribute("BlockSize")    #size of block
        map_w = map_attr.getAttribute("WidthBlocks")        #num of blocks wide
        map_h = map_attr.getAttribute("HeightBlocks")       #num of blocks tall
        input_res = map_attr.getAttribute("InputReso")      #resolution of input data
        totalbasins = map_attr.getAttribute("TotalBasins")       #total number of basins in map
        
        receivingblocks = []
        for i in range(int(totalbasins)):
            receivingblocks.append(blockcityin.getAttributes("BasinID"+str(i+1)).getAttribute("DownBlockID"))
        
        print "Receiving Blocks: "
        print receivingblocks
            
        system_list = []
        for i in range(int(blocks_num)):
            lot_count = techconfigin.getAttributes("BlockID"+str(i+1)+"L").getAttribute("TotSystems")
            street_count = techconfigin.getAttributes("BlockID"+str(i+1)+"S").getAttribute("TotSystems")
            neigh_count = techconfigin.getAttributes("BlockID"+str(i+1)+"N").getAttribute("TotSystems")
            prec_count = techconfigin.getAttributes("BlockID"+str(i+1)+"P").getAttribute("TotSystems")
            total_systems = lot_count + street_count + neigh_count + prec_count
            system_list.append([lot_count, street_count, neigh_count, prec_count])
        print system_list
        
        ufile = umusic.createMUSICmsf("C://","urbanbeatsMUSIC")
        umusic.writeMUSICheader(ufile, "melbourne")      #write the header line
        scalar = 10
        ncount = 1
        musicnodedb = [[],[]]       #contains the database of nodes [[ID], [details]]
            
        for i in range(int(blocks_num)):
            currentID = i+1
            currentAttList = blockcityin.getAttributes("BlockID"+str(currentID))        #attribute list of current block structure
            
            if currentAttList.getAttribute("Status") == 0:
                #skips the for loop iteration to the next block, not more needs to be done
                continue
            
            musicnodedb[0].append(currentID)        #add the nodeID list for current block to a central matrix
            
            blockX = currentAttList.getAttribute("Centre_x")
            blockY = currentAttList.getAttribute("Centre_y")
            #lot scale node = x - size/2, y + size/2
            #lot scale untreated = x - size/2, y
            #street scale = x - size/2, y - size/2
            #lot system = x, y + size/2
            #street system = x, y
            #neigh system = x, y-size/2
            #prec system = x + size/2, y    
            
            #write catchment nodes - maximum possibility of two nodes
            catchment_paramter_list = [1,120,30,80,200,1,10,25,5,0]
            total_catch_imparea = currentAttList.getAttribute("ResTIArea")/10000
            total_lot_impA = (currentAttList.getAttribute("ResAllots")*currentAttList.getAttribute("ResLotImpA"))/10000
            street_imp_area = total_catch_imparea - total_lot_impA
            
            ncount_list = []
                
            if system_list[i][0] == 0:
                #No strategies - GET AREAS AND PARAMETERS FOR A SINGLE CATCHMENT NODE
                ncount_list.append(0)
                umusic.writeMUSICcatchmentnode(ufile, currentID, "", ncount, (blockX-blocks_size/4)*scalar, (blockY)*scalar, total_catch_imparea,1, catchment_paramter_list)
                ncount_list.append(ncount)
                ncount += 1
                
            elif system_list[i][0] != 0:
                #There are lot systems so get the lot sub-catchment node and merge the other untreated lots into the other node
                #get lot areas
                ncount_list.append(ncount)
                umusic.writeMUSICcatchmentnode(ufile, currentID, "LT", ncount, (blockX-blocks_size/4)*scalar, (blockY+blocks_size/4)*scalar, total_lot_impA ,1, catchment_paramter_list)
                ncount += 1
                #get other areas
                ncount_list.append(ncount)
                umusic.writeMUSICcatchmentnode(ufile, currentID, "R", ncount, (blockX-blocks_size/4)*scalar, (blockY)*scalar, street_imp_area,1, catchment_paramter_list)
                ncount += 1
                
            #write treatment nodes
            
            #Find lot-scale system, write the node
            if system_list[i][0] != 0:
                lottype = techconfigin.getAttributes("BlockID"+str(i+1)+"L").getStringAttribute("Sys1Type") #inblock_sys[0].getType()
                print lottype
                parameter_list = [1,1]
                ncount_list.append(ncount)
                if lottype == "BF":
                    #setup parameter list: 
                    parameter_list = [0.2, 10, 10, 14, 100, 0.5, 0]             #EDD, Asystem, FilterArea, UnlinedPerimeter, ksat, depth, exfil rate]
                    umusic.writeMUSICnodeBF(ufile, currentID, "L", ncount, blockX*scalar, (blockY+blocks_size/4)*scalar, parameter_list)
                elif lottype == "IS":
                    #setup parameter list
                    parameter_list = [10, 0.2, 10, 14, 1, 100]                  #[pond_area, EDD, filter area, unlined filter perimeter, depth, exfil rate]
                    umusic.writeMUSICnodeIS(ufile, currentID, "L", ncount, blockX*scalar, (blockY+blocks_size/4)*scalar, parameter_list)
                #writedetail = eval('umusic.writeMUSICnode'+str(lottype)+'('+str(ufile)+','+str(currentID)+',L,'+str(ncount)+','+str(blockX*scalar)+","+str((blockY+blocks_size/4)*scalar)+','+str(parameter_list)+')')
                ncount += 1
            else:
                ncount_list.append(0)
                
                #Find the street-scale system, write the node
            if system_list[i][1] != 0:
                streettype = techconfigin.getAttributes("BlockID"+str(i+1)+"S").getStringAttribute("Sys1Type")
                parameter_list = [1,1]
                ncount_list.append(ncount)
                if streettype == "BF":
                    #setup parameter list:
                    parameter_list = [0.2, 10, 10, 14, 100, 0.5, 0]             #EDD, Asystem, FilterArea, UnlinedPerimeter, ksat, depth, exfil rate]
                    umusic.writeMUSICnodeBF(ufile, currentID, "S", ncount, blockX*scalar, blockY*scalar, parameter_list)
                    pass
                elif streettype == "IS":
                    #setup parameter list:
                    parameter_list = [10, 0.2, 10, 14, 1, 100]                  #[pond_area, EDD, filter area, unlined filter perimeter, depth, exfil rate]
                    umusic.writeMUSICnodeIS(ufile, currentID, "S", ncount, blockX*scalar, blockY*scalar, parameter_list)
                    pass
                elif streettype == "SW":
                    #setup parameter list
                    parameter_list = [100,3,1,5,0.5,0.25,0]                     #[length, bedslope, Wbase, Wtop, depth, veg.height, exfilrate]
                    umusic.writeMUSICnodeSW(ufile, currentID, "S", ncount, blockX*scalar, blockY*scalar, parameter_list)
                    pass
                #writedetail = eval('umusic.writeMUSICnode'+str(streettype)+'('+str(ufile)+','+str(currentID)+',S,'+str(ncount)+','+str(blockX*scalar)+","+str(blockY*scalar)+','+str(parameter_list)+')')
                ncount += 1
            else:
                ncount_list.append(0)
                
            #Find the neigh-scale system, write the node
            if system_list[i][2] != 0:
                neightype = techconfigin.getAttributes("BlockID"+str(i+1)+"N").getStringAttribute("Sys1Type")
                parameter_list = [1,1]
                ncount_list.append(ncount)
                if neightype == "BF":
                    #setup parameter list:
                    parameter_list = [0.2, 10, 10, 14, 100, 0.5, 0]             #EDD, Asystem, FilterArea, UnlinedPerimeter, ksat, depth, exfil rate]
                    umusic.writeMUSICnodeBF(ufile, currentID, "N", ncount, blockX*scalar, (blockY-blocks_size/4)*scalar, parameter_list)
                    pass
                elif neightype == "IS":
                    #setup parameter list:
                    parameter_list = [10, 0.2, 10, 14, 1, 100]                  #[pond_area, EDD, filter area, unlined filter perimeter, depth, exfil rate]
                    umusic.writeMUSICnodeIS(ufile, currentID, "N", ncount, blockX*scalar, (blockY-blocks_size/4)*scalar, parameter_list)
                    pass
                elif neightype == "WSUR":
                    #setup parameter list:
                    parameter_list = [50, 1, 50, 0, 200]                        #[Asurface, EDD, Perm. Pool Vol, Exfil Rate, Pipe Diameter]
                    umusic.writeMUSICnodeWSUR(ufile, currentID, "N", ncount, blockX*scalar, (blockY-blocks_size/4)*scalar, parameter_list)
                    pass
                elif neightype == "PB":
                    #setup parameter list:
                    parameter_list = [50, 2, 50, 0, 300]                        #[Asurface, EDD, Perm. Pool Vol, Exfil Rate, Pipe Diameter]
                    umusic.writeMUSICnodePB(ufile, currentID, "N", ncount, blockX*scalar, (blockY-blocks_size/4)*scalar, parameter_list)
                    pass
                #writedetail = eval('umusic.writeMUSICnode'+str(neightype)+'('+str(ufile)+','+str(currentID)+',N,'+str(ncount)+','+str(blockX*scalar)+","+str((blockY-blocks_size/4)*scalar)+','+str(parameter_list)+')')
                ncount += 1
            else:
                ncount_list.append(0)
                
            #write the Block's Junction
            ncount_list.append(ncount)
            umusic.writeMUSICjunction(ufile, currentID, ncount, (blockX+blocks_size/4)*scalar, (blockY)*scalar)
            ncount += 1
            
            #write links
            #Link 1: Lot catch to Lot System
            if ncount_list[0] == 0:
                pass
            else:
                umusic.writeMUSIClink(ufile, ncount_list[0], ncount_list[2])
            
            #Link 2: Other Catch to smallest scale treat system
            blocksystemIDs = ncount_list[3:]
            while 0 in blocksystemIDs:
                blocksystemIDs.remove(0)
            umusic.writeMUSIClink(ufile, ncount_list[1],min(blocksystemIDs))
            
            #Link 3: Lot scale system 
            if ncount_list[2] == 0:
                pass
            else:
                umusic.writeMUSIClink(ufile,ncount_list[2], min(blocksystemIDs))
            
            #Link 4: Street system
            if ncount_list[3] == 0:
                pass
            else:
                blocksystemIDs = ncount_list[4:]
                while 0 in blocksystemIDs:
                    blocksystemIDs.remove(0)
                umusic.writeMUSIClink(ufile, ncount_list[3], min(blocksystemIDs))
            
            #Link 5: Neigh system
            if ncount_list[4] == 0:
                pass
            else:
                umusic.writeMUSIClink(ufile, ncount_list[4], ncount_list[5])
            
            #write the Precinct-scale system
            if system_list[i][3] == 0:
                ncount_list.append(0)
            else:
                prectype = techconfigin.getAttributes("BlockID"+str(i+1)+"P").getStringAttribute("Sys1Type")
                parameter_list = [1,1]
                ncount_list.append(ncount)
                if prectype == "BF":
                    #setup parameter list:
                    parameter_list = [0.2, 10, 10, 14, 100, 0.5, 0]             #EDD, Asystem, FilterArea, UnlinedPerimeter, ksat, depth, exfil rate]
                    umusic.writeMUSICnodeBF(ufile, currentID, "P", ncount, (blockX+blocks_size/4)*scalar, (blockY-blocks_size/4)*scalar, parameter_list)
                    pass
                elif prectype == "IS":
                    #setup parameter list:
                    parameter_list = [10, 0.2, 10, 14, 1, 100]                  #[pond_area, EDD, filter area, unlined filter perimeter, depth, exfil rate]
                    umusic.writeMUSICnodeIS(ufile, currentID, "P", ncount, (blockX+blocks_size/4)*scalar, (blockY-blocks_size/4)*scalar, parameter_list)
                    pass
                elif prectype == "WSUR":
                    #setup parameter list
                    parameter_list = [50, 1, 50, 0, 200]                        #[Asurface, EDD, Perm. Pool Vol, Exfil Rate, Pipe Diameter]
                    umusic.writeMUSICnodeWSUR(ufile, currentID, "P", ncount, (blockX+blocks_size/4)*scalar, (blockY-blocks_size/4)*scalar, parameter_list)
                    pass
                elif prectype == "PB":
                    #setup parameter list:
                    parameter_list = [50, 2, 50, 0, 300]                        #[Asurface, EDD, Perm. Pool Vol, Exfil Rate, Pipe Diameter]
                    umusic.writeMUSICnodePB(ufile, currentID, "P", ncount, (blockX+blocks_size/4)*scalar, (blockY-blocks_size/4)*scalar, parameter_list)
                    pass
                #writedetail = eval('umusic.writeMUSICnode'+str(neightype)+'('+str(ufile)+','+str(currentID)+',N,'+str(ncount)+','+str(blockX*scalar)+","+str((blockY-blocks_size/4)*scalar)+','+str(parameter_list)+')')
                ncount += 1
            
            #Link 6: Junction to prec tech
            if system_list[i][3] != 0:
                umusic.writeMUSIClink(ufile, ncount_list[5], ncount_list[6])
                
            #write receiving node for the basin
            #Check if that Block is the downstream-most in the basin
            if currentID in receivingblocks:
                print currentID
                ncount_list.append(ncount)
                umusic.writeMUSICreceiving(ufile, currentID, ncount, (blockX)*scalar, (blockY-blocks_size/2)*scalar)
                ncount += 1
                #Link 7: Junction/Prec-Tech to receiving Node
                if system_list[i][3] != 0:              #if there is a precinct technology...
                    umusic.writeMUSIClink(ufile, ncount_list[6], ncount_list[7])
                else:
                    umusic.writeMUSIClink(ufile, ncount_list[5], ncount_list[7])
                
            musicnodedb[1].append(ncount_list)
                
            print "NCOUNT-LIST"
            print ncount_list
                
            print musicnodedb
            
        #CONNECT ALL BLOCK JUNCTIONS/TOGETHER TO STRING THE CATCHMENT TOGETHER
        for i in range(int(blocks_num)):
            currentID = i+1
            currentAttList = blockcityin.getAttributes("BlockID"+str(currentID))        #attribute list of current block structure
            
            block_status = currentAttList.getAttribute("Status")
            if block_status == 0:
                #skips the for loop iteration to the next block, not more needs to be done
                continue
            
            print currentID
            upindex = musicnodedb[0].index(currentID)
            ncount_list_up = musicnodedb[1][upindex]
            
            downID = currentAttList.getAttribute("downstrID")
            print downID
            if downID == -1:
                downID = currentAttList.getAttribute("drainto_ID")
            else:
                downID == 0
            if downID == 0:
                pass
            else:
                downindex = musicnodedb[0].index(downID)
                ncount_list_down = musicnodedb[1][downindex]
                umusic.writeMUSIClink(ufile, max(ncount_list_up[5:]), ncount_list_down[5])
                
        umusic.writeMUSICfooter(ufile)