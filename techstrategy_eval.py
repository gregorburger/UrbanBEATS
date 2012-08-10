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
import ubeats_music_interface as umusic
import random as rand
import numpy as np
import math as math
import gc as garbage
from pyvibe import *
import pyvibe


class techstrategy_eval(Module):
    """description of this module
        
    Describe the inputs and outputso f this module.
	- <description of inputs/outputs>
    
    Log of Updates made at each version:
    
    v0.80 (March 2012):
        - 
        Future work:
            - 
            - 
    
	@ingroup UrbanBEATS
	@author Peter M Bach
	"""

    def __init__(self):
        Module.__init__(self)
        self.lot_opps = VectorDataIn
        self.street_opps = VectorDataIn
        self.neigh_opps = VectorDataIn
        self.prec_opps = VectorDataIn
        self.blockcityin = VectorDataIn
        self.patchcityin = VectorDataIn
        self.designdetails = VectorDataIn
        self.blockcityout = VectorDataIn
        self.patchcityout = VectorDataIn
        self.systemsout = VectorDataIn
        self.addParameter(self, "lot_opps", VIBe2.VECTORDATA_IN)
        self.addParameter(self, "street_opps", VIBe2.VECTORDATA_IN)
        self.addParameter(self, "neigh_opps", VIBe2.VECTORDATA_IN)
        self.addParameter(self, "prec_opps", VIBe2.VECTORDATA_IN)
        self.addParameter(self, "blockcityin", VIBe2.VECTORDATA_IN)
        self.addParameter(self, "patchcityin", VIBe2.VECTORDATA_IN)
        self.addParameter(self, "designdetails", VIBe2.VECTORDATA_IN)
        self.addParameter(self, "blockcityout", VIBe2.VECTORDATA_OUT)
        self.addParameter(self, "patchcityout", VIBe2.VECTORDATA_OUT)
        self.addParameter(self, "systemsout", VIBe2.VECTORDATA_OUT)
        
        self.reportin = VectorDataIn
        self.reportout = VectorDataIn
        self.addParameter(self, "reportin", VIBe2.VECTORDATA_IN)
        self.addParameter(self, "reportout", VIBe2.VECTORDATA_OUT)
    
    def run(self):
        rand.seed()
        #Link input vectors with local variables
        lot_opps = self.lot_opps.getItem()
        street_opps = self.street_opps.getItem()
        neigh_opps = self.neigh_opps.getItem()
        prec_opps = self.prec_opps.getItem()
        blockcityin = self.blockcityin.getItem()
        patchcityin = self.patchcityin.getItem()
        patchcityout = self.patchcityout.getItem()
        designdetails = self.designdetails.getItem()
        blockcityout = self.blockcityout.getItem()
        systemsout = self.systemsout.getItem()
        
        map_attr = blockcityin.getAttributes("MapAttributes")
        des_attr = designdetails.getAttributes("DesignAttributes")
        
        #Open a file to write output to
        output_file = open("UBEATS_BlockStrategies.csv", 'w')
        output_file.write("UrbanBEATS Block Strategies Evaluation File\n\n")
        output_file.write("BlockID, Strategy No., Total Imp Served, Deg. Lot, Deg. Street, Deg. Neigh, Lot Tech, Scale, Size [sqm], AServed [sqm], Street Tech, Scale, Size [sqm], AServed [sqm], Neigh Tech, Scale, Size [sqm], AServed [sqm], Tech Score, Env Score, Ecn Score, Soc Score, Tot Score,\n")
        
        #get data needed to being for loop analysis
        blocks_num = map_attr.getAttribute("NumBlocks")     #number of blocks to loop through
        blocks_size = map_attr.getAttribute("BlockSize")    #size of block
        map_w = map_attr.getAttribute("WidthBlocks")        #num of blocks wide
        map_h = map_attr.getAttribute("HeightBlocks")       #num of blocks tall
        input_res = map_attr.getAttribute("InputReso")      #resolution of input data
        basins = map_attr.getAttribute("TotalBasins")       #total number of basins in map
            
        #Get increment values and work out vector of degrees
        lot_increment = des_attr.getAttribute("lot_increment")
        street_increment = des_attr.getAttribute("street_increment")
        neigh_increment = des_attr.getAttribute("neigh_increment")
        prec_increment = des_attr.getAttribute("prec_increment")
        basin_target_min = des_attr.getAttribute("basin_target_min")/100
        basin_target_max = des_attr.getAttribute("basin_target_max")/100
        
        lot_alts = [0]
        for i in range(int(lot_increment)):
            lot_alts.append(float(1/lot_increment*(i+1)))
        
        street_alts = [0]
        for i in range(int(street_increment)):
            street_alts.append(float(1/street_increment*(i+1)))
        
        neigh_alts = [0]
        for i in range(int(neigh_increment)):
            neigh_alts.append(float(1/neigh_increment*(i+1)))
        
        prec_alts = [0]
        for i in range(int(prec_increment)):
            prec_alts.append(float(1/prec_increment*(i+1))*basin_target_min)
        for i in range(int(prec_increment)):
            deg = float(1/prec_increment*(i+1))*basin_target_max
            if deg in prec_alts:
                continue
            else:
                prec_alts.append(deg)
        print "Prec_ALTS:", prec_alts
        
        #get the number of bins for the blocks, based on prec-alts and reverse it to match prec_alts
        block_bins = []
        for i in range(len(prec_alts)-1):
            block_bins.append([prec_alts[i]])
        block_bins.sort(reverse=True)
        print "==============="
        print block_bins
        print "==============="
        
        #---------------------------------------------------------------------------------#
        # Get all MCA parameters relevant for performing scoring                          #
        #---------------------------------------------------------------------------------#
        if des_attr.getStringAttribute("scoringmatrix_default") == 1:
            score_type = 1      #uses UBeats matrix     (coming soon)
            mca_fname = "default"
            mca_allcrit = des_attr.getAttribute("scoring_include_all")
        else:
            score_type = 0      #uses custom matrix
            mca_fname = des_attr.getStringAttribute("scoringmatrix_path")
            mca_techN = des_attr.getAttribute("bottomlines_tech_n")                 #number of criteria involved (if not "default" score type)
            mca_envN = des_attr.getAttribute("bottomlines_env_n")
            mca_ecnN = des_attr.getAttribute("bottomlines_ecn_n")
            mca_socN = des_attr.getAttribute("bottomlines_soc_n")
            
        mca_tech = des_attr.getAttribute("bottomlines_tech")                    #Booleans to include criteria
        mca_env = des_attr.getAttribute("bottomlines_env")
        mca_ecn = des_attr.getAttribute("bottomlines_ecn")
        mca_soc = des_attr.getAttribute("bottomlines_soc")
        
        mca_techW = des_attr.getAttribute("bottomlines_tech_w")                 #weightings of different criteria
        mca_envW = des_attr.getAttribute("bottomlines_env_w")
        mca_ecnW = des_attr.getAttribute("bottomlines_ecn_w")
        mca_socW = des_attr.getAttribute("bottomlines_soc_w")
        
        mca_techP = des_attr.getAttribute("bottomlines_tech_p")                 #pareto exploration mode increments
        mca_envP = des_attr.getAttribute("bottomlines_env_p")
        mca_ecnP = des_attr.getAttribute("bottomlines_ecn_p")
        mca_socP = des_attr.getAttribute("bottomlines_soc_p")
        
        mca_stoch = des_attr.getAttribute("scope_stoch")
        mca_method = des_attr.getStringAttribute("score_method")
        mca_t2s = des_attr.getStringAttribute("tech2strat_method")
        
        mca_topranklimit = des_attr.getAttribute("topranklimit")                #limit ranking to the top x where x is the topranklimit
        mca_confint = des_attr.getAttribute("conf_int")/100                     #confidence interval converted to proportion
        mca_ingroupscore = des_attr.getStringAttribute("ingroup_sorting")
        
        #---------------------------------------------------------------------------------#
        # Get MCA Scoring Matrix and transfer into local variable IF CUSTOM WAS CLICKED   #
        #---------------------------------------------------------------------------------#
        mca_scoring_matrix = []
        mca_techindex = []
        mca_scoring_tech = []           #scoring_matrix transfers tech criteria into this 
        mca_scoring_env = []            #as above with env criteria
        mca_scoring_ecn = []            #as above with ecn criteria
        mca_scoring_soc = []            #as above with soc criteria
        mca_fname = des_attr.getStringAttribute("scoringmatrix_path")
        
        eval_mode = des_attr.getStringAttribute("eval_mode")
        ranktype = des_attr.getStringAttribute("ranktype")                      #CI = confidence interval, RK = top ranking
        print "MCA Evaluation Mode: "+str(eval_mode)+" and Rank Type: "+str(ranktype)
        
        #open file and get information from it
        f = open(str(mca_fname), 'r')
        for lines in f:
            readingline = lines.split(',')
            mca_scoring_matrix.append(readingline)
        f.close()
        total_criteria = len(mca_scoring_matrix[0])-1
        total_tech = len(mca_scoring_matrix)-1
        
        #fill out tech crits
        for lines in range(len(mca_scoring_matrix)):
            mca_techindex.append(mca_scoring_matrix[lines][0])
            mca_scoring_tech.append(mca_scoring_matrix[lines][1:int(1+mca_techN)])
            mca_scoring_env.append(mca_scoring_matrix[lines][int(mca_techN+1):int(mca_techN+mca_envN+1)])
            mca_scoring_ecn.append(mca_scoring_matrix[lines][int(mca_techN+mca_envN+1):int(mca_techN+mca_envN+mca_ecnN+1)])
            mca_scoring_soc.append(mca_scoring_matrix[lines][int(mca_techN+mca_envN+mca_ecnN+1):int(mca_techN+mca_envN+mca_ecnN+mca_socN+1)])
        
        for f in range(len(mca_scoring_tech)):                  #TECHNICAL CRITERION --------#
            for g in range(len(mca_scoring_tech[0])):
                if f == 0:
                    pass
                else:
                    mca_scoring_tech[f][g] = float(mca_scoring_tech[f][g])
        if mca_tech == 0:
            mca_scoring_tech = 0
            mca_techW = 0
            
        for f in range(len(mca_scoring_env)):                   #ENVIRONMENTAL CRITERION --------#
            for g in range(len(mca_scoring_env[0])):
                if f == 0:
                    pass
                else:
                    mca_scoring_env[f][g] = float(mca_scoring_env[f][g])
        if mca_env == 0:
            mca_scoring_env = 0
            mca_envW = 0
            
        for f in range(len(mca_scoring_ecn)):                   #ECONOMICS CRITERION --------#
            for g in range(len(mca_scoring_ecn[0])):
                if f == 0:
                    pass
                else:
                    mca_scoring_ecn[f][g] = float(mca_scoring_ecn[f][g])
        if mca_ecn == 0:
            mca_scoring_ecn = 0
            mca_ecnW = 0
            
        for f in range(len(mca_scoring_soc)):                   #SOCIAL CRITERION ----------#
            for g in range(len(mca_scoring_soc[0])):
                if f == 0:
                    pass
                else:
                    mca_scoring_soc[f][g] = float(mca_scoring_soc[f][g])
        if mca_soc == 0:
            mca_scoring_soc = 0
            mca_socW = 0
            
        #print mca_techindex                           
        #print mca_scoring_tech
        #print mca_scoring_env
        #print mca_scoring_ecn
        #print mca_scoring_soc
        
        #---------------------------------------------------------------------------------#
        # TIME TO LOOP OVER THE COLLECTION OF BLOCKS AND PIECE STRATS TOGETHER (IN-BLOCK) #
        #---------------------------------------------------------------------------------#
        #Initialize arrays to hold in-block strategy objects
        block_strategies_matrix = []                    #holds a collection of arrays consisting of the Strategies for EACH BLOCK. Index 0 = Block ID1, to Index n-1 = Block IDn
        region_bin_scores = []                          #holds a collection of arrays consisting of the bin scores for EACH BLOCK.      
        
        for i in range(int(blocks_num)):                #loops over all Blocks, in each block, need to loop over all strategies
            currentID = i+1                             #current Block ID
            stratID = 0                                 #current strategy ID (for the output file mainly)
            currentAttList = blockcityin.getAttributes("BlockID"+str(currentID))        #attribute list of current block structure
            
            #Grab geometric info and attributes for Blocks, networks and patches for transfer later on to output
            plist = blockcityin.getPoints("BlockID"+str(currentID))
            flist = blockcityin.getFaces("BlockID"+str(currentID))
            pnetlist = blockcityin.getPoints("NetworkID"+str(currentID))
            enetlist = blockcityin.getEdges("NetworkID"+str(currentID))
            network_attr = blockcityin.getAttributes("NetworkID"+str(currentID))
            currentPatchList = patchcityin.getAttributes("PatchDataID"+str(currentID))
            
            #-----------------------------------------------------------------#
            #        DETERMINE WHETHER TO UPDATE CURRENT BLOCK AT ALL         #
            #-----------------------------------------------------------------#
            
            block_status = currentAttList.getAttribute("Status")
            if block_status == 0 or currentAttList.getAttribute("ResTIArea") == 0:
                print "BlockID"+str(currentID)+" is not active in simulation or has no residential area"
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
                
                block_strategies_matrix.append([])      #if block Status = 0, then no strategies, but need the empty array in the index
                region_bin_scores.append([])            #no score because no strategy
                
                #skips the for loop iteration to the next block, not more needs to be done
                continue
            
            #--- GET SOME BLOCK INFORMATION -------#
            print "Block ID: "+str(currentID)
            allotments = currentAttList.getAttribute("ResAllots")
            totalimparea = currentAttList.getAttribute("ResTIArea")
            
            #--STEP 1-- Get the attribute lists for different strategies -----------------#
            lot_strats = lot_opps.getAttributes("BlockID"+str(currentID)+"_Lot")
            street_strats = street_opps.getAttributes("BlockID"+str(currentID)+"_Street")
            neigh_strats = neigh_opps.getAttributes("BlockID"+str(currentID)+"_Neigh")
            
            lot_options = lot_strats.getAttribute("TotalLotOptions")
            street_totcombos = street_strats.getAttribute("TotalCombinations")
            neigh_totcombos = neigh_strats.getAttribute("TotalCombinations")
            
            #print "Total Street Combos: "+str(street_totcombos)
            #print "Total Neighbourhood Combos: "+str(neigh_totcombos)
            
            #--STEP 2-- Setup Vectors containing ALL WSUD OBJECTS ---------------------#
            #tech_array_<scale> = [WSUD object]
            tech_array_lot = []         #all lot options
            tech_array_street = []      #all street options in all possible degrees, 3D Array, each Column holds one street_deg list
            tech_array_neigh = []       #all neigh options in all possible degrees, 
            
            ### >>>>>> FILL OUT TECH_ARRAY_LOT >>>>>>                                                   #COMMENT ON USE OF CLASS TECHNOLOGY
            for a in range(int(lot_options)):                                                           #each element in tech_array contains one
                currentoption = lot_strats.getStringAttribute("LotOption_"+str(a+1))                    #WSUD Object as written in technology.py
                currentoption = currentoption.split(',')                                                #it has several attributes that can be
                currentoption.remove('')                                                                #accessed simply by typing the following:
                tech_array_lot.append(tech.WSUD(currentoption[0], currentoption[1], 'sqm', 'L', currentoption[2]))    #   tech_array[index].function()
            
            #COMMENT NOTES -----------------------------------------------------------------------------------------------------------------------------------------
            #
            #fill out street tech array based on lot_deg and street_deg
            #(e.g. lot_deg = 0, 0.25, 0.5, 0.75, 1.0 and neigh_deg = 0.25, 0.5, 0.75, 1.0 the Total Combos = 20)
            #3D Array: tech_array_neigh[lot_degree][neigh_degree][combination] written as
            #     Lot Deg   0                         0.25                      0.5                      0.75                     1.00
            #   Neigh Deg   0.25, 0.50, 0.75, 1.00    0.25, 0.50, 0.75, 1.00    0.25, 0.50, 0.75, 1.00   0.25, 0.50, 0.75, 1.00   0.25, 0.50, 0.75, 1.0
            #               [...] [...] [...] [...]     becomes [[[option1, option2, etc.]],[[option1, option2, etc.]],[[option1, option2, etc.]]]
            #
            #Loop through all degrees of implementation and search out the correct one for each, creating a list each time
            #Total options of strategies available is calculated across each scale e.g.
            #           2 Lot scale, 2 street scale, 3 neighbourhood scale at one degree of implementation
            #           = 2+1 x 2+1 x 3+1 = 36 strategies (1 = not to use option at all) 
            #           1L 1S 1N, 1L 1S 2N, 1L 1S 3N    2L 1S, 1N       etc.
            #           1L 2S 1N, 1L 2S 2N, 1L 2S 3N    2L 2S, 1N       etc.
            #Need to check the current combination if it is realistic before coming up with strategies, e.g.
            #           if lot_deg = 0.25, street_deg = 0.25, neigh_deg = 0.25 --> check OK!
            #           if lot_deg = 0.25, street)deg = 0.25, neigh_deg = 1.00 --> check NOT OK! SKIP (neigh_deg + street_deg <= 1)
            #
            #NOTE: NEED TO CHECK HOW IF NO COMBINATIONS ARE IN NEIGHBOURHOOD SCALE TO DEAL WITH THE MAKING OF STRATEGIES
            #
            # --------------------------------------------------------------------------------------------------------------------------------------------------------
            
            ### >>>>>> FILL OUT TECH_ARRAY_STREET >>>>>>        (based on lot_alts)
            for a in range(len(lot_alts)):
                tech_array_street.append([])    #append one group for each lot_deg
                lot_deg = lot_alts[a]
                for b in range(len(street_alts)):     #begin looping from 0.25, not from zero
                    tech_array_street[a].append([])        #append one group for each street_deg
                    street_deg = street_alts[b]       #loop from offset index + 1
                    if street_deg == 0:
                        tech_array_street[a][b].append(0)               #CONDITION - NO DEGREE = APPEND ZERO
                        continue
                    street_strats_combo = street_opps.getAttributes("BlockID"+str(currentID)+"_Street_"+str(lot_deg)+"_"+str(street_deg))
                    street_options = street_strats_combo.getAttribute("TotalOptions")
                    for c in range(int(street_options)):
                        currentoption = street_strats_combo.getStringAttribute("StreetOption_"+str(c+1))
                        currentoption = currentoption.split(',')
                        currentoption.remove('')
                        tech_array_street[a][b].append(tech.WSUD(currentoption[0],currentoption[1], 'sqm', 'S', currentoption[2]))
            
            ### >>>>>> FILL OUT TECH_ARRAY_NEIGH >>>>>>    (based on lot_deg and neigh_deg)   
            for a in range(len(lot_alts)):
                tech_array_neigh.append([])
                lot_deg = lot_alts[a]
                for b in range(len(neigh_alts)):
                    tech_array_neigh[a].append([])
                    neigh_deg = neigh_alts[b]
                    if neigh_deg == 0:
                        tech_array_neigh[a][b].append(0)                #CONDITION - NO DEGREE = APPEND ZERO
                        continue
                    neigh_strats_combo = neigh_opps.getAttributes("BlockID"+str(currentID)+"_Neigh_"+str(lot_deg)+"_"+str(neigh_deg))
                    neigh_options = neigh_strats_combo.getAttribute("TotalOptions")
                    for c in range(int(neigh_options)):
                        currentoption = neigh_strats_combo.getStringAttribute("NeighOption_"+str(c+1))
                        currentoption = currentoption.split(',')
                        currentoption.remove('')
                        tech_array_neigh[a][b].append(tech.WSUD(currentoption[0],currentoption[1],'sqm', 'N', currentoption[2]))
            
            
            #--STEP 3-- Piece together Strategy Objects using WSUD Object Vectors ----#
            strategies_collection = []
            strategies = []
            combo_counter = 0
            for a in range(len(lot_alts)):                      #LOOP OVER LOTS e.g. [0, 0.25, 0.5, 0.75, 1.0]
                lot_deg = lot_alts[a]
                
                for b in range(len(street_alts)):               #LOOP OVER STREETS e.g. [0, 0.25, 0.5, 0.75, 1.0]
                    street_deg = street_alts[b]
                    if street_deg > 0 and street_totcombos == 0:        #CONDITION 1: if there is supposed to be street system, but no options, skip
                        continue
                    
                    for c in range(len(neigh_alts)):            #LOOP OVER NEIGHBOURHOODS e.g. [0, 0.25, 0.5, 0.75, 1.0]
                        neigh_deg = neigh_alts[c]
                        if street_deg + neigh_deg > 1:                  #CONDITION 2: if proportions of street-neigh add up to more than 100%, skip
                            continue    #skip combo
                        if neigh_deg > 0 and neigh_totcombos == 0:      #CONDITION 3: if there is supposed to be neigh system, but no options, skip
                            continue    #skip combo as well
                        current_combo = [lot_deg, street_deg, neigh_deg]
                        
                        if lot_deg == 0:
                            array_lot = [0]                     #CONDITION - NO DEGREE = APPEND ZERO in LOT MATRIX
                        else:
                            array_lot = tech_array_lot
                            
                        for d in array_lot:                             #LOOP OVER LOT OPTIONS (WSUD OBJECTS)
                            for e in tech_array_street[a][b]:           #LOOP OVER STREET OPTIONS (WSUD OBJECTS)
                                for f in tech_array_neigh[a][c]:        #LOOP OVER NEIGH OPTIONS(WSUD OBJECTS)
                                    stratID += 1
                                    
                                    #create the strategy object         [d,e,f] represents a vector of three systems at three scales
                                    currentstrategy = tech.BlockStrategy(current_combo, [d, e, f], allotments, totalimparea)
                                    currentstrategy.checkTechnologies() #the following function performs a check and makes sure that the object is in order
                                    
                                    #--STEP 4-- SCORE EACH STRATEGY ACCORDING TO MCA TO GET THE STRATEGY.MCASCORE PROPERTY ----#
                                    #bear in mind:      how techs add up to strategy score - option
                                                    #   weightings of criteria
                                                    #   tally method (use WSM for now)
                                                    #   include stochastic noise?
                                    
                                    #CALCULATE SCORES FOR THE TECHNOLOGIES INDIVIDUALLY AND ADD UP FOR THE DIFFERENT CRITERIA
                                    currentstrategy.calcTechScores(mca_techindex, mca_scoring_tech, mca_scoring_env, mca_scoring_ecn, mca_scoring_soc, mca_t2s)
                                    
                                    #TALLY UP THE FINAL MCA SCORE ACROSS CRITERIA USING THE WEIGHTINGS DEPENDING ON EVALUATION MODE
                                    if eval_mode == "W":
                                        currentstrategy.calcStratScoreSingle(mca_method, mca_stoch, mca_techW, mca_envW, mca_ecnW, mca_socW)
                                    elif eval_mode == "P":
                                        currentstrategy.calcStratScorePareto(mca_method, mca_techP, mca_envP, mca_ecnP, mca_socP)
                                        
                                    #each strategy now has updated MCA scores
                                    
                                    #create the list of strategies for current block so you can rank them later on
                                    strategies_collection.append([currentstrategy.getMCAtotscore(), currentstrategy.reportStrategy()])
                                    strategies.append(currentstrategy)
                                    
                                    #Write the line to the output-file table
                                    output_file.write(str(currentID)+","+str(stratID)+","+str(currentstrategy.getTotalImpServed())+","+currentstrategy.writeReportCombo()+currentstrategy.writeReportSystems()+currentstrategy.writeReportScores()+"\n")
                                    
                        combo_counter += 1
            
            #print strategies_collection
            print "Total Combinations: "+str(len(strategies_collection))            
            
            
            #--STEP 5a-- SORT INTO BINS ----#
            strategy_bins = []  #array holds x sub-arrays, where x is the number of prec_alts - 1 e.g. if prec_alts = [0, 0.5, 1], then bins = [1, >0.5, >0]
            strategy_bins_score = []                    #holds the avg/med/min/max score of the bin
            strategy_as = []
            for bins in range(len(prec_alts)):          #sets up the matrix
                strategy_bins.append([])                #first one is [[prec = 0], [prec = 0.5],etc.]
                strategy_bins_score.append([])         
                strategy_as.append([])
            #sort strategies into bins, depending on the total area serviced
            for a in strategies:
                #check for each [0, 0.5, etc.], i.e. first it's if it's under 1-0 but above 1-0.5, then under 1-0.5, but above 1-1
                prec_index = 0
                bin_found = 0
                
                #COMMENT NOTES --------------------------------------------------------------------------------------------------
                #e.g. [0, 0.25, 0.5, 0.75, 1.0], a.getTotalImpServed() = 0.18 i.e. block treats 18% of imp area
                #       Iteration 1: index = 0 ==> 0.18 smaller than 1-0=1 but not bigger than 1-0.25=0.75
                #       Iteration 2: index = 1 ==> 0.18 smaller than 1-0.25=0.75 but not bigger than 1-0.5=0.5
                #       Iteration 3: index = 2 ==> 0.18 smaller than 1-0.5=0.5 but not bigger than 1-0.75 = 0.25
                #       Iteration 4: index = 3 ==> 0.18 smaller than 1-0.25 and bigger than 1-1 = 0, hence bin_found = 1
                #       Add 0.18 to Index 3 in strategy_bins[3]: = [ =100%[] >=75%[] >=50%[] >=25%[0.18], >=0%[] ]
                #       index 1 means for precinct to treat nothing 0%, we have block strategies that treat 100%
                #       index 2 means for precinct to treat 25%, we have block strategies that treat 75% and above
                #if exactly 100%, add to position 0 of bins
                # ----------------------------------------------------------------------------------------------------------------
                
                #THE FOLLOWING SORTS THE STRATEGY INTO A BIN - FOR ONLY ONE STRATEGY AS THE OUTER LOOP CONTINUES THROUGH THE LIST
                if a.getTotalImpServed() == 1.0:        #if the total imp served is exactly 100% then add it to the 0th prec_index
                    strategy_bins[prec_index].append([a.getMCAtotscore(), a])
                    strategy_as[prec_index].append(a.getTotalImpServed())
                    bin_found = 1
                else:
                    prec_index += 1             #otherwise increase index by 1 and go into while loop
                while bin_found == 0:           #if 100% found, then can continue, else stop
                    if a.getTotalImpServed() >= (1-prec_alts[prec_index]):    #if it were 100% it would have been caught earlier
                        strategy_bins[prec_index].append([a.getMCAtotscore(), a])
                        strategy_as[prec_index].append(a.getTotalImpServed())
                        bin_found = 1
                    else:
                        prec_index += 1
            print strategy_as
            
            #--STEP 5b-- GET TOP RANKS ----#
            if eval_mode == "W":                #SINGLE WEIGHTED RESULT
                for a in range(len(strategy_bins)):
                    #print strategy_bins[a]
                    strategy_bins[a].sort(reverse=True) #Reverse sort the bin
                    #print strategy_bins[a]
                    
                    if ranktype == "RK":        #CODE FOR RANKING THE OPTIONS BASED ON TOP X RANKING
                        if mca_topranklimit < len(strategy_bins[a]):
                            strategy_bins[a] = strategy_bins[a][0:int(mca_topranklimit)]
                    elif ranktype == "CI":      #CODE FOR RANKING THE OPTIONS BASED ON PERCENTILE, CONFIDENCE INTERVALS
                        if len(strategy_bins[a]) == 0:
                            strategy_bins[a].append([-999,None])              ###>>>>>>>>>>>>>>>>>>NOTE INPUT POINT: MAY APPEND OBJECT IN FUTURE in index [1]
