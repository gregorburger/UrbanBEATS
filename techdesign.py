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
import math as m

########################################################
#DESIGN FUNCTIONS FOR DIFFERENT TECHNOLOGIES           #
########################################################

#---BIOFILTRATION SYSTEM/RAINGARDEN [BF]----------------------------------------
def design_BF(Aimp, tarQ, tarTSS, tarTP, tarTN, soilK, maxsize ):
    #Design of Biofiltration systems
    #   input: Imparea = Impervious Area to treat
    #          tarQ = Runoff reduction target
    #          tarTSS = TSS reduction target
    #          tarTP = TP reduction target
    #          tarTN = TN reduction target
    #          soilK = soil hydraulic conductivity
    #          maxsize = maximum allowable system size
    
    dcBF = [[0,0.2,0.4,0.6,0.8,1,1.2,1.4,1.6,1.8,2], \
            [0,58,72,79,84,87,89,90,91,91.5,92], \
            [0,28,43,50,59,64,68,71,73,77,79], \
            [0,9,16,20,25,29,30,32,35,37,39]]
            #design curves for biofiltration systems with 100mm EDD
            #column 0 = area of system (as % of imp. area)
            #columns 1-3 = TSS, TP, TN reduction achieved (%)
    
    sizes = []         #initialize variables
    targets = [tarTSS, tarTP, tarTN]
    pollutant = ["TSS", "TP", "TN"]
    cannot_meet = 0             #checks this variable after the loop to see if Areq is to be set to 9999999
    for pol_index in [1, 2, 3]:
        #find size for TSS
        lower_bound = None
        upper_bound = dcBF[pol_index][0]
        up_row = 0
        for i in dcBF[pol_index][1:]:
            if max(dcBF[pol_index]) < targets[pol_index-1]:
                print "Warning, cannot meet "+str(pollutant[pol_index-1])+" Target with current design standards!"
                cannot_meet = 1
                sizes.append(max(dcBF[0]))
                break
            up_row = up_row + 1
            lower_bound = upper_bound
            upper_bound = i
            if targets[pol_index-1] <= upper_bound:
                slope = (dcBF[0][up_row] - dcBF[0][up_row-1])/(upper_bound - lower_bound)
                sizes.append(dcBF[0][up_row-1]+(slope*(targets[pol_index-1] - lower_bound)))    
                break
    
    #calculate surface area of system required
    if cannot_meet == 1:
        Areq = 999999999
        return Areq
    else:
        size_req = max(sizes)
        Asystem = Aimp * size_req/100
    
    #an infiltrating system (extra space around it required)
    if soilK > 180:
        setback = 1.0   #metres
    elif soilK > 36:
        setback = 2.0   #metres
    elif soilK > 3.6:
        setback = 4.0   #metres
    else:
        setback = 5.0   #metres
    
    if Aimp == 0:
        Areq = 999999999
        #print "no area - no system"
    else:
        Areq = m.pow((m.sqrt(Asystem)+2*setback),2)
    
    if Areq > maxsize:          #if the final design exceeds the maximum allowable size, forget it!
        print "Warning, Maximum System Size Exceeded"
        Areq = 999999999
        
    return Areq


#---INFILTRATION SYSTEMS [IS]---------------------------------------------------
def design_IS(Aimp, tarQ, tarTSS, tarTP, tarTN, soilK, maxsize ):
    #Design of Infiltration systems
    #   input: Imparea = Impervious Area to treat
    #          tarQ = Runoff reduction target
    #          tarTSS = TSS reduction target
    #          tarTP = TP reduction target
    #          tarTN = TN reduction target
    #          soilK = soil hydraulic conductivity
    #          maxsize = maximum allowable system size

    dcIS = [[0,0.02,0.04,0.06,0.08,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0], \
            [0,1,2.5,4,5,6,11,16,21,26,31,35,40,44,49], \
            [0,4,6,10,14,16,30,41,50,56,61,66,70,75,79], \
            [0,10,19,27,34,40,60,73,81,86,89,91,93,95,96],\
            [0,25,44,55,65,70,86,94,95,96,97,98,99,99.5], \
            [0,40,59,71,80,83,93,96,98,99,99.5,99.75,100,100,100]]       
            #design curve for infiltration systems
            #column 0 = area of system (as % of imp. area)
            #columns 1 to 5 = hyd.effectiveness for (3.6, 36, 360, 1800 and 3600mm/hr)
    
    size = 0         #initialize variables
    target = tarQ
    #find column for soil
    if soilK >= 3600:
        col_index = 5
        setback = 1.0
    elif soilK >= 1800:
        col_index = 4
        setback = 1.0
    elif soilK >= 360:
        col_index = 3
        setback = 1.0
    elif soilK >= 180:
        col_index = 2
        setback = 1.0
    elif soilK > 36:
        col_index = 2
        setback = 2
    elif soilK > 3.6:
        col_index = 1
        setback = 4.0   #metres
    else:
        print "Soil is unsuitable for infiltration"
        size = 0
        Areq = 999999999
        return Areq

    lower_bound = None
    upper_bound = dcIS[col_index][0]
    up_row = 0
    cannot_meet = 0
    for i in dcIS[col_index][1:]:
        if max(dcIS[col_index]) < target:
            print "Cannot meet water management target with current design standards"
            cannot_meet = 1
            size = max(dcIS[0])
            break
        up_row = up_row + 1
        lower_bound = upper_bound
        upper_bound = i
        if target <= upper_bound:
            slope = (dcIS[0][up_row] - dcIS[0][up_row-1])/(upper_bound - lower_bound)
            size = dcIS[0][up_row-1]+(slope*(target - lower_bound))   
            break
    
    #calculate surface area of system required
    if cannot_meet == 1:
        Areq = 999999999
        return Areq
    else:
        size_req = size
        Asystem = Aimp * size_req/100
        
    #an infiltrating system (extra space around it required)
    if Aimp == 0:
        Areq = 999999999                #large enough number to make it impossible to fit
        #print "no area - no system"
    else:
        Areq = m.pow((m.sqrt(Asystem)+2*setback),2)
    
    if Areq > maxsize:          #if the final design exceeds the maximum allowable size, forget it!
        print "Warning, Maximum System Size Exceeded"
        Areq = 999999999
        
    return Areq

