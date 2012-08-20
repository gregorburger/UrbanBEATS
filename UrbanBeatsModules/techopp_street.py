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

class techopp_street(Module):
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

	self.blocks = View("Block",FACE,READ)
	self.blocks.getAttribute("BlockID")
	self.blocks.getAttribute("Status")
	self.blocks.getAttribute("HasLotS")
	self.blocks.getAttribute("AvlResLot")
	self.blocks.getAttribute("Soil_k")
	self.blocks.getAttribute("ResLotConImpA")

	self.mapattributes = View("Mapattributes", COMPONENT,READ)
	self.mapattributes.getAttribute("NumBlocks")
	self.mapattributes.getAttribute("WidthBlocks")
	self.mapattributes.getAttribute("HeightBlocks")
	self.mapattributes.getAttribute("InputReso")
	self.mapattributes.getAttribute("TotalBasins")

	self.desAttr = View("DesAttr", COMPONENT,READ)
	self.desAttr.getAttribute("techcheckedstreet")
	self.desAttr.getAttribute("strategy_street_check")
	self.desAttr.getAttribute("lot_increment")
	self.desAttr.getAttribute("street_increment")
	self.desAttr.getAttribute("targets_runoff")
	self.desAttr.getAttribute("targets_TSS")
	self.desAttr.getAttribute("targets_TN")
	self.desAttr.getAttribute("targets_TP")
    
    	self.streetStrats = View("StreetStrats", COMPONENT,WRITE)
	self.streetStrats.addAttribute("BlockID")
	self.streetStrats.addAttribute("TotalCombinations")
	
	self.streetStratsCombo = View("StreetStratsCombo",COMPONENT,WRITE)
	self.streetStratsCombo.addAttribute("Name")
	self.streetStratsCombo.addAttribute("TotalOptions")

	datastream = []
	datastream.append(self.mapattributes)
	datastream.append(self.blocks)
	datastream.append(self.desAttr)
	datastream.append(self.streetStrats)
	datastream.append(self.streetStratsCombo)
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
        street_scale_status = des_attr.getAttribute("strategy_street_check").getDouble()
        #Get list of street-scale technologies to loop over
        techcheckedstreetstring = des_attr.getAttribute("techcheckedstreet").getString()
        techcheckedstreet = techcheckedstreetstring.split(',')
        techcheckedstreet.remove('')
        
        lot_increment = des_attr.getAttribute("lot_increment").getDouble()
        street_increment = des_attr.getAttribute("street_increment").getDouble()
        
        lot_alts_complete = [0]                          #e.g. [0, 0.25, 0.5, 0.75, 1.0]
        for i in range(int(lot_increment)):
            lot_alts_complete.append(float(1/lot_increment*(i+1.0)))
            
        print lot_alts_complete
        
        street_alts = []                       #e.g. [0.25, 0.5, 0.75, 1.0]
        for i in range(int(street_increment)):
            street_alts.append(float(1/street_increment*(i+1.0)))
        
        print street_alts
        
        #Management Targets
        targets_runoff = des_attr.getAttribute("targets_runoff").getDouble()
        targets_TSS = des_attr.getAttribute("targets_TSS").getDouble()
        targets_TN = des_attr.getAttribute("targets_TN").getDouble()
        targets_TP = des_attr.getAttribute("targets_TP").getDouble()
        
        #--------------------------------------------------------------------------------#
        #       BEGIN LOOPING ACROSS ALL BLOCKS IN MAP                                   #
        #--------------------------------------------------------------------------------#
        
        print "Begin Street-Neighbourhood Scale Analysis"
        
        for i in range(int(blocks_num)):
            currentID = i + 1
            currentAttList = self.getBlockUUID(currentID,city)#attribute list of current block structure
            street_strats = Component()				#will hold all strategies assessed at this stage
	    city.addComponent(street_strats, self.streetStrats)                                            
            street_strats.addAttribute("BlockID", currentID)                       #each block ID will have a list of strategies
            
            #--------------------------------------------------------------------------------#
            #            CONDITIONAL CHECK TO SEE IF CURRENT BLOCK IS RELEVANT               #
            #--------------------------------------------------------------------------------#
            
            block_status = currentAttList.getAttribute("Status").getDouble()
            if currentAttList.getAttribute("HasStreetS").getDouble() == 0:
                street_avail_sp = currentAttList.getAttribute("AvlStreet").getDouble()
            else:
                street_avail_sp = 0
                
            #2 conditions to skip: (1) block status = 0, (2) no available space on street
            if block_status == 0 or street_avail_sp == 0:          
                print "BlockID"+str(currentID)+" is not active or has no available space"
                continue
            #IF NOT SKIPPED, assess technologies
            
            ## --> print "currently on Block ID"+str(currentID)
            print "Block "+str(currentID)
            
            #GET INFORMATION FROM VECTOR DATA
            soilK = currentAttList.getAttribute("Soil_k").getDouble()                       #soil infiltration rate on area
            Aimplot = currentAttList.getAttribute("ResLotConImpA").getDouble()              #connected impervious area on ONE lot
            
            #Modify the combinations vector just for this block
            lot_alts = []
            for deg in lot_alts_complete:
                lot_alts.append(deg)
            max_houses = currentAttList.getAttribute("MaxLotDeg").getDouble()
            if max_houses != 1.0:               #if not 100%, adjust the possible degrees
		lot_alts.append(max_houses)
		lot_alts.sort()
		lastindex = lot_alts.index(max_houses)
		lot_alts.remove(max_houses)
		lot_alts = lot_alts[0:lastindex]
            
            print "Modified Lot-alts: ", str(lot_alts)
            
            allotments = currentAttList.getAttribute("ResAllots").getDouble()
            total_res_Aimp = currentAttList.getAttribute("IADeficit").getDouble()           #NOTE: This is the deficit area after passing through retrofit, etc.
            
            combinations = len(lot_alts)*len(street_alts)
            street_strats.addAttribute("TotalCombinations", combinations)
            
            for lot_deg in lot_alts:          #looping over e.g. [0, 0.25, 0.5, 0.75, 1.0]
                Aimpremain = total_res_Aimp - allotments*lot_deg*Aimplot        #remaining impervious area after lot treatment
                
                for street_deg in street_alts:   #looping over e.g. [0.25, 0.5, 0.75, 1.0]
                    street_strats_combo = Component()                   #Holds the Options for current combinations
                    city.addComponent(street_strats_combo,self.streetStratsCombo)
		    street_name = str(currentID)+"_Street_"+str(lot_deg)+"_"+str(street_deg)
                    street_strats_combo.addAttribute("Name", street_name)
                    
                    Aimpstreet = Aimpremain * street_deg        #impervious area to be treated by a street scale system
                    
                    #--------------------------------------------------------------------------------#
                    #            Street Technologies Design                                          #
                    #--------------------------------------------------------------------------------#
                        
                    streettechs = []
                    for j in techcheckedstreet:
                        maxsize = des_attr.getAttribute(str(j)+"maxsize").getDouble()           #gets the specific system's maximum size
                        dcvpath = des_attr.getAttribute(str(j)+"descur_path").getString()
                        system_tarQ = targets_runoff * float(des_attr.getAttribute(str(j)+"flow").getDouble())
                        system_tarTSS = targets_TSS * float(des_attr.getAttribute(str(j)+"pollute").getDouble())
                        system_tarTP = targets_TP * float(des_attr.getAttribute(str(j)+"pollute").getDouble())
                        system_tarTN = targets_TN * float(des_attr.getAttribute(str(j)+"pollute").getDouble())
                        print "Aimpstreet: "+str(Aimpstreet)+", System Targets: "+str(system_tarQ)+", "+str(system_tarTSS)+", "+str(system_tarTP)+", "+str(system_tarTN)+" Soil K: "+str(soilK)+", Max Size: "+str(maxsize)
                        
                        Asystem = eval('td.design_'+str(j)+'('+str(Aimpstreet)+',"'+str(dcvpath)+'",'+str(system_tarQ)+','+str(system_tarTSS)+','+str(system_tarTP)+','+str(system_tarTN)+','+str(soilK)+','+str(maxsize)+')')
                        print Asystem
                        streettechs.append([j, Asystem[0], Aimpstreet, Asystem[1]])
                    print "Street-Scale Technology Areas Required (in sqm)"
                    print streettechs
                    
                    #check if there is space on the street to fit
                    final_street_techs = []
                    for tech in range(len(streettechs)):
                        currenttech = streettechs[tech][0]
                        if currenttech == 'SW':                                 #SPECIAL CASE #1: A swale is limited by the width of the nature strip
                            if currentAttList.getAttribute("NStrip_W").getDouble() <= 2:
                                print "Nature strip width inadequate for Swales"
                                continue
                        if streettechs[tech][1] < street_avail_sp:
                            print "Possible to fit "+str(currenttech)+" at the street scale"
                            final_street_techs.append([currenttech, streettechs[tech][1], streettechs[tech][2], streettechs[tech][3]])
            
                    #--------------------------------------------------------------------------------#
                    #            TRANSFER TECHNOLOGY DESIGNS INTO VECTOR                             #
                    #--------------------------------------------------------------------------------#
            
                    options = len(final_street_techs)
                    street_strats_combo.addAttribute("TotalOptions", options)
                    j_index = 0
                    for j in final_street_techs:
                        optionstring = ""               #outputs the options as: TechAbbr,SurfaceArea, (simply split and remove last element)
                        k_index = 0
                        for k in range(len(final_street_techs[j_index])):              #2 properties to copy over into the options string: abbr. & surface
                            optionstring += str(final_street_techs[j_index][k_index])+','
                            street_strats_combo.addAttribute("StreetOption_"+str(j_index+1), str(optionstring))
                            k_index += 1
                        j_index += 1
                        
                    #street_opps.addAttributes("BlockID"+str(currentID)+"_Street_"+str(lot_deg)+"_"+str(street_deg),street_strats_combo)
            
            #street_opps.setAttributes("BlockID"+str(currentID)+"_Street", street_strats)
            
            #END OF FOR LOOP, REPEAT FOR NEXT BLOCK
        
        #END OF MODULE
            
        
