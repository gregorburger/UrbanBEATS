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

class urbplansummary(Module):
    """Description of class
	
    Description of Inputs & Outputs 
	- <description of inputs/outputs>
    
    Log of Updates made at each version:
    
    v0.80 (March 2012):
        - Created urbplansummary for more modularity
        - Collates the information from the four ubp modules and writes it to the existing block map
        - Passes the patches map onto the next section of UrbanBEATS - techplacement
        
	@ingroup DAnCE4Water
	@author Peter M Bach
	"""
    def __init__(self):
        Module.__init__(self)
        #Summary Module received four copies of BlockCity and merges these to one final version.
        self.residential = VectorDataIn
        self.nonres = VectorDataIn
        self.facilities = VectorDataIn
        self.space = VectorDataIn
        self.blockcityin = VectorDataIn
        self.blockcityout = VectorDataIn
        self.patchcityin = VectorDataIn
        self.patchcityout = VectorDataIn
        self.addParameter(self, "residential", VIBe2.VECTORDATA_IN)
        self.addParameter(self, "nonres", VIBe2.VECTORDATA_IN)
        self.addParameter(self, "facilities", VIBe2.VECTORDATA_IN)
        self.addParameter(self, "space", VIBe2.VECTORDATA_IN)
        self.addParameter(self, "blockcityin", VIBe2.VECTORDATA_IN)
        self.addParameter(self, "blockcityout", VIBe2.VECTORDATA_OUT)
        self.addParameter(self, "patchcityin", VIBe2.VECTORDATA_IN)
        self.addParameter(self, "patchcityout", VIBe2.VECTORDATA_OUT)
        
        self.reportin = VectorDataIn
        self.reportout = VectorDataIn
        self.addParameter(self, "reportin", VIBe2.VECTORDATA_IN)
        self.addParameter(self, "reportout", VIBe2.VECTORDATA_OUT)
        
    def run(self):
        residential_vec = self.residential.getItem()
        nonres_vec = self.nonres.getItem()
        facilities_vec = self.facilities.getItem()
        spaces_vec = self.space.getItem()
        blockcityin = self.blockcityin.getItem()
        blockcityout = self.blockcityout.getItem()
        patchcityout = self.patchcityout.getItem()
        patchcityin = self.patchcityin.getItem()
        
        map_attr = blockcityin.getAttributes("MapAttributes")   #GET map attributes
        
        #Get some Parameters
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
        
        #--------------------------------------------------------------------------------#
        #         LOOP OVER EACH BLOCK IN THE GRID AND UPDATE THE ATTRIBUTES LIST        #
        #--------------------------------------------------------------------------------#
        
        for i in range(int(blocks_num)):
            currentID = i + 1
            currentAttList = blockcityin.getAttributes("BlockID"+str(currentID))
            currentPatchList = patchcityin.getAttributes("PatchDataID"+str(currentID))
            #existingAttList = existingblock.getAttributes("BlockID"+str(currentID))    #attribute list of the existing block structure
            plist = blockcityin.getPoints("BlockID"+str(currentID))
            flist = blockcityin.getFaces("BlockID"+str(currentID))
            pnetlist = blockcityin.getPoints("NetworkID"+str(currentID))
            enetlist = blockcityin.getEdges("NetworkID"+str(currentID))
            network_attr = blockcityin.getAttributes("NetworkID"+str(currentID))
            
            #--------------------------------------------------------------------------------#
            #            CONDITIONAL CHECK TO SEE IF CURRENT BLOCK IS RELEVANT               #
            #--------------------------------------------------------------------------------#
            
            block_status = currentAttList.getAttribute("Status")
            if block_status == 0:
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
            
            #--------------------------------------------------------------------------------#
            #            WRITE RESIDENTIAL ATTRIBUTES INTO THE MAP                           #
            #--------------------------------------------------------------------------------#
            #   - Note about updating the list: if new attributes are added or old inputs    #
            #     are removed, these will have to be made here, in the ubp_<x>.py and in 2   #
            #     locations in urbplanbb: (a) parameter list in __init__ and (b) vector list #
            #   - Keep the names consistent!                                                 #
            #                                                                                #
            #--------------------------------------------------------------------------------#
            
            res_list = residential_vec.getAttributes("BlockID"+str(currentID))
            if res_list.getAttribute("HasResidential") == 0:
                pass
            else:
                currentAttList.setAttribute("ResAllots", res_list.getAttribute("ResAllots"))
                currentAttList.setAttribute("ResType", res_list.getAttribute("ResType"))
                currentAttList.setAttribute("ResLotOccup", res_list.getAttribute("ResLotOccup"))
                currentAttList.setAttribute("AvgAllot_A", res_list.getAttribute("AvgAllot_A"))
                currentAttList.setAttribute("AvgAllot_W", res_list.getAttribute("AvgAllot_W"))
                currentAttList.setAttribute("AvgAllot_D", res_list.getAttribute("AvgAllot_D"))
                currentAttList.setAttribute("ResLotPubDW_A", res_list.getAttribute("ResLotPubDW_A"))
                currentAttList.setAttribute("ResLotPrivDW_A", res_list.getAttribute("ResLotPrivDW_A"))
                currentAttList.setAttribute("Collect_WLane", res_list.getAttribute("Collect_WLane"))
                currentAttList.setAttribute("Foot_W", res_list.getAttribute("Foot_W"))
                currentAttList.setAttribute("NStrip_W", res_list.getAttribute("NStrip_W"))
                currentAttList.setAttribute("ResLotRoofA", res_list.getAttribute("ResLotRoofA"))
                currentAttList.setAttribute("ResLotImpA", res_list.getAttribute("ResLotImpA"))
                currentAttList.setAttribute("ResLotConImpA", res_list.getAttribute("ResLotConImpA"))
                currentAttList.setAttribute("ResLotDscImpA", res_list.getAttribute("ResLotDscImpA"))
                currentAttList.setAttribute("ResLotRoofConnect", res_list.getAttribute("ResLotRoofConnect"))
                currentAttList.setAttribute("ResTIArea", res_list.getAttribute("ResTIArea"))
                currentAttList.setAttribute("ResEIArea", res_list.getAttribute("ResEIArea"))
                currentAttList.setAttribute("ResTIF", res_list.getAttribute("ResTIF"))
                currentAttList.setAttribute("ResEIF", res_list.getAttribute("ResEIF"))
                currentAttList.setAttribute("ResPVArea", res_list.getAttribute("ResPVArea"))
                currentAttList.setAttribute("ResDCIArea", res_list.getAttribute("ResDCIArea"))
                currentAttList.setAttribute("AvlResLot", res_list.getAttribute("AvlResLot"))                   #available space on lot
                currentAttList.setAttribute("TotStreetA", res_list.getAttribute("TotStreetA"))     #total street Area
                currentAttList.setAttribute("AvlStreet", res_list.getAttribute("AvlStreet"))    #available street space
                
            #--------------------------------------------------------------------------------#
            #            WRITE NON-RESIDENTIAL ATTRIBUTES INTO THE MAP                       #
            #--------------------------------------------------------------------------------#
            
            #Temporary version of planning algorithm, future version to come
            nonres_list = nonres_vec.getAttributes("BlockID"+str(currentID))
            if nonres_list.getAttribute("HasNonRes") == 0:
                pass
            else:
                currentAttList.setAttribute("HasIndustry", nonres_list.getAttribute("HasIndustry"))
                currentAttList.setAttribute("HasCommercial", nonres_list.getAttribute("HasCommercial"))
                currentAttList.setAttribute("AIndustry", nonres_list.getAttribute("AIndustry"))
                currentAttList.setAttribute("ACommercial", nonres_list.getAttribute("ACommercial"))
                currentAttList.setAttribute("AImp_Ind", nonres_list.getAttribute("AImp_Ind"))
                currentAttList.setAttribute("AImp_Com", nonres_list.getAttribute("AImp_Com"))
            
            #--------------------------------------------------------------------------------#
            #            WRITE FACILITIES ATTRIBUTES INTO THE MAP                            #
            #--------------------------------------------------------------------------------#
            
            #Temporary version of planning algorithm, future version to come
            facilities_list = facilities_vec.getAttributes("BlockID"+str(currentID))
            if facilities_list.getAttribute("HasFacilities") == 0:
                pass
            else:
                currentAttList.setAttribute("MunATot", facilities_list.getAttribute("MunATot"))
                currentAttList.setAttribute("MunAimp", facilities_list.getAttribute("MunAimp"))
                currentAttList.setAttribute("MunAeimp", facilities_list.getAttribute("MunAeimp"))
                currentAttList.setAttribute("MunAperv", facilities_list.getAttribute("MunAperv"))
                currentAttList.setAttribute("MunAroof", facilities_list.getAttribute("MunAroof"))
                currentAttList.setAttribute("MunTIF", facilities_list.getAttribute("MunTIF"))
                currentAttList.setAttribute("MunEIF", facilities_list.getAttribute("MunEIF"))
                
                currentAttList.setAttribute("TrATot", facilities_list.getAttribute("TrATot"))
                currentAttList.setAttribute("TrAimp", facilities_list.getAttribute("TrAimp"))
                currentAttList.setAttribute("TrAeimp", facilities_list.getAttribute("TrAeimp"))
                currentAttList.setAttribute("TrAperv", facilities_list.getAttribute("TrAperv"))
                currentAttList.setAttribute("TrAroof", facilities_list.getAttribute("TrAroof"))
                currentAttList.setAttribute("TrTIF", facilities_list.getAttribute("TrTIF"))
                currentAttList.setAttribute("TrEIF", facilities_list.getAttribute("TrEIF"))
            
            
            #--------------------------------------------------------------------------------#
            #            WRITE SPACES ATTRIBUTES INTO THE MAP                                #
            #--------------------------------------------------------------------------------#
            
            spaces_list = spaces_vec.getAttributes("BlockID"+str(currentID))
            if spaces_list.getAttribute("HasSpaces") == 0:
                pass
            else:
                currentAttList.setAttribute("rfw_Adev", spaces_list.getAttribute("rfw_Adev"))
            
            #--------------------------------------------------------------------------------#
            #            CALCULATE ADDITIONAL ATTRIBUTES AND WRITE TO MAP                    #
            #--------------------------------------------------------------------------------#
            
            #Nothing at this stage
            
            
            #--------------------------------------------------------------------------------#
            #            SAVE UPDATED ATTRIBUTES LIST & TRANSFER DATA TO OUTPORT             #
            #--------------------------------------------------------------------------------#
            
            blockcityout.setPoints("BlockID"+str(currentID),plist)
            blockcityout.setFaces("BlockID"+str(currentID),flist)
            blockcityout.setAttributes("BlockID"+str(currentID),currentAttList)
            blockcityout.setPoints("NetworkID"+str(currentID), pnetlist)
            blockcityout.setEdges("NetworkID"+str(currentID), enetlist)
            blockcityout.setAttributes("NetworkID"+str(currentID), network_attr)
            
            patchcityout.setPoints("PatchDataID"+str(currentID), plist)
            patchcityout.setFaces("PatchDataID"+str(currentID),flist)
            patchcityout.setAttributes("PatchDataID"+str(currentID), currentPatchList)
        
            #END OF FOR LOOP (loop through for next Block ID)
        
        blockcityout.setAttributes("MapAttributes", map_attr)
        #END OF MODULE
    