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
from delinblocksguic import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from pyvibe import *
import pyvibe
import math

class delinblocks(Module):
    """Processes information from either UrbanSim or four input biophysical rasters
    and an optional two social-economic rasters and creates a preliminary grid of
    building blocks. 
	
	A coarser resolution grid of the input raster is output
	- blockcity
            contains N number of cells depending on user-specified resolution
            and input raster size, note that all four layers need to match up
            in size, this can be prepared in GIS software.
        - inputs:
            BlockSize = size of cell, model assumes square cells, specify size
                in metres [m]
	- code is split into two possible options based on whether the data is derived
            from UrbanSim or not.
    
    Log of Updates made at each version:
    
    v0.75 update (October 2011):
        - Added neighbourhood --> block searches all 8 neighbours to get IDs
        - Added terrain delineation --> D8 method only with edge drawing
        - Added additional inputs (planning map, locality map and road network map)
        - Cleaned up code a bit with extra headings and better differentiation between
          UrbanSim Forks and other code
        - Updated GUI with new inputs
        - Does Moore/vonNeumann differentiation now in block flow directions
        - Can account for sinks, but only within existing neighbourhood.
        - Writes attributes to the extracted drainage network
        - Receives and processes Planner's Map, mapping it onto the relevant land uses
        - Implemented calculation of four diversity metrics: richness, Shannon's Diversity, Dominance and Evenness
        Future work:
            - add processing of locality map
            - add processing of natural sink map
            - add processing of road network map
            - Make code more modular, perhaps splitting terrain delineation with rest
            - Implement hexagonal blocks
    
    v0.5 update (August 2011):
        - implemented UrbanSim forks, labelled in the code at five locations
        - implemented additional raster inputs: social parameters 1 and 2 with naming
          treats these as probabilities and returns the average probability for the area
        - processes either the land use, population rasters OR UrbanSim data
        - updated GUI for delinblocks to include UrbanSim and social parameter inputs
        
    v0.5 first (July 2011):
        - implemented block delineation algorithm for basic parameters
        - looks for von Neumann neighbourhood and returns Block IDs, writes to Shp file output
        - draws the grid of blocks
        - designed GUI for delinblocks
	
	@ingroup DAnCE4Water
	@author Peter M Bach
	"""

    def __init__(self):
        Module.__init__(self)  
        self.BlockSize = 500                    #size of the blocks (in m)
        self.input_from_urbansim = False        #is the input derived from UrbanSim output?
        self.landuseraster = RasterDataIn
        self.popdensityraster = RasterDataIn
        self.elevationraster = RasterDataIn
        self.soilraster = RasterDataIn
        self.blockcity = VectorDataIn
        self.patchcity = VectorDataIn
        self.urbansim_out = VectorDataIn
        self.addParameter(self, "BlockSize", VIBe2.DOUBLE)
        self.addParameter(self, "input_from_urbansim", VIBe2.BOOL)
        self.addParameter(self, "landuseraster", VIBe2.RASTERDATA_IN)
        self.addParameter(self, "elevationraster", VIBe2.RASTERDATA_IN)
        self.addParameter(self, "soilraster", VIBe2.RASTERDATA_IN)
        self.addParameter(self, "popdensityraster", VIBe2.RASTERDATA_IN)
        self.addParameter(self, "blockcity", VIBe2.VECTORDATA_OUT)
        self.addParameter(self, "patchcity", VIBe2.VECTORDATA_OUT)
        self.addParameter(self, "urbansim_out", VIBe2.VECTORDATA_IN)
        
        self.reportin = VectorDataIn
        self.reportout = VectorDataIn
        self.addParameter(self, "reportin", VIBe2.VECTORDATA_IN)
        self.addParameter(self, "reportout", VIBe2.VECTORDATA_OUT)
        
        #Urban planning information
        self.include_plan_map = False            #planner's map displaying typology distributions
        self.include_local_map = False           #locality map displaying location of centres
        self.include_road_net = False            #road network map not working yet
        self.plan_map = RasterDataIn            
        self.local_map = RasterDataIn
        self.road_network = VectorDataIn           
        self.addParameter(self, "include_plan_map", VIBe2.BOOL)
        self.addParameter(self, "include_local_map", VIBe2.BOOL)
        self.addParameter(self, "include_road_net", VIBe2.BOOL)
        self.addParameter(self, "plan_map", VIBe2.RASTERDATA_IN)
        self.addParameter(self, "local_map", VIBe2.RASTERDATA_IN)
        self.addParameter(self, "road_network", VIBe2.VECTORDATA_IN)
        
        #Social parameter input (at present need to include rasters, but possible future modify to be user-defined ports)
        self.include_soc_par1 = True
        self.include_soc_par2 = True
        self.social_parameter1 = RasterDataIn
        self.social_par1_name = "unnamed1"
        self.social_parameter2 = RasterDataIn
        self.social_par2_name = "unnamed2"
        self.addParameter(self, "include_soc_par1", VIBe2.BOOL)
        self.addParameter(self, "include_soc_par2", VIBe2.BOOL)
        self.addParameter(self, "social_par1_name", VIBe2.STRING)
        self.addParameter(self, "social_par2_name", VIBe2.STRING)
        self.addParameter(self, "social_parameter1", VIBe2.RASTERDATA_IN)
        self.addParameter(self, "social_parameter2", VIBe2.RASTERDATA_IN)
        
        #Map Connectivity inputs
        self.Neighbourhood = "N"                #three options: M = Moore, N = von Neumann, S = Single
        self.flow_method = "DI"                 #three options: DI = D-infinity (Tarboton), D8 = D8 (O'Callaghan & Mark) and MS = Divergent (Freeman)
        self.demsmooth_choose = False
        self.demsmooth_passes = 1
        self.addParameter(self, "Neighbourhood", VIBe2.STRING)
        self.addParameter(self, "flow_method", VIBe2.STRING)
        self.addParameter(self, "demsmooth_choose", VIBe2.BOOL)
        self.addParameter(self, "demsmooth_passes", VIBe2.DOUBLE)
        
        self.vn4FlowPaths = False
        self.vn4Patches = False
        self.addParameter(self, "vn4FlowPaths", VIBe2.BOOL)
        self.addParameter(self, "vn4Patches", VIBe2.BOOL)
        
        self.basinlimit = False
        self.basinAmax = 0
        self.addParameter(self, "basinlimit", VIBe2.BOOL)
        self.addParameter(self, "basinAmax", VIBe2.DOUBLE)
        
        
        #Need to implement input parameters for the future relating to the conceptual networks!
        
        #------------------------------------------
        #END OF INPUT PARAMETER LIST
        
    def run(self):
        print "BEGIN DELINBLOCKS RUN! ----------------------------------------------------"
        if self.Neighbourhood == "N":
            neighbourhood_type = 4              #von Neumann = 4 neighbours
        else: 
            neighbourhood_type = 8              #Moore = 8 neighbours
        
        #Get the vector data into local variables
        blockcity = self.blockcity.getItem()
        patchcity = self.patchcity.getItem()
        elevationraster = self.elevationraster.getItem()                        #ELEVATION AND SOIL DATA ARE NOT URBANSIM DEPENDENT!
        soilraster = self.soilraster.getItem()
        
        plan_map = self.plan_map.getItem()                                      #get plan_map and local_map data anyway even if not selected
        local_map = self.local_map.getItem()
        road_net = self.road_network.getItem()                                      ###DO NOT USE THIS FOR NOW###
        
        cs = self.BlockSize                                                     #BlockSize stored locally [m]
        inputres = elevationraster.getCellSize()                                #input data resolution [m]
        width =  elevationraster.getWidth() * elevationraster.getCellSize()     #"getWidth" syntax returns no. of cells
        height =  elevationraster.getHeight() * elevationraster.getCellSize()   #to get actual width, need to multiply by cell size [m]         
        cellsinblock = int(cs/inputres)                                         #tells us how many smaller cells are in one length of block  
        print "cells in block: "+str(cellsinblock)
        print inputres
        print "Width", width
        print "Height", height
        
        #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        ###########################
        ###URBANSIM FORK #1     ###
        ###########################
        if self.input_from_urbansim == True:                    
            urbansimdata = "Yes"                                #global attribute for later modules
            urbansim_out = self.urbansim_out.getItem()          #get the UrbanSim vector data
            USinputres = 200                                    #at moment cell size is fixed but this line needs to be changed in future when urban sim resolution is different
            if float(cs/USinputres) > float(int(cs/USinputres)):
                print "WARNING, UrbanSim resolution and Block Size conflict"
            UScellsinblock = int(cs/USinputres)
            numUScells = int(UScellsinblock*width/cs * UScellsinblock*height/cs)
        else:
            urbansimdata = "No"         #global attribute
            landuseraster = self.landuseraster.getItem()
            popdensityraster = self.popdensityraster.getItem()
            social_parameter1 = self.social_parameter1.getItem()
            social_parameter2 = self.social_parameter2.getItem()
            if self.landuseraster.getItem().getWidth() != self.soilraster.getItem().getWidth():
                print "WARNING, input rasters are not equal in size!"
        
        ##### -------- END OF URBANSIM FORK #1 -------- #####
        #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
        #Note that the simulation area needs to have a larger width and larger height than the data input area!
        whfactor = 1 - (1/(cs*2))               #factor replaces the rounding function and speeds up computation
        widthnew = int(width/cs+whfactor)       #width of the simulation area (divide total width by block size and round) [#Blocks]
        heightnew = int(height/cs+whfactor)      #height of the simulation area (multiply block size with this to get actual length) [#Blocks]
        numblocks = widthnew * heightnew        #number of blocks based on how many blocks wide x how many blocks tall [#Blocks]
        
        print "widthnew", widthnew
        print "heighnew", heightnew
        print "numblocks", numblocks
        
        #Map Attributes - The Global Attributes List
        map_attr = Attribute()
        map_attr.setAttribute("NumBlocks", numblocks)                   #Number of blocks in the grid
        map_attr.setAttribute("WidthBlocks", widthnew)                  #Width of simulation area in # of blocks
        map_attr.setAttribute("HeightBlocks", heightnew)                #Height of simulation area in # of blocks
        map_attr.setAttribute("BlockSize", cs)                          #Size of block [m]
        map_attr.setAttribute("InputReso", inputres)                    #Resolution of the input data [m]
        map_attr.setAttribute("UrbanSimData", urbansimdata)             #"Yes" or "no" as to whether input derived from UrbanSim
        map_attr.setAttribute("Neigh_Type", neighbourhood_type) 
        
        if self.input_from_urbansim == True:                            #add urbansim input details if data is derived from UrbanSim
            map_attr.setAttribute("UrbanSimReso", USinputres)
        blockcity.setAttributes("MapAttributes",map_attr)               #===> Save attributes to "MapAttributes" in blockcity vector
        
        #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        ########################################################################
        ###URBANSIM FORK #2                                                  ###
        ###IF DATA IS TO COME FROM URBANSIM, ASSIGN EACH GRID WITH A BLOCK ID###
        ########################################################################        
        if self.input_from_urbansim == True:
            for a in range(numUScells):
                currentGRIDattr = urbansim_out.getAttributes("GRID_"+str(a+1))
                plist = urbansim_out.getPoints("GRID_"+str(a+1))
                elist = urbansim_out.getEdges("GRID_"+str(a+1))
                flist = urbansim_out.getFaces("GRID_"+str(a+1))
                rx = currentGRIDattr.getAttribute("relative_x")
                ry = currentGRIDattr.getAttribute("relative_y")
                
                roundingfactor = float(1.0-(1.0/(UScellsinblock*2.0)))
                bx = int(rx/UScellsinblock+roundingfactor)
                by = int(ry/UScellsinblock+roundingfactor)
                belongBlockID = bx+(by-1)*widthnew
                currentGRIDattr.setAttribute("BlockID", belongBlockID)
                blockcity.setPoints("GRID_"+str(a+1),plist)
                blockcity.setEdges("GRID_"+str(a+1), elist)
                blockcity.setFaces("GRID_"+str(a+1),flist)
                blockcity.setAttributes("GRID_"+str(a+1), currentGRIDattr)
        
        ##### -------- END OF URBANSIM FORK #2 -------- #####
        #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
        x_adj = 0
        y_adj = 0
        
        ########################################################################
        ###DRAW BLOCKS AND ASSIGN INFO                                       ###
        ###v0.75                                                             ###
        ######################################################################## 
        blockIDcount = 1     #counts through Block ID, initialize this variable here
        for y in range(heightnew):              #outer loop scans through rows
            for x in range(widthnew):           #inner loop scans through columns
                block_attr = Attribute()        #list of block attributes saved to this variable (recreated each time step)
                block_attr.setAttribute("BlockID", blockIDcount)
                patch_attr = Attribute()        #list of within-block Patch information saved to this variable
                                
                #get coordinates for the current block in a points and face list
                plist = pyvibe.PointList()
                plist.append(Point((x+x_adj)*cs,(y+y_adj)*cs,0))
                plist.append(Point((x+x_adj+1)*cs,(y+y_adj)*cs,0))
                plist.append(Point((x+x_adj+1)*cs,(y+y_adj+1)*cs,0))
                plist.append(Point((x+x_adj)*cs,(y+y_adj+1)*cs,0))
                
                flist = pyvibe.FaceList()
                f = pyvibe.LongList()
                f.append(0)
                f.append(1)
                f.append(2)
                f.append(3)
                flist.append(Face(f))
                
                xorigin = x*cs+0.5*cs               
                yorigin = y*cs+0.5*cs
                
                #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                ###############################################################################
                ###URBANSIM FORK #3 (True)                                                 ###
                ###Sum up the information of all GRIDs with Block ID equal to current Block ###
                ###############################################################################
                if self.input_from_urbansim == True:
                    #do urbansim stuff
                    #tally up pop and unitsR
                    total_pop = 0
                    total_unitsR = 0
                    for a in range(numUScells):
                        currentGRIDattr = blockcity.getAttributes("GRID_"+str(a+1))
                        if int(currentGRIDattr.getAttribute("BlockID")) == int(blockIDcount):
                            total_pop = total_pop + currentGRIDattr.getAttribute("Population")
                            total_unitsR = total_unitsR + currentGRIDattr.getAttribute("UnitsR")
                        else:
                            continue
                    dwelling_density = total_unitsR/(cs*cs/10000)
                    
                    #Write attributes to vector data
                    block_attr.setAttribute("POP_Res", total_pop)               #This attribute exists regardless of option
                    block_attr.setAttribute("US_ResUnits", total_unitsR)        #This parameter is only for UrbanSim
                    block_attr.setAttribute("DwellDens", dwelling_density)      #This parameter is only for UrbanSim
                
                ##### -------- END OF URBANSIM FORK #3a -------- #####
                #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                
                #do some stats from input rasters
                #soil properties, tally up, average out
                #elevation, due to triangulation, need to make sure that we only draw values from valid fields
                x_start = x*cellsinblock
                y_start = y*cellsinblock
                raster_sum_soil = 0
                raster_sum_elev = 0
                total_n_soil = 0
                total_n_elev = 0
                
                if self.input_from_urbansim == False:                   #IF input not derived from UrbanSim, initialize variables
                    landclassfreq = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]       #for land use, population and the social parameters.
                    planmaptotal = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                    planmapfreq = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                    popdens = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                    landclassprop = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                    landclassarea = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                    total_n_luc = 0
                    soc_par1 = 0            #to tally up an average in case
                    total_n_soc_par1 = 0
                    soc_par2 = 0            #to tally up an average in case
                    total_n_soc_par2 = 0    
                    #local_matrix = []
                
                    #define matrices for patch delineation
                    
                
                ####################################################
                ### PATCH DELINEATION ALGORITHM - IMPLEMENT HERE ###
                ####################################################
                lucdatamatrix = 0          #holds land use data from input
                lucdatamatrix = []          
                popdatamatrix = 0          #holds population data from input
                popdatamatrix = []          
                elevdatamatrix = 0         #holds elevation data from input
                elevdatamatrix = []
                soildatamatrix = 0         #holds soil data from input
                soildatamatrix = []
                statusmatrix = 0           #tracks cell status in CA Algorithm
                statusmatrix = []
                camatrix = 0               #performs the CA    
                camatrix = []         
                 
                #Tally up details for rasters that are global
                for i in range(cellsinblock):
                    #add an element to the matrices
                    lucdatamatrix.append([])
                    popdatamatrix.append([])
                    elevdatamatrix.append([])
                    soildatamatrix.append([])
                    statusmatrix.append([])
                    camatrix.append([])
                    for j in range(cellsinblock):
                        statusmatrix[i].append(0)                                           #PATCH DELIN = statusmatrix
                        camatrix[i].append(0)                                               #PATCH DELIN = camatrix
                        if elevationraster.getValue(x_start+i,y_start+j)== -9999:
                            elevdatamatrix[i].append(-9999)                                     #PATCH DELIN = elevdatamatrix
                            soildatamatrix[i].append(-9999)
                            lucdatamatrix[i].append(-9)                  #PATCH DELIN = LUC Data matrix
                            popdatamatrix[i].append(-9)                  #PATCH DELIN = Pop data matrix
                            pass
                        else:
                            elevdatamatrix[i].append(elevationraster.getValue(x_start+i,y_start+j))
                            raster_sum_elev = raster_sum_elev + elevationraster.getValue(x_start+i,y_start+j)
                            total_n_elev += 1
                            
                            if soilraster.getValue(x_start+i,y_start+j)==-9999:
                                soildatamatrix[i].append(-9999)                         #PATCH DELIN = soil matrix
                                pass
                            else:
                                soildatamatrix[i].append(soilraster.getValue(x_start+i,y_start+j))
                                raster_sum_soil = raster_sum_soil + soilraster.getValue(x_start+i,y_start+j)
                                total_n_soil += 1
                                
                                #localities saved in a matrix, block will therefore have a number of different localities
