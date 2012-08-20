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
import technology as tech
import techdesign as td
#from pyvibe import *
from pydynamind import *


class techopp_lot(Module):
    """description of this module
        
    Describe the inputs and outputso f this module.
	- <description of inputs/outputs>
    
    Log of Updates made at each version:
    
    v0.80 (March 2012):
        - 
        Future work:
            - 
            - 
    
	@ingroup DAnCE4Water
	@author Peter M Bach
	"""

    def __init__(self):
        Module.__init__(self)
	#Views
	self.blocks = View("Block",FACE,READ)
	self.blocks.getAttribute("BlockID")
	self.blocks.getAttribute("Status")
	self.blocks.getAttribute("HasLotS")
	self.blocks.getAttribute("Soil_k")
	self.blocks.getAttribute("ResLotConImpA")
	self.blocks.getAttribute("MaxLotDeg")
	self.blocks.getAttribute("ResAllots")
	self.blocks.getAttribute("IADeficit")

	self.mapattributes = View("Mapattributes", COMPONENT,READ)
	self.mapattributes.getAttribute("NumBlocks")
	self.mapattributes.getAttribute("WidthBlocks")
	self.mapattributes.getAttribute("HeightBlocks")
	self.mapattributes.getAttribute("InputReso")
	self.mapattributes.getAttribute("TotalBasins")

	self.desAttr = View("DesAttr", COMPONENT,READ)
	self.desAttr.getAttribute("strategy_lot_check")
	self.desAttr.getAttribute("techcheckedlot")
	self.desAttr.getAttribute("targets_runoff")
	self.desAttr.getAttribute("targets_TSS")
	self.desAttr.getAttribute("targets_TN")
	self.desAttr.getAttribute("targets_TP")

	self.lotStrats = View("LotStrats",COMPONENT,WRITE)
	self.lotStrats.addAttribute("BlockID")
	self.lotStrats.addAttribute("TotalLotOptions")
	#self.lotStrats.addAttribute("
   
    
	datastream = []
	datastream.append(self.mapattributes)
	datastream.append(self.blocks)
	datastream.append(self.desAttr)
	datastream.append(self.lotStrats)
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
        map_attr = city.getComponent(strvec[0])
	strvec = city.getUUIDsOfComponentsInView(self.desAttr)
        des_attr = city.getComponent(strvec[0])
        
        #get data needed to being for loop analysis
        blocks_num = map_attr.getAttribute("NumBlocks").getDouble()     #number of blocks to loop through
        blocks_size = map_attr.getAttribute("BlockSize").getDouble()    #size of block
        map_w = map_attr.getAttribute("WidthBlocks").getDouble()        #num of blocks wide
        map_h = map_attr.getAttribute("HeightBlocks").getDouble()       #num of blocks tall
        input_res = map_attr.getAttribute("InputReso").getDouble()      #resolution of input data
        
        #--------------------------------------------------------------------------------#
        #       DISASSEMBLE DESIGN RULES INTO USABLE FORMAT FROM PREVIOUS MODULE         #
        #--------------------------------------------------------------------------------#
        lot_scale_status = des_attr.getAttribute("strategy_lot_check").getDouble()
        #Get list of technologies at Lot Scale to Loop over
        techcheckedlotstring = des_attr.getAttribute("techcheckedlot").getString()
        techcheckedlot = techcheckedlotstring.split(',')
        techcheckedlot.remove('')
        
        #Management Targets
        targets_runoff = des_attr.getAttribute("targets_runoff").getDouble()
        targets_TSS = des_attr.getAttribute("targets_TSS").getDouble()
        targets_TN = des_attr.getAttribute("targets_TN").getDouble()
        targets_TP = des_attr.getAttribute("targets_TP").getDouble()
        print [targets_runoff, targets_TSS, targets_TP, targets_TN]
        
        print "Beginning Lot-Scale Analysis"
        #--------------------------------------------------------------------------------#
        #       BEGIN LOOPING ACROSS ALL BLOCKS IN MAP                                   #
        #--------------------------------------------------------------------------------#
        
        for i in range(int(blocks_num)):
            currentID = i + 1
            currentAttList = self.getBlockUUID(currentID,city)#attribute list of current block structure
            lot_strats = Component()
	    city.addComponent(lot_strats, self.lotStrats)                                          #will hold all strategies assessed at this stage
            lot_strats.addAttribute("BlockID", currentID)                       #each block ID will have a list of strategies
            #block.setAttribute("Link_lostst", lotstrats.getUUID())

            #--------------------------------------------------------------------------------#
            #            CONDITIONAL CHECK TO SEE IF CURRENT BLOCK IS RELEVANT               #
            #--------------------------------------------------------------------------------#
            
            block_status = currentAttList.getAttribute("Status").getDouble()
            if currentAttList.getAttribute("HasLotS").getDouble() == 0:
                lot_avail_sp = currentAttList.getAttribute("AvlResLot").getDouble()      #available lot space
            else:
                lot_avail_sp = 0
                
            #2 conditions to skip: (1) block status = 0, (2) no available space
            if block_status == 0 or lot_avail_sp == 0:          
                print "BlockID"+str(currentID)+" is not active or has no available space"
                continue
            #IF NOT SKIPPED, assess technologies
            
            #--------------------------------------------------------------------------------#
            #            CONDITIONAL CHECK TO SEE IF CURRENT BLOCK IS RELEVANT               #
            #--------------------------------------------------------------------------------#
            
            ## --> print "currently on Block ID"+str(currentID)
            print "Block "+str(currentID)
            
            #GET INFORMATION FROM VECTOR DATA
            soilK = currentAttList.getAttribute("Soil_k").getDouble()                       #soil infiltration rate on area
            print "Soil infiltration rate (mm/hr): "+str(soilK)
            Aimplot = currentAttList.getAttribute("ResLotConImpA").getDouble()              #connected impervious area on ONE lot
            
            lottechs = []
            for j in techcheckedlot:
                maxsize = des_attr.getAttribute(str(j)+"maxsize").getDouble()           #gets the specific system's maximum size
                dcvpath = des_attr.getAttribute(str(j)+"descur_path").getString()
                system_tarQ = targets_runoff * float(des_attr.getAttribute(str(j)+"flow").getDouble())
                system_tarTSS = targets_TSS * float(des_attr.getAttribute(str(j)+"pollute").getDouble())
                system_tarTP = targets_TP * float(des_attr.getAttribute(str(j)+"pollute").getDouble())
                system_tarTN = targets_TN * float(des_attr.getAttribute(str(j)+"pollute").getDouble())
                print "Aimplot: "+str(Aimplot)+", System Targets: "+str(system_tarQ)+", "+str(system_tarTSS)+", "+str(system_tarTP)+", "+str(system_tarTN)+" Soil K: "+str(soilK)+", Max Size: "+str(maxsize)
                
                Asystem = eval('td.design_'+str(j)+'('+str(Aimplot)+',"'+str(dcvpath)+'",'+str(system_tarQ)+','+str(system_tarTSS)+','+str(system_tarTP)+','+str(system_tarTN)+','+str(soilK)+','+str(maxsize)+')')
                print Asystem
                lottechs.append([j, Asystem[0], Aimplot, Asystem[1]])          #append [Tech Abbreviation, Size, Area Served]
            print "Lot-Scale Technology Areas Required (in sqm)"
            print lottechs
            
            #check if there is space on the lot to fit
            final_lot_techs = []      #first column = tech, second column = size of system
            for tech in range(len(lottechs)):        #loop across all systems designed for
                currenttech = lottechs[tech][0]
                if lottechs[tech][1] < lot_avail_sp:
                    print "Possible to fit "+str(currenttech)+" at the lot scale"
                    final_lot_techs.append([currenttech, lottechs[tech][1], lottechs[tech][2], lottechs[tech][3]])
                else:
                    print "Not possible to fit "+str(currenttech)+" at the lot scale"
            
            print "Final List of Possible Lot Strategies for Lot Scale"
            print final_lot_techs
            print "------------------------------ END OF BLOCK --------------------------------------------------"
            
            #--------------------------------------------------------------------------------#
            #            TRANSFER TECHNOLOGY DESIGNS INTO VECTOR                             #
            #--------------------------------------------------------------------------------#
            #get a vector of the possible technologies that fit
            options = len(final_lot_techs)
            lot_strats.addAttribute("TotalLotOptions", options)
            for j in range(len(final_lot_techs)):
                optionstring = ""               #outputs the options as: TechAbbr,SurfaceArea, (simply split and remove last element)
                for k in range(len(final_lot_techs[j])):
                    optionstring += str(final_lot_techs[j][k])+','
                lot_strats.addAttribute("LotOption_"+str(j+1), str(optionstring))
                        
