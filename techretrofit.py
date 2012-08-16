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
        self.addParameter(self, "blockcityin", VIBe2.VECTORDATA_IN)
        self.addParameter(self, "blockcityout", VIBe2.VECTORDATA_OUT)
        self.addParameter(self, "patchcityin", VIBe2.VECTORDATA_IN)
        self.addParameter(self, "design_details", VIBe2.VECTORDATA_IN)
        self.addParameter(self, "techconfigin", VIBe2.VECTORDATA_IN)
        self.addParameter(self, "techconfigout", VIBe2.VECTORDATA_OUT)
        self.technames = ["ASHP", "AQ", "ASR", "BF", "GR", "GT", "GPT", "IS", "PPL", "PB", "PP", "RT", "SF", "ST", "IRR", "WSUB", "WSUR", "SW", "TPS", "UT", "WWRR", "WT", "WEF"]
        
        
        
    def run(self):
        #Link input vectors with local variables
        blockcityin = self.blockcityin.getItem()
        blockcityout = self.blockcityout.getItem()
        patchcityin = self.patchcityin.getItem()
        techconfigin = self.techconfigin.getItem()
        techconfigout = self.techconfigout.getItem()
        design_details = self.design_details.getItem()
        
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
        
            #"With Renewal Scenario Parameters"
        cycle_def = des_attr.getAttribute("renewal_cycle_def")
        lot_years = des_attr.getAttribute("renewal_lot_years")
        street_years = des_attr.getAttribute("renewal_street_years")
        neigh_years = des_attr.getAttribute("renewal_neigh_years")
        lot_perc = des_attr.getAttribute("renewal_lot_perc")
        renewal_parameters = [cycle_def, lot_years, street_years, neigh_years, lot_perc]
        
            #"Forced Retrofit Scenario Parameters"
        fstreet = des_attr.getAttribute("force_street")
        fneigh = des_attr.getAttribute("force_neigh")
        fprec = des_attr.getAttribute("force_prec")
        forced_parameters = [fstreet, fneigh, fprec]
        
            #"Individual Systems Parameters"
        lot_renew = des_attr.getAttribute("lot_renew")
        lot_decom = des_attr.getAttribute("lot_decom")
        street_renew = des_attr.getAttribute("street_renew")
        street_decom = des_attr.getAttribute("street_decom")
        neigh_renew = des_attr.getAttribute("neigh_renew")
        neigh_decom = des_attr.getAttribute("neigh_decom")
        prec_renew = des_attr.getAttribute("prec_renew")
        prec_decom = des_attr.getAttribute("prec_decom")
        decom_thresh = des_attr.getAttribute("decom_thresh")
        renewal_thresh = des_attr.getAttribute("renewal_thresh")
        renewal_alternative = des_attr.getStringAttribute("renewal_alternative")
        
        
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
                self.retrofit_WithRenewal(renewal_parameters)
            elif retrofit_scenario == "F":              #Forced Scenario
                self.retrofit_Forced(forced_parameters)
            
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
            print "Lot Count: ", str(sys_descr.getAttribute("TotSystems"))
            imptreated = self.retrieveNewAimpTreated(ID, "L", sys_descr)
            inblock_imp_treated += imptreated
                                  
        #STREET SYSTEMS
        sys_descr = self.locatePlannedSystems(sys_implement, "S")
        if sys_descr == None:
            currentAttList.setAttribute("HasStreetS", 0)
        else:
            currentAttList.setAttribute("HasStreetS", 1) #mark the system as having been taken
            print "Street Count: ", str(sys_descr.getAttribute("TotSystems"))
            imptreated = self.retrieveNewAimpTreated(ID, "S", sys_descr)
            inblock_imp_treated += imptreated
            
        #NEIGHBOURHOOD SYSTEMS
        sys_descr = self.locatePlannedSystems(sys_implement, "N")
        if sys_descr == None:
            currentAttList.setAttribute("HasNeighS", 0)
        else:
            currentAttList.setAttribute("HasNeighS", 1)
            print "Neigh Count: ", str(sys_descr.getAttribute("TotSystems"))
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
        max_houses = max((inblock_impdeficit/Aimplot)/allotments, 1)
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
            print "Prec Count: ", str(sys_descr.getAttribute("TotSystems"))
            currentAttList.setAttribute("UpstrImpTreat", precimptreated)
            
        
        blockcityout.setAttributes("BlockID"+str(ID), currentAttList)
        print "---------------------------------------------"
        
        return True
    
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
        totsystems = sys_descr.getAttribute("TotSystems")
        imptreated = 0      #initialize to tally up
        
        #Write to outputs
        techimpl_attr = Attribute()
        techimpl_attr.setAttribute("Location", ID)
        techimpl_attr.setAttribute("Scale", scale)
        techimpl_attr.setAttribute("TotSystems", totsystems)
        
        for i in range(int(totsystems)):         #loop through systems and grab all info
            #Get WSUD attributes and set for output...
            typeN = sys_descr.getAttribute("TypeN"+str(i+1))
            techimpl_attr.setAttribute("Sys"+str(i+1)+"TypeN", typeN)

            type = sys_descr.getStringAttribute("Type"+str(i+1))
            techimpl_attr.setAttribute("Sys"+str(i+1)+"Type", type)
            
            Asys = sys_descr.getAttribute("Area"+str(i+1))
            techimpl_attr.setAttribute("Sys"+str(i+1)+"Area", Asys)
             
            deg = sys_descr.getAttribute("Service"+str(i+1))
            techimpl_attr.setAttribute("Sys"+str(i+1)+"Degree", deg)
                        
            status_sys = sys_descr.getAttribute("Status"+str(i+1))
            techimpl_attr.setAttribute("Sys"+str(i+1)+"Status", status_sys)
                        
            yearbuilt = sys_descr.getAttribute("YearConst"+str(i+1))
            techimpl_attr.setAttribute("Sys"+str(i+1)+"Year", yearbuilt)
            
            qty = sys_descr.getAttribute("Quantity"+str(i+1))
            techimpl_attr.setAttribute("Sys"+str(i+1)+"Qty", qty)
            
            areafactor = sys_descr.getAttribute("AreaFactor"+str(i+1))
            techimpl_attr.setAttribute("Sys"+str(i+1)+"EAFact", areafactor)
                        
            Asyseffectivetotal = (Asys * qty)/areafactor                        #need to be using the effective area, not the planning area!

            print "System of Type: ", type
            print "treats: "+str(deg)+" degree"
            print "Residential Imp area: "+str(currentAttList.getAttribute("ResTIArea"))
            print "System size = "+str(Asys)
            print "Total System Size = "+str(Asyseffectivetotal)
            
            techconfigout.setAttributes("BlockID"+str(int(ID))+scale, techimpl_attr)
            
            ### EXCEPTION FOR SWALES AT THE MOMENT WHILE THERE ARE NO DESIGN CURVE FILES ###
            if type == "SW":
                return 0
            ### END OF EXCEPTION ###
            
            #Grab targets and adjust for particular system type
            tarQ = design_attr.getAttribute(type+"flow")*design_attr.getAttribute("targets_runoff")
            tarTSS = design_attr.getAttribute(type+"pollute")*design_attr.getAttribute("targets_TSS")
            tarTP = design_attr.getAttribute(type+"pollute")*design_attr.getAttribute("targets_TP")
            tarTN = design_attr.getAttribute(type+"pollute")*design_attr.getAttribute("targets_TN")
            targets = [tarQ, tarTSS, tarTP, tarTN, 100]
            
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
            else:
                #calculate the system's current Atreated
                print "Results"
                print sys_perc
                imptreatedbysystem = Asyseffectivetotal/sys_perc
                imptreated += imptreatedbysystem
                print imptreatedbysystem
        return imptreated
    
    
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
        Aimptotal = currentAttList.getAttribute("ResTIArea")   #tally for total upstream impervious area
        for i in upstreamIDs:
            Aimptotal += blockcityin.getAttributes("BlockID"+str(i)).getAttribute("ResTIArea")
        return Aimptotal        #in sqm units
        
        
        
        
        
        
        