#                            top_score = 0
#                            bottom_limit = 0
                            print "Current Bin has no strategies"
#                            strategy_bins[a] = strategy_bins[a]
                        else:
                            top_score = strategy_bins[a][0][0]
                            print "Top Score: "+str(top_score)
                            bottom_limit = top_score * mca_confint
                            print "Bottom Limit: "+str(bottom_limit)
                            corres_rank = 0
                            for findrank in range(len(strategy_bins[a])):
                                if strategy_bins[a][findrank][0] > bottom_limit:
                                    corres_rank += 1
                            print "Corresponding Number of Options: "+str(corres_rank)
                            if top_score != 0:
                                strategy_bins[a] = strategy_bins[a][0:int(corres_rank)]
                            else:
                                pass
                    else:
                        print "Error, cannot find corresponding rank type"
                        
                    print "bin no.: "+str(a)+ "--------------------"
                    print strategy_bins[a]   
                
                block_strategies_matrix.append(strategy_bins)                #put the final bunch of in-block strategies into master array
                
            elif eval_mode == "P":              #PARETO EXPLORATION MODE
                #If Pareto Exploration Mode, then ranking does not count
                #Simply write the strategies to the matrix
                pass
            
            #--STEP 5c-- GET BIN SCORES ----#
            #Grab the individual scores in each bin from the matrix
            for a in range(len(strategy_bins)):
                for b in range(len(strategy_bins[a])):
                    strategy_bins_score[a].append(strategy_bins[a][b][0])
            #print strategy_bins_score
            
            if des_attr.getStringAttribute("ingroup_scoring") == "Avg":
                for a in range(len(strategy_bins_score)):
                    if strategy_bins_score[a] != -999:
                        strategy_bins_score[a] = np.average(strategy_bins_score[a])
            elif des_attr.getStringAttribute("ingroup_scoring") == "Med":
                for a in range(len(strategy_bins_score)):
                    if strategy_bins_score[a] != -999:
                        strategy_bins_score[a] = np.median(strategy_bins_score[a])
            elif des_attr.getStringAttribute("ingroup_scoring") == "Min":
                for a in range(len(strategy_bins_score)):
                    if strategy_bins_score[a] != -999:
                        strategy_bins_score[a] = np.min(strategy_bins_score[a])
            elif des_attr.getStringAttribute("ingroup_scoring") == "Max":
                for a in range(len(strategy_bins_score)):
                    if strategy_bins_score[a] != -999:
                        strategy_bins_score[a] = np.max(strategy_bins_score[a])
            region_bin_scores.append(strategy_bins_score)
            
            print "Strategy_bins_score --------------------------------------"
            print strategy_bins_score
            print "----------------------------------------------------------"
            
            #---------------------------------------------------------------------------------#
            #            WRITE OUTPUTS TO VECTOR FILE FOR NOW TO END THE LOOP                 #
            #---------------------------------------------------------------------------------#
            blockcityout.setPoints("BlockID"+str(currentID),plist)
            blockcityout.setFaces("BlockID"+str(currentID),flist)
            blockcityout.setAttributes("BlockID"+str(currentID),currentAttList)
            
            blockcityout.setPoints("NetworkID"+str(currentID), pnetlist)
            blockcityout.setEdges("NetworkID"+str(currentID), enetlist)
            blockcityout.setAttributes("NetworkID"+str(currentID), network_attr)
            
            patchcityout.setPoints("PatchDataID"+str(currentID), plist)
            patchcityout.setFaces("PatchDataID"+str(currentID),flist)
            patchcityout.setAttributes("PatchDataID"+str(currentID), currentPatchList)
            
            #IN-BLOCK FOR LOOP END (Repeat for next BlockID)
            
        #NEXT FOR LOOP TO CHECK PRECINCT STRATEGIES
            
            #BASE INDENTATION FOR WITHIN LOOPING ACROSS BLOCKS FOR LOOP
        
        #Footer line for first output table
        output_file.write("End of Strategy List \n\n")
        
        #print block_strategies_matrix
        #debugging
        print "Length of the Master Matrix"
        print len(block_strategies_matrix)
        print len(region_bin_scores)
        print "Master Score List"
        print region_bin_scores
        
        #Prepare header and title for top rank table
        output_file.write("List of Top Block Strategies\n\n")
        #Code to write out the same as earlier, just with the top block strategies now 
        output_file.write("BlockID, Bin Type, Strategy No., Total Imp Served [sqm], Deg. Lot, Deg. Street, Deg. Neigh, Lot Tech, Scale, Size [sqm], AServed [sqm], Street Tech, Scale, Size [sqm], AServed [sqm], Neigh Tech, Scale, Size [sqm], AServed [sqm], Tech Score, Env Score, Ecn Score, Soc Score, Tot Score,\n")
            
        #loop over block_strategies_matrix[ID][bin][strategy][property]    
        for i in range(len(block_strategies_matrix)):                   #loop over blocks
            currentBlockID = i+1
            if len(block_strategies_matrix[i]) == 0:                #if no bins were assigned, skip
                output_file.write(str(currentBlockID)+","+"no strategies"+"\n")
            for j in range(len(block_strategies_matrix[i])):            #loop over bin groups           BLOCKS_STRATEGIES_MATRIX[blockID][bin][#][property]
                if len(block_strategies_matrix[i]) == 0:
                    currentBin = 0
                else:
                    currentBin = prec_alts[len(block_strategies_matrix[i])-1-j]
                stratID = 0 
                for k in range(len(block_strategies_matrix[i][j])):     #loop over list of strategies in bin
                    curstrobj = block_strategies_matrix[i][j][k][1]     #current strategy object - gets the exact object out of the matrix so that the functions can be used
                    if curstrobj == None:          #if that object is literally the number zero (then it is NO object, hence continue)
                        continue
                    stratID += 1
                    output_file.write(str(currentBlockID)+","+str(currentBin)+","+str(stratID)+","+str(curstrobj.getTotalImpServed())+","+curstrobj.writeReportCombo()+curstrobj.writeReportSystems()+curstrobj.writeReportScores()+"\n")
        output_file.write("End of Block Bins Log\n\n")        
        output_file.close()
        #Debug Printing Of Block Strategies Matrix        