#                                if local_map.getValue(x_start+i, y_start+j) == -9999:
#                                    pass
#                                else:
#                                    if local_map.getValue(x_start+i, y_start+j) in local_matrix:
#                                        pass 
#                                    else: 
#                                        local_matrix.append(local_map.getValue(x_start+i, y_start+j))
                            
                            #if there is no urbansim input, do LUC, POP density and Social Parameters
                            if self.input_from_urbansim == False:
                                if landuseraster.getValue(x_start+i, y_start+j) == -9999:
                                    lucdatamatrix[i].append(-9)                  #PATCH DELIN = LUC Data matrix
                                    popdatamatrix[i].append(-9)                  #PATCH DELIN = Pop data matrix
                                    pass
                                else:
                                    currentLUC = landuseraster.getValue(x_start+i,y_start+j)
                                    currentPOP = popdensityraster.getValue(x_start+i,y_start+j)
                                    lucdatamatrix[i].append(currentLUC)
                                    popdatamatrix[i].append(currentPOP)
                                    if self.include_plan_map == False or plan_map.getValue(x_start+i, y_start+j) == -9999:
                                        pass
                                    else:
                                        currentPLAN = plan_map.getValue(x_start+i, y_start+j)
                                        planmapfreq[int(currentLUC)-1] += 1
                                        planmaptotal[int(currentLUC)-1] += currentPLAN

                                    landclassfreq[int(currentLUC)-1] += 1
                                    popdens[int(currentLUC)-1] = popdens[int(currentLUC)-1] + currentPOP
                                    total_n_luc += 1
                                    
                                    if self.include_soc_par1 == True:
                                        soc_par1 = soc_par1 + social_parameter1.getValue(x_start+i, y_start+j)
                                        total_n_soc_par1 += 1
                                    if self.include_soc_par2 == True:
                                        soc_par2 = soc_par2 + social_parameter2.getValue(x_start+i, y_start+j)
                                        total_n_soc_par2 += 1
                            #Following this step, we have tallied up the total values/frequencies of all input data, but have not averaged it yet
                
                #for PATCH DELINEATION - all data has been obtained for current block from input and is ready for delineation
                
                if self.input_from_urbansim == False:
                    if total_n_luc == 0:
                        #no point to delineate patches
                        patch_delin = -1         #this variable indicates if patch delineation is needed. -1,0 = NO (because no data or one single land use), 1 = YES
                        richness = 0
                        shandiv = 0
                        shandom = 0
                        shaneven = 0
                        pass
                    else:
                        #potentially need to delineate patches
                        for m in range(len(landclassfreq)):
                            if landclassfreq[m] == 0:
                                pass
                            else:
                                popdens[m] = int(float(popdens[m])/float(landclassfreq[m]))     #evaluates average pop density for that class
                                landclassprop[m] = float(landclassfreq[m])/float(total_n_luc)   #evaluates proportion of land use
                                landclassarea[m] = float(landclassfreq[m])*inputres*inputres
                                
                                if self.include_plan_map == True:
                                    planmaptotal[m] = float(planmaptotal[m])/float(planmapfreq[m])
                                
                                #CALCULATE DIVERSITY METRICS
                                #Richness - The number of different types of "species" or "land classes" in the area
                                richness = 0
                                for rich in landclassfreq:              #scan the frequency matrix e.g. [64, 20, 0,0,0,14, ...]
                                    if rich != 0:                       #if the value isn't zero i.e. if that LUC is present
                                        richness += 1                   #add one to richness
                                
                                if richness == 0:
                                    pass
                                else:
                                    #Shannon Diversity Index (Shannon, 1948) - measures diversity in categorical data, the information entropy of
                                    #       the distribution: H = -sum(pi ln(pi))
                                    shandiv = 0
                                    for sdiv in landclassprop:
                                        if sdiv != 0:
                                            shandiv = shandiv + sdiv * math.log(sdiv)
                                        else:
                                            pass
                                    shandiv = -1*shandiv
                                    
                                    #Shannon Dominance Index: The degree to which a single class dominates in the area, 0 = evenness
                                    shandom = 0
                                    shandom = math.log(richness) - shandiv
                                    
                                    #Shannon Evenness Index: Similar to dominance, the level of evenness among the land classes
                                    shaneven = 0
                                    if richness == 1:
                                        shaneven = 1
                                    else:
                                        shaneven = shandiv/math.log(richness)
                                
                                if landclassprop[m] == 1:
                                    patch_delin = 0             #NO because it is one single land use
                                else:
                                    patch_delin = 1             #YES if there's more than one single land use
                    print "Block "+str(blockIDcount)
                    print landclassfreq
                    
                    #################################################################
                    ########## PATCH DELINEATION ALGORITHM  #########################
                    #################################################################
                    
                    landpatchfreq = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                    #landpatchfreq = [[],[],[],[],[],[],[],[],[],[],[],[],[],[]]         #matrix containing all the patch information
                    if patch_delin == -1:
                        total_patches = 0       #no data
                        patch_attr.setAttribute("TotPatches", total_patches)
                    elif patch_delin == 0:
                        total_patches = 1       #uniform land use
                        patch_attr.setAttribute("TotPatches", total_patches)
                        #write code to grab area
                    else:
                        
                        #DEBUG STRING
                        print "Block: "+str(blockIDcount)
                        patchIDcounter = 0              #counts the number of non-data patches    
                        #END DEBUG STRING
                        total_patches = 0       #reset this variable at beginning of patch algorithm
                        finished_sign = 0       #variable that indicates when all data cells in the block have been accounted for
                        while finished_sign == 0:
                            point_found = 0
                            
                            #first find the start position and note the coordinates
                            for iCA in range(len(statusmatrix[0])):
                                if point_found == 1:
                                    break
                                for jCA in range(len(statusmatrix[0])):
                                    if point_found == 1:
                                        break
                                    if statusmatrix[iCA][jCA] == 0:
                                        point_found = 1
                                        irow = iCA
                                        jcol = jCA
                                        print "next starting point: "+str(iCA)+","+str(jCA)
                                        continue
                                    else:
                                        point_found = 0
                            if point_found == 0:
                                finished_sign = 1
                                break
                            
                            #find current land use class, mark the status and camatrix
                            currentCALU = lucdatamatrix[irow][jcol]
                            print "currentLU = "+str(currentCALU)
                            statusmatrix[irow][jcol] = 1                                                
                            camatrix[irow][jcol] = 1
                            
                            #write Patch ID and Land use Attribute to Patch Output IF current CALU is not NODATA
                            if currentCALU != -9:
                                patch_attr.setAttribute("PaID"+str(patchIDcounter)+"_LU", int(currentCALU))
                            
                            #begin delineating patch with CA algorithm
                            patch_area_previous = 0
                            patch_area_current = -9999
                            while patch_area_current != patch_area_previous:
                                patch_area_previous = patch_area_current
                                camatrix_new = camatrix
                                for iCA in range(len(camatrix[0])):
                                    for jCA in range(len(camatrix[0])):
                                        #check if current cell's value is identical to currentCALU
                                        if statusmatrix[iCA][jCA] == 1:
                                            continue
                                        if lucdatamatrix[iCA][jCA] != currentCALU:
                                            continue
                                        else:
                                            pass #all good, can go on
                                        
                                        #get cell's neighbourhood
                                        if jCA == 0:
                                            dx = [0,1]                  #if we have first column then only forward
                                        else:
                                            if j == (len(camatrix[0])-1):
                                                dx = [-1,0]             #if we have last column then only backward
                                            else:
                                                dx = [-1,0,1]           #otherwise allow both
                                        
                                        if iCA == 0:
                                            dy = [0,1]                  #if we have top row, only move down
                                        else:
                                            if iCA == (len(camatrix[0])-1):
                                                dy = [-1,0]             #if we have bottom row, only move up
                                            else:
                                                dy = [-1,0,1]           #otherwise allow both
                                        
                                        total_neighbour_sum = 0
                                        for a in dy:
                                            for b in dx:
                                                total_neighbour_sum += camatrix[iCA+a][jCA+b]
                                        
                                        if total_neighbour_sum >= 1:
                                            camatrix_new[iCA][jCA] = 1
                                        else:
                                            camatrix_new[iCA][jCA] = 0
                                
                                camatrix = camatrix_new
                                patch_area_current = 0
                                for i in range(len(camatrix[0])):
                                    patch_area_current += sum(camatrix[i])
                            
                            #write patch data to status matrix                                  
                            for iCA in range(len(statusmatrix[0])):
                                for jCA in range(len(statusmatrix[0])):
                                    if statusmatrix[iCA][jCA] == 1:
                                        continue
                                    else:
                                        statusmatrix[iCA][jCA] = camatrix[iCA][jCA]
                            
                            
                                                                                                            #<<<<<<<<<<<<<<<OBTAIN DATA FROM OTHER LAYERS FOR INDIV. PATCHES HERE
                            #get other data from CAmatrix (elevation, soil avg, population, if necessary)
                            #   - future versions of this code, if you have additional input rasters that you require patch-based data, insert in here
                            elevation_tally = 0         #reset the tally
                            elev_patch_counter = 0      #counts the number of cells
                            for iCA in range(len(camatrix[0])):
                                for jCA in range(len(camatrix[0])):
                                    if camatrix[iCA][jCA] != 0:
                                        if elevdatamatrix[iCA][jCA] != -9999:
                                            elevation_tally += elevdatamatrix[iCA][jCA]
                                        elev_patch_counter += 1
                            #-----------------------------------------------------
                            
                            #reset the camatrix
                            for iCA in range(len(camatrix[0])):
                                for jCA in range(len(camatrix[0])):
                                    camatrix[iCA][jCA] = 0
                            
                            print "Total Area: "+str(patch_area_current)
                            print "ElevPatchCounter: "+str(elev_patch_counter)
                            print "ElevationAvg: "+str(elevation_tally/elev_patch_counter)
                            
                            
                            #finished ONE patch, write info to matrix before going on
                            #write patch information into matrix of land use patch information [ matrix of N land uses [ submatrix of M patches [ sub-submatrix of K properties ] [] [] ...] [] [] ...]
                            if currentCALU != -9:
                                patch_attr.setAttribute("PaID"+str(patchIDcounter)+"_Area", patch_area_current)
                                patch_attr.setAttribute("PaID"+str(patchIDcounter)+"_Z", elevation_tally/elev_patch_counter)
                                patchIDcounter += 1
                                landpatchfreq[int(currentCALU - 1)] += 1
                            
                            total_patches += 1
                            
                        #END OF cellular automata PATCH delineation, begin writing up details
                        print "Total patches found: "+str(total_patches)
                        print "Total data-filled patches found: "+str(patchIDcounter)
                        print landpatchfreq
                        patch_attr.setAttribute("TotPatches", (patchIDcounter+1))       #total number of non-NODATA patches in the block
                        block_attr.setAttribute("TotPatches", (patchIDcounter+1))
                        #block_attr.setAttribute("Number of patches", )
                        
                        #I know.... total patch size, land use belonging to patch
                        print "-------------------------------------------END of BLOCK"
                    
                    
                #tally up average soil conditions and elevation conditions across block    
                if total_n_soil == 0:
                    block_status = 0
                    block_activity = 0
                    block_soil_k = 0
                    block_elevation_avg = 0
                else:
                    block_status = 1
                    block_activity = float(total_n_soil)*100/cellsinblock/cellsinblock                      
                    block_soil_k = raster_sum_soil/float(total_n_soil)
                    if total_n_elev == 0:
                        block_elevation_avg = -9999
                    else:
                        block_elevation_avg = raster_sum_elev/float(total_n_elev)
                
                ### NEIGHBOURHOODs - Search for all 8 neighbours. Neighbourhood box dealt with later ###
                neighbour_assign = 0
                #check neighbour IDs
                #check for corner pieces
                if blockIDcount - 1 == 0:                            #bottom left
                    neighbour_assign = 1
                    N_neighbour = blockIDcount + widthnew 
                    S_neighbour = 0
                    W_neighbour = 0
                    E_neighbour = blockIDcount + 1
                    NE_neighbour = N_neighbour + 1
                    NW_neighbour = 0
                    SE_neighbour = 0
                    SW_neighbour = 0
                if blockIDcount + 1 == numblocks+1:                  #top right
                    neighbour_assign = 1
                    N_neighbour = 0
                    S_neighbour = blockIDcount - widthnew
                    W_neighbour = blockIDcount - 1
                    E_neighbour = 0
                    NE_neighbour = 0
                    NW_neighbour = 0
                    SE_neighbour = 0
                    SW_neighbour = S_neighbour - 1
                if blockIDcount - widthnew == 0:                     #bottom right
                    neighbour_assign = 1
                    N_neighbour = blockIDcount + widthnew
                    S_neighbour = 0
                    W_neighbour = blockIDcount - 1
                    E_neighbour = 0
                    NE_neighbour = 0
                    NW_neighbour = N_neighbour - 1
                    SE_neighbour = 0
                    SW_neighbour = 0
                if blockIDcount + widthnew == numblocks+1:           #top left
                    neighbour_assign = 1
                    N_neighbour = 0
                    S_neighbour = blockIDcount - widthnew
                    W_neighbour = 0
                    E_neighbour = blockIDcount + 1
                    NE_neighbour = 0
                    NW_neighbour = 0
                    SE_neighbour = S_neighbour + 1
                    SW_neighbour = 0
                
                #check for edge piece
                if neighbour_assign == 1:
                    pass
                else:
                    if float(blockIDcount)/widthnew == y+1:                  #East edge
                        neighbour_assign = 1
                        N_neighbour = blockIDcount + widthnew
                        S_neighbour = blockIDcount - widthnew
                        W_neighbour = blockIDcount - 1
                        E_neighbour = 0
                        NE_neighbour = 0
                        NW_neighbour = N_neighbour - 1
                        SE_neighbour = 0
                        SW_neighbour = S_neighbour - 1
                    if float(blockIDcount-1)/widthnew == y:                  #West edge
                        neighbour_assign = 1
                        N_neighbour = blockIDcount + widthnew
                        S_neighbour = blockIDcount - widthnew
                        W_neighbour = 0
                        E_neighbour = blockIDcount + 1
                        NE_neighbour = N_neighbour + 1
                        NW_neighbour = 0
                        SE_neighbour = S_neighbour + 1
                        SW_neighbour = 0
                    if blockIDcount - widthnew < 0:                          #South edge
                        neighbour_assign = 1
                        N_neighbour = blockIDcount + widthnew
                        S_neighbour = 0
                        W_neighbour = blockIDcount - 1
                        E_neighbour = blockIDcount + 1
                        NE_neighbour = N_neighbour + 1
                        NW_neighbour = N_neighbour - 1
                        SE_neighbour = 0
                        SW_neighbour = 0
                    if blockIDcount + widthnew > numblocks+1:                #North edge
                        neighbour_assign = 1
                        N_neighbour = 0
                        S_neighbour = blockIDcount - widthnew
                        W_neighbour = blockIDcount - 1
                        E_neighbour = blockIDcount + 1
                        NE_neighbour = 0
                        NW_neighbour = 0
                        SE_neighbour = S_neighbour + 1
                        SW_neighbour = S_neighbour - 1
                
                #if there is still no neighbours assigned then assume standard cross
                if neighbour_assign == 1:
                    pass
                else:
                    neighbour_assign = 1
                    N_neighbour = blockIDcount + widthnew
                    S_neighbour = blockIDcount - widthnew
                    W_neighbour = blockIDcount - 1
                    E_neighbour = blockIDcount + 1
                    NE_neighbour = N_neighbour + 1
                    NW_neighbour = N_neighbour - 1
                    SE_neighbour = S_neighbour + 1
                    SW_neighbour = S_neighbour - 1
                ###END OF NEIGHBOURHOOD DETERMINATION
                
                #write attributes to output blocks                    
                block_attr.setAttribute("Locate_x", x+1)
                block_attr.setAttribute("Locate_y", y+1)
                block_attr.setAttribute("Centre_x", xorigin)
                block_attr.setAttribute("Centre_y", yorigin)        
                block_attr.setAttribute("Status", block_status)
                block_attr.setAttribute("Activity", block_activity)
                block_attr.setAttribute("Neighb_N", N_neighbour)
                block_attr.setAttribute("Neighb_S", S_neighbour)
                block_attr.setAttribute("Neighb_W", W_neighbour)
                block_attr.setAttribute("Neighb_E", E_neighbour)
                block_attr.setAttribute("Neighb_NE", NE_neighbour)
                block_attr.setAttribute("Neighb_NW", NW_neighbour)
                block_attr.setAttribute("Neighb_SE", SE_neighbour)
                block_attr.setAttribute("Neighb_SW", SW_neighbour)
                block_attr.setAttribute("Soil_k", block_soil_k)
                block_attr.setAttribute("AvgAltitude", block_elevation_avg)
                
                
                if self.input_from_urbansim == False:
                    landclasses = ["Res","Trad","ORC", "LI", "HI", "Edu", "HnC", "SnU", "Rd", "Tr","PG", "RFlood", "Und", "NA"]
                    for i in range(len(landclasses)):
                        block_attr.setAttribute("pLUC_"+landclasses[i], landclassprop[i])
                        block_attr.setAttribute("ALUC_"+landclasses[i], landclassarea[i])
                        block_attr.setAttribute("POP_"+landclasses[i], popdens[i])
                        if self.include_plan_map == True and i in [0, 1, 3, 4]:
                            block_attr.setAttribute("PRatio_"+landclasses[i], planmaptotal[i])
                    if self.include_soc_par1 == True:
                        if total_n_soc_par1 == 0:
                            pass
                        else:
                            soc_par1_value = soc_par1/total_n_soc_par1/100
                            block_attr.setAttribute(self.social_par1_name, soc_par1_value)
                    if self.include_soc_par2 == True:
                        if total_n_soc_par2 == 0:
                            pass
                        else:
                            soc_par2_value = soc_par2/total_n_soc_par2/100
                            block_attr.setAttribute(self.social_par2_name, soc_par2_value)
                    #Write Diversity Metrics
                    block_attr.setAttribute("Richness", richness)
                    block_attr.setAttribute("ShannonDIV", shandiv)
                    block_attr.setAttribute("ShannonDOM", shandom)
                    block_attr.setAttribute("ShannonEVEN", shaneven)
                    
                ##### -------- END OF URBANSIM FORK #5 -------- #####
                
                #Transfer attributes to output vector data
                blockcity.setPoints("BlockID"+str(blockIDcount), plist)
                blockcity.setFaces("BlockID"+str(blockIDcount), flist)
                blockcity.setAttributes("BlockID"+str(blockIDcount), block_attr)
                patchcity.setPoints("PatchDataID"+str(blockIDcount), plist)
                patchcity.setFaces("PatchDataID"+str(blockIDcount), flist)                
                patchcity.setAttributes("PatchDataID"+str(blockIDcount), patch_attr)
                blockIDcount += 1    #increase counter by one before next loop to represent next Block ID
    
        ########################################################################
        ###TERRAIN DELINEATION                                               ###
        ###v0.75 uses only D8 method                                         ###
        ######################################################################## 
        sinkIDs = []    #array to catch all block IDs that were found to be sinks
        for i in range(numblocks):
            currentID = i + 1
            currentAttList = blockcity.getAttributes("BlockID"+str(currentID))
            currentZ = currentAttList.getAttribute("AvgAltitude")
            block_status = currentAttList.getAttribute("Status")
            if block_status == 0:
                blockcity.setAttributes("BlockID"+str(currentID), currentAttList)
                continue
            #GET NEIGHBOUR IDs (based on Moore or vonNeumann/Single)
            ID_N = currentAttList.getAttribute("Neighb_N")
            ID_S = currentAttList.getAttribute("Neighb_S")
            ID_W = currentAttList.getAttribute("Neighb_W")
            ID_E = currentAttList.getAttribute("Neighb_E")
            if neighbourhood_type == 8:
                ID_NE = currentAttList.getAttribute("Neighb_NE")
                ID_NW = currentAttList.getAttribute("Neighb_NW")
                ID_SE = currentAttList.getAttribute("Neighb_SE")
                ID_SW = currentAttList.getAttribute("Neighb_SW")
                current_neighb = [ID_N, ID_S, ID_W, ID_E, ID_NE, ID_NW, ID_SE, ID_SW]
            else:
                current_neighb = [ID_N, ID_S, ID_W, ID_E]
            
            current_neighbdZ = []
            for j in current_neighb:            #scan all 8 neighbours and get the altitudes, 99999 for no values
                if blockcity.getAttributes("BlockID"+str(int(j))).getAttribute("Status") == 0: #if neighbour with the ID j has 0 status, no elevation
                    neighZ = 99999
                    current_neighbdZ.append(currentZ - neighZ)
                else:
                    neighZ = blockcity.getAttributes("BlockID"+str(int(j))).getAttribute("AvgAltitude")
                    current_neighbdZ.append(currentZ - neighZ)
            flow_direction = max(current_neighbdZ)
            if flow_direction < 0:              #identify sinks or outlets
                downstreamID = -1
                sinkIDs.append(currentID)
            else:
                downstreamID = current_neighb[current_neighbdZ.index(flow_direction)]        
            
            #calculate avg slope between the two blocks
            if current_neighbdZ.index(flow_direction) > 3:
                dx = cs
            else:
                dx = cs
            avg_slope = flow_direction/dx               #slope: downhill = +ve, uphill = -ve (when in sink)
            currentAttList.setAttribute("downstrID", downstreamID)
            currentAttList.setAttribute("max_Zdrop", max(flow_direction,0))
            currentAttList.setAttribute("avg_slope", avg_slope)
            
            #Draw network lines    
            if downstreamID == -1 or downstreamID == 0:
                pass
            else:
                plist = pyvibe.PointList()
                x_up = currentAttList.getAttribute("Centre_x")
                y_up = currentAttList.getAttribute("Centre_y")
                z_up = currentAttList.getAttribute("AvgAltitude") 
                plist.append(Point(x_up,y_up,z_up))
                x_down = blockcity.getAttributes("BlockID"+str(int(downstreamID))).getAttribute("Centre_x")
                y_down = blockcity.getAttributes("BlockID"+str(int(downstreamID))).getAttribute("Centre_y")
                z_down = blockcity.getAttributes("BlockID"+str(int(downstreamID))).getAttribute("AvgAltitude")
                plist.append(Point(x_down, y_down, z_down))
                
                network_attr = Attribute()
                network_attr.setAttribute("BlockID", currentID)
                network_attr.setAttribute("Z_up", z_up)
                network_attr.setAttribute("Z_down", z_down)
                network_attr.setAttribute("max_Zdrop", max(flow_direction,0))
                network_attr.setAttribute("Type", 1)                            #1 = basic downstream, -1 = unblocked sink
                network_attr.setAttribute("avg_slope", avg_slope)
                
                elist = pyvibe.EdgeList()
                elist.append(Edge(0,1))
                
                blockcity.setPoints("NetworkID"+str(currentID), plist)
                blockcity.setEdges("NetworkID"+str(currentID), elist)
                blockcity.setAttributes("NetworkID"+str(currentID), network_attr)
            
            blockcity.setAttributes("BlockID"+str(currentID), currentAttList) 
        
        total_sinks = len(sinkIDs)
        print "A total of: "+str(total_sinks)+" sinks found in map!"
            
        #Sink unblocking algorithm for immediate neighbourhood
        for i in sinkIDs:
            print i
            currentID = i
            currentAttList = blockcity.getAttributes("BlockID"+str(currentID))
            currentZ = currentAttList.getAttribute("AvgAltitude")    
            
            #Scan the 8 neighbours, if all of them drain into the sink, then proceed further
            ID_N = currentAttList.getAttribute("Neighb_N")
            ID_S = currentAttList.getAttribute("Neighb_S")
            ID_W = currentAttList.getAttribute("Neighb_W")
            ID_E = currentAttList.getAttribute("Neighb_E")
            if neighbourhood_type == 8:
                ID_NE = currentAttList.getAttribute("Neighb_NE")
                ID_NW = currentAttList.getAttribute("Neighb_NW")
                ID_SE = currentAttList.getAttribute("Neighb_SE")
                ID_SW = currentAttList.getAttribute("Neighb_SW")
                current_neighb = [ID_N, ID_S, ID_W, ID_E, ID_NE, ID_NW, ID_SE, ID_SW]
            else:
                current_neighb = [ID_N, ID_S, ID_W, ID_E]
           
            possible_IDdrains = []
            possible_ID_dZ = []
            possibility = 0
            for j in current_neighb:
                if blockcity.getAttributes("BlockID"+str(int(j))).getAttribute("downstrID") != currentID:
                    if blockcity.getAttributes("BlockID"+str(int(j))).getAttribute("Status") != 0:
                        possible_IDdrains.append(j)
                        possible_ID_dZ.append(blockcity.getAttributes("BlockID"+str(int(j))).getAttribute("AvgAltitude")-currentZ)
                        possibility += 1
            if possibility > 0:         #if algorithm found a possible pathway for sink to unblock, then get the ID and connect network
                sink_path = min(possible_ID_dZ)
                sink_drainID = possible_IDdrains[possible_ID_dZ.index(sink_path)]
                currentAttList.setAttribute("drainto_ID", sink_drainID)
                currentAttList.setAttribute("h_pond", min(possible_ID_dZ))
            else:               #need to broaden search space and start again
                continue                #PROBLEM: cannot simply expand the neighbourhood, we risk running a loop through the network
                                        # Solutions to this problem: will probably need the waterways data set and the outlet location!
                                        # Search the space adding blocks to the current_neighb matrix that are linked with the existing IDs
                                        # until we find one that isn't part of the basin.
            
            ##Draw the network in
            plist = pyvibe.PointList()
            x_up = currentAttList.getAttribute("Centre_x")
            y_up = currentAttList.getAttribute("Centre_y")
            z_up = currentAttList.getAttribute("AvgAltitude") 
            plist.append(Point(x_up,y_up,z_up))
            
            x_down = blockcity.getAttributes("BlockID"+str(int(sink_drainID))).getAttribute("Centre_x")
            y_down = blockcity.getAttributes("BlockID"+str(int(sink_drainID))).getAttribute("Centre_y")
            z_down = blockcity.getAttributes("BlockID"+str(int(sink_drainID))).getAttribute("AvgAltitude")
            plist.append(Point(x_down, y_down, z_down))
                
            elist = pyvibe.EdgeList()
            elist.append(Edge(0,1))
            
            network_attr = Attribute()
            network_attr.setAttribute("BlockID", currentID)
            network_attr.setAttribute("Z_up", z_up)
            network_attr.setAttribute("Z_down", z_down)
            network_attr.setAttribute("max_Zdrop", (min(possible_ID_dZ)*-1))
            network_attr.setAttribute("Type", -1)                            #1 = basic downstream, -1 = unblocked sink
                
            blockcity.setPoints("NetworkID"+str(currentID), plist)
            blockcity.setEdges("NetworkID"+str(currentID), elist)
            blockcity.setAttributes("NetworkID"+str(currentID), network_attr)
            
            blockcity.setAttributes("BlockID"+str(currentID), currentAttList)
            
            #-----------------------------------------------------------------------#
        ###---------TERRAIN DELINEATION END ------------------------------------------------------------------###
        
        
        ### SCAN FOR BASINS NOW ###
        #Set up for loop to scan through blocks
        #For each block, scan the loop of blocks again for the blocks that drain into it
