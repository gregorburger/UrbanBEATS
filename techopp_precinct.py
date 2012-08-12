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
from pyvibe import *

class techopp_precinct(Module):
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
        self.blockcityin = VectorDataIn
        self.prec_opps = VectorDataIn
        self.patchcityin = VectorDataIn
        self.designdetails = VectorDataIn
        self.addParameter(self, "blockcityin", VIBe2.VECTORDATA_IN)
        self.addParameter(self, "prec_opps", VIBe2.VECTORDATA_OUT)
        self.addParameter(self, "patchcityin", VIBe2.VECTORDATA_IN)
        self.addParameter(self, "designdetails", VIBe2.VECTORDATA_IN)
    
    
    def run(self):
        #Link input vectors with local variables
        blockcityin = self.blockcityin.getItem()
        prec_opps = self.prec_opps.getItem()
        patchcityin = self.patchcityin.getItem()
        designdetails = self.designdetails.getItem()

        map_attr = blockcityin.getAttributes("MapAttributes")
        des_attr = designdetails.getAttributes("DesignAttributes")
        
        #get data needed to being for loop analysis
        blocks_num = map_attr.getAttribute("NumBlocks")     #number of blocks to loop through
        blocks_size = map_attr.getAttribute("BlockSize")    #size of block
        map_w = map_attr.getAttribute("WidthBlocks")        #num of blocks wide
        map_h = map_attr.getAttribute("HeightBlocks")       #num of blocks tall
        input_res = map_attr.getAttribute("InputReso")      #resolution of input data
        
        #--------------------------------------------------------------------------------#
        #       DISASSEMBLE DESIGN RULES INTO USABLE FORMAT FROM PREVIOUS MODULE         #
        #--------------------------------------------------------------------------------#
        prec_scale_status = des_attr.getAttribute("strategy_prec_check")
        #Get list of precinct scale technologies to loop over
        techcheckedprecstring = des_attr.getStringAttribute("techcheckedprec")
        techcheckedprec = techcheckedprecstring.split(',')
        techcheckedprec.remove('')
        
        #Calculate the increments to work with
        basin_target_min = des_attr.getAttribute("basin_target_min")/100
        basin_target_max = des_attr.getAttribute("basin_target_max")/100
        prec_increment = des_attr.getAttribute("prec_increment")
        
        prec_alts = []          #e.g. [0.25,0.5,0.75,1.0]
        for i in range(int(prec_increment)):
            prec_alts.append(float(1/prec_increment*(i+1))*basin_target_min)
        for i in range(int(prec_increment)):
            deg = float(1/prec_increment*(i+1))*basin_target_max
            if deg in prec_alts:
                continue
            else:
                prec_alts.append(deg)
        print prec_alts
        
        print "Begin Precinct Scale Analysis"
        
        #Management Targets
        targets_runoff = des_attr.getAttribute("targets_runoff")
        targets_TSS = des_attr.getAttribute("targets_TSS")
        targets_TN = des_attr.getAttribute("targets_TN")
        targets_TP = des_attr.getAttribute("targets_TP")
        
        
        #--------------------------------------------------------------------------------#
        #       BEGIN LOOPING ACROSS ALL BLOCKS IN MAP                                   #
        #--------------------------------------------------------------------------------#
        for i in range(int(blocks_num)):
            currentID = i + 1
            currentAttList = blockcityin.getAttributes("BlockID"+str(currentID))#attribute list of current block structure
            prec_strats = Attribute()                                            #will hold all strategies assessed at this stage
            prec_strats.setAttribute("BlockID", currentID)                       #each block ID will have a list of strategies
            
            #--------------------------------------------------------------------------------#
            #            CONDITIONAL CHECK TO SEE IF CURRENT BLOCK IS RELEVANT               #
            #--------------------------------------------------------------------------------#
            
            block_status = currentAttList.getAttribute("Status")
            neigh_avail_sp = currentAttList.getAttribute("ALUC_PG")      #available lot space
            
            if block_status == 0 or neigh_avail_sp == 0:                                        #SKIP CONDITION #1: If Status = 0
                print "BlockID"+str(currentID)+" is not active or has no available space"       #SKIP CONDITION #2: If no available space
                continue
            #IF NOT SKIPPED, check condition #3
            print "Block "+str(currentID)
            
            #--------------------------------------------------------------------------------#
            #            GET ALL UPSTREAM BLOCKS                                             #
            #--------------------------------------------------------------------------------#
            upstreamstring = currentAttList.getStringAttribute("BasinBlocks")
            upstreamIDs = upstreamstring.split(',')
            upstreamIDs.remove('')
            print "Upstream IDs"
            print upstreamIDs
            print len(upstreamIDs)
            
            if len(upstreamIDs) == 0:                                                           #SKIP CONDITION #3: If block has no upstream blocks
                print "BlockID"+str(currentID)+" does not have an upstream catchment, skipping"
                continue
            #IF NOT SKIPPED, keep going
            
            #--------------------------------------------------------------------------------#
            #            GET UPSTREAM IMPERVIOUS AREA                                        #
            #--------------------------------------------------------------------------------#
            #GET INFORMATION FROM VECTOR DATA
            soilK = currentAttList.getAttribute("Soil_k")                       #soil infiltration rate on area
            Aimptot = self.getUpstreamImpArea(currentID, upstreamIDs) + currentAttList.getAttribute("ResTIArea")
            
            if Aimptot == 0:                                                                   #SKIP CONDITION #4: If there is no impervious area (likely to disappear in future)
                print "BlockID"+str(currentID)+" does not need to service any upstream impervious area"
                continue
            
            #--------------------------------------------------------------------------------#
            #            DESIGN PRECINCT SCALE SYSTEM                                        #
            #--------------------------------------------------------------------------------#
            prec_strats.setAttribute("TotalCombinations", len(prec_alts))
            
            for prec_deg in prec_alts:
                Aimpprec = Aimptot * prec_deg * basin_target_min  #how much of the total upstream basin imperviousness to treat?
                prec_strats_combo = Attribute()
                prec_name = str(currentID)+"_Pr_"+str(prec_deg)
                prec_strats_combo.setAttribute("Name", prec_name)
            
                #--------------------------------------------------------------------------------#
                #            Precinct Technologies Design                                        #
                #--------------------------------------------------------------------------------#
                prectechs = []
                for j in techcheckedprec:
                    maxsize = des_attr.getAttribute(str(j)+"maxsize")           #gets the specific system's maximum size
                    dcvpath = des_attr.getStringAttribute(str(j)+"descur_path")
                    system_tarQ = targets_runoff * float(des_attr.getAttribute(str(j)+"flow"))
                    system_tarTSS = targets_TSS * float(des_attr.getAttribute(str(j)+"pollute"))
                    system_tarTP = targets_TP * float(des_attr.getAttribute(str(j)+"pollute"))
                    system_tarTN = targets_TN * float(des_attr.getAttribute(str(j)+"pollute"))
                    print "Aimpprec: "+str(Aimpprec)+", System Targets: "+str(system_tarQ)+", "+str(system_tarTSS)+", "+str(system_tarTP)+", "+str(system_tarTN)+" Soil K: "+str(soilK)+", Max Size: "+str(maxsize)
                    
                    Asystem = eval('td.design_'+str(j)+'('+str(Aimpprec)+',"'+str(dcvpath)+'",'+str(system_tarQ)+','+str(system_tarTSS)+','+str(system_tarTP)+','+str(system_tarTN)+','+str(soilK)+','+str(maxsize)+')')
                
                    prectechs.append([j, Asystem, Aimpprec])
                print "Precinct-Scale Technology Areas Required (in sqm)"
                print prectechs
                
                #check if there is space on the neighbourhood to fit
                final_prec_techs = []
                for tech in range(len(prectechs)):
                    currenttech = prectechs[tech][0]
                    if prectechs[tech][1] < neigh_avail_sp:
                        print "Possible to fit "+str(currenttech)+" at the precinct scale to serve all upstream areas"
                        final_prec_techs.append([currenttech, prectechs[tech][1], prectechs[tech][2]])
                #--------------------------------------------------------------------------------#
                #            TRANSFER TECHNOLOGY DESIGNS INTO VECTOR                             #
                #--------------------------------------------------------------------------------#
        
                options = len(final_prec_techs)
                prec_strats_combo.setAttribute("TotalOptions", options)
                j_index = 0
                for j in final_prec_techs:
                    optionstring = ""               #outputs the options as: TechAbbr,SurfaceArea, (simply split and remove last element)
                    k_index = 0
                    for k in range(len(final_prec_techs[j_index])):              #2 properties to copy over into the options string: abbr. & surface
                        optionstring += str(final_prec_techs[j_index][k_index])+','
                        prec_strats_combo.setAttribute("PrecOption_"+str(j_index+1), str(optionstring))
                        k_index += 1
                    j_index += 1
                    
                prec_opps.setAttributes("BlockID"+str(currentID)+"_Prec_"+str(prec_deg), prec_strats_combo)
            
            prec_opps.setAttributes("BlockID"+str(currentID)+"_Prec", prec_strats)
            
            #END OF FOR LOOP, REPEAT FOR NEXT BLOCK
        #END OF MODULE
            
            
    def getUpstreamImpArea(self, BlockID, upstreamIDs):
        #This function scans the database of blockIDs and tallies up the total 
        #upstream impervious area returning it to the main run function of the
        #module.
        
        blockcityin = self.blockcityin.getItem()
        currentID = BlockID
        currentAttList = blockcityin.getAttributes("BlockID"+str(currentID))
        total_upstream_blocks = len(upstreamIDs)
        Aimptotal = 0   #tally for total upstream impervious area
        for i in range(int(total_upstream_blocks)):
            current_upstreamID = int(upstreamIDs[i])
            addImpArea = blockcityin.getAttributes("BlockID"+str(current_upstreamID)).getAttribute("ResTIArea")
            Aimptotal += addImpArea
        print "Total upstream imperviousness [ha]: "+str(Aimptotal/10000)
        return Aimptotal        #in sqm units
    
    def getGreenSpacePatchData(self, BlockID):
        #This function returns the current Block ID's patch structure for assessment
        #of whether the patch structure allows for precinct scale WSUD systems
        #To be implemented in UrbanBEATS v0.85
        pass
        return True #matrix of patch information
            