#---PONDS & BASINS [PB]---------------------------------------------------------
def design_PB(Aimp, tarQ, tarTSS, tarTP, tarTN, soilK, maxsize ):
    #Design of Ponds & Lakes
    #   input: Imparea = Impervious Area to treat
    #          tarQ = Runoff reduction target
    #          tarTSS = TSS reduction target
    #          tarTP = TP reduction target
    #          tarTN = TN reduction target
    #          soilK = soil hydraulic conductivity
    #          maxsize = maximum allowable system size
    
    dcPB = [[0,0.1,0.25,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5],\
            [0,26,45,60,75,81,85,87,89,89.5,90,90.5,91],\
            [0,17,29,40,51,58,60,61.5,63,65,66,67,68],\
            [0,4,9,15,24,30,35,39,41,43,45,46,47]]
            #design curve for ponds & lakes
            #column 0 = area of system (as % of imp. area)
            #columns 1 to 3 = TSS, TP, TN reduction achieved (%)
    
    sizes = []         #initialize variables
    targets = [tarTSS, tarTP, tarTN]
    pollutant = ["TSS", "TP", "TN"]
    cannot_meet = 0
    for pol_index in [1, 2, 3]:
        #find size for TSS
        lower_bound = None
        upper_bound = dcPB[pol_index][0]
        up_row = 0
        for i in dcPB[pol_index][1:]:
            if max(dcPB[pol_index]) < targets[pol_index-1]:
                print "Warning, cannot meet "+str(pollutant[pol_index-1])+" Target with current design standards!"
                cannot_meet = 1
                sizes.append(max(dcPB[0]))
                break
            up_row = up_row + 1
            lower_bound = upper_bound
            upper_bound = i
            if targets[pol_index-1] <= upper_bound:
                slope = (dcPB[0][up_row] - dcPB[0][up_row-1])/(upper_bound - lower_bound)
                sizes.append(dcPB[0][up_row-1]+(slope*(targets[pol_index-1] - lower_bound)))    
                break
    
    #calculate surface area of system required
    if cannot_meet == 1:
        Areq = 999999999
        return Areq
    else:
        size_req = max(sizes)
        Asystem = Aimp * size_req/100
    
    #add extra area to the system (multipliers for batters)
    batter_multiplier = 1.3
    
    if Aimp == 0:
        Areq = 999999999
    else:
        Areq = Asystem * batter_multiplier
    
    if Areq > maxsize:          #if the final design exceeds the maximum allowable size, forget it!
        print "Warning, Maximum System Size Exceeded"
        Areq = 999999999
    
    return Areq

#---RAINWATER TANKS [RT]--------------------------------------------------------
def design_RT(self, currentID):
    
    dcRT = [[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.5,2.0], \
            [0,45,59,70,78,81,86,90,91,95,97,98,99,99.9,100], \
            [0,40,49,56,61,69,71,78,81,82,85,88,90,91,96], \
            [0,37,41,48,51,58,60,65,69,71,73,78,80,84,90], \
            [0,34,39,42,48,50,54,59,60,62,67,69,70,76,81]]
    
    return