#        upstreamIDs = []
#        for i in range(numblocks):
#            currentID = i+1
#            currentAttlist = blockcity.getAttributes("BlockID"+str(currentID))
#            #check activity
#            upstreamIDs.append([])
#            if currentAttlist.getAttribute("Status") == 0:
#                continue
#            for j in range(numblocks):
#                if blockcity.getAttributes("BlockID"+str(j+1)).getAttribute("Status") == 0:
#                    continue
#                if blockcity.getAttributes("BlockID"+str(j+1)).getAttribute("downstrID") == currentID:
#                    upstreamIDs[i].append(j+1)
#                if blockcity.getAttributes("BlockID"+str(j+1)).getAttribute("downstrID") == -1:
#                    if blockcity.getAttributes("BlockID"+str(j+1)).getAttribute("drainto_ID") == currentID:
#                        upstreamIDs[i].append(j+1)
        
#        for i in range(numblocks):              #now loop over each block
#            if blockcity.getAttributes("BlockID"+str(i+1)).getAttribute("Status") == 0:
#                continue
#            if len(upstreamIDs[i]) == 0:        #if the matrix for that block ID is zero, skip
#                continue
#            for j in upstreamIDs[i]:            #otherwise loop over the elements of this expanding vector
#                currentSID = j                  #j takes value of the next immediate upstream block
#                print "Now scanning for upstream blocks that drain into: "+str(j)
#                for k in range(numblocks):      #repeat the scanning process now across all blocks for ID j
#                    if blockcity.getAttributes("BlockID"+str(k+1)).getAttribute("Status") == 0:
#                        continue
#                    if blockcity.getAttributes("BlockID"+str(k+1)).getAttribute("BlockID") == currentSID:
#                        continue
#                    if blockcity.getAttributes("BlockID"+str(k+1)).getAttribute("downstrID") == currentSID:
#                        upstreamIDs[i].append(k+1)
#                    if blockcity.getAttributes("BlockID"+str(k+1)).getAttribute("downstrID") == -1:
#                        if blockcity.getAttributes("BlockID"+str(k+1)).getAttribute("drainto_ID") == currentSID:
#                            upstreamIDs[i].append(k+1)
        
#        print upstreamIDs    
#        #upstream IDs is a 2D matrix with following: [ Block ID ][ Comma-separated list of upstream blocks ]    
            
#        #Write code to transfer information into vector
        
        
    ########################################################
    #LINK WITH GUI                                         #
    ########################################################        
                        
    def createInputDialog(self):
        form = activatedelinblocksGUI(self, QApplication.activeWindow())
        form.show()
        return True             