#        for i in range(len(block_strategies_matrix)):
#            print "Block: "+str(i+1)
#            for j in range(len(block_strategies_matrix[i])):
#                print "Increment Change"
#                print len(block_strategies_matrix[i][j])
#                print block_strategies_matrix[i][j]

        ###########################################
        ## CHECKPOINT                            ##
        ###########################################################################################
        #
        # - A matrix block_strategies_matrix of top ranking block strategies for each block
        # - We have prec_alts available
        # - We know what the basin treatment goal is
        # - We have a list of prec_opps for each block at prec_alts
        # - 
        #
        ###########################################################################################
        
        #--STEP 6-- SCORE THE PRECINCT STRATEGIES ----#
        basin_strategies_collection = []
        basin_strategies_scores = []        
        #its length equal to number of basins e.g. [ []100% block, []25%p-75%b, []50%p-50%b, []75%p-25%b, []100% precinct] ]
        for i in prec_alts:             #this "collection array" has number of columns equal to number of prec_alts, in there contains all strategies
            basin_strategies_collection.append([])
            basin_strategies_scores.append([])
        
        #create second output file for basins
        output_file = open("UB_BasinStrategies.csv", 'w')
        output_file.write("UrbanBEATS Basin Strategies Evaluation File\n\n")
        output_file.write("List of All Basin Strategies\n\n")
        output_file.write("Basin ID, Strategy No., Service [%], TotalMCAScore, # Precinct, # Blocks Local\n")
        
        basin_strategy_groups = []              #will contain the final chosen strategy for each basin
        for i in range(int(basins)):
            currentID = i+1     #current Basin ID
            stratID = 0         #counter for strategies in the basin
            
            #Get Basin Attributes List
            print "Current Basin ID"+str(currentID)
            basin_attr = blockcityin.getAttributes("BasinID"+str(currentID))
            
            #get basin blocks list
            upstr = basin_attr.getStringAttribute("UpStr")
            basinblockIDs = upstr.split(',')
            basinblockIDs.remove('')
            for j in range(len(basinblockIDs)):
                basinblockIDs[j] = int(basinblockIDs[j])
                
            print basinblockIDs
            print len(basinblockIDs)
            
            #LOOP OVER THE UPSTREAM IDs of the Basin first and see which of the IDs can accommodate precinct-scale technologies
            #Find the blocks in the basin that can fit a precinct system (so we can Monte Carlo them later)
            prec_blocks_partakeIDs = []         #holds all IDs that can fit precinct scale systems
            for currentBlockID in basinblockIDs:
                total_options = 0               #counter for options
                currentblock_opps = prec_opps.getAttributes("BlockID"+str(currentBlockID)+"_Prec")
                print "Current Block ID"+str(currentBlockID)
                
                #SKIP CONDITION #1: no combinations for block, i.e. "TotalCombinations" == 0
                if currentblock_opps.getAttribute("TotalCombinations") == 0:
                    print "No precinct options available for Block ID"+str(currentBlockID)
                    continue
                
                #SKIP CONDITION #2: inside each degree (prec_deg) Total Options for that degree == 0
                for prec_deg in prec_alts:
                    prec_strats_combo = prec_opps.getAttributes("BlockID"+str(currentBlockID)+"_Prec_"+str(prec_deg))
                    if prec_strats_combo.getAttribute("TotalOptions") == 0:
                        print "No precinct options available for BlockID"+str(currentBlockID)+" at prec deg: "+str(prec_deg)
                        continue
                    else:
                        total_options += prec_strats_combo.getAttribute("TotalOptions")
                print "BlockID"+str(currentBlockID)+" total options: "+str(total_options)
                if total_options == 0:
                    print "No precinct options available for BlockID"+str(currentBlockID)
                    continue
                else:
                    prec_blocks_partakeIDs.append(currentBlockID)
                
            print "Total Blocks able to fit Precinct Scale Techs: "+str(len(prec_blocks_partakeIDs))
            print prec_blocks_partakeIDs
                
            print "end of line for now"
            
            #CREATE ARRAY OF WSUD OBJECTS REPRESENTING PRECINCT-SCALE SYSTEMS
            prec_technologies_list = [] #will hold all WSUD objects for prec technologies length is dependent on len(prec_blocks_partakeIDs)
            partake_index = 0
            
            for currentBlockID in prec_blocks_partakeIDs:
                #tech_array prec gets appended to prec_technologies_list[partake_index]
                tech_array_prec = []        #holds one column for one degree = [ [options @0.25], [options @0.5], [options @0.75], [options @1.0] ]
                currentAttList = blockcityout.getAttributes("BlockID"+str(currentBlockID))       #get the Block's main info
                prec_strats = prec_opps.getAttributes("BlockID"+str(currentBlockID)+"_Prec")
                #prec_strats_combo will be gotten later
                
                #UPSTREAM IDs for block - get list and create array of integers
                upstreamString = currentAttList.getStringAttribute("BasinBlocks")
                upstreamIDs = upstreamString.split(',')
                upstreamIDs.remove('')
                for idnum in range(len(upstreamIDs)):
                    upstreamIDs[idnum] = int(upstreamIDs[idnum])
                if currentBlockID in upstreamIDs:
                    upstreamIDs.remove(currentBlockID)
                print "Upstream IDs for Block ID"+str(currentBlockID)
                print upstreamIDs
                tech_array_prec.append(len(upstreamIDs))
                tech_array_prec.append(currentBlockID)
                tech_array_prec.append(upstreamIDs)
                tech_array_prec.append([])      #for the bins of WSUD objects
                
                #DOWNSTREAM IDs for block - repeat
                downstreamString = currentAttList.getStringAttribute("BasinDownBlocks")
                downstreamIDs = downstreamString.split(',')
                downstreamIDs.remove('')
                for idnum in range(len(downstreamIDs)):
                    downstreamIDs[idnum] = int(downstreamIDs[idnum])
                print "Downstream IDs"
                print downstreamIDs
                
                index_counter = 0       #for tech_array_prec
                for prec_deg in prec_alts:
                    if prec_deg == 0:   #skip the 0th degree since we've done this earlier
                        tech_array_prec[3].append([])      #but adds an empty container to tech_array [options @ 0% = 0]
                        continue
                    index_counter += 1
                    tech_array_prec[3].append([])
                    print "Current Degree: "+str(prec_deg)
                    prec_strats_combo = prec_opps.getAttributes("BlockID"+str(currentBlockID)+"_Prec_"+str(prec_deg))
                    total_options = prec_strats_combo.getAttribute("TotalOptions")
                    if total_options == 0:
                        continue
                    print "Total options at "+str(prec_deg)+" are: "+str(total_options)
                    for opts in range(int(total_options)):
                        #get the current tech option at the current degree for the current block
                        optionstring = prec_strats_combo.getStringAttribute("PrecOption_"+str(opts+1))
                        currentoption = optionstring.split(',')
                        currentoption.remove('')
                        print currentoption
                        print "Prec_deg = "+str(prec_deg)
                        
                        #create the WSUD object
                        tech_object = tech.WSUD(currentoption[0],currentoption[1], 'sqm', 'P', currentoption[2])
                        tech_array_prec[3][index_counter].append(tech_object)
                
                prec_technologies_list.append(tech_array_prec)
                partake_index += 1    
            prec_technologies_list.sort()
            print prec_technologies_list
            
            #create the newly sorted prec_blocks_partakeIDs matrix
            prec_blocks_partakeIDs = []
            for j in range(len(prec_technologies_list)):
                prec_blocks_partakeIDs.append(prec_technologies_list[j][1])
            
            #print "Block Strategies_matrix"