#---SURFACE WETLANDS [WSUR]-----------------------------------------------------
def design_WSUR(Aimp, tarQ, tarTSS, tarTP, tarTN, soilK, maxsize ):
    #Design of Ponds & Lakes
    #   input: Imparea = Impervious Area to treat
    #          tarQ = Runoff reduction target
    #          tarTSS = TSS reduction target
    #          tarTP = TP reduction target
    #          tarTN = TN reduction target
    #          soilK = soil hydraulic conductivity
    #          maxsize = maximum allowable system size
    
    dcWSUR = [[0,0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0], \
              [0,44,60,70,77,82,86,89,90,91,92], \
              [0,31,45,54,60,66,69,71,74,76,77], \
              [0,19,29,36,41,45,49,51,53,55,56]]
            #design curve for surface wetlands
            #column 0 = area of system (as % of imp. area)
            #columns 1 to 3 = TSS, TP, TN reduction achieved (%)
          
    sizes = []         #initialize variables
    targets = [tarTSS, tarTP, tarTN]
    pollutant = ["TSS", "TP", "TN"]
    cannot_meet = 0
    for pol_index in [1, 2, 3]:
        #find size for TSS
        lower_bound = None
        upper_bound = dcWSUR[pol_index][0]
        up_row = 0
        for i in dcWSUR[pol_index][1:]:
            if max(dcWSUR[pol_index]) < targets[pol_index-1]:
                print "Warning, cannot meet "+str(pollutant[pol_index-1])+" Target with current design standards!"
                cannot_meet = 1
                sizes.append(max(dcWSUR[0]))
                break
            up_row = up_row + 1
            lower_bound = upper_bound
            upper_bound = i
            if targets[pol_index-1] <= upper_bound:
                slope = (dcWSUR[0][up_row] - dcWSUR[0][up_row-1])/(upper_bound - lower_bound)
                sizes.append(dcWSUR[0][up_row-1]+(slope*(targets[pol_index-1] - lower_bound)))    
                break
    
    #calculate surface area of system required
    if cannot_meet == 1:
        Areq = 999999999
        return Areq
    else:
        size_req = max(sizes)
        Asystem = Aimp * size_req/100
    
    #add extra area to the system (multipliers for batters)
    batter_multiplier = 1.3
    
    if Aimp == 0:
        Areq = 999999999
        #print "no area - no system"
    else:
        Areq = Asystem * batter_multiplier
    
    if Areq > maxsize:          #if the final design exceeds the maximum allowable size, forget it!
        print "Warning, Maximum System Size Exceeded"
        Areq = 999999999
    
    return Areq

#---SWALES & BUFFER STRIPS [SW]-------------------------------------------------
def design_SW(Aimp, tarQ, tarTSS, tarTP, tarTN, soilK, maxsize ):
    #Design of Ponds & Lakes
    #   input: Imparea = Impervious Area to treat
    #          tarQ = Runoff reduction target
    #          tarTSS = TSS reduction target
    #          tarTP = TP reduction target
    #          tarTN = TN reduction target
    #          soilK = soil hydraulic conductivity
    #          maxsize = maximum allowable system size
    
    dcSW = [[0,0.1,0.2,0.5,1.0,1.5,2,2.5,3], \
            [0,50,70,81,89,90,91,91.5,92], \
            [0,30,45,55,60,62,64,65,65], \
            [0,7,11,19,24,28,30,32.5,35]]
            #design curve for swales & buffer strips
            #column 0 = area of system (as % of imp. area)
            #columns 1 to 3 = TSS, TP, TN reduction achieved (%)
    
    sizes = []         #initialize variables
    targets = [tarTSS, tarTP, tarTN]
    pollutant = ["TSS", "TP", "TN"]
    cannot_meet = 0
    for pol_index in [1, 2, 3]:
        #find size for TSS
        lower_bound = None
        upper_bound = dcSW[pol_index][0]
        up_row = 0
        for i in dcSW[pol_index][1:]:
            if max(dcSW[pol_index]) < targets[pol_index-1]:
                print "Warning, cannot meet "+str(pollutant[pol_index-1])+" Target with current design standards!"
                cannot_meet = 1
                sizes.append(max(dcSW[0]))
                break
            up_row = up_row + 1
            lower_bound = upper_bound
            upper_bound = i
            if targets[pol_index-1] <= upper_bound:
                slope = (dcSW[0][up_row] - dcSW[0][up_row-1])/(upper_bound - lower_bound)
                sizes.append(dcSW[0][up_row-1]+(slope*(targets[pol_index-1] - lower_bound)))    
                break
    
    #calculate surface area of system required
    if cannot_meet == 1:
        Areq = 999999999
        return Areq
    else:
        size_req = max(sizes)
        Asystem = Aimp * size_req/100
    
    #add extra area to the system
    
    if Aimp == 0:
        Areq = 999999999
        #print "no area - no system"
    else:
        Areq = Asystem      #swales drain into a pipe, so no additional area required, just need to check what minimum allowable width is
    
    if Areq > maxsize:          #if the final design exceeds the maximum allowable size, forget it!
        print "Warning, Maximum System Size Exceeded"
        Areq = 999999999
    
    return Areq

