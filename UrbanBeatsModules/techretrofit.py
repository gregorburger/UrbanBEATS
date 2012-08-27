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

import math as mat
import numpy as np
#from pyvibe import *
from pydynamind import *
import designbydcv as dcv
import techdesign as td

class techretrofit(Module):
    """description of this module
        
    Describe the inputs and outputso f this module.
	- <description of inputs/outputs>
    
    Log of Updates made at each version:
    
    v0.80 update (March 2012):
        -
        -
        Future work:
            -
            -
    
    
    v0.75 update (October 2011):
        - 
        Future work:
            - 
            - 
    
    v0.5 update (August 2011):
        - 
        -
        
    v0.5 first (July 2011):
        - 
	
	@ingroup DAnCE4Water
	@author Peter M Bach
	"""


    def initBLOCKIDtoUUID(self, city):
	blockuuids = city.getUUIDsOfComponentsInView(self.blocks)
        for blockuuid in blockuuids:
            block = city.getFace(blockuuid)
            ID = int(round(block.getAttribute("BlockID").getDouble()))
	    self.BLOCKIDtoUUID[ID] = blockuuid

    def initSYSIDtoUUID(self, city):
	sysuuids = city.getUUIDsOfComponentsInView(self.sysAttr)
        for sysuuid in sysuuids:
            sys = city.getComponent(sysuuid)
            ID = int(round(sys.getAttribute("SystemID").getDouble()))
	    self.SYSTEMIDtoUUID[ID] = sysuuid



    def getBlockUUID(self, blockid,city):
	try:
		key = self.BLOCKIDtoUUID[blockid]
	except KeyError:
		key = ""
	return city.getFace(key)

    def getSysComp(self, sysID,city):
	try:
		key = self.SYSTEMIDtoUUID[sysID]
	except KeyError:
		key = ""
	return city.getComponent(key)

    def __init__(self):
        Module.__init__(self)

        self.technames = ["ASHP", "AQ", "ASR", "BF", "GR", "GT", "GPT", "IS", "PPL", "PB", "PP", "RT", "SF", "ST", "IRR", "WSUB", "WSUR", "SW", "TPS", "UT", "WWRR", "WT", "WEF"]
        self.startyear = 1960
        self.currentyear = 1960

	#views
	self.blocks = View("Block",FACE,WRITE)
	self.blocks.addAttribute("HasLotS")
	self.blocks.addAttribute("HasStreetS")
	self.blocks.addAttribute("hasNeighS")
	self.blocks.addAttribute("IAServiced")
	self.blocks.getAttribute("ResTIArea")
	self.blocks.addAttribute("IADeficit")
	self.blocks.getAttribute("ResAllots")
	self.blocks.getAttribute("ResLotImpA")
	self.blocks.addAttribute("MaxLotDeg")
	self.blocks.addAttribute("HasPrecS")
	self.blocks.addAttribute("UpstrImpTreat")
	self.blocks.getAttribute("AvlStreet")
	self.blocks.getAttribute("BasinBlocks")
	self.blocks.getAttribute("Soil_k")
	self.blocks.getAttribute("Area_Landclass")


	self.mapattributes = View("Mapattributes", COMPONENT,WRITE)
	self.mapattributes.getAttribute("NumBlocks")
	self.mapattributes.getAttribute("BlockSize")
	self.mapattributes.getAttribute("WidthBlocks")
	self.mapattributes.getAttribute("HeightBlocks")
	self.mapattributes.getAttribute("InputReso")
	self.mapattributes.addAttribute("TotalBasins")

	self.desAttr = View("DesAttr",COMPONENT,READ)
	self.desAttr.getAttribute("retrofit_scenario")
	self.desAttr.getAttribute("force_street")
	self.desAttr.getAttribute("force_neigh")
	self.desAttr.getAttribute("force_prec")
	self.desAttr.getAttribute("renewal_alternative")
	self.desAttr.getAttribute("renewal_cycle_def")
	self.desAttr.getAttribute("renewal_lot_years")
	self.desAttr.getAttribute("renewal_street_years")
	self.desAttr.getAttribute("renewal_neigh_years")
	self.desAttr.getAttribute("renewal_lot_perc")
	self.desAttr.getAttribute("lot_renew")
	self.desAttr.getAttribute("lot_decom")
	self.desAttr.getAttribute("street_renew")
	self.desAttr.getAttribute("street_decom")
	self.desAttr.getAttribute("neigh_renew")
	self.desAttr.getAttribute("neigh_decom")
	self.desAttr.getAttribute("prec_renew")
	self.desAttr.getAttribute("prec_decom")
	self.desAttr.getAttribute("decom_thresh")
	self.desAttr.getAttribute("renewal_thresh")

	self.sysGlobal = View("SystemGlobal",COMPONENT,READ)
	self.sysGlobal.getAttribute("TotalSystems")

	self.sysAttr = View("SystemAttribute",COMPONENT,WRITE)
	self.sysAttr.addAttribute("SystemID")
	self.sysAttr.addAttribute("Location")
	self.sysAttr.addAttribute("ScaleN")
	self.sysAttr.addAttribute("Scale")
	self.sysAttr.addAttribute("TypeN")
	self.sysAttr.addAttribute("Type")
	self.sysAttr.addAttribute("SysArea")
	self.sysAttr.addAttribute("Degree")
	self.sysAttr.addAttribute("Status")
	self.sysAttr.addAttribute("Year")
	self.sysAttr.addAttribute("Qty")
	self.sysAttr.addAttribute("GoalQty")
	self.sysAttr.addAttribute("EAFact")
	self.sysAttr.addAttribute("ImpT")
	self.sysAttr.addAttribute("CurImpT")
	self.sysAttr.addAttribute("Upgrades")
	self.sysAttr.addAttribute("WDepth")
	self.sysAttr.addAttribute("FDepth")


	#datastream
	datastream = []
	datastream.append(self.mapattributes)
	datastream.append(self.blocks)
	datastream.append(self.desAttr)
	datastream.append(self.sysAttr)
	
	self.addData("City",datastream)

	self.BLOCKIDtoUUID = {}
	self.SYSTEMIDtoUUID = {}

    def run(self):
	city = self.getData("City")
	self.initBLOCKIDtoUUID(city)
	self.initSYSIDtoUUID(city)

        startyear = self.startyear
        currentyear = self.currentyear

	strvec = city.getUUIDsOfComponentsInView(self.mapattributes)
        map_attr = city.getComponent(strvec[0])

	strvec = city.getUUIDsOfComponentsInView(self.sysGlobal)
        totsystems = city.getComponent(strvec[0]).getAttribute("TotalSystems").getDouble()
        print "Total Existing Systems in map: "+str(totsystems)
        
        #get data needed to being for loop analysis
        blocks_num = map_attr.getAttribute("NumBlocks").getDouble()     #number of blocks to loop through
        blocks_size = map_attr.getAttribute("BlockSize").getDouble()    #size of block
        map_w = map_attr.getAttribute("WidthBlocks").getDouble()        #num of blocks wide
        map_h = map_attr.getAttribute("HeightBlocks").getDouble()       #num of blocks tall
        input_res = map_attr.getAttribute("InputReso").getDouble()      #resolution of input data

        

        
      #Get all systems
        system_list = []
        for i in range(int(blocks_num)):
            system_list.append([])
        
        for j in range(int(totsystems)):
            locate = self.getSysComp(j,city).getAttribute("Location").getDouble()
            system_list[int(locate-1)].append(j)
        print system_list
            
        #RETRIEVE RETROFIT PARAMETERS
	strvec = city.getUUIDsOfComponentsInView(self.desAttr)
        des_attr = city.getComponent(strvec[0])
        retrofit_scenario = des_attr.getAttribute("retrofit_scenario").getString()
        
        #BEGIN ALGORITHM FOR RETROFITTING - CHOOSE WHAT TO DO WITH THE AREA AND THEN DECIDE WHAT TO DO WITH SYSTEM
        for i in range(int(blocks_num)):
            currentID = i + 1
            #currentAttList = self.getBlockUUID(currentID,city) #attribute list of current block structure
            #plist = blockcityin.getPoints("BlockID"+str(currentID))
            #flist = blockcityin.getFaces("BlockID"+str(currentID))
            #pnetlist = blockcityin.getPoints("NetworkID"+str(currentID))
            #enetlist = blockcityin.getEdges("NetworkID"+str(currentID))
            #network_attr = blockcityin.getAttributes("NetworkID"+str(currentID))
            
            #-----------------------------------------------------------------#
            # DETERMINE WHETHER TO UPDATE CURRENT BLOCK AT ALL #
            #-----------------------------------------------------------------#
            
            ### QUIT CONDITION #1 - BLOCK STATUS = 0 ###
            if self.skipIfStatusZero(currentID, city):
                continue
            
            ### QUIT CONDITION #2 - NO SYSTEMS PLANNED FOR BLOCK AT ALL ###
            sys_implement = system_list[i]
            if self.skipIfNoSystems(currentID, sys_implement):
                continue
            
            #If the program reaches this line, begin retrofitting depending on the case
            if retrofit_scenario == "N": #Do nothing Scenario
                self.retrofit_DoNothing(currentID, sys_implement,city)
            elif retrofit_scenario == "R": #With Renewal Scenario
                self.retrofit_WithRenewal(currentID, sys_implement,city)
            elif retrofit_scenario == "F": #Forced Scenario
                self.retrofit_Forced(currentID, sys_implement,city)
            
            #blockcityout.setPoints("BlockID"+str(currentID),plist)
            #blockcityout.setFaces("BlockID"+str(currentID),flist)
            #blockcityout.setAttributes("BlockID"+str(currentID),currentAttList)
            #blockcityout.setPoints("NetworkID"+str(currentID), pnetlist)
            #blockcityout.setEdges("NetworkID"+str(currentID), enetlist)
            #blockcityout.setAttributes("NetworkID"+str(currentID), network_attr)
            
            #FOR LOOP END (Repeat for next BlockID)
            

        
    
    ############################
    ### ADDITIONAL FUNCTIONS ###
    ############################
    def retrofit_DoNothing(self, ID, sys_implement,city):
        #Implements the "DO NOTHING" Retrofit Scenario across the entire map
        #Do Nothing: Technologies already in place will be left as is
        # - The impervious area they already treat will be removed from the
        # outstanding impervious area to be treated
        # - The Block will be marked at the corresponding scale as "occupied"
        # so that techopp functions cannot place anything there ('no space case')

        
        print "Block: "+str(ID)
        print sys_implement
        
        currentAttList = self.getBlockUUID(ID,city)
        inblock_imp_treated = 0 #Initialize to keep track of treated in-block imperviousness
        
        #LOT SYSTEMS
        sys_descr = self.locatePlannedSystems(sys_implement, "L",city)
        if sys_descr == None:
            inblock_imp_treated += 0
            currentAttList.addAttribute("HasLotS", 0)
        else:
            currentAttList.addAttribute("HasLotS", 1) #mark the system as having been taken
            print "Lot Location: ", str(sys_descr.getAttribute("Location").getDouble())
            imptreated = self.retrieveNewAimpTreated(ID, "L", sys_descr,city)
            inblock_imp_treated += imptreated
                                  
        #STREET SYSTEMS
        sys_descr = self.locatePlannedSystems(sys_implement, "S",city)
        if sys_descr == None:
            currentAttList.addAttribute("HasStreetS", 0)
        else:
            currentAttList.addAttribute("HasStreetS", 1) #mark the system as having been taken
            print "Street Location: ", str(sys_descr.getAttribute("Location").getDouble())
            imptreated = self.retrieveNewAimpTreated(ID, "S", sys_descr,city)
            inblock_imp_treated += imptreated
            
        #NEIGHBOURHOOD SYSTEMS
        sys_descr = self.locatePlannedSystems(sys_implement, "N",city)
        if sys_descr == None:
            currentAttList.addAttribute("HasNeighS", 0)
        else:
            currentAttList.addAttribute("HasNeighS", 1)
            print "Neigh Location: ", str(sys_descr.getAttribute("Location").getDouble())
            imptreated = self.retrieveNewAimpTreated(ID, "N", sys_descr,city)
            inblock_imp_treated += imptreated
        
        currentAttList.addAttribute("IAServiced", inblock_imp_treated)
        inblock_impdeficit = max(currentAttList.getAttribute("ResTIArea").getDouble() - inblock_imp_treated, 0)
        currentAttList.addAttribute("IADeficit", inblock_impdeficit)
        print "Deficit Area still to treat inblock: ", str(inblock_impdeficit)
        
        #Calculate the maximum degree of lot implementation allowed (no. of houses)
        allotments = currentAttList.getAttribute("ResAllots").getDouble()
        Aimplot = currentAttList.getAttribute("ResLotImpA").getDouble()
        print "Allotments = "+str(allotments)+" of each "+str(Aimplot)+" sqm impervious"
        max_houses = min((inblock_impdeficit/Aimplot)/allotments, 1)
        print "A Lot Strategy in this Block would permit a maximum implementation in: "+str(max_houses*100)+"% of houses"
        currentAttList.addAttribute("MaxLotDeg", max_houses)
        
        #PRECINCT SYSTEMS
        sys_descr = self.locatePlannedSystems(sys_implement, "P",city)
        if sys_descr == None:
            currentAttList.addAttribute("HasPrecS", 0)
            currentAttList.addAttribute("UpstrImpTreat", 0)
        else:
            currentAttList.addAttribute("HasPrecS", 1)
            precimptreated = self.retrieveNewAimpTreated(ID, "P", sys_descr,city)
            print "Prec Location: ", str(sys_descr.getAttribute("Location").getDouble())
            currentAttList.addAttribute("UpstrImpTreat", precimptreated)
            
        print "---------------------------------------------"
        
        return True
    
    def retrofit_Forced(self, ID, sys_implement,city):
        #Implements the "FORCED" Retrofit Scenario across the entire map
        #Forced: Technologies at the checked scales are retrofitted depending on the three
        # options available: keep, upgrade, decommission
        # - See comments under "With Renewal" scenario for further details

	strvec = city.getUUIDsOfComponentsInView(self.desAttr)
        des_attr = city.getComponent(strvec[0])

        
        #Grab relevant parameters for this:
        fstreet = des_attr.getAttribute("force_street").getDouble()
        fneigh = des_attr.getAttribute("force_neigh").getDouble()
        fprec = des_attr.getAttribute("force_prec").getDouble()
        
        print "Block: "+str(ID)
        print sys_implement
        
        currentAttList = self.getBlockUUID(ID,city)
        inblock_imp_treated = 0
        
        #LOT
        sys_descr = self.locatePlannedSystems(sys_implement, "L",city)
        if sys_descr == None:
            inblock_imp_treated += 0
            currentAttList.addAttribute("HasLotS", 0)
        else:
            decision, newImpT = self.dealWithSystem(ID, sys_descr, "L",city)
            decision = 1 #YOU CANNOT FORCE RETROFIT ON LOT, SO KEEP THE SYSTEMS
            if decision == 1: #keep
                print "Keeping the System, Lot-scale forced retrofit not possible anyway!"
                currentAttList.addAttribute("HasLotS", 1)
                inblock_imp_treated += newImpT
            #elif decision == 2: #renewal
            # #REDESIGN THE SYSTEM
            # pass
            #elif decision == 3: #decom
            # currentAttList.setAttribute("HasLotS", 0) #remove the system
            # inblock_imp_treated += 0 #quite self-explanatory but is added here for clarity
            # #remove all attributes, wipe the attributes entry in techconfigout with a blank attribute object
            # techimpl_attr = Attribute()
            # techconfigout.setAttributes("BlockID"+str(ID)+"L", techimpl_attr)
                
        #STREET
        sys_descr = self.locatePlannedSystems(sys_implement, "S",city)
        if sys_descr == None:
            currentAttList.addAttribute("HasStreetS", 0)
        else:
            oldImp = sys_descr.getAttribute("ImpT")
            decision, newImpT = self.dealWithSystem(ID, sys_descr, "S",city)
            if fstreet == 0: #if we do not force retrofit on street, just keep the system
                decision = 1
            
            if decision == 1: #keep
                print "Keeping the System"
                currentAttList.addAttribute("HasStreetS", 1)
                inblock_imp_treated += newImpT
            
            elif decision == 2: #renewal
                print "Renewing the System - Redesigning and Assessing Space Requirements"
                newAsys, newEAFact = self.redesignSystem(ID, sys_descr, "S", oldImp,city) #get new system size & EA
                avlSpace = currentAttList.getAttribute("AvlStreet").getDouble() #get available space
                if newAsys > avlSpace and renewal_alternative == "K": #if system does not fit and alternative is 'Keep'
                    print "Cannot fit new system design, keeping old design instead"
                    currentAttList.addAttribute("HasStreetS", 1)
                    inblock_imp_treated += newImpT
                elif newAsys > avlSpace and renewal_alternative == "D": #if system does not fit and alternative is 'Decommission'
                    print "Cannot fit new system design, decommissioning instead"
                    inblock_imp_treated += 0 #quite self-explanatory but is added here for clarity
                    currentAttList.addAttribute("HasStreetS", 0) #Remove system placeholder
		    city.removeComponent(self.getSysComp(ID,city).getUUID())

                else: #otherwise it'll fit, transfer new information
                    print "New System Upgrades fit, transferring this information to output"
                    currentAttList.addAttribute("HasStreetS", 1)
                    self.defineUpgradedSystemAttributes(ID, sys_descr, "S", newAsys, newEAFact, oldImp,city)
                    inblock_imp_treated += oldImp
                
            elif decision == 3: #decom
                print "Decommissioning the system"
                inblock_imp_treated += 0 #quite self-explanatory but is added here for clarity
                #remove all attributes, wipe the attributes entry in techconfigout with a blank attribute object
                currentAttList.addAttribute("HasStreetS", 0) #Remove system placeholder
		city.removeComponent(self.getSysComp(ID,city).getUUID())
            
        #NEIGH
        sys_descr = self.locatePlannedSystems(sys_implement, "N",city)
        if sys_descr == None:
            currentAttList.addAttribute("HasNeighS", 0)
        else:
            oldImp = sys_descr.getAttribute("ImpT")
            decision, newImpT = self.dealWithSystem(ID, sys_descr, "N",city)
            if fneigh == 0: #if we do not force retrofit on neighbourhood, just keep the system
                decision = 1
            
            if decision == 1: #keep
                print "Keeping the System"
                currentAttList.addAttribute("HasNeighS", 1)
                inblock_imp_treated += newImpT
                
            elif decision == 2: #renewal
                print "Renewing the System - Redesigning and Assessing Space Requirements"
                newAsys, newEAFact = self.redesignSystem(ID, sys_descr, "N", oldImp,city) #get new system size & EA
		landclassvec = self.getBlockUUID(ID,city).getAttribute("Area_Landclass").getDoubleVector()                
		avlSpace = landclassvec[10] #get available space
                if newAsys > avlSpace and renewal_alternative == "K": #if system does not fit and alternative is 'Keep'
                    print "Cannot fit new system design, keeping old design instead"
                    currentAttList.addAttribute("HasNeighS", 1)
                    inblock_imp_treated += newImpT
                elif newAsys > avlSpace and renewal_alternative == "D": #if system does not fit and alternative is 'Decommission'
                    print "Cannot fit new system design, decommissioning instead"
                    inblock_imp_treated += 0 #quite self-explanatory but is added here for clarity
                    currentAttList.addAttribute("HasNeighS", 0) #Remove system placeholder
                    city.removeComponent(self.getSysComp(ID,city).getUUID())
                else: #otherwise it'll fit, transfer new information
                    print "New System Upgrades fit, transferring this information to output"
                    currentAttList.addAttribute("HasNeighS", 1)
                    self.defineUpgradedSystemAttributes(ID, sys_descr, "N", newAsys, newEAFact, oldImp,city)
                    inblock_imp_treated += oldImp
                    
            elif decision == 3: #decom
                print "Decommissioning the system"
                inblock_imp_treated += 0 #quite self-explanatory but is added here for clarity
                #remove all attributes, wipe the attributes entry in techconfigout with a blank attribute object
                currentAttList.addAttribute("HasNeighS", 0)
                city.removeComponent(self.getSysComp(ID,city).getUUID())
        
        currentAttList.addAttribute("IAServiced", inblock_imp_treated)
        inblock_impdeficit = max(currentAttList.getAttribute("ResTIArea").getDouble() - inblock_imp_treated, 0)
        currentAttList.addAttribute("IADeficit", inblock_impdeficit)
        
        allotments = currentAttList.getAttribute("ResAllots").getDouble()
        Aimplot = currentAttList.getAttribute("ResLotImpA").getDouble()
        print "Allotments = "+str(allotments)+" of each "+str(Aimplot)+" sqm impervious"
        max_houses = min((inblock_impdeficit/Aimplot)/allotments, 1)
        print "A Lot Strategy in this Block would permit a maximum implementation in: "+str(max_houses*100)+"% of houses"
        currentAttList.addAttribute("MaxLotDeg", max_houses)
        
        #PREC
        sys_descr = self.locatePlannedSystems(sys_implement, "P",city)
        if sys_descr == None:
            currentAttList.addAttribute("HasPrecS", 0)
        else:
            oldImp = sys_descr.getAttribute("ImpT").getDouble()
            decision, newImpT = self.dealWithSystem(ID, sys_descr, "P",city)
            if fprec == 0: #if we do not force retrofit on precinct, just keep the system
                decision = 1
                
            if decision == 1: #keep
                print "Keeping the System"
                currentAttList.addAttribute("HasPrecS", 1)
                currentAttList.addAttribute("UpstrImpTreat", newImpT)
            elif decision == 2: #renewal
                print "Renewing the System - Redesigning and Assessing Space Requirements"
                newAsys, newEAFact = self.redesignSystem(ID, sys_descr, "P", oldImp,city) #get new system size & EA
                landclassvec = self.getBlockUUID(ID,city).getAttribute("Area_Landclass").getDoubleVector()                
		avlSpace = landclassvec[10] #get available space
                if newAsys > avlSpace and renewal_alternative == "K": #if system does not fit and alternative is 'Keep'
                    print "Cannot fit new system design, keeping old design instead"
                    currentAttList.addAttribute("HasPrecS", 1)
                    currentAttList.addAttribute("UpstrImpTreat", newImpT)
                elif newAsys > avlSpace and renewal_alternative == "D": #if system does not fit and alternative is 'Decommission'
                    print "Cannot fit new system design, decommissioning instead"
                    currentAttList.addAttribute("UpstrImpTreat", 0)
                    currentAttList.addAttribute("HasPrecS", 0) #Remove system placeholder
                    city.removeComponent(self.getSysComp(ID,city).getUUID())
                else: #otherwise it'll fit, transfer new information
                    print "New System Upgrades fit, transferring this information to output"
                    currentAttList.addAttribute("HasPrecS", 1)
                    self.defineUpgradedSystemAttributes(ID, sys_descr, "P", newAsys, newEAFact, oldImp,city)
                    currentAttList.addAttribute("UpstrImpTreat", oldImp)
                    
            elif decision == 3: #decom
                print "Decommissioning the system"
                currentAttList.addAttribute("UpstrImpTreat", 0)
                #remove all attributes, wipe the attributes entry in techconfigout with a blank attribute object
                currentAttList.addAttribute("HasPrecS", 0)
                city.removeComponent(self.getSysComp(ID,city).getUUID())
        

        return True

    def retrofit_WithRenewal(self, ID, sys_implement,city):
        #Implements the "WITH RENEWAL" Retrofit Scenario across the entire map
        #With Renewal: Technologies at different scales are selected for retrofitting
        # depending on the block's age and renewal cycles configured by the user
        # - Technologies are first considered for keeping, upgrading or decommissioning
        # - Keep: impervious area they already treat will be removed from the outstanding
        # impervious area to be treated and that scale in said Block marked as 'taken'
        # - Upgrade: technology targets will be looked at and compared, the upgraded technology
        # is assessed and then implemented. Same procedures as for Keep are subsequently
        # carried out with the new design
        # - Decommission: technology is removed from the area, impervious area is freed up
        # scale in said block is marked as 'available'

	strvec = city.getUUIDsOfComponentsInView(self.desAttr)
        des_attr = city.getComponent(strvec[0])
        renewal_alternative = des_attr.getAttribute("renewal_alternative").getString()

        
        currentyear = self.currentyear
        startyear = self.startyear
        time_passed = currentyear - startyear
        
        #Grab relevant parameters for this:
        cycle_def = des_attr.getAttribute("renewal_cycle_def").getDouble()
        lot_years = des_attr.getAttribute("renewal_lot_years").getDouble()
        street_years = des_attr.getAttribute("renewal_street_years").getDouble()
        neigh_years = des_attr.getAttribute("renewal_neigh_years").getDouble()
        lot_perc = des_attr.getAttribute("renewal_lot_perc").getDouble()
        
        print "Block: "+str(ID)
        print sys_implement
        
        currentAttList = self.getBlockUUID(ID,city)
        inblock_imp_treated = 0
        
        if cycle_def == 0:
            self.retrofit_DoNothing(ID, sys_implement,city) #if no renewal cycle was defined
            return True #go through the Do Nothing Loop instead
            
        #LOT
        sys_descr = self.locatePlannedSystems(sys_implement, "L",city)
        if sys_descr == None:
            inblock_imp_treated += 0
            currentAttList.addAttribute("HasLotS", 0)
        else:
            #DO SOMETHING TO DETERMINE IF YES/NO RETROFIT, then check the decision
            if time_passed - (time_passed // lot_years)*lot_years == 0:
                go_retrofit = 1 #then it's time for renewal
                print "Before: "+str(sys_descr.getAttribute("GoalQty").getDouble())
                #modify the current sys_descr attribute to take into account lot systems that have disappeared.
                #If systems have disappeared the final quantity of lot implementation (i.e. goalqty) will drop
                sys_descr = self.updateForBuildingStockRenewal(ID, sys_descr, lot_perc)
                print "After: "+str(sys_descr.getAttribute("GoalQty").getDouble())
            else:
                go_retrofit = 0
                
            #NOW DETERMINE IF ARE RETROFITTING OR NOT: IF NOT READY FOR RETROFIT, KEEP, ELSE GO INTO CYCLE
            oldImp = sys_descr.getAttribute("ImpT").getDouble() #Old ImpT using the old GoalQty value
            decision, newImpT = self.dealWithSystem(ID, sys_descr, "L",city) #gets the new ImpT using new GoalQty value (if it changed)
            if go_retrofit == 0:
                decision = 1
                
            if decision == 1: #keep
                print "Keeping the System"
                currentAttList.addAttribute("HasLotS", 1)
                inblock_imp_treated += newImpT
                
            elif decision == 2: #renewal
                print "Lot-scale systems will not allow renewal, instead the systems will be kept as is until plan is abandoned"
                currentAttList.addAttribute("HasLotS", 1)
                inblock_imp_treated += newImpT
                #FUTURE DYNAMICS TO BE INTRODUCED
                
            elif decision == 3: #decom
                print "Decommissioning the system"
                inblock_imp_treated += 0 #quite self-explanatory but is added here for clarity
                #remove all attributes, wipe the attributes entry in techconfigout with a blank attribute object
                currentAttList.addAttribute("HasLotS", 0) #remove the system
                city.removeComponent(self.getSysComp(ID,city).getUUID())
            
        #STREET
        sys_descr = self.locatePlannedSystems(sys_implement, "S",city)
        if sys_descr == None:
            currentAttList.addAttribute("HasStreetS", 0)
        else:
            #DO SOMETHING TO DETERMINE IF YES/NO RETROFIT, then check the decision
            if time_passed - (time_passed // street_years)*street_years == 0:
                go_retrofit = 1 #then it's time for renewal
            else:
                go_retrofit = 0
            
            #NOW DETERMINE IF ARE RETROFITTING OR NOT: IF NOT READY FOR RETROFIT, KEEP, ELSE GO INTO CYCLE
            oldImp = sys_descr.getAttribute("ImpT").getDouble()
            decision, newImpT = self.dealWithSystem(ID, sys_descr, "S",city)
            if go_retrofit == 0:
                decision = 1
                
            if decision == 1: #keep
                print "Keeping the System"
                currentAttList.addAttribute("HasStreetS", 1)
                inblock_imp_treated += newImpT
                
            elif decision == 2: #renewal
                print "Renewing the System - Redesigning and Assessing Space Requirements"
                newAsys, newEAFact = self.redesignSystem(ID, sys_descr, "S", oldImp,city) #get new system size & EA
                avlSpace = currentAttList.getAttribute("AvlStreet").getDouble() #get available space
                if newAsys > avlSpace and renewal_alternative == "K": #if system does not fit and alternative is 'Keep'
                    print "Cannot fit new system design, keeping old design instead"
                    currentAttList.addAttribute("HasStreetS", 1)
                    inblock_imp_treated += newImpT
                elif newAsys > avlSpace and renewal_alternative == "D": #if system does not fit and alternative is 'Decommission'
                    print "Cannot fit new system design, decommissioning instead"
                    inblock_imp_treated += 0 #quite self-explanatory but is added here for clarity
                    currentAttList.addAttribute("HasStreetS", 0) #Remove system placeholder
                    city.removeComponent(self.getSysComp(ID,city).getUUID())
                else: #otherwise it'll fit, transfer new information
                    print "New System Upgrades fit, transferring this information to output"
                    currentAttList.addAttribute("HasStreetS", 1)
                    self.defineUpgradedSystemAttributes(ID, sys_descr, "S", newAsys, newEAFact, oldImp,city)
                    inblock_imp_treated += oldImp
                    
            elif decision == 3: #decom
                print "Decommissioning the system"
                inblock_imp_treated += 0 #quite self-explanatory but is added here for clarity
                #remove all attributes, wipe the attributes entry in techconfigout with a blank attribute object
                currentAttList.addAttribute("HasStreetS", 0) #remove the system
                city.removeComponent(self.getSysComp(ID,city).getUUID())
        
        #NEIGH
        sys_descr = self.locatePlannedSystems(sys_implement, "N",city)
        if sys_descr == None:
            currentAttList.addAttribute("HasNeighS", 0)
        else:
            #DO SOMETHING TO DETERMINE IF YES/NO RETROFIT, then check the decision
            if time_passed - (time_passed // neigh_years)*neigh_years == 0:
                go_retrofit = 1 #then it's time for renewal
            else:
                go_retrofit = 0
                
            #NOW DETERMINE IF ARE RETROFITTING OR NOT: IF NOT READY FOR RETROFIT, KEEP, ELSE GO INTO CYCLE
            oldImp = sys_descr.getAttribute("ImpT").getDouble()
            decision, newImpT = self.dealWithSystem(ID, sys_descr, "N",city)
            if go_retrofit == 0: #if not 1 then keep the system
                decision = 1
            
            if decision == 1: #keep
                print "Keeping the System"
                currentAttList.addAttribute("HasNeighS", 1)
                inblock_imp_treated += newImpT
                
            elif decision == 2: #renewal
                print "Renewing the System - Redesigning and Assessing Space Requirements"
                newAsys, newEAFact = self.redesignSystem(ID, sys_descr, "N", oldImp,city) #get new system size & EA
            	landclassvec = self.getBlockUUID(ID,city).getAttribute("Area_Landclass").getDoubleVector()                
		avlSpace = landclassvec[10] #get available space
                if newAsys > avlSpace and renewal_alternative == "K": #if system does not fit and alternative is 'Keep'
                    print "Cannot fit new system design, keeping old design instead"
                    currentAttList.addAttribute("HasNeighS", 1)
                    inblock_imp_treated += newImpT
                elif newAsys > avlSpace and renewal_alternative == "D": #if system does not fit and alternative is 'Decommission'
                    print "Cannot fit new system design, decommissioning instead"
                    inblock_imp_treated += 0 #quite self-explanatory but is added here for clarity
                    currentAttList.addAttribute("HasNeighS", 0) #Remove system placeholder
                    city.removeComponent(self.getSysComp(ID,city).getUUID())
                else: #otherwise it'll fit, transfer new information
                    print "New System Upgrades fit, transferring this information to output"
                    currentAttList.addAttribute("HasNeighS", 1)
                    self.defineUpgradedSystemAttributes(ID, sys_descr, "N", newAsys, newEAFact, oldImp,city)
                    inblock_imp_treated += oldImp
                    
            elif decision == 3: #decom
                print "Decommissioning the system"
                inblock_imp_treated += 0 #quite self-explanatory but is added here for clarity
                #remove all attributes, wipe the attributes entry in techconfigout with a blank attribute object
                currentAttList.addAttribute("HasNeighS", 0)
                city.removeComponent(self.getSysComp(ID,city).getUUID())
        
        currentAttList.addAttribute("IAServiced", inblock_imp_treated)
        inblock_impdeficit = max(currentAttList.getAttribute("ResTIArea").getDouble() - inblock_imp_treated, 0)
        currentAttList.addAttribute("IADeficit", inblock_impdeficit)
        
        allotments = currentAttList.getAttribute("ResAllots").getDouble()
        Aimplot = currentAttList.getAttribute("ResLotImpA").getDouble()
        print "Allotments = "+str(allotments)+" of each "+str(Aimplot)+" sqm impervious"
        max_houses = min((inblock_impdeficit/Aimplot)/allotments, 1)
        print "A Lot Strategy in this Block would permit a maximum implementation in: "+str(max_houses*100)+"% of houses"
        currentAttList.addAttribute("MaxLotDeg", max_houses)
        
        #PREC
        sys_descr = self.locatePlannedSystems(sys_implement, "P",city)
        if sys_descr == None:
            currentAttList.addAttribute("HasPrecS", 0)
        else:
            #DO SOMETHING TO DETERMINE IF YES/NO RETROFIT, then check the decision
            if time_passed - (time_passed // neigh_years)*neigh_years == 0:
                go_retrofit = 1 #then it's time for renewal
            else:
                go_retrofit = 0 #otherwise do not do anything
                
            #NOW DETERMINE IF ARE RETROFITTING OR NOT: IF NOT READY FOR RETROFIT, KEEP, ELSE GO INTO CYCLE
            oldImp = sys_descr.getAttribute("ImpT").getDouble()
            decision, newImpT = self.dealWithSystem(ID, sys_descr, "P",city)
            if go_retrofit == 0:
                decision = 1
                
            if decision == 1: #keep
                print "Keeping the System"
                currentAttList.addAttribute("HasPrecS", 1)
                currentAttList.addAttribute("UpstrImpTreat", newImpT)
                
            elif decision == 2: #renewal
                print "Renewing the System - Redesigning and Assessing Space Requirements"
                newAsys, newEAFact = self.redesignSystem(ID, sys_descr, "P", oldImp,city) #get new system size & EA
            	landclassvec = self.getBlockUUID(ID,city).getAttribute("Area_Landclass").getDoubleVector()                
		avlSpace = landclassvec[10] #get available space
                if newAsys > avlSpace and renewal_alternative == "K": #if system does not fit and alternative is 'Keep'
                    print "Cannot fit new system design, keeping old design instead"
                    currentAttList.addAttribute("HasPrecS", 1)
                    currentAttList.addAttribute("UpstrImpTreat", newImpT)
                elif newAsys > avlSpace and renewal_alternative == "D": #if system does not fit and alternative is 'Decommission'
                    print "Cannot fit new system design, decommissioning instead"
                    currentAttList.addAttribute("UpstrImpTreat", 0)
                    currentAttList.addAttribute("HasPrecS", 0) #Remove system placeholder
                    city.removeComponent(self.getSysComp(ID,city).getUUID())
                else: #otherwise it'll fit, transfer new information
                    print "New System Upgrades fit, transferring this information to output"
                    currentAttList.addAttribute("HasPrecS", 1)
                    self.defineUpgradedSystemAttributes(ID, sys_descr, "P", newAsys, newEAFact, oldImp,city)
                    currentAttList.addAttribute("UpstrImpTreat", oldImp)
                    
            elif decision == 3: #decom
                print "Decommissioning the system"
                currentAttList.addAttribute("UpstrImpTreat", 0) #if system removed: imp treated = 0
                #remove all attributes, wipe the attributes entry in techconfigout with a blank attribute object
                currentAttList.addAttribute("HasPrecS", 0)
                city.removeComponent(self.getSysComp(ID,city).getUUID())
        

        return True

    def dealWithSystem(self, ID, sys_descr, scale,city):
        blockcityin, blockcityout = self.getBlockCityVectors()
        currentyear = self.currentyear
        
	strvec = city.getUUIDsOfComponentsInView(self.desAttr)
        des_attr = city.getComponent(strvec[0])
        currentAttList = self.getBlockUUID(ID,city)
        
        #Grab 'what to do with system' parameters
        lot_renew = des_attr.getAttribute("lot_renew").getDouble()
        lot_decom = des_attr.getAttribute("lot_decom").getDouble()
        street_renew = des_attr.getAttribute("street_renew").getDouble()
        street_decom = des_attr.getAttribute("street_decom").getDouble()
        neigh_renew = des_attr.getAttribute("neigh_renew").getDouble()
        neigh_decom = des_attr.getAttribute("neigh_decom").getDouble()
        prec_renew = des_attr.getAttribute("prec_renew").getDouble()
        prec_decom = des_attr.getAttribute("prec_decom").getDouble()
        decom_thresh = float(des_attr.getAttribute("decom_thresh").getDouble())/100
        renewal_thresh = float(des_attr.getAttribute("renewal_thresh").getDouble())/100
        
        scalecheck = [[lot_renew, lot_decom], [street_renew, street_decom], [neigh_renew, neigh_decom], [prec_renew, prec_decom]]
        scalematrix = ["L", "S", "N", "P"]
        scaleconditions = scalecheck[scalematrix.index(scale)]
        
        decision_matrix = [] #contains numbers of each decision 1=Keep, 2=Renew, 3=Decom
                                    #1st pass: decision based on the maximum i.e. if [1, 3], decommission
        
        ###-------------------------------------------------------
        ### DECISION FACTOR 1: SYSTEM AGE
        ### Determine where the system age lies
        ###-------------------------------------------------------
        sys_yearbuilt = sys_descr.getAttribute("Year").getDouble()
        sys_type = sys_descr.getAttribute("Type").getString()
        avglife = des_attr.getAttribute(sys_type+"avglife").getDouble()
        age = currentyear - sys_yearbuilt
        print "System Age: "+str(age)
        
        if scaleconditions[1] == 1 and age > avglife: #decom
            decision_matrix.append(3)
        elif scaleconditions[0] == 1 and age > avglife/2: #renew
            decision_matrix.append(2)
        else: #keep
            decision_matrix.append(1)
        
        ###-------------------------------------------------------
        ### DECISION FACTOR 2: DROP IN PERFORMANCE
        ### Determine where the system performance lies
        ###-------------------------------------------------------
        old_imp = sys_descr.getAttribute("ImpT").getDouble()
        if old_imp == 0: #This can happen if for example it was found previously that
            perfdeficit = 1.0 #the system can no longer meet new targets, but is not retrofitted because of renewal cycles.
            new_imp = 0
        else: #Need to catch this happening or else there will be a float division error!
            new_imp = self.retrieveNewAimpTreated(ID, scale, sys_descr,city)
            perfdeficit = abs(old_imp - new_imp)/old_imp
            
        print "Old Imp: "+str(old_imp)
        print "New Imp: "+str(new_imp)
        print "Performance Deficit of System: "+str(perfdeficit)
        
        if scaleconditions[1] == 1 and perfdeficit >= decom_thresh: #Decom = Checked, threshold exceeded
            decision_matrix.append(3)
        elif scaleconditions[0] == 1 and perfdeficit >= renewal_thresh: #Renew = checked, threshold exceeded
            decision_matrix.append(2)
        else:
            decision_matrix.append(1)
        
        ###-------------------------------------------------------
        ### FUTURE DECISION FACTORS: ---
        ### ... description
        ###-------------------------------------------------------
        
        ### MAKE FINAL DECISION ###
        print decision_matrix
        final_decision = max(decision_matrix) #1st pass: the worst-case chosen, i.e. maximum
                                                    #future passes: more complex decision-making
        return final_decision, new_imp
    
    def retrieveNewAimpTreated(self, ID, scale, sys_descr,city):
        #Grab the vectors and relevant attribute lists


	strvec = city.getUUIDsOfComponentsInView(self.desAttr)
        design_attr = city.getComponent(strvec[0])
        #Determine impervious area to deal with depending on scale
        currentAttList = self.getBlockUUID(ID,city)
        
        #grab relevant information about the block
        
        ksat = currentAttList.getAttribute("Soil_k").getDouble()
        
        #Grab the current WSUD information
        imptreated = 0 #initialize to tally up
        
        #Get WSUD attributes and set for output...
        techimpl_attr = Component()
	city.addComponent(techimpl_attr,self.sysAttr)
        techimpl_attr.addAttribute("Location", ID)
        techimpl_attr.addAttribute("Scale", scale)
        
        scaleN = sys_descr.getAttribute("ScaleN").getDouble()
        techimpl_attr.addAttribute("ScaleN", scaleN)
        
        typeN = sys_descr.getAttribute("TypeN").getDouble()
        techimpl_attr.addAttribute("TypeN", typeN)
        
        type = sys_descr.getAttribute("Type").getString()
        techimpl_attr.addAttribute("Type", type)
        
        Asys = sys_descr.getAttribute("SysArea").getDouble()
        techimpl_attr.addAttribute("SysArea", Asys)
         
        deg = sys_descr.getAttribute("Degree").getDouble()
        techimpl_attr.addAttribute("Degree", deg)
                    
        status_sys = sys_descr.getAttribute("Status").getDouble()
        techimpl_attr.addAttribute("Status", status_sys)
                    
        yearbuilt = sys_descr.getAttribute("Year").getDouble()
        techimpl_attr.addAttribute("Year", yearbuilt)
        
        qty = sys_descr.getAttribute("Qty").getDouble()
        techimpl_attr.addAttribute("Qty", qty)
        
        goalqty = sys_descr.getAttribute("GoalQty").getDouble()
        techimpl_attr.addAttribute("GoalQty", goalqty)
        
        areafactor = sys_descr.getAttribute("EAFact").getDouble()
        techimpl_attr.addAttribute("EAFact", areafactor)
        
        currentimpT = sys_descr.getAttribute("CurImpT").getDouble()
        techimpl_attr.addAttribute("CurImpT", currentimpT)
        
        upgrades = sys_descr.getAttribute("Upgrades").getDouble()
        techimpl_attr.addAttribute("Upgrades", upgrades)
        
        wdepth = sys_descr.getAttribute("WDepth").getDouble()
        techimpl_attr.addAttribute("WDepth", wdepth)
        
        fdepth = sys_descr.getAttribute("FDepth").getDouble()
        techimpl_attr.addAttribute("FDepth", fdepth)
        
        Asyseffectivetotal = (Asys)/areafactor #need to be using the effective area, not the planning area!

        print "System of Type: ", type
        print "treats: "+str(deg)+" degree"
        print "Residential Imp area: "+str(currentAttList.getAttribute("ResTIArea").getDouble())
        print "System size = "+str(Asys)
        print "Total System Size = "+str(Asyseffectivetotal)
        
        ### EXCEPTION FOR SWALES AT THE MOMENT WHILE THERE ARE NO DESIGN CURVE FILES ###
        if type == "SW":
            return 0
        ### END OF EXCEPTION ###
        
        #Grab targets and adjust for particular system type
        targets = self.getCurrentTargets(type,city)
        print targets
        
        #Piece together the pathname from current system information: FUTURE
        #pathname = self.findDCVpath(type, sys_descr)

        #NOTE: CURRENT TECH DESIGNS WILL NOT BE CHANGED! THEREFORE PATHNAME WE RETRIEVE FROM
        #DESIGN DETAILS VECTOR LIST
        pathname = design_attr.getAttribute(type+"descur_path").getString()
        print pathname
        
        sys_perc = dcv.retrieveDesign(pathname, type, ksat, targets)
        if sys_perc == np.inf:
            #release the imp area, but mark the space as taken!
            print "Results - new targets cannot be met, system will not be considered"
            imptreatedbysystem = 0
            imptreated += imptreatedbysystem
            techimpl_attr.addAttribute("ImpT", imptreatedbysystem)
        else:
            #calculate the system's current Atreated
            print "Results"
            print "percentage of catchment: ", str(sys_perc)
            imptreatedbysystem = Asyseffectivetotal/sys_perc
            
            #Account for Lot Scale as exception
            if scale == "L":
                imptreated += imptreatedbysystem * goalqty #imp treated by ONE lot system * the desired qty that can be implemented
            else:
                imptreated += imptreatedbysystem
            print "impervious area treated by system: "+str(imptreatedbysystem)
            techimpl_attr.addAttribute("ImpT", imptreatedbysystem)
        

            
        return imptreated

    def redesignSystem(self, ID, sys_descr, scale, originalAimpTreated,city):
        #Redesigns the system for BlockID at the given 'scale' for the original Impervious
        #Area that it was supposed to treat, but now according to new targets.
        # - ID: BlockID, i.e. the system's location
        # - sys_descr: the original vector of the system
        # - scale: the letter denoting system scale
        # - originalAimpTreated: the old impervious area the system was meant to treat
        
        #Grab information
        currentAttList = self.getBlockUUID(ID,city)
	strvec = city.getUUIDsOfComponentsInView(self.desAttr)
        design_attr = city.getComponent(strvec[0])
        type = sys_descr.getAttribute("Type").getString()
        
        #TO BE CHANGED LATER ON, BUT FOR NOW WE ASSUME THIS IS THE SAME PATH
        dcvpath = design_attr.getAttribute(type+"descur_path").getString()
        #GET THE DCV FILENAME
        #dcvpath = self.findDCVpath(type, sys_descr)
        
        #Some additional arguments for the design function
        maxsize = design_attr.getAttribute(type+"maxsize").getDouble()
        soilK = currentAttList.getAttribute("Soil_k").getDouble()
        
        #Current targets
        targets = self.getCurrentTargets(type,city)
        
        #Call the design function using eval, due to different system Types
        newdesign = eval('td.design_'+str(type)+'('+str(originalAimpTreated)+',"'+str(dcvpath)+'",'+str(targets[0])+','+str(targets[1])+','+str(targets[2])+','+str(targets[3])+','+str(soilK)+','+str(maxsize)+')')
        Anewsystem = newdesign[0]
        newEAFactor = newdesign[1]
        
        return Anewsystem, newEAFactor

    def defineUpgradedSystemAttributes(self, ID, sys_descr, scale, newAsys, newEAFact, impT,city):

        techimpl_attr = Component()
	city.addComponent(techimpl_attr,self.sysAttr)
        techimpl_attr.addAttribute("Location", ID)
        techimpl_attr.addAttribute("Scale", scale)
        techimpl_attr.addAttribute("ScaleN", sys_descr.getAttribute("ScaleN").getDouble())
        techimpl_attr.addAttribute("TypeN", sys_descr.getAttribute("TypeN").getDouble())
        techimpl_attr.addAttribute("Type", sys_descr.getAttribute("Type").getString())
	techimpl_attr.addAttribute("SysArea", newAsys) #New System Area
        techimpl_attr.addAttribute("Degree", sys_descr.getAttribute("Degree").getDouble())
        techimpl_attr.addAttribute("Status", sys_descr.getAttribute("Status").getDouble())
	techimpl_attr.addAttribute("Year", sys_descr.getAttribute("Year").getDouble())
        techimpl_attr.addAttribute("Qty", sys_descr.getAttribute("Qty").getDouble())
        techimpl_attr.addAttribute("GoalQty", sys_descr.getAttribute("GoalQty").getDouble())                                           
	techimpl_attr.addAttribute("EAFact", newEAFact) #NEW Effective Area Factor
        techimpl_attr.addAttribute("CurImpT", sys_descr.getAttribute("CurImpT").getDouble())
        techimpl_attr.addAttribute("ImpT", impT) #Still treats the same imperviousness
        techimpl_attr.addAttribute("WDepth", sys_descr.getAttribute("WDepth").getDouble())
        techimpl_attr.addAttribute("FDepth", sys_descr.getAttribute("FDepth").getDouble())
        #System was upgraded, add one to the upgrade count
        upgrades = sys_descr.getAttribute("Upgrades").getDouble() + 1
        techimpl_attr.addAttribute("Upgrades", upgrades)
        

        return True
    
    def updateForBuildingStockRenewal(self, ID, sys_descr, lot_perc):
        #Number of houses removed from area = total currently there * lot_perc
        #evenly distribute this across those that have lot system and those that don't
        #we therefore end up calculate how many systems lost as lot-perc * how many in place
        num_lots_lost = float(sys_descr.getAttribute("Qty").getDouble())*lot_perc/100
        goalquantity = sys_descr.getAttribute("GoalQty").getDouble()
        
        adjustedgoalQty = goalquantity - num_lots_lost
        #Update goal quantity: This is how many we can only reach now because we lost some
        sys_descr.addAttribute("GoalQty", int(adjustedgoalQty))
        return sys_descr
    
    def skipIfNoSystems(self, ID, sys_implement):
        if len(sys_implement) == 0:
            print "No Systems planned for Block "+str(ID)+", skipping..."
            return True
        else:
            return False


    def skipIfStatusZero(self, ID,city):
        #Determines if the current BlockID's status is 1 or 0, if 0 transfers all its data
        #to the output vector and returns true. If main function receives true

        if self.getBlockUUID(ID,city).getAttribute("Status").getDouble() == 0:
            print "BlockID"+str(ID)+" is not active in simulation"
            return True
        else:
            return False
    
    def findDCVpath(self, type, sys_descr):
        #Finds the correct pathname of the design curve file based on system type and specs
        if type in ["IS", "BF"]: #then file = BF-EDDx.xm-FDx.xm.dcv
            pathname = 0
        elif type in ["WSUR"]: #then file = WSUR-EDDx.xm.dcv
            pathname = 0
        elif type in ["PB"]: #then file = PB-MDx.xm.dcv
            pathname = 0
        return pathname
    
    def locatePlannedSystems(self, system_list, scale,city):
        #Searches the input planned technologies list for a system that fits the scale in the block
        #Returns the system attribute list
        system_object = None
        for i in system_list:
            if str(self.getSysComp(i,city).getAttribute("Scale").getString()) == scale:
                system_object = self.getSysComp(i,city)
        return system_object

    def getCurrentTargets(self, systype,city):
        #Grab targets and adjust for particular system type

	strvec = city.getUUIDsOfComponentsInView(self.desAttr)
        design_attr = city.getComponent(strvec[0])
        tarQ = design_attr.getAttribute(systype+"flow").getDouble()*design_attr.getAttribute("targets_runoff").getDouble()
        tarTSS = design_attr.getAttribute(systype+"pollute").getDouble()*design_attr.getAttribute("targets_TSS").getDouble()
        tarTP = design_attr.getAttribute(systype+"pollute").getDouble()*design_attr.getAttribute("targets_TP").getDouble()
        tarTN = design_attr.getAttribute(systype+"pollute").getDouble()*design_attr.getAttribute("targets_TN").getDouble()
        targets = [tarQ, tarTSS, tarTP, tarTN, 100]
        return targets

    def getUpstreamIDs(self, ID,city):

        currentAttList = self.getBlockUUID(ID,city)
        upstr_string = currentAttList.getAttribute("BasinBlocks").getString() #does not include current ID itself
        upstreamIDs = upstr_string.split(',')
        upstreamIDs.remove('')
        for i in range(len(upstreamIDs)):
            upstreamIDs[i] = int(upstreamIDs[i])
        return upstreamIDs


    def getUpstreamImpArea(self, ID, upstreamIDs,city):
        #This function scans the database of blockIDs and tallies up the total
        #upstream impervious area returning it to the main run function of the
        #module.

        Aimptotal = self.getBlockUUID(ID,city).getAttribute("ResTIArea").getDouble() #tally for total upstream impervious area
        for i in upstreamIDs:
            Aimptotal += self.getBlockUUID(i,city).getAttribute("ResTIArea").getDouble()
        return Aimptotal #in sqm units
        
        
        
        
        
