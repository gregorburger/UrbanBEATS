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
from pyvibe import *
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

    def __init__(self):
        Module.__init__(self)
        self.blockcityin = VectorDataIn
        self.blockcityout = VectorDataIn
        self.patchcityin = VectorDataIn
        self.design_details = VectorDataIn
        self.techconfigin = VectorDataIn
        self.techconfigout = VectorDataIn
        self.startyear = 1960
        self.currentyear = 1960
        self.addParameter(self, "blockcityin", VIBe2.VECTORDATA_IN)
        self.addParameter(self, "blockcityout", VIBe2.VECTORDATA_OUT)
        self.addParameter(self, "patchcityin", VIBe2.VECTORDATA_IN)
        self.addParameter(self, "design_details", VIBe2.VECTORDATA_IN)
        self.addParameter(self, "techconfigin", VIBe2.VECTORDATA_IN)
        self.addParameter(self, "techconfigout", VIBe2.VECTORDATA_OUT)
        self.addParameter(self, "startyear", VIBe2.DOUBLEDATA_IN)
        self.addParameter(self, "currentyear", VIBe2.DOUBLEDATA_IN)
        self.technames = ["ASHP", "AQ", "ASR", "BF", "GR", "GT", "GPT", "IS", "PPL", "PB", "PP", "RT", "SF", "ST", "IRR", "WSUB", "WSUR", "SW", "TPS", "UT", "WWRR", "WT", "WEF"]
        
    def run(self):
        #Link input vectors with local variables
        blockcityin = self.blockcityin.getItem()
        blockcityout = self.blockcityout.getItem()
        patchcityin = self.patchcityin.getItem()
        techconfigin = self.techconfigin.getItem()
        techconfigout = self.techconfigout.getItem()
        design_details = self.design_details.getItem()
        
        startyear = self.startyear
        currentyear = self.currentyear
        print "StartYear"+str(startyear)
        print "CurrentYear"+str(currentyear)
        
        map_attr = blockcityin.getAttributes("MapAttributes")
        globsys_attr = techconfigin.getAttributes("GlobalSystemAttributes")
        totsystems = globsys_attr.getAttribute("TotalSystems")
        
        print "Total Existing Systems in map: "+str(totsystems)
        
        #get data needed to being for loop analysis
        blocks_num = map_attr.getAttribute("NumBlocks")     #number of blocks to loop through
        blocks_size = map_attr.getAttribute("BlockSize")    #size of block
        map_w = map_attr.getAttribute("WidthBlocks")        #num of blocks wide
        map_h = map_attr.getAttribute("HeightBlocks")       #num of blocks tall
        input_res = map_attr.getAttribute("InputReso")      #resolution of input data
        urbansimdata = map_attr.getStringAttribute("UrbanSimData")
        
        #Transfer Basin Data across
        basins = map_attr.getAttribute("TotalBasins")
        for i in range(int(basins)):
            currentID = i+1
            basin_attr = blockcityin.getAttributes("BasinID"+str(currentID))
            blockcityout.setAttributes("BasinID"+str(currentID), basin_attr)
        
        #Get all systems
        system_list = []
        for i in range(int(blocks_num)):
            system_list.append([])
        
        for j in range(int(totsystems)):
            locate = techconfigin.getAttributes("System"+str(j)).getAttribute("Location")
            system_list[int(locate-1)].append(j)
        print system_list
            
        #RETRIEVE RETROFIT PARAMETERS
        des_attr = design_details.getAttributes("DesignAttributes")
        retrofit_scenario = des_attr.getStringAttribute("retrofit_scenario")
        
        #BEGIN ALGORITHM FOR RETROFITTING - CHOOSE WHAT TO DO WITH THE AREA AND THEN DECIDE WHAT TO DO WITH SYSTEM
        for i in range(int(blocks_num)):
            currentID = i + 1
            currentAttList = blockcityin.getAttributes("BlockID"+str(currentID))        #attribute list of current block structure
            plist = blockcityin.getPoints("BlockID"+str(currentID))
            flist = blockcityin.getFaces("BlockID"+str(currentID))
            pnetlist = blockcityin.getPoints("NetworkID"+str(currentID))
            enetlist = blockcityin.getEdges("NetworkID"+str(currentID))
            network_attr = blockcityin.getAttributes("NetworkID"+str(currentID))
            
            #-----------------------------------------------------------------#
            #        DETERMINE WHETHER TO UPDATE CURRENT BLOCK AT ALL         #
            #-----------------------------------------------------------------#
            
            ### QUIT CONDITION #1 - BLOCK STATUS = 0 ###
            if self.skipIfStatusZero(currentID, plist, flist, pnetlist, enetlist, network_attr):
                continue
            
            ### QUIT CONDITION #2 - NO SYSTEMS PLANNED FOR BLOCK AT ALL ###
            sys_implement = system_list[i]
            if self.skipIfNoSystems(currentID, sys_implement, plist, flist, pnetlist, enetlist, network_attr):
                continue
            
            #If the program reaches this line, begin retrofitting depending on the case
            if retrofit_scenario == "N":                #Do nothing Scenario
                self.retrofit_DoNothing(currentID, sys_implement)
            elif retrofit_scenario == "R":              #With Renewal Scenario
                self.retrofit_WithRenewal(currentID, sys_implement)
            elif retrofit_scenario == "F":              #Forced Scenario
                self.retrofit_Forced(currentID, sys_implement)
            
            blockcityout.setPoints("BlockID"+str(currentID),plist)
            blockcityout.setFaces("BlockID"+str(currentID),flist)
            #blockcityout.setAttributes("BlockID"+str(currentID),currentAttList)
            blockcityout.setPoints("NetworkID"+str(currentID), pnetlist)
            blockcityout.setEdges("NetworkID"+str(currentID), enetlist)
            blockcityout.setAttributes("NetworkID"+str(currentID), network_attr)
            
            #FOR LOOP END (Repeat for next BlockID)
            
        #Output vector update
        techconfigout.setAttributes("GlobalSystemAttributes", globsys_attr)
        blockcityout.setAttributes("MapAttributes", map_attr)
        
    
    ############################
    ### ADDITIONAL FUNCTIONS ###
    ############################
    def retrofit_DoNothing(self, ID, sys_implement):
        #Implements the "DO NOTHING" Retrofit Scenario across the entire map
        #Do Nothing: Technologies already in place will be left as is
        #   - The impervious area they already treat will be removed from the
        #     outstanding impervious area to be treated
        #   - The Block will be marked at the corresponding scale as "occupied"
        #     so that techopp functions cannot place anything there ('no space case')
        blockcityin, blockcityout = self.getBlockCityVectors()
        
        print "Block: "+str(ID)
        print sys_implement
        
        currentAttList = blockcityin.getAttributes("BlockID"+str(ID))
        inblock_imp_treated = 0         #Initialize to keep track of treated in-block imperviousness
        
        #LOT SYSTEMS
        sys_descr = self.locatePlannedSystems(sys_implement, "L")
        if sys_descr == None:
            inblock_imp_treated += 0
            currentAttList.setAttribute("HasLotS", 0)
        else:
            currentAttList.setAttribute("HasLotS", 1)    #mark the system as having been taken
            print "Lot Location: ", str(sys_descr.getAttribute("Location"))
            imptreated = self.retrieveNewAimpTreated(ID, "L", sys_descr)
            inblock_imp_treated += imptreated
                                  
        #STREET SYSTEMS
        sys_descr = self.locatePlannedSystems(sys_implement, "S")
        if sys_descr == None:
            currentAttList.setAttribute("HasStreetS", 0)
        else:
            currentAttList.setAttribute("HasStreetS", 1) #mark the system as having been taken
            print "Street Location: ", str(sys_descr.getAttribute("Location"))
            imptreated = self.retrieveNewAimpTreated(ID, "S", sys_descr)
            inblock_imp_treated += imptreated
            
        #NEIGHBOURHOOD SYSTEMS
        sys_descr = self.locatePlannedSystems(sys_implement, "N")
        if sys_descr == None:
            currentAttList.setAttribute("HasNeighS", 0)
        else:
            currentAttList.setAttribute("HasNeighS", 1)
            print "Neigh Location: ", str(sys_descr.getAttribute("Location"))
            imptreated = self.retrieveNewAimpTreated(ID, "N", sys_descr)
            inblock_imp_treated += imptreated
        
        currentAttList.setAttribute("IAServiced", inblock_imp_treated)
        inblock_impdeficit = max(currentAttList.getAttribute("ResTIArea") - inblock_imp_treated, 0)
        currentAttList.setAttribute("IADeficit", inblock_impdeficit)
        print "Deficit Area still to treat inblock: ", str(inblock_impdeficit)
        
        #Calculate the maximum degree of lot implementation allowed (no. of houses)
        allotments = currentAttList.getAttribute("ResAllots")
        Aimplot = currentAttList.getAttribute("ResLotImpA")
        print "Allotments = "+str(allotments)+" of each "+str(Aimplot)+" sqm impervious"
        max_houses = min((inblock_impdeficit/Aimplot)/allotments, 1)
        print "A Lot Strategy in this Block would permit a maximum implementation in: "+str(max_houses*100)+"% of houses"
        currentAttList.setAttribute("MaxLotDeg", max_houses)
        
        #PRECINCT SYSTEMS
        sys_descr = self.locatePlannedSystems(sys_implement, "P")
        if sys_descr == None:
            currentAttList.setAttribute("HasPrecS", 0)
            currentAttList.setAttribute("UpstrImpTreat", 0)
        else:
            currentAttList.setAttribute("HasPrecS", 1)
            precimptreated = self.retrieveNewAimpTreated(ID, "P", sys_descr)
            print "Prec Location: ", str(sys_descr.getAttribute("Location"))
            currentAttList.setAttribute("UpstrImpTreat", precimptreated)
            
        blockcityout.setAttributes("BlockID"+str(ID), currentAttList)
        print "---------------------------------------------"
        
        return True
    
    def retrofit_Forced(self, ID, sys_implement):
        #Implements the "FORCED" Retrofit Scenario across the entire map
        #Forced: Technologies at the checked scales are retrofitted depending on the three
        #           options available: keep, upgrade, decommission
        #   - See comments under "With Renewal" scenario for further details
        blockcityin, blockcityout = self.getBlockCityVectors()
        des_attr = self.design_details.getItem().getAttributes("DesignAttributes")
        techconfigout = self.techconfigout.getItem()
        
        #Grab relevant parameters for this:
        fstreet = des_attr.getAttribute("force_street")
        fneigh = des_attr.getAttribute("force_neigh")
        fprec = des_attr.getAttribute("force_prec")
        
        print "Block: "+str(ID)
        print sys_implement
        
        currentAttList = blockcityin.getAttributes("BlockID"+str(ID))
        inblock_imp_treated = 0
        
        #LOT
        sys_descr = self.locatePlannedSystems(sys_implement, "L")
        if sys_descr == None:
            inblock_imp_treated += 0
            currentAttList.setAttribute("HasLotS", 0)
        else:
            decision, newImpT = self.dealWithSystem(ID, sys_descr, "L")
            decision = 1        #YOU CANNOT FORCE RETROFIT ON LOT, SO KEEP THE SYSTEMS
            if decision == 1:       #keep
                print "Keeping the System, Lot-scale forced retrofit not possible anyway!"
                currentAttList.setAttribute("HasLotS", 1)
                inblock_imp_treated += newImpT
            #elif decision == 2:     #renewal
            #    #REDESIGN THE SYSTEM
            #    pass
            #elif decision == 3:     #decom
            #    currentAttList.setAttribute("HasLotS", 0)   #remove the system
            #    inblock_imp_treated += 0    #quite self-explanatory but is added here for clarity
            #    #remove all attributes, wipe the attributes entry in techconfigout with a blank attribute object
            #    techimpl_attr = Attribute()
            #    techconfigout.setAttributes("BlockID"+str(ID)+"L", techimpl_attr)
                
        #STREET
        sys_descr = self.locatePlannedSystems(sys_implement, "S")
        if sys_descr == None:
            currentAttList.setAttribute("HasStreetS", 0)
        else:
            oldImp = sys_descr.getAttribute("ImpT")
            decision, newImpT = self.dealWithSystem(ID, sys_descr, "S")
            if fstreet == 0:    #if we do not force retrofit on street, just keep the system
                decision = 1
            
            if decision == 1:       #keep
                print "Keeping the System"
                currentAttList.setAttribute("HasStreetS", 1)
                inblock_imp_treated += newImpT
            
            elif decision == 2:     #renewal
                print "Renewing the System - Redesigning and Assessing Space Requirements"
                newAsys, newEAFact = self.redesignSystem(ID, sys_descr, "S", oldImp)      #get new system size & EA
                avlSpace = currentAttList.getAttribute("AvlStreet")                     #get available space
                if newAsys > avlSpace and renewal_alternative == "K":                   #if system does not fit and alternative is 'Keep'
                    print "Cannot fit new system design, keeping old design instead"
                    currentAttList.setAttribute("HasStreetS", 1)
                    inblock_imp_treated += newImpT
                elif newAsys > avlSpace and renewal_alternative == "D":                 #if system does not fit and alternative is 'Decommission'
                    print "Cannot fit new system design, decommissioning instead"
                    inblock_imp_treated += 0    #quite self-explanatory but is added here for clarity
                    currentAttList.setAttribute("HasStreetS", 0)    #Remove system placeholder
                    techimpl_attr = Attribute()                     #Remove all attributes
                    techconfigout.setAttributes("BlockID"+str(ID)+"S", techimpl_attr)
                else:                                                                   #otherwise it'll fit, transfer new information
                    print "New System Upgrades fit, transferring this information to output"
                    currentAttList.setAttribute("HasStreetS", 1)
                    self.defineUpgradedSystemAttributes(ID, sys_descr, "S", newAsys, newEAFact, oldImp)
                    inblock_imp_treated += oldImp
                
            elif decision == 3:     #decom
                print "Decommissioning the system"
                inblock_imp_treated += 0    #quite self-explanatory but is added here for clarity
                #remove all attributes, wipe the attributes entry in techconfigout with a blank attribute object
                currentAttList.setAttribute("HasStreetS", 0)    #Remove system placeholder
                techimpl_attr = Attribute()                     #Remove all attributes
                techconfigout.setAttributes("BlockID"+str(ID)+"S", techimpl_attr)
            
        #NEIGH
        sys_descr = self.locatePlannedSystems(sys_implement, "N")
        if sys_descr == None:
            currentAttList.setAttribute("HasNeighS", 0)
        else:
            oldImp = sys_descr.getAttribute("ImpT")
            decision, newImpT = self.dealWithSystem(ID, sys_descr, "N")
            if fneigh == 0:     #if we do not force retrofit on neighbourhood, just keep the system
                decision = 1
            
            if decision == 1:       #keep
                print "Keeping the System"
                currentAttList.setAttribute("HasNeighS", 1)
                inblock_imp_treated += newImpT
                
            elif decision == 2:     #renewal
                print "Renewing the System - Redesigning and Assessing Space Requirements"
                newAsys, newEAFact = self.redesignSystem(ID, sys_descr, "N", oldImp)      #get new system size & EA
                avlSpace = currentAttList.getAttribute("ALUC_PG")                     #get available space
                if newAsys > avlSpace and renewal_alternative == "K":                   #if system does not fit and alternative is 'Keep'
                    print "Cannot fit new system design, keeping old design instead"
                    currentAttList.setAttribute("HasNeighS", 1)
                    inblock_imp_treated += newImpT
                elif newAsys > avlSpace and renewal_alternative == "D":                 #if system does not fit and alternative is 'Decommission'
                    print "Cannot fit new system design, decommissioning instead"
                    inblock_imp_treated += 0    #quite self-explanatory but is added here for clarity
                    currentAttList.setAttribute("HasNeighS", 0)    #Remove system placeholder
                    techimpl_attr = Attribute()                     #Remove all attributes
                    techconfigout.setAttributes("BlockID"+str(ID)+"N", techimpl_attr)
                else:                                                                   #otherwise it'll fit, transfer new information
                    print "New System Upgrades fit, transferring this information to output"
                    currentAttList.setAttribute("HasNeighS", 1)
                    self.defineUpgradedSystemAttributes(ID, sys_descr, "N", newAsys, newEAFact, oldImp)
                    inblock_imp_treated += oldImp
                    
            elif decision == 3:     #decom
                print "Decommissioning the system"
                inblock_imp_treated += 0    #quite self-explanatory but is added here for clarity
                #remove all attributes, wipe the attributes entry in techconfigout with a blank attribute object
                currentAttList.setAttribute("HasNeighS", 0)
                techimpl_attr = Attribute()
                techconfigout.setAttributes("BlockID"+str(ID)+"N", techimpl_attr)
        
        currentAttList.setAttribute("IAServiced", inblock_imp_treated)
        inblock_impdeficit = max(currentAttList.getAttribute("ResTIArea") - inblock_imp_treated, 0)
        currentAttList.setAttribute("IADeficit", inblock_impdeficit)
        
        allotments = currentAttList.getAttribute("ResAllots")
        Aimplot = currentAttList.getAttribute("ResLotImpA")
        print "Allotments = "+str(allotments)+" of each "+str(Aimplot)+" sqm impervious"
        max_houses = min((inblock_impdeficit/Aimplot)/allotments, 1)
        print "A Lot Strategy in this Block would permit a maximum implementation in: "+str(max_houses*100)+"% of houses"
        currentAttList.setAttribute("MaxLotDeg", max_houses)
        
        #PREC
        sys_descr = self.locatePlannedSystems(sys_implement, "P")
        if sys_descr == None:
            currentAttList.setAttribute("HasPrecS", 0)
        else:
            oldImp = sys_descr.getAttribute("ImpT")
            decision, newImpT = self.dealWithSystem(ID, sys_descr, "P")
            if fprec == 0:      #if we do not force retrofit on precinct, just keep the system
                decision = 1
                
            if decision == 1:       #keep
                print "Keeping the System"
                currentAttList.setAttribute("HasPrecS", 1)
                currentAttList.setAttribute("UpstrImpTreat", newImpT)
            elif decision == 2:     #renewal
                print "Renewing the System - Redesigning and Assessing Space Requirements"
                newAsys, newEAFact = self.redesignSystem(ID, sys_descr, "P", oldImp)      #get new system size & EA
                avlSpace = currentAttList.getAttribute("ALUC_PG")                     #get available space
                if newAsys > avlSpace and renewal_alternative == "K":                   #if system does not fit and alternative is 'Keep'
                    print "Cannot fit new system design, keeping old design instead"
                    currentAttList.setAttribute("HasPrecS", 1)
                    currentAttList.setAttribute("UpstrImpTreat", newImpT)
                elif newAsys > avlSpace and renewal_alternative == "D":                 #if system does not fit and alternative is 'Decommission'
                    print "Cannot fit new system design, decommissioning instead"
                    currentAttList.setAttribute("UpstrImpTreat", 0)
                    currentAttList.setAttribute("HasPrecS", 0)    #Remove system placeholder
                    techimpl_attr = Attribute()                     #Remove all attributes
                    techconfigout.setAttributes("BlockID"+str(ID)+"P", techimpl_attr)
                else:                                                                   #otherwise it'll fit, transfer new information
                    print "New System Upgrades fit, transferring this information to output"
                    currentAttList.setAttribute("HasPrecS", 1)
                    self.defineUpgradedSystemAttributes(ID, sys_descr, "P", newAsys, newEAFact, oldImp)
                    currentAttList.setAttribute("UpstrImpTreat", oldImp)
                    
            elif decision == 3:     #decom
                print "Decommissioning the system"
                currentAttList.setAttribute("UpstrImpTreat", 0)
                #remove all attributes, wipe the attributes entry in techconfigout with a blank attribute object
                currentAttList.setAttribute("HasPrecS", 0)
                techimpl_attr = Attribute()
                techconfigout.setAttributes("BlockID"+str(ID)+"P", techimpl_attr)
        
        blockcityout.setAttributes("BlockID"+str(ID), currentAttList)
        return True

    def retrofit_WithRenewal(self, ID, sys_implement):
        #Implements the "WITH RENEWAL" Retrofit Scenario across the entire map
        #With Renewal: Technologies at different scales are selected for retrofitting
        #           depending on the block's age and renewal cycles configured by the user
        #   - Technologies are first considered for keeping, upgrading or decommissioning
        #   - Keep: impervious area they already treat will be removed from the outstanding
        #           impervious area to be treated and that scale in said Block marked as 'taken'
        #   - Upgrade: technology targets will be looked at and compared, the upgraded technology
        #           is assessed and then implemented. Same procedures as for Keep are subsequently
        #           carried out with the new design
        #   - Decommission: technology is removed from the area, impervious area is freed up
        #           scale in said block is marked as 'available'
        blockcityin, blockcityout = self.getBlockCityVectors()
        des_attr = self.design_details.getItem().getAttributes("DesignAttributes")
        renewal_alternative = des_attr.getStringAttribute("renewal_alternative")
        techconfigout = self.techconfigout.getItem()
        
        currentyear = self.currentyear
        startyear = self.startyear
        time_passed = currentyear - startyear
        
        #Grab relevant parameters for this:
        cycle_def = des_attr.getAttribute("renewal_cycle_def")
        lot_years = des_attr.getAttribute("renewal_lot_years")
        street_years = des_attr.getAttribute("renewal_street_years")
        neigh_years = des_attr.getAttribute("renewal_neigh_years")
        lot_perc = des_attr.getAttribute("renewal_lot_perc")
        
        print "Block: "+str(ID)
        print sys_implement
        
        currentAttList = blockcityin.getAttributes("BlockID"+str(ID))
        inblock_imp_treated = 0
        
        if cycle_def == 0:
            self.retrofit_DoNothing(ID, sys_implement)      #if no renewal cycle was defined
            return True                                     #go through the Do Nothing Loop instead
            
        #LOT
        sys_descr = self.locatePlannedSystems(sys_implement, "L")
        if sys_descr == None:
            inblock_imp_treated += 0
            currentAttList.setAttribute("HasLotS", 0)
        else:
            #DO SOMETHING TO DETERMINE IF YES/NO RETROFIT, then check the decision
            if time_passed - (time_passed // lot_years)*lot_years == 0:
                go_retrofit = 1     #then it's time for renewal
                print "Before: "+str(sys_descr.getAttribute("GoalQty"))
                #modify the current sys_descr attribute to take into account lot systems that have disappeared.
                #If systems have disappeared the final quantity of lot implementation (i.e. goalqty) will drop
                sys_descr = self.updateForBuildingStockRenewal(ID, sys_descr, lot_perc)
                print "After: "+str(sys_descr.getAttribute("GoalQty"))
            else:
                go_retrofit = 0
                
            #NOW DETERMINE IF ARE RETROFITTING OR NOT: IF NOT READY FOR RETROFIT, KEEP, ELSE GO INTO CYCLE        
            oldImp = sys_descr.getAttribute("ImpT")             #Old ImpT using the old GoalQty value
            decision, newImpT = self.dealWithSystem(ID, sys_descr, "L") #gets the new ImpT using new GoalQty value (if it changed)
            if go_retrofit == 0:
                decision = 1
                
            if decision == 1:       #keep
                print "Keeping the System"
                currentAttList.setAttribute("HasLotS", 1)
                inblock_imp_treated += newImpT
                
            elif decision == 2:     #renewal
                print "Lot-scale systems will not allow renewal, instead the systems will be kept as is until plan is abandoned"
                currentAttList.setAttribute("HasLotS", 1)
                inblock_imp_treated += newImpT
                #FUTURE DYNAMICS TO BE INTRODUCED
                
            elif decision == 3:     #decom
                print "Decommissioning the system"
                inblock_imp_treated += 0    #quite self-explanatory but is added here for clarity
                #remove all attributes, wipe the attributes entry in techconfigout with a blank attribute object
                currentAttList.setAttribute("HasLotS", 0)   #remove the system
                techimpl_attr = Attribute()
                techconfigout.setAttributes("BlockID"+str(ID)+"L", techimpl_attr)
            
        #STREET
        sys_descr = self.locatePlannedSystems(sys_implement, "S")
        if sys_descr == None:
            currentAttList.setAttribute("HasStreetS", 0)
        else:
            #DO SOMETHING TO DETERMINE IF YES/NO RETROFIT, then check the decision
            if time_passed - (time_passed // street_years)*street_years == 0:
                go_retrofit = 1     #then it's time for renewal
            else:
                go_retrofit = 0
            
            #NOW DETERMINE IF ARE RETROFITTING OR NOT: IF NOT READY FOR RETROFIT, KEEP, ELSE GO INTO CYCLE   
            oldImp = sys_descr.getAttribute("ImpT")
            decision, newImpT = self.dealWithSystem(ID, sys_descr, "S")
            if go_retrofit == 0:
                decision = 1
                
            if decision == 1:       #keep
                print "Keeping the System"
                currentAttList.setAttribute("HasStreetS", 1)
                inblock_imp_treated += newImpT
                
            elif decision == 2:     #renewal
                print "Renewing the System - Redesigning and Assessing Space Requirements"
                newAsys, newEAFact = self.redesignSystem(ID, sys_descr, "S", oldImp)      #get new system size & EA
                avlSpace = currentAttList.getAttribute("AvlStreet")                     #get available space
                if newAsys > avlSpace and renewal_alternative == "K":                   #if system does not fit and alternative is 'Keep'
                    print "Cannot fit new system design, keeping old design instead"
                    currentAttList.setAttribute("HasStreetS", 1)
                    inblock_imp_treated += newImpT
                elif newAsys > avlSpace and renewal_alternative == "D":                 #if system does not fit and alternative is 'Decommission'
                    print "Cannot fit new system design, decommissioning instead"
                    inblock_imp_treated += 0    #quite self-explanatory but is added here for clarity
                    currentAttList.setAttribute("HasStreetS", 0)    #Remove system placeholder
                    techimpl_attr = Attribute()                     #Remove all attributes
                    techconfigout.setAttributes("BlockID"+str(ID)+"S", techimpl_attr)
                else:                                                                   #otherwise it'll fit, transfer new information
                    print "New System Upgrades fit, transferring this information to output"
                    currentAttList.setAttribute("HasStreetS", 1)
                    self.defineUpgradedSystemAttributes(ID, sys_descr, "S", newAsys, newEAFact, oldImp)
                    inblock_imp_treated += oldImp
                    
            elif decision == 3:     #decom
                print "Decommissioning the system"
                inblock_imp_treated += 0    #quite self-explanatory but is added here for clarity
                #remove all attributes, wipe the attributes entry in techconfigout with a blank attribute object
                currentAttList.setAttribute("HasStreetS", 0)   #remove the system
                techimpl_attr = Attribute()
                techconfigout.setAttributes("BlockID"+str(ID)+"S", techimpl_attr)
        
        #NEIGH
        sys_descr = self.locatePlannedSystems(sys_implement, "N")
        if sys_descr == None:
            currentAttList.setAttribute("HasNeighS", 0)
        else:
            #DO SOMETHING TO DETERMINE IF YES/NO RETROFIT, then check the decision
            if time_passed - (time_passed // neigh_years)*neigh_years == 0:
                go_retrofit = 1     #then it's time for renewal
            else:
                go_retrofit = 0
                
            #NOW DETERMINE IF ARE RETROFITTING OR NOT: IF NOT READY FOR RETROFIT, KEEP, ELSE GO INTO CYCLE   
            oldImp = sys_descr.getAttribute("ImpT")
            decision, newImpT = self.dealWithSystem(ID, sys_descr, "N")
            if go_retrofit == 0:    #if not 1 then keep the system
                decision = 1
            
            if decision == 1:       #keep
                print "Keeping the System"
                currentAttList.setAttribute("HasNeighS", 1)
                inblock_imp_treated += newImpT
                
            elif decision == 2:     #renewal
                print "Renewing the System - Redesigning and Assessing Space Requirements"
                newAsys, newEAFact = self.redesignSystem(ID, sys_descr, "N", oldImp)      #get new system size & EA
                avlSpace = currentAttList.getAttribute("ALUC_PG")                     #get available space
                if newAsys > avlSpace and renewal_alternative == "K":                   #if system does not fit and alternative is 'Keep'
                    print "Cannot fit new system design, keeping old design instead"
                    currentAttList.setAttribute("HasNeighS", 1)
                    inblock_imp_treated += newImpT
                elif newAsys > avlSpace and renewal_alternative == "D":                 #if system does not fit and alternative is 'Decommission'
                    print "Cannot fit new system design, decommissioning instead"
                    inblock_imp_treated += 0    #quite self-explanatory but is added here for clarity
                    currentAttList.setAttribute("HasNeighS", 0)    #Remove system placeholder
                    techimpl_attr = Attribute()                     #Remove all attributes
                    techconfigout.setAttributes("BlockID"+str(ID)+"N", techimpl_attr)
                else:                                                                   #otherwise it'll fit, transfer new information
                    print "New System Upgrades fit, transferring this information to output"
                    currentAttList.setAttribute("HasNeighS", 1)
                    self.defineUpgradedSystemAttributes(ID, sys_descr, "N", newAsys, newEAFact, oldImp)
                    inblock_imp_treated += oldImp
                    
            elif decision == 3:     #decom
                print "Decommissioning the system"
                inblock_imp_treated += 0    #quite self-explanatory but is added here for clarity
                #remove all attributes, wipe the attributes entry in techconfigout with a blank attribute object
                currentAttList.setAttribute("HasNeighS", 0)
                techimpl_attr = Attribute()
                techconfigout.setAttributes("BlockID"+str(ID)+"N", techimpl_attr)
        
        currentAttList.setAttribute("IAServiced", inblock_imp_treated)
        inblock_impdeficit = max(currentAttList.getAttribute("ResTIArea") - inblock_imp_treated, 0)
        currentAttList.setAttribute("IADeficit", inblock_impdeficit)
        
        allotments = currentAttList.getAttribute("ResAllots")
        Aimplot = currentAttList.getAttribute("ResLotImpA")
        print "Allotments = "+str(allotments)+" of each "+str(Aimplot)+" sqm impervious"
        max_houses = min((inblock_impdeficit/Aimplot)/allotments, 1)
        print "A Lot Strategy in this Block would permit a maximum implementation in: "+str(max_houses*100)+"% of houses"
        currentAttList.setAttribute("MaxLotDeg", max_houses)
        
        #PREC
        sys_descr = self.locatePlannedSystems(sys_implement, "P")
        if sys_descr == None:
            currentAttList.setAttribute("HasPrecS", 0)
        else:
            #DO SOMETHING TO DETERMINE IF YES/NO RETROFIT, then check the decision
            if time_passed - (time_passed // neigh_years)*neigh_years == 0:
                go_retrofit = 1     #then it's time for renewal
            else:
                go_retrofit = 0     #otherwise do not do anything
                
            #NOW DETERMINE IF ARE RETROFITTING OR NOT: IF NOT READY FOR RETROFIT, KEEP, ELSE GO INTO CYCLE   
            oldImp = sys_descr.getAttribute("ImpT")
            decision, newImpT = self.dealWithSystem(ID, sys_descr, "P")
            if go_retrofit == 0:
                decision = 1
                
            if decision == 1:       #keep
                print "Keeping the System"
                currentAttList.setAttribute("HasPrecS", 1)
                currentAttList.setAttribute("UpstrImpTreat", newImpT)
                
            elif decision == 2:     #renewal
                print "Renewing the System - Redesigning and Assessing Space Requirements"
                newAsys, newEAFact = self.redesignSystem(ID, sys_descr, "P", oldImp)      #get new system size & EA
                avlSpace = currentAttList.getAttribute("ALUC_PG")                     #get available space
                if newAsys > avlSpace and renewal_alternative == "K":                   #if system does not fit and alternative is 'Keep'
                    print "Cannot fit new system design, keeping old design instead"
                    currentAttList.setAttribute("HasPrecS", 1)
                    currentAttList.setAttribute("UpstrImpTreat", newImpT)
                elif newAsys > avlSpace and renewal_alternative == "D":                 #if system does not fit and alternative is 'Decommission'
                    print "Cannot fit new system design, decommissioning instead"
                    currentAttList.setAttribute("UpstrImpTreat", 0)
                    currentAttList.setAttribute("HasPrecS", 0)    #Remove system placeholder
                    techimpl_attr = Attribute()                     #Remove all attributes
                    techconfigout.setAttributes("BlockID"+str(ID)+"P", techimpl_attr)
                else:                                                                   #otherwise it'll fit, transfer new information
                    print "New System Upgrades fit, transferring this information to output"
                    currentAttList.setAttribute("HasPrecS", 1)
                    self.defineUpgradedSystemAttributes(ID, sys_descr, "P", newAsys, newEAFact, oldImp)
                    currentAttList.setAttribute("UpstrImpTreat", oldImp)
                    
            elif decision == 3:     #decom
                print "Decommissioning the system"
                currentAttList.setAttribute("UpstrImpTreat", 0)     #if system removed: imp treated = 0
                #remove all attributes, wipe the attributes entry in techconfigout with a blank attribute object
                currentAttList.setAttribute("HasPrecS", 0)
                techimpl_attr = Attribute()
                techconfigout.setAttributes("BlockID"+str(ID)+"P", techimpl_attr)
        
        blockcityout.setAttributes("BlockID"+str(ID), currentAttList)
        return True

    def dealWithSystem(self, ID, sys_descr, scale):
        blockcityin, blockcityout = self.getBlockCityVectors()
        currentyear = self.currentyear
        
        des_attr = self.design_details.getItem().getAttributes("DesignAttributes")
        currentAttList = blockcityin.getAttributes("BlockID"+str(ID))
        
        #Grab 'what to do with system' parameters
        lot_renew = des_attr.getAttribute("lot_renew")
        lot_decom = des_attr.getAttribute("lot_decom")
        street_renew = des_attr.getAttribute("street_renew")
        street_decom = des_attr.getAttribute("street_decom")
        neigh_renew = des_attr.getAttribute("neigh_renew")
        neigh_decom = des_attr.getAttribute("neigh_decom")
        prec_renew = des_attr.getAttribute("prec_renew")
        prec_decom = des_attr.getAttribute("prec_decom")
        decom_thresh = float(des_attr.getAttribute("decom_thresh"))/100
        renewal_thresh = float(des_attr.getAttribute("renewal_thresh"))/100
        
        scalecheck = [[lot_renew, lot_decom], [street_renew, street_decom], [neigh_renew, neigh_decom], [prec_renew, prec_decom]]
        scalematrix = ["L", "S", "N", "P"]
        scaleconditions = scalecheck[scalematrix.index(scale)]
        
        decision_matrix = []        #contains numbers of each decision 1=Keep, 2=Renew, 3=Decom
                                    #1st pass: decision based on the maximum i.e. if [1, 3], decommission
        
        ###-------------------------------------------------------
        ### DECISION FACTOR 1: SYSTEM AGE
        ###         Determine where the system age lies
        ###-------------------------------------------------------
        sys_yearbuilt = sys_descr.getAttribute("Year")
        sys_type = sys_descr.getStringAttribute("Type")
        avglife = des_attr.getAttribute(sys_type+"avglife")
        age = currentyear - sys_yearbuilt
        print "System Age: "+str(age)
        
        if scaleconditions[1] == 1 and age > avglife:             #decom
            decision_matrix.append(3)
        elif scaleconditions[0] == 1 and age > avglife/2:         #renew
            decision_matrix.append(2)
        else:                                                     #keep
            decision_matrix.append(1)
        
        ###-------------------------------------------------------
        ### DECISION FACTOR 2: DROP IN PERFORMANCE
        ###         Determine where the system performance lies
        ###-------------------------------------------------------
        old_imp = sys_descr.getAttribute("ImpT")
        if old_imp == 0:                        #This can happen if for example it was found previously that 
            perfdeficit = 1.0                   #the system can no longer meet new targets, but is not retrofitted because of renewal cycles.
            new_imp = 0
        else:                                   #Need to catch this happening or else there will be a float division error!
            new_imp = self.retrieveNewAimpTreated(ID, scale, sys_descr)
            perfdeficit = abs(old_imp - new_imp)/old_imp
            
        print "Old Imp: "+str(old_imp)
        print "New Imp: "+str(new_imp)
        print "Performance Deficit of System: "+str(perfdeficit)
        
        if scaleconditions[1] == 1 and perfdeficit >= decom_thresh: #Decom = Checked, threshold exceeded
            decision_matrix.append(3)
        elif scaleconditions[0] == 1 and perfdeficit >= renewal_thresh:     #Renew = checked, threshold exceeded
            decision_matrix.append(2)
        else:
            decision_matrix.append(1)
        
        ###-------------------------------------------------------
        ### FUTURE DECISION FACTORS: ---
        ###         ... description
        ###-------------------------------------------------------
        
        ### MAKE FINAL DECISION ###
        print decision_matrix
        final_decision = max(decision_matrix)       #1st pass: the worst-case chosen, i.e. maximum
                                                    #future passes: more complex decision-making
        return final_decision, new_imp
    
    def retrieveNewAimpTreated(self, ID, scale, sys_descr):
        #Grab the vectors and relevant attribute lists
        blockcityin, blockcityout = self.getBlockCityVectors()
        techconfigout = self.techconfigout.getItem()
        
        design_attr = self.design_details.getItem().getAttributes("DesignAttributes")
        #Determine impervious area to deal with depending on scale
        currentAttList = blockcityin.getAttributes("BlockID"+str(ID))
        
        #grab relevant information about the block
        
        ksat = currentAttList.getAttribute("Soil_k")
        
        #Grab the current WSUD information
        imptreated = 0      #initialize to tally up
        
        #Get WSUD attributes and set for output...
        techimpl_attr = Attribute()
        techimpl_attr.setAttribute("Location", ID)
        techimpl_attr.setAttribute("Scale", scale)
        
        scaleN = sys_descr.getAttribute("ScaleN")
        techimpl_attr.setAttribute("ScaleN", scaleN)
        
        typeN = sys_descr.getAttribute("TypeN")
        techimpl_attr.setAttribute("TypeN", typeN)
        
        type = sys_descr.getStringAttribute("Type")
        techimpl_attr.setAttribute("Type", type)
        
        Asys = sys_descr.getAttribute("SysArea")
        techimpl_attr.setAttribute("SysArea", Asys)
         
        deg = sys_descr.getAttribute("Degree")
        techimpl_attr.setAttribute("Degree", deg)
                    
        status_sys = sys_descr.getAttribute("Status")
        techimpl_attr.setAttribute("Status", status_sys)
                    
        yearbuilt = sys_descr.getAttribute("Year")
        techimpl_attr.setAttribute("Year", yearbuilt)
        
        qty = sys_descr.getAttribute("Qty")
        techimpl_attr.setAttribute("Qty", qty)
        
        goalqty = sys_descr.getAttribute("GoalQty")
        techimpl_attr.setAttribute("GoalQty", goalqty)
        
        areafactor = sys_descr.getAttribute("EAFact")
        techimpl_attr.setAttribute("EAFact", areafactor)
        
        currentimpT = sys_descr.getAttribute("CurImpT")
        techimpl_attr.setAttribute("CurImpT", currentimpT)
        
        upgrades = sys_descr.getAttribute("Upgrades")
        techimpl_attr.setAttribute("Upgrades", upgrades)
        
        wdepth = sys_descr.getAttribute("WDepth")
        techimpl_attr.setAttribute("WDepth", wdepth)
        
        fdepth = sys_descr.getAttribute("FDepth")
        techimpl_attr.setAttribute("FDepth", fdepth)
        
        Asyseffectivetotal = (Asys)/areafactor                        #need to be using the effective area, not the planning area!

        print "System of Type: ", type
        print "treats: "+str(deg)+" degree"
        print "Residential Imp area: "+str(currentAttList.getAttribute("ResTIArea"))
        print "System size = "+str(Asys)
        print "Total System Size = "+str(Asyseffectivetotal)
        
        ### EXCEPTION FOR SWALES AT THE MOMENT WHILE THERE ARE NO DESIGN CURVE FILES ###
        if type == "SW":
            return 0
        ### END OF EXCEPTION ###
        
        #Grab targets and adjust for particular system type
        targets = self.getCurrentTargets(type)
        print targets
        
        #Piece together the pathname from current system information: FUTURE
        #pathname = self.findDCVpath(type, sys_descr)

        #NOTE: CURRENT TECH DESIGNS WILL NOT BE CHANGED! THEREFORE PATHNAME WE RETRIEVE FROM
        #DESIGN DETAILS VECTOR LIST
        pathname = design_attr.getStringAttribute(type+"descur_path")
        print pathname
        
        sys_perc = dcv.retrieveDesign(pathname, type, ksat, targets)
        if sys_perc == np.inf:
            #release the imp area, but mark the space as taken!
            print "Results - new targets cannot be met, system will not be considered"
            imptreatedbysystem = 0
            imptreated += imptreatedbysystem
            techimpl_attr.setAttribute("ImpT", imptreatedbysystem)
        else:
            #calculate the system's current Atreated
            print "Results"
            print "percentage of catchment: ", str(sys_perc)
            imptreatedbysystem = Asyseffectivetotal/sys_perc
            
            #Account for Lot Scale as exception
            if scale == "L":
                imptreated += imptreatedbysystem * goalqty      #imp treated by ONE lot system * the desired qty that can be implemented
            else:
                imptreated += imptreatedbysystem
            print "impervious area treated by system: "+str(imptreatedbysystem)
            techimpl_attr.setAttribute("ImpT", imptreatedbysystem)
        
        techconfigout.setAttributes("BlockID"+str(int(ID))+scale, techimpl_attr)    
            
        return imptreated

    def redesignSystem(self, ID, sys_descr, scale, originalAimpTreated):
        #Redesigns the system for BlockID at the given 'scale' for the original Impervious
        #Area that it was supposed to treat, but now according to new targets.
        #   - ID: BlockID, i.e. the system's location
        #   - sys_descr: the original vector of the system
        #   - scale: the letter denoting system scale
        #   - originalAimpTreated: the old impervious area the system was meant to treat
        
        #Grab information
        currentAttList = self.blockcityin.getItem().getAttributes("BlockID"+str(ID))
        design_attr = self.design_details.getItem().getAttributes("DesignAttributes")
        type = sys_descr.getStringAttribute("Type")
        
        #TO BE CHANGED LATER ON, BUT FOR NOW WE ASSUME THIS IS THE SAME PATH
        dcvpath = design_attr.getStringAttribute(type+"descur_path")
        #GET THE DCV FILENAME
        #dcvpath = self.findDCVpath(type, sys_descr)
        
        #Some additional arguments for the design function
        maxsize = design_attr.getAttribute(type+"maxsize")
        soilK = currentAttList.getAttribute("Soil_k")
        
        #Current targets
        targets = self.getCurrentTargets(type)
        
        #Call the design function using eval, due to different system Types
        newdesign = eval('td.design_'+str(type)+'('+str(originalAimpTreated)+',"'+str(dcvpath)+'",'+str(targets[0])+','+str(targets[1])+','+str(targets[2])+','+str(targets[3])+','+str(soilK)+','+str(maxsize)+')')
        Anewsystem = newdesign[0]
        newEAFactor = newdesign[1]
        
        return Anewsystem, newEAFactor

    def defineUpgradedSystemAttributes(self, ID, sys_descr, scale, newAsys, newEAFact, impT):
        techconfigout = self.techconfigout.getItem()
        techimpl_attr = Attribute()
        techimpl_attr.setAttribute("Location", ID)
        techimpl_attr.setAttribute("Scale", scale)
        techimpl_attr.setAttribute("ScaleN", sys_descr.getAttribute("ScaleN"))
        techimpl_attr.setAttribute("TypeN", sys_descr.getAttribute("TypeN"))
        techimpl_attr.setAttribute("Type", sys_descr.getStringAttribute("Type"))
        techimpl_attr.setAttribute("SysArea", newAsys)              #New System Area
        techimpl_attr.setAttribute("Degree", sys_descr.getAttribute("Degree"))
        techimpl_attr.setAttribute("Status", sys_descr.getAttribute("Status"))
        techimpl_attr.setAttribute("Year", sys_descr.getAttribute("Year"))
        techimpl_attr.setAttribute("Qty", sys_descr.getAttribute("Qty"))
        techimpl_attr.setAttribute("GoalQty", sys_descr.getAttribute("GoalQty"))
        techimpl_attr.setAttribute("EAFact", newEAFact)             #NEW Effective Area Factor
        techimpl_attr.setAttribute("CurImpT", sys_descr.getAttribute("CurImpT"))
        techimpl_attr.setAttribute("ImpT", impT)                  #Still treats the same imperviousness
        techimpl_attr.setAttribute("WDepth", sys_descr.getAttribute("WDepth"))
        techimpl_attr.setAttribute("FDepth", sys_descr.getAttribute("FDepth"))
        #System was upgraded, add one to the upgrade count
        upgrades = sys_descr.getAttribute("Upgrades") + 1
        techimpl_attr.setAttribute("Upgrades", upgrades)
        
        techconfigout.setAttributes("BlockID"+str(int(ID))+"S", techimpl_attr)
        return True
    
    def updateForBuildingStockRenewal(self, ID, sys_descr, lot_perc):
        #Number of houses removed from area = total currently there * lot_perc
        #evenly distribute this across those that have lot system and those that don't
        #we therefore end up calculate how many systems lost as lot-perc * how many in place
        num_lots_lost = float(sys_descr.getAttribute("Qty"))*lot_perc/100
        goalquantity = sys_descr.getAttribute("GoalQty")
        
        adjustedgoalQty = goalquantity - num_lots_lost
        #Update goal quantity: This is how many we can only reach now because we lost some
        sys_descr.setAttribute("GoalQty", int(adjustedgoalQty))
        return sys_descr
    
    def skipIfNoSystems(self, ID, sys_implement, plist, flist, pnetlist, enetlist, network_attr):
        blockcityin, blockcityout = self.getBlockCityVectors()
        if len(sys_implement) == 0:
            print "No Systems planned for Block "+str(ID)+", skipping..."
            #even if block isn't active at all, attributes from previous module are passed on
            blockcityout.setPoints("BlockID"+str(ID),plist)
            blockcityout.setFaces("BlockID"+str(ID),flist)
            blockcityout.setAttributes("BlockID"+str(ID),blockcityin.getAttributes("BlockID"+str(ID)))
            blockcityout.setPoints("NetworkID"+str(ID), pnetlist)
            blockcityout.setEdges("NetworkID"+str(ID), enetlist)
            blockcityout.setAttributes("NetworkID"+str(ID), network_attr)
            return True
        else:
            return False

    def getBlockCityVectors(self):
        blockcityin = self.blockcityin.getItem()
        blockcityout = self.blockcityout.getItem()
        return [blockcityin, blockcityout]

    def skipIfStatusZero(self, ID, plist, flist, pnetlist, enetlist, network_attr):
        #Determines if the current BlockID's status is 1 or 0, if 0 transfers all its data
        #to the output vector and returns true. If main function receives true
        blockcityin, blockcityout = self.getBlockCityVectors()
        if blockcityin.getAttributes("BlockID"+str(ID)).getAttribute("Status") == 0:
            print "BlockID"+str(ID)+" is not active in simulation"
            blockcityout.setPoints("BlockID"+str(ID), plist)
            blockcityout.setFaces("BlockID"+str(ID),flist)
            blockcityout.setAttributes("BlockID"+str(ID),blockcityin.getAttributes("BlockID"+str(ID)))
            blockcityout.setPoints("NetworkID"+str(ID), pnetlist)
            blockcityout.setEdges("NetworkID"+str(ID), enetlist)
            blockcityout.setAttributes("NetworkID"+str(ID), network_attr)
            return True
        else:
            return False
    
    def findDCVpath(self, type, sys_descr):
        #Finds the correct pathname of the design curve file based on system type and specs
        if type in ["IS", "BF"]:    #then file = BF-EDDx.xm-FDx.xm.dcv
            pathname = 0
        elif type in ["WSUR"]:      #then file = WSUR-EDDx.xm.dcv
            pathname = 0
        elif type in ["PB"]:        #then file = PB-MDx.xm.dcv
            pathname = 0
        return pathname
    
    def locatePlannedSystems(self, system_list, scale):
        #Searches the input planned technologies list for a system that fits the scale in the block
        #Returns the system attribute list
        techconfigin = self.techconfigin.getItem()
        system_object = None
        for i in system_list:
            if str(techconfigin.getAttributes("System"+str(i)).getStringAttribute("Scale")) == scale:
                system_object = techconfigin.getAttributes("System"+str(i))
        return system_object

    def getCurrentTargets(self, systype):
        #Grab targets and adjust for particular system type
        design_details = self.design_details.getItem()
        design_attr = design_details.getAttributes("DesignAttributes")
        tarQ = design_attr.getAttribute(systype+"flow")*design_attr.getAttribute("targets_runoff")
        tarTSS = design_attr.getAttribute(systype+"pollute")*design_attr.getAttribute("targets_TSS")
        tarTP = design_attr.getAttribute(systype+"pollute")*design_attr.getAttribute("targets_TP")
        tarTN = design_attr.getAttribute(systype+"pollute")*design_attr.getAttribute("targets_TN")
        targets = [tarQ, tarTSS, tarTP, tarTN, 100]
        return targets

    def getUpstreamIDs(self, ID):
        blockcityin = self.blockcityin.getItem()
        currentAttList = blockcityin.getAttributes("BlockID"+str(ID))
        upstr_string = currentAttList.getStringAttribute("BasinBlocks") #does not include current ID itself
        upstreamIDs = upstr_string.split(',')
        upstreamIDs.remove('')
        for i in range(len(upstreamIDs)):
            upstreamIDs[i] = int(upstreamIDs[i])
        return upstreamIDs

    def getUpstreamImpArea(self, ID, upstreamIDs):
        #This function scans the database of blockIDs and tallies up the total 
        #upstream impervious area returning it to the main run function of the
        #module.
        blockcityin = self.blockcityin.getItem()
        currentAttList = blockcityin.getAttributes("BlockID"+str(ID))
        Aimptotal = currentAttList.getAttribute("ResTIArea")   #tally for total upstream impervious area including the block itself
        for i in upstreamIDs:
            Aimptotal += blockcityin.getAttributes("BlockID"+str(i)).getAttribute("ResTIArea")
        return Aimptotal        #in sqm units
        
        
        
        
        
        
        