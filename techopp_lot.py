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
        self.blockcityin = VectorDataIn
        self.lot_opps = VectorDataIn
        self.patchcityin = VectorDataIn
        self.designdetails = VectorDataIn
        self.addParameter(self, "blockcityin", VIBe2.VECTORDATA_IN)
        self.addParameter(self, "lot_opps", VIBe2.VECTORDATA_OUT)
        self.addParameter(self, "patchcityin", VIBe2.VECTORDATA_IN)
        self.addParameter(self, "designdetails", VIBe2.VECTORDATA_IN)
    
    
    def run(self):
        #Link input vectors with local variables
        blockcityin = self.blockcityin.getItem()
        lot_opps = self.lot_opps.getItem()
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
        lot_scale_status = des_attr.getAttribute("strategy_lot_check")
        #Get list of technologies at Lot Scale to Loop over
        techcheckedlotstring = des_attr.getStringAttribute("techcheckedlot")
        techcheckedlot = techcheckedlotstring.split(',')
        techcheckedlot.remove('')
        
        #Management Targets
        targets_runoff = des_attr.getAttribute("targets_runoff")
        targets_TSS = des_attr.getAttribute("targets_TSS")
        targets_TN = des_attr.getAttribute("targets_TN")
        targets_TP = des_attr.getAttribute("targets_TP")
        print [targets_runoff, targets_TSS, targets_TP, targets_TN]
        
        print "Beginning Lot-Scale Analysis"
        #--------------------------------------------------------------------------------#
        #       BEGIN LOOPING ACROSS ALL BLOCKS IN MAP                                   #
        #--------------------------------------------------------------------------------#
        
        for i in range(int(blocks_num)):
            currentID = i + 1
            currentAttList = blockcityin.getAttributes("BlockID"+str(currentID))#attribute list of current block structure
            lot_strats = Attribute()                                            #will hold all strategies assessed at this stage
            lot_strats.setAttribute("BlockID", currentID)                       #each block ID will have a list of strategies
            
            #--------------------------------------------------------------------------------#
            #            CONDITIONAL CHECK TO SEE IF CURRENT BLOCK IS RELEVANT               #
            #--------------------------------------------------------------------------------#
            
            block_status = currentAttList.getAttribute("Status")
            if currentAttList.getAttribute("HasLotS") == 0:
                lot_avail_sp = currentAttList.getAttribute("AvlResLot")      #available lot space
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
            soilK = currentAttList.getAttribute("Soil_k")                       #soil infiltration rate on area
            print "Soil infiltration rate (mm/hr): "+str(soilK)
            Aimplot = currentAttList.getAttribute("ResLotConImpA")              #connected impervious area on ONE lot
            
            lottechs = []
            for j in techcheckedlot:
                maxsize = des_attr.getAttribute(str(j)+"maxsize")           #gets the specific system's maximum size
                dcvpath = des_attr.getStringAttribute(str(j)+"descur_path")
                system_tarQ = targets_runoff * float(des_attr.getAttribute(str(j)+"flow"))
                system_tarTSS = targets_TSS * float(des_attr.getAttribute(str(j)+"pollute"))
                system_tarTP = targets_TP * float(des_attr.getAttribute(str(j)+"pollute"))
                system_tarTN = targets_TN * float(des_attr.getAttribute(str(j)+"pollute"))
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
            lot_strats.setAttribute("TotalLotOptions", options)
            for j in range(len(final_lot_techs)):
                optionstring = ""               #outputs the options as: TechAbbr,SurfaceArea, (simply split and remove last element)
                for k in range(len(final_lot_techs[j])):
                    optionstring += str(final_lot_techs[j][k])+','
                lot_strats.setAttribute("LotOption_"+str(j+1), str(optionstring))
            
            lot_opps.setAttributes("BlockID"+str(currentID)+"_Lot",lot_strats)    
            