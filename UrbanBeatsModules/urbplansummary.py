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
	self.blocks = View("Block",FACE,WRITE)
	self.blocks.getAttribute("BlockID")
	self.blocks.addAttribute("ResAllots")
        self.blocks.addAttribute("ResType")
        self.blocks.addAttribute("ResLotOccup")
        self.blocks.addAttribute("AvgAllot_A")
        self.blocks.addAttribute("AvgAllot_W")
        self.blocks.addAttribute("AvgAllot_D")
        self.blocks.addAttribute("ResLotPubDW_A")
        self.blocks.addAttribute("ResLotPrivDW_A",)
        self.blocks.addAttribute("Collect_WLane")
        self.blocks.addAttribute("Foot_W")
        self.blocks.addAttribute("NStrip_W")
        self.blocks.addAttribute("ResLotRoofA")
        self.blocks.addAttribute("ResLotImpA")
        self.blocks.addAttribute("ResLotConImpA")
        self.blocks.addAttribute("ResLotDscImpA")
        self.blocks.addAttribute("ResLotRoofConnect")
        self.blocks.addAttribute("ResTIArea")
        self.blocks.addAttribute("ResEIArea")
        self.blocks.addAttribute("ResTIF")
        self.blocks.addAttribute("ResEIF")
        self.blocks.addAttribute("ResPVArea")
        self.blocks.addAttribute("ResDCIArea")
        self.blocks.addAttribute("AvlResLot")
        self.blocks.addAttribute("TotStreetA")
        self.blocks.addAttribute("AvlStreet")
	self.blocks.addAttribute("HasIndustry")
	self.blocks.addAttribute("HasCommerical")
	self.blocks.addAttribute("AIndustry")
	self.blocks.addAttribute("ACommercial")
	self.blocks.addAttribute("AImp_Ind")
	self.blocks.addAttribute("AImp_Com")
	self.blocks.addAttribute("MunATot")
	self.blocks.addAttribute("MunAimp")
	self.blocks.addAttribute("MunAeimp")
	self.blocks.addAttribute("MunAperv")
	self.blocks.addAttribute("MunAroof")
	self.blocks.addAttribute("MinTIF")
	self.blocks.addAttribute("MinEIF")
	self.blocks.addAttribute("TrATot")
	self.blocks.addAttribute("TrAimp")
	self.blocks.addAttribute("TrAeimp")
	self.blocks.addAttribute("TrAperv")
	self.blocks.addAttribute("TrAroof")
	self.blocks.addAttribute("TrTIF")
	self.blocks.addAttribute("TrEIF")
	self.blocks.getAttribute("ResidentialID")


	self.mapattributes = View("Mapattributes",COMPONENT,READ)
    	self.mapattributes.getAttribute("NumBlocks")
	self.mapattributes.getAttribute("BlockSize")
	self.mapattributes.getAttribute("WidthBlocks")
	self.mapattributes.getAttribute("HeightBlocks")
	self.mapattributes.getAttribute("InputReso")
	self.mapattributes.getAttribute("TotalBasins")

	self.residential = View("Residential",COMPONENT,READ)
	self.residential.getAttribute("BlockID")
	self.residential.getAttribute("HasResidential")
	self.residential.getAttribute("ResAllots")
        self.residential.getAttribute("ResType")
        self.residential.getAttribute("ResLotOccup")
        self.residential.getAttribute("AvgAllot_A")
        self.residential.getAttribute("AvgAllot_W")
        self.residential.getAttribute("AvgAllot_D")
        self.residential.getAttribute("ResLotPubDW_A")
        self.residential.getAttribute("ResLotPrivDW_A",)
        self.residential.getAttribute("Collect_WLane")
        self.residential.getAttribute("Foot_W")
        self.residential.getAttribute("NStrip_W")
        self.residential.getAttribute("ResLotRoofA")
        self.residential.getAttribute("ResLotImpA")
        self.residential.getAttribute("ResLotConImpA")
        self.residential.getAttribute("ResLotDscImpA")
        self.residential.getAttribute("ResLotRoofConnect")
        self.residential.getAttribute("ResTIArea")
        self.residential.getAttribute("ResEIArea")
        self.residential.getAttribute("ResTIF")
        self.residential.getAttribute("ResEIF")
        self.residential.getAttribute("ResPVArea")
        self.residential.getAttribute("ResDCIArea")
        self.residential.getAttribute("AvlResLot")
        self.residential.getAttribute("TotStreetA")
        self.residential.getAttribute("AvlStreet")

	self.nonResidential = View("NonResidential",COMPONENT,READ)
	self.nonResidential.getAttribute("BlockID")
	self.nonResidential.getAttribute("HasNonRes")
	self.nonResidential.getAttribute("HasIndustry")
	self.nonResidential.getAttribute("HasCommerical")
	self.nonResidential.getAttribute("AIndustry")
	self.nonResidential.getAttribute("ACommercial")
	self.nonResidential.getAttribute("AImp_Ind")
	self.nonResidential.getAttribute("AImp_Com")

	self.facilitiesAttr = View("Facilities",COMPONENT,READ)
	self.facilitiesAttr.getAttribute("BlockID")
	self.facilitiesAttr.getAttribute("HasFacilities")
	self.facilitiesAttr.getAttribute("MunATot")
	self.facilitiesAttr.getAttribute("MunAimp")
	self.facilitiesAttr.getAttribute("MunAeimp")
	self.facilitiesAttr.getAttribute("MunAperv")
	self.facilitiesAttr.getAttribute("MunAroof")
	self.facilitiesAttr.getAttribute("MinTIF")
	self.facilitiesAttr.getAttribute("MinEIF")
	self.facilitiesAttr.getAttribute("TrATot")
	self.facilitiesAttr.getAttribute("TrAimp")
	self.facilitiesAttr.getAttribute("TrAeimp")
	self.facilitiesAttr.getAttribute("TrAperv")
	self.facilitiesAttr.getAttribute("TrAroof")
	self.facilitiesAttr.getAttribute("TrTIF")
	self.facilitiesAttr.getAttribute("TrEIF")

	self.spacesAttr = View("Spaces",COMPONENT,WRITE)
	self.spacesAttr.addAttribute("BlockID")
	self.spacesAttr.addAttribute("HasSpaces")
	self.spacesAttr.addAttribute("rfw_Adev")

 	#Datastream
	datastream = []
	datastream.append(self.blocks)
	datastream.append(self.mapattributes)
	datastream.append(self.residential)
	datastream.append(self.nonResidential)
	datastream.append(self.facilitiesAttr)
	datastream.append(self.spacesAttr)
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

        
        basins = map_attr.getAttribute("TotalBasins").getDouble()

        
        #--------------------------------------------------------------------------------#
        #         LOOP OVER EACH BLOCK IN THE GRID AND UPDATE THE ATTRIBUTES LIST        #
        #--------------------------------------------------------------------------------#
        
        for i in range(int(blocks_num)):
            currentID = i + 1
            currentAttList = self.getBlockUUID(currentID,city)
            
            #--------------------------------------------------------------------------------#
            #            CONDITIONAL CHECK TO SEE IF CURRENT BLOCK IS RELEVANT               #
            #--------------------------------------------------------------------------------#
            
            block_status = currentAttList.getAttribute("Status").getDouble()
            if block_status == 0:
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
            res_uuid = currentAttList.getAttribute("ResidentialID").getString()
	    res_list = city.getComponent( res_uuid)
	    
	    #if str(ress_uuid).empty() 
            if res_list.getAttribute("HasResidential").getDouble() == 0:
                pass
            else:
                currentAttList.addAttribute("ResAllots", res_list.getAttribute("ResAllots").getDouble())
                currentAttList.addAttribute("ResType", res_list.getAttribute("ResType").getDouble())
                currentAttList.addAttribute("ResLotOccup", res_list.getAttribute("ResLotOccup").getDouble())
                currentAttList.addAttribute("AvgAllot_A", res_list.getAttribute("AvgAllot_A").getDouble())
                currentAttList.addAttribute("AvgAllot_W", res_list.getAttribute("AvgAllot_W").getDouble())
                currentAttList.addAttribute("AvgAllot_D", res_list.getAttribute("AvgAllot_D").getDouble())
                currentAttList.addAttribute("ResLotPubDW_A", res_list.getAttribute("ResLotPubDW_A").getDouble())
                currentAttList.addAttribute("ResLotPrivDW_A", res_list.getAttribute("ResLotPrivDW_A").getDouble())
                currentAttList.addAttribute("Collect_WLane", res_list.getAttribute("Collect_WLane").getDouble())
                currentAttList.addAttribute("Foot_W", res_list.getAttribute("Foot_W").getDouble())
                currentAttList.addAttribute("NStrip_W", res_list.getAttribute("NStrip_W").getDouble())
                currentAttList.addAttribute("ResLotRoofA", res_list.getAttribute("ResLotRoofA").getDouble())
                currentAttList.addAttribute("ResLotImpA", res_list.getAttribute("ResLotImpA").getDouble())
                currentAttList.addAttribute("ResLotConImpA", res_list.getAttribute("ResLotConImpA").getDouble())
                currentAttList.addAttribute("ResLotDscImpA", res_list.getAttribute("ResLotDscImpA").getDouble())
                currentAttList.addAttribute("ResLotRoofConnect", res_list.getAttribute("ResLotRoofConnect").getDouble())
                currentAttList.addAttribute("ResTIArea", res_list.getAttribute("ResTIArea").getDouble())
                currentAttList.addAttribute("ResEIArea", res_list.getAttribute("ResEIArea").getDouble())
                currentAttList.addAttribute("ResTIF", res_list.getAttribute("ResTIF").getDouble())
                currentAttList.addAttribute("ResEIF", res_list.getAttribute("ResEIF").getDouble())
                currentAttList.addAttribute("ResPVArea", res_list.getAttribute("ResPVArea").getDouble())
                currentAttList.addAttribute("ResDCIArea", res_list.getAttribute("ResDCIArea").getDouble())
                currentAttList.addAttribute("AvlResLot", res_list.getAttribute("AvlResLot").getDouble())                   #available space on lot
                currentAttList.addAttribute("TotStreetA", res_list.getAttribute("TotStreetA").getDouble())     #total street Area
                currentAttList.addAttribute("AvlStreet", res_list.getAttribute("AvlStreet").getDouble())    #available street space

            #--------------------------------------------------------------------------------#
            #            WRITE NON-RESIDENTIAL ATTRIBUTES INTO THE MAP                       #
            #--------------------------------------------------------------------------------#
            
            #Temporary version of planning algorithm, future version to come
            nonres_uuid = currentAttList.getAttribute("NonResidentialID").getString()
	    nonres_list = city.getComponent( nonres_uuid)
            if nonres_list.getAttribute("HasNonRes").getDouble() == 0:
                pass
            else:
                currentAttList.addAttribute("HasIndustry", nonres_list.getAttribute("HasIndustry").getDouble())
                currentAttList.addAttribute("HasCommercial", nonres_list.getAttribute("HasCommercial").getDouble())
                currentAttList.addAttribute("AIndustry", nonres_list.getAttribute("AIndustry").getDouble())
                currentAttList.addAttribute("ACommercial", nonres_list.getAttribute("ACommercial").getDouble())
                currentAttList.addAttribute("AImp_Ind", nonres_list.getAttribute("AImp_Ind").getDouble())
                currentAttList.addAttribute("AImp_Com", nonres_list.getAttribute("AImp_Com").getDouble())
            
            #--------------------------------------------------------------------------------#
            #            WRITE FACILITIES ATTRIBUTES INTO THE MAP                            #
            #--------------------------------------------------------------------------------#
            
            #Temporary version of planning algorithm, future version to come
            fac_uuid = currentAttList.getAttribute("FacilitiesID").getString()
	    facilities_list = city.getComponent( fac_uuid)
            if facilities_list.getAttribute("HasFacilities").getDouble() == 0:
                pass
            else:
                currentAttList.addAttribute("MunATot", facilities_list.getAttribute("MunATot").getDouble())
                currentAttList.addAttribute("MunAimp", facilities_list.getAttribute("MunAimp").getDouble())
                currentAttList.addAttribute("MunAeimp", facilities_list.getAttribute("MunAeimp").getDouble())
                currentAttList.addAttribute("MunAperv", facilities_list.getAttribute("MunAperv").getDouble())
                currentAttList.addAttribute("MunAroof", facilities_list.getAttribute("MunAroof").getDouble())
                currentAttList.addAttribute("MunTIF", facilities_list.getAttribute("MunTIF").getDouble())
                currentAttList.addAttribute("MunEIF", facilities_list.getAttribute("MunEIF").getDouble())
                
                currentAttList.addAttribute("TrATot", facilities_list.getAttribute("TrATot").getDouble())
                currentAttList.addAttribute("TrAimp", facilities_list.getAttribute("TrAimp").getDouble())
                currentAttList.addAttribute("TrAeimp", facilities_list.getAttribute("TrAeimp").getDouble())
                currentAttList.addAttribute("TrAperv", facilities_list.getAttribute("TrAperv").getDouble())
                currentAttList.addAttribute("TrAroof", facilities_list.getAttribute("TrAroof").getDouble())
                currentAttList.addAttribute("TrTIF", facilities_list.getAttribute("TrTIF").getDouble())
                currentAttList.addAttribute("TrEIF", facilities_list.getAttribute("TrEIF").getDouble())
            
            
            #--------------------------------------------------------------------------------#
            #            WRITE SPACES ATTRIBUTES INTO THE MAP                                #
            #--------------------------------------------------------------------------------#
            
	    strvec = city.getUUIDsOfComponentsInView(self.spacesAttr)
            spaces_list = city.getComponent(strvec[0])
            if spaces_list.getAttribute("HasSpaces").getDouble() == 0:
                pass
            else:
                currentAttList.addAttribute("rfw_Adev", spaces_list.getAttribute("rfw_Adev").getDouble())
            
 
        #END OF MODULE
    