#            block_strat_mam = []
#            for a in range(len(block_strategies_matrix)):
#                for b in range(len(block_strategies_matrix[a])):
#                    for c in range(len(block_strategies_matrix[a][b])):
#                        block_strategies_matrix[a][b][c] = block_strategies_matrix[a][b][c][1].reportStrategy()
                        
#            print block_strategies_matrix
#            print "Block Strategies_score"
#            print region_bin_scores
            
            #Get the total basin's imperviousness (and population for future versions)
            cumu_Aimp = 0
            for j in range(len(basinblockIDs)):
                currentblockID = basinblockIDs[j]
                cumu_Aimp += blockcityout.getAttributes("BlockID"+str(currentblockID)).getAttribute("ResTIArea")
            print "Total Basin Imperviousness: ", cumu_Aimp
            print prec_blocks_partakeIDs
            
        #########################################################################################################################
        # MONTE CARLO STRATEGY PIECING TOGETHER ALGORITHM
        #########################################################################################################################
  
            #Create the freq distribution and get CDF for both precinct and blocks
            #Define the distribution
            dist_prec = "Linear"
            eV = 1                      #lambda for the poisson distribution
            dist_block = "Linear"
            #-----------------------
            
            prec_N = len(prec_blocks_partakeIDs)+1
            print "Precinct N = ", prec_N
            if dist_prec == "Linear":
                prec_cdf = self.getSamplingCDFLinear(prec_N, 0, -1)
                print prec_cdf
            elif dist_prec == "Exponential":
                prec_cdf = self.getSamplingCDFExponential(prec_N, 2, 1)
                print prec_cdf
            elif dist_prec == "Poisson":
                prec_cdf = self.getSamplingCDFPoisson(prec_N, eV)
                print prec_cdf
                
            blocks_N = len(basinblockIDs)+1
            print "Block N = ", blocks_N
            if dist_block == "Linear":
                blocks_cdf = self.getSamplingCDFLinear(blocks_N, 0, -1)
                print blocks_cdf
            elif dist_block == "Exponential":
                blocks_cdf = self.getSamplingCDFExponential(blocks_N, 2, 1)
                print blocks_cdf
            
            
            #BEGIN MONTE CARLO LOOP
            basin_strategies_matrix = []
            for iterations in range(10):       #10 options, can be changed                                    <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< SET THE ITERATIONS FOR STRATEGY CONSTRUCTION <<<<<<<<<<<<<<<<<<
                print "Iteration No. ", iterations+1," -----------------------"
                
                #PART 1a - SETTING UP THE STORAGE CONTAINER OF INFORMATION
                #Create a basin strategy object
                #       - Has information on which blocks are in the basin
                #       - Has information about the basin's imperviousness, etc.
                #       - Has information about the precinct-scale systems and in-block strategies (containers first)
                
            
                #PART 1b - INITIALIZE TRACKING VARIABLES
                treat_remainAimp = cumu_Aimp      #remaining impervious area to be treated (will need to adjust this for overdesign)
                subbasin_ID_treatedAimp = []
                
                #-Variable: partakeIDs_copy-#
                #an identical array to prec_blocks_partakeIDs, except that it is used to find upstream basins
                #and to avoid double-up, is shortened in length by removing the already identified sub-basin block IDs 
                partakeIDs_copy = []
                partakeIDs_samplecopy = []              #sample copy is used for the sampling
                for pID in prec_blocks_partakeIDs:
                    partakeIDs_copy.append(pID)         #in every Monte Carlo Run it is "re-initiated"
                    subbasin_ID_treatedAimp.append(0)
                    partakeIDs_samplecopy.append(pID)
                #---------------------------------------------------
                basinblockIDs_samplecopy = []           #sample copy of all IDs in basin used for sampling later on
                for pID in basinblockIDs:
                    basinblockIDs_samplecopy.append(pID)
                
                #---------------------------------------------------------------
                #RANDOM SAMPLE PART A - DRAW A NUMBER OF IDs FROM PREC_BLOCK_PARTAKEIDS FOR PLACEMENT OF SYSTEMS
                
                #(1) draw the random number that represents the number of locations to implement
                prec_prob = rand.random()
                prec_sample_size = self.getSamplingCDFIndex(prec_cdf, prec_prob)
                #prec_sample_size = rand.randint(0, len(partakeIDs_samplecopy))         #Old Code: uniform distribution
                
                #(2) draw the x chosen samples from the pool
                prec_blocks_chosenIDs = []
                j = 0
                while j < prec_sample_size:
                    #get a random value, remove it from the one array, add it to the other
                    prec_sample_index = rand.randint(0, len(partakeIDs_samplecopy)-1)
                    prec_blocks_chosenIDs.append(partakeIDs_samplecopy[prec_sample_index])
                    partakeIDs_samplecopy.remove(partakeIDs_samplecopy[prec_sample_index])
                    j += 1
                print "=========================> PRECINCT SAMPLE", prec_blocks_chosenIDs
                partakeIDs_samplecopy = []      #remove the array for reinitiatilization later
                
                #---------------------------------------------------------------
                #RANDOM SAMPLE PART B - DRAW A NUMBER OF IDs FROM BASIN_BLOCKIDS FOR PLACEMENT OF IN-BLOCK SYSTEMS
                #(1) draw the random number that represents the number of locations to implement
                #maxinblock_samples = len(basinblockIDs) #if want to allow precinct and block systems in the same block
                maxinblock_samples = len(basinblockIDs) - len(prec_blocks_chosenIDs)    #cannot draw more blocks than what would be allowed
                inblocks_sample_size = 9999999                                          #set to some unrealistically high number
                while inblocks_sample_size > maxinblock_samples:                        #usually only needs to loop once, but could have issues if a lot of precinct blocks
                    blocks_prob = rand.random()
                    inblocks_sample_size = self.getSamplingCDFIndex(blocks_cdf, blocks_prob)
                print "inblock_sample_size: ", inblocks_sample_size
                #inblocks_sample_size = rand.randint(0, len(basinblockIDs)-len(prec_blocks_chosenIDs))          #Old Code: Uniform distribution
                
                #(2) draw the x chosen samples from the pool
                inblocks_chosenIDs = []
                j = 0
                while j < inblocks_sample_size:
                    print len(basinblockIDs_samplecopy) - 1
                    inblocks_sample_index = rand.randint(0, len(basinblockIDs_samplecopy)-1)
                    
                    if basinblockIDs_samplecopy[inblocks_sample_index] in prec_blocks_chosenIDs:
                        #CODE START - REMOVAL OF PRECINCT CONSTRAINT
                        #inblocks_chosenIDs.append(basinblockIDs_samplecopy[inblocks_sample_index])
                        #j += 1
                        #CODE END - REMOVAL OF PRECINCT CONSTRAINT
                        pass                #if the chosen blockID for a strategy already has been chosen for a precinct tech, skip
                    else:
                        inblocks_chosenIDs.append(basinblockIDs_samplecopy[inblocks_sample_index])
                        j += 1
                    basinblockIDs_samplecopy.remove(basinblockIDs_samplecopy[inblocks_sample_index])
                print "=========================> BLOCK SAMPLE", inblocks_chosenIDs
                basinblockIDs_samplecopy = []   #remove the array for reinitialization later
                
                #---------------------------------------------------------------
                #Create the object BasinManagementStrategy(No., currentID of basin, all block ids in basin, all precinct blocks partaking, total Aimp)
                current_bstrategy = tech.BasinManagementStrategy(iterations+1, currentID, basinblockIDs, prec_blocks_partakeIDs, cumu_Aimp)
                #---------------------------------------------------------------
                
                #PART 2 - LOOP THROUGH ALL THE PARTAKE IDs beginning at the upstream most
                for pID in range(len(prec_blocks_partakeIDs)):
                    currentblockID = prec_blocks_partakeIDs[pID]                #get currentID
                    upstreamIDs = prec_technologies_list[pID][2]                #get upstream IDs
                    
                    print "Block ID: ",currentblockID
                    print upstreamIDs
                    
                    #-Variable: remain_upstreamIDs-#
                    #an identical copy to upstreamIDs, but will have elements removed depending on subbasins
                    #as the model tracks through the basin, blocks that have been dealt with in subbasins will be removed so they're not doubled up
                    remain_upstreamIDs = []
                    for uID in upstreamIDs:
                        remain_upstreamIDs.append(uID)
                    #----------------------------------------------
                    
                    #CHECK IF THERE ARE OTHER SUB-BASINS UPSTREAM
                    subbasinIDs = []            #holds the IDs of upstream blocks                                            
                    for sbID in partakeIDs_copy:
                        if sbID in upstreamIDs:         #if a partake_ID is that that current block's list of upstream blocks
                            subbasinIDs.append(sbID)    #then add the ID to the vector for later on
                    if len(subbasinIDs) > 0:
                        print "There are sub basins upstream of this block!"
                        print subbasinIDs
                        for sbID in subbasinIDs:                    
                            partakeIDs_copy.remove(sbID)  #if the ID has been found to be immediately upstream, remove it from the copied list
                    else:
                        print "No sub basins upstream of this Block"
                    
                    #remove all the blocks in the sub-basins from remain_upstreamIDs to leave only those blocks in the current subbasin
                    for sbID in subbasinIDs:
                        remain_upstreamIDs.remove(sbID)     #remove the precinct block itself
                        index_num = prec_blocks_partakeIDs.index(sbID)
                        upstrID = prec_technologies_list[index_num][2]
                        for uID in upstrID:
                            remain_upstreamIDs.remove(uID)  #then remove that precinct's upstream blockIDs as well
                    print "Remaining Upstream Blocks to deal with: ", remain_upstreamIDs
                    #this matrix will represents the individual blocks not part of the sub-basin that we need to scan aside from subbasins
                    
                    #get the total impervious area of the sub-basin = currentID's imp + ResTIArea for all upstreamIDs
                    totalAimp_subbasin = blockcityout.getAttributes("BlockID"+str(currentblockID)).getAttribute("ResTIArea")
                    for sbID in upstreamIDs:
                        totalAimp_subbasin += blockcityout.getAttributes("BlockID"+str(sbID)).getAttribute("ResTIArea")
                    print "Total Sub-basin Impervious Area: ", totalAimp_subbasin
                    print "as proportion of overall imp Area: ", totalAimp_subbasin/cumu_Aimp*100, "%"
                    
                    #### Add this information to the basin_strategy Object ####
                    current_bstrategy.addSubBasinInfo(currentblockID,upstreamIDs,subbasinIDs,totalAimp_subbasin)
                    
                    #Work out the remaining impervious area to deal with and what maximum degree this corresponds to
                    upstream_treatedAimp = 0
                    for sbID in subbasinIDs:                #if there ARE subbasins, then need to tally up the treated Aimp and subtracted from total
                        index_num = prec_blocks_partakeIDs.index(sbID)      #gets the row_number
                        upstream_treatedAimp += subbasin_ID_treatedAimp[index_num]  #fetches the imp_treated and adds it to upstream_treatedAimp
                    subbasin_remainAimp = totalAimp_subbasin - upstream_treatedAimp     #Area to treat is total unless there is upstream treated
                    
                    max_degree = subbasin_remainAimp/totalAimp_subbasin         #use this line if you want to limit design and not allow overdesign
                    #max_degree = 1     #use this line if you want to not limit design and allow overdesign
                    
                    print "upstream area treated: ", upstream_treatedAimp
                    print "max degree: ", max_degree
                    print "Remaining Impervious Area to deal with (before): ", subbasin_remainAimp
                    
                    # ----------------------------------- # -------------------- #
                    # NOW PICK A PRECINCT SYSTEM RANDOMLY #                      #
                    # ----------------------------------- # -------------------- #
                    # Three different sampling procedures to determine if precinct should have a system:
                    #   (1) If a random number chosen is greater than the minimum basin target
                    #   (2) If a random number of 0 or 1 is chosen
                    #   (3) Both options
                    #   (4) If the initial sample of system has included this particular basin's ID
                    # COMMENTED OUT OLD CODE
                    # if rand.random() >= basin_target_min:       #design/choose a precinct tech IF the probability is less than target (e.g. 50% target = 50-50 chance)  
                    # if rand.randint(0,1) == 0 and rand.random() >= basin_target_min:
                    # if True:
                    #-----------------------------------------------------------
                    if currentblockID in prec_blocks_chosenIDs:         #if the ID is among those chosen previously, plan a system
                        #get the increments possible
                        indices = []
                        for deg in prec_alts:
                            if deg <= max_degree:
                                indices.append(deg)
                        if len(indices) == 0:
                            print "Avoid excessive design, skipping"
                            prec_alt_chosen = 0 #if skipped, then same as ZERO
                            choice = 0          #must set choice or else will be referenced before assignment
                            pass
                        else:
                            choice = rand.randint(0, len(indices)-1)
                            prec_alt_chosen = prec_alts[choice]
                            print "Chosen increment: ", prec_alt_chosen
                    else:
                        #no precinct system
                        print "Choice is zero, skipping"
                        prec_alt_chosen = 0
                        choice = 0
                        pass
                    
                    subbasin_treatedAimp = upstream_treatedAimp
                    additional_treatedAimp = 0  #tallies the additional treated impervious area
                    if len(prec_technologies_list[pID][3][choice]) == 0:
                        print "No options available at that increment, skipping"
                    else:
                        Nopt = len(prec_technologies_list[pID][3][choice])      #Nopt = NUMBER of options
                        print "Total Options available: ", len(prec_technologies_list[pID][3][choice])
                        additional_treatedAimp += prec_alt_chosen * subbasin_remainAimp
                        subbasin_remainAimp -= additional_treatedAimp
                        print "Remaining Impervious area to deal with (after prec): ", subbasin_remainAimp
                        
                        #choose a technology from the optinos
                        nchosen = rand.randint(0, Nopt - 1)     #nchosen = chosen position n in (Nopt-1)
                        chosen_obj = prec_technologies_list[pID][3][choice][nchosen]
                        print "Chosen System: ", chosen_obj.getType()
                        
                        #### Add this information to the basin_strategy Object ####
                        current_bstrategy.addPrecTechnology(currentblockID, prec_alt_chosen, chosen_obj)
                        
                    subbasin_treatedAimp += additional_treatedAimp
                    treat_remainAimp -= additional_treatedAimp
                    
                    # ------------------------------ #
                    # NOW DEAL WITH IN-BLOCK OPTIONS #
                    # ------------------------------ #
                    
                    total_blocks_contribution = 0                #reset
                    for rbID in remain_upstreamIDs:             #loop across the remaining IDs If there are none, loop won't start
                        #rbID is the current BlockID in the remaining ID list
                        print "Block ID: ", rbID
                        #get impervious area
                        block_Aimp = blockcityout.getAttributes("BlockID"+str(rbID)).getAttribute("ResTIArea")
                        print "Block Impervious Area: ", block_Aimp
                        if block_Aimp == 0:
                            print "No impervious area, therefore continuing"
                            continue
                        #get the maximum degree possible for this particular block
                        if subbasin_remainAimp > block_Aimp:
                            max_degree = 1.0
                        else:
                            max_degree = subbasin_remainAimp / block_Aimp      #if you want to limit overdesign
                            #max_degree = 1.0                                    #if you don't want to limit overdesign
                            
                        # ---------------------------------------------------- #
                        # NOW CHOOSE A RANDOM BLOCK TECH IF ID IS IN LIST      #
                        # ---------------------------------------------------- # -------------------
                        indices = []
                        for deg in prec_alts:
                            if (1-deg) <= max_degree:   #if the degree is 
                                indices.append(1-deg)
                        if len(indices) == 0:
                            print "Avoid excessive design, skipping"
                            block_alt_chosen = 0        #if skipped, then same as ZERO
                            choice = len(prec_alts)-1     #must set choice or else will be referenced before assignment
                            continue
                        else:
                            #if rand.random() <= basin_target_min:       #same for blocks, there is a x% chance based on target of designing for it
                            #if rand.randint(0,1) == 1 and rand.random() <= basin_target_min:
                            #if True:
                            if rbID in inblocks_chosenIDs:
                                #choice = 0
                                choice = rand.randint(0, len(indices)-1)        #a random integer between indices
                                block_alt_chosen = indices[choice]
                                print "Chosen increment: ", block_alt_chosen
                            else:
                                choice = len(indices)-1                         #It's 1-deg above hence 0 is the end of the list
                                block_alt_chosen = indices[choice]
                                print "Choice is zero, skipping! ", block_alt_chosen
                            if block_alt_chosen == 0:
                                continue
                            
                        #tally up areas   
                        if len(block_strategies_matrix[rbID-1][choice]) == 0:          #if there are block options at that increment
                            print "No options available at that increment, skipping"
                        else:
                            Nopt = len(block_strategies_matrix[rbID-1][choice])
                            print "Total Options available: ", Nopt
                            
                            nchosen = rand.randint(0, Nopt - 1)     #nchosen = chosen position n in (Nopt-1)
                            chosen_obj = block_strategies_matrix[rbID-1][choice][nchosen][1]
                            print "Chosen Strategy: ", chosen_obj.reportStrategy()
                            
                            additional_treatedAimp = chosen_obj.getTotalAImpServed()
                            print "Area treated: ", additional_treatedAimp
                            total_blocks_contribution += additional_treatedAimp
                            print "Total Blocks Contribution: ", total_blocks_contribution
                            subbasin_remainAimp -= additional_treatedAimp
                            print "Remaining Subbasin-Imp", subbasin_remainAimp
                            
                            #### Add this information to the basin_strategy Object ####
                            current_bstrategy.addBlockStrategy(rbID, block_alt_chosen, chosen_obj)      #rbID = current upstream block in subbasin
                                                                                                        #currentblockID = current precinct block in subbasin
                    print "Remaining Impervious area to deal with (after blocks): ", subbasin_remainAimp
                    
                    subbasin_treatedAimp += total_blocks_contribution
                    treat_remainAimp -= total_blocks_contribution
                    
                    #FINALIZE THE TREATED IMPERVIOUS AREA VALUES
                    print "Total Treated Imperviousness so far: ", subbasin_treatedAimp
                    print "as a percentage: ", subbasin_treatedAimp/cumu_Aimp * 100, "%"
                    subbasin_ID_treatedAimp[pID] = subbasin_treatedAimp
                     
                    #add the TREATED IMPERVIOUS AREA OF THIS SUB-BASIN (a subset of totalAimp_subbasin) to the
                    #vector 'subbasin_ID_treatedAimp' at position 'pID', i.e. subbasin_ID_treatedAimp[pID]
                    
                print "Remaining Impervious Area to be treated: ", treat_remainAimp/cumu_Aimp * 100, "%"
                [tis, pis] = current_bstrategy.updateBasinService()
                current_bstrategy.reportBasinStrategy()
                print "Total Imperviousness Served: ", pis, " %"
                
                # ------------------------------------------ #
                # SCORE THE STRATEGY USING THE MCA FUNCTIONS #
                # ------------------------------------------ #
                
                current_bstrategy.calcTechScores(mca_techindex, mca_scoring_tech, mca_scoring_env, mca_scoring_ecn, mca_scoring_soc)
                 
                if eval_mode == "W":
                    current_bstrategy.calcStratScoreSingle(mca_method, mca_stoch, mca_techW, mca_envW, mca_ecnW, mca_socW)
                elif eval_mode == "P":
                    #current_bstrategy.calcStratScorePareto(mca_method, mca_techP, mca_envP, mca_ecnP, mca_socP)
                    pass
                
                basin_strategies_matrix.append([current_bstrategy.getPropImpServed(), current_bstrategy.getMCAtotscore(), current_bstrategy])
                output_file.write(str(currentID)+","+str(iterations+1)+","+str(current_bstrategy.getPropImpServed())+","+str(current_bstrategy.getMCAtotscore())+","+str(len(prec_blocks_chosenIDs))+","+str(len(inblocks_chosenIDs))+"\n")
            
            del current_bstrategy       #delete the reference in current_bstrategy
            
            
            #Grab all options within the desired minimum basin target
            #check if they are above the top-ten/number
            final_basin_strategies = []
            for ind_strat in basin_strategies_matrix:
                if ind_strat[0]/100 > basin_target_min:
                    final_basin_strategies.append(ind_strat)
            del ind_strat
            
            
            #Determine the threshold
            if ranktype == "CI":
                topthreshold = int((1-mca_confint)*len(final_basin_strategies) + 0.5 + 1.0)     #using truncation to assist rounding (faster) e.g. round up 2.44 to 3 involves + 1 = 3.44, cut off to integer = 3
            elif ranktype == "RK":
                topthreshold = mca_topranklimit
            
            #Sort the final_basin_strategies from lowest to highest
            final_basin_strategies.sort()
            print final_basin_strategies
            
            #Grab the top values
            ranking_cdf = []    #holds the scores of the MCA for later choosing
            for i in range(min(len(final_basin_strategies), topthreshold)):
                final_basin_strategies[i][2].writeReportFile()
                ranking_cdf.append(final_basin_strategies[i][1])
            
            print ranking_cdf
            
            ranking_cdf_tot = sum(ranking_cdf)                                  #Normalize ranking_cdf
            cumulative_p = 0
            for i in range(len(ranking_cdf)):
                cumulative_p += ranking_cdf[i]/ranking_cdf_tot
                ranking_cdf[i] = cumulative_p
            
            print ranking_cdf
            
            chosen_strategy_p = rand.random()
            for i in range(len(ranking_cdf)):
                if chosen_strategy_p < ranking_cdf[i]:
                    index = i
                else:
                    pass
            
            top_wsud_strategy = final_basin_strategies[index][2]        #select the final strategy
            basin_strategy_groups.append(top_wsud_strategy)
            
            #Now we have the top_wsud_strategy variable, which holds the chosen basin management strategy, we will now write this info into the output shapefile as a map of points
            #Loop across all blocks
            system_type_matrix = ['BF', 'SW', 'WSUR', 'PB', 'IS']               
            system_type_numeric = [2463, 7925, 9787, 7663, 4635]                #Think Telephone Buttons :) ('Biof', 'Swal', 'WSUR', 'Pond', 'Infl')
            
            for i in range(len(basinblockIDs)):
                currentID = basinblockIDs[i]
                currentAttList = blockcityin.getAttributes("BlockID"+str(currentID))        #attribute list of current block structure
                centreX = currentAttList.getAttribute("Centre_x")
                centreY = currentAttList.getAttribute("Centre_y")
                
                #Grab the strategy objects
                inblock_strat = top_wsud_strategy.getInBlockStrategy(currentID)
                if inblock_strat == None:
                    inblock_systems = [0,0,0]
                    inblock_degs = [0,0,0]
                else:
                    inblock_systems = inblock_strat.getSystemList()
                    inblock_degs = inblock_strat.getSystemDegs()
                
                #define an offsets_matrix, holds the (x,y) coordinates based on current block's centre position. these are where the points will go for different scales, an aesthetic thing
                offsets_matrix = [[centreX+blocks_size/8, centreY+blocks_size/4],[centreX+blocks_size/4, centreY-blocks_size/8],[centreX-blocks_size/8, centreY-blocks_size/4],[centreX-blocks_size/4, centreY+blocks_size/8]]
                blockscale_names = ['L', 'S', 'N']
                for j in range(len(blockscale_names)):
                    if inblock_strat == None or inblock_systems[j] == 0:
                        continue
                    else:
                        current_wsud = inblock_systems[j]
                        print current_wsud
                    
                    scale = blockscale_names[j]
                    coordinates = offsets_matrix[j]
                    
                    plist = pyvibe.PointList()
                    plist.append(Point(coordinates[0],coordinates[1],0))
                    
                    #Transfer existing systems across if any
                    #....
                    
                    wsud_attr = Attribute()
                    wsud_attr.setAttribute("Scale", j)                          #0 = LOT, 1 = STREET, 2 = NEIGHBOURHOOD, 3 = PRECINCT
                    wsud_attr.setAttribute("TotSystems", 1)
                    wsud_attr.setAttribute("Location", currentID)
                    print "CurrentWSUD Type"
                    print current_wsud.getType()
                    wsud_attr.setAttribute("Sys"+str(1)+"Type", current_wsud.getType())
                    wsud_attr.setAttribute("Sys"+str(1)+"TypeN", system_type_numeric[system_type_matrix.index(current_wsud.getType())]) 
                    wsud_attr.setAttribute("Sys"+str(1)+"Degree", inblock_degs[j])
                    wsud_attr.setAttribute("Sys"+str(1)+"Area", current_wsud.getSize())
                    wsud_attr.setAttribute("Sys"+str(1)+"Status", 0)            #0 = Planned, 1 = constructed
                    wsud_attr.setAttribute("Sys"+str(1)+"Year", 9999)           #Year constructed
                    
                    systemsout.setPoints("BlockID"+str(currentID)+str(scale), plist)
                    systemsout.setAttributes("BlockID"+str(currentID)+str(scale), wsud_attr)
                
                #PRECINCT
                outblock_strat = top_wsud_strategy.getOutBlockStrategy(currentID)
                if outblock_strat == None:
                    pass
                else:
                    scale = 'P'
                    coordinates = offsets_matrix[3]
                    
                    plist = pyvibe.PointList()
                    plist.append(Point(coordinates[0],coordinates[1],0))
                    
                    wsud_attr = Attribute()
                    wsud_attr.setAttribute("Scale", 3)                          #0 = LOT, 1 = STREET, 2 = NEIGHBOURHOOD, 3 = PRECINCT
                    wsud_attr.setAttribute("TotSystems", 1)
                    wsud_attr.setAttribute("Location", currentID)
                    wsud_attr.setAttribute("Sys"+str(1)+"Type", outblock_strat.getType())
                    wsud_attr.setAttribute("Sys"+str(1)+"TypeN", system_type_numeric[system_type_matrix.index(outblock_strat.getType())])
                    wsud_attr.setAttribute("Sys"+str(1)+"Degree", 0)
                    wsud_attr.setAttribute("Sys"+str(1)+"Area", outblock_strat.getSize())
                    wsud_attr.setAttribute("Sys"+str(1)+"Status", 0)            #0 = Planned, 1 = constructed
                    wsud_attr.setAttribute("Sys"+str(1)+"Year", 9999)           #Year constructed
                    
                    systemsout.setPoints("BlockID"+str(currentID)+str(scale), plist)
                    systemsout.setAttributes("BlockID"+str(currentID)+str(scale), wsud_attr)

            #Write the overarching strategy output to Basin ID
            blockcityout.setAttributes("BasinID"+str(currentID), basin_attr)
            
            
        #Output vector update
        blockcityout.setAttributes("MapAttributes", map_attr)
        print "saving log file"
        output_file.write("End of Basin Strategies tried Log\n\n") 
        output_file.close()
        print "log file saved"

        #Run the garbage collector
        del basin_strategies_matrix             #delete the basin_strategies_matrix for gc
        del final_basin_strategies              #delete the final_basin_strategies for gc
        if garbage.isenabled() == True:
            pass
        else:
            garbage.enable()
        
        print "Performing garbage collection..."    
        garbage.collect()
        print "Done ..."

        #END OF MODULE

    def getSamplingCDFLinear(self, N, sf, sd):
        #N = number of elements in the sample (including zero)
        #sf = slope factor
        #sd = slope direction       Note: m = slope_factor x slope_direction
        
        if sd < 0:
            b = sf*N+1
        else:
            b = 0
        
        fdf = []
        pdf = []
        cdf = []
        for i in range(N):
            fdf.append(sf*sd*float(i+1)+b)
        for i in range(N):
            pdf.append(float(fdf[i]/sum(fdf)))
        cdf.append(pdf[0])
        for i in range(N-1):
            cdf.append(cdf[i]+pdf[i+1])
        return cdf
    
    def getSamplingCDFExponential(self, N, sf, sd):
        #N = number of elements in sample (including zero)
        #sf = slope factor (the strength of decrease of the curve)
        #sd = slope direction (positive or negative depending on direction)
        
        if sd < 0:
            a = N
        else:
            a = 1
            
        fdf = []
        pdf = []
        cdf = []
        for i in range(N):
            fdf.append(a*np.exp(0.15767*sf*sd*float(i)))
        for i in range(N):
            pdf.append(float(fdf[i]/sum(fdf)))
        cdf.append(pdf[0])
        for i in range(N-1):
            cdf.append(cdf[i]+pdf[i+1])
        return cdf
    
    def getSamplingCDFIndex(self, cdf, r):
        #cdf = the cumulative density function
        #r = cumulative probability to look up (mostly randomly chosen)
        
        #Case 1: r is < first element
        if r < cdf[0]:
            index = 0
            return  index
        
        #Case 2: r is in between one of the elements
        counter = 0
        N = len(cdf)
        while counter < N-1:
            lower = cdf[counter]
            upper = cdf[counter+1]
            if r < upper and r >= lower:
                index = counter + 1
                return index
            else:
                counter += 1
        
        #Case 3: r is exactly or the highest probability)
        if r >= cdf[len(cdf)-1]:
            index = len(cdf)-1
            return index
        else:
            print "cannot find"
            index = counter
            return index
    
    def getSamplingCDFPoisson(self, N, eV):
        #N = number of elements in the sample (including zeros), this defines k
        #eV = lambda of the Poisson distribution
        
        pdf = []
        cdf = []
        
        for i in range(N):              #PDist = (lambda^k*e^-lambda)/k!
            p_value = (eV**(i+1)*np.exp(-1*eV))/math.factorial(i+1)
            pdf.append(p_value)
            print p_value
        if sum(pdf) != 1:
            for i in range(N):
                pdf[i] = pdf[i]/sum(pdf)
            print pdf
        cdf.append(pdf[0])
        for i in range(N-1):
            cdf.append(cdf[i]+pdf[i+1])
        return cdf
        
        