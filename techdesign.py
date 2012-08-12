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
import numpy as np
import designbydcv as ddcv

########################################################
#DESIGN FUNCTIONS FOR DIFFERENT TECHNOLOGIES           #
########################################################

#---BIOFILTRATION SYSTEM/RAINGARDEN [BF]----------------------------------------
def design_BF(Aimp, dcv, tarQ, tarTSS, tarTP, tarTN, soilK, maxsize ):
    #Design of Biofiltration systems
    #   input: Imparea = Impervious Area to treat
    #          tarQ = Runoff reduction target
    #          tarTSS = TSS reduction target
    #          tarTP = TP reduction target
    #          tarTN = TN reduction target
    #          soilK = soil hydraulic conductivity
    #          maxsize = maximum allowable system size

    if Aimp == 0:   #if there is no impervious area to design for, why bother?
        return np.inf
    #size the system    
    psystem = ddcv.retrieveDesign(dcv, "BF", soilK, [tarQ, tarTSS, tarTP, tarTN, 100])
    
    if psystem == np.inf:
        return np.inf
    
    system_area = Aimp * psystem
    
    #if the system design has passed to this point: i.e. not impossible and there is impervious to treat, then add planning constraints
    
    #an infiltrating system (extra space around it required), determine the setback required
    if soilK > 180:
        setback = 1.0   #metres
    elif soilK > 36:
        setback = 2.0   #metres
    elif soilK > 3.6:
        setback = 4.0   #metres
    else:
        setback = 5.0   #metres
    
    Areq = m.pow((m.sqrt(system_area)+2*setback),2)
    
    #final check, if the system has exceeded maximum size, return 'impossible' = inf
    if Areq > maxsize:          #if the final design exceeds the maximum allowable size, forget it!
        print "Warning, Maximum System Size Exceeded"
        return np.inf
        
    return Areq

#---INFILTRATION SYSTEMS [IS]---------------------------------------------------
def design_IS(Aimp, dcv, tarQ, tarTSS, tarTP, tarTN, soilK, maxsize ):
    #Design of Infiltration systems
    #   input: Imparea = Impervious Area to treat
    #          tarQ = Runoff reduction target
    #          tarTSS = TSS reduction target
    #          tarTP = TP reduction target
    #          tarTN = TN reduction target
    #          soilK = soil hydraulic conductivity
    #          maxsize = maximum allowable system size
    
    if Aimp == 0:   #if there is no impervious area to design for, why bother?
        return np.inf
    #size the system
    psystem = ddcv.retrieveDesign(dcv, "IS", soilK, [tarQ, tarTSS, tarTP, tarTN, 100])
    
    if psystem == np.inf:       #if the system cannot be designed, it will return infinity
        return np.inf
    
    system_area = Aimp * psystem
    
    #if the system design has passed to this point: i.e. not impossible and there is impervious to treat, then add planning constraints
    #find setback requirement based on soilK
    if soilK >= 3600:
        setback = 1.0
    elif soilK >= 1800:
        setback = 1.0
    elif soilK >= 360:
        setback = 1.0
    elif soilK >= 180:
        setback = 1.0
    elif soilK > 36:
        setback = 2
    elif soilK > 3.6:
        setback = 4.0   #metres
    else:
        print "Soil is unsuitable for infiltration"
        return np.inf

    Areq = m.pow((m.sqrt(system_area)+2*setback),2)
    
    if Areq > maxsize:          #if the final design exceeds the maximum allowable size, forget it!
        print "Warning, Maximum System Size Exceeded"
        return np.inf
    
    return Areq

#---PONDS & BASINS [PB]---------------------------------------------------------
def design_PB(Aimp, dcv, tarQ, tarTSS, tarTP, tarTN, soilK, maxsize ):
    #Design of Ponds & Lakes
    #   input: Imparea = Impervious Area to treat
    #          tarQ = Runoff reduction target
    #          tarTSS = TSS reduction target
    #          tarTP = TP reduction target
    #          tarTN = TN reduction target
    #          soilK = soil hydraulic conductivity
    #          maxsize = maximum allowable system size
    
    if Aimp == 0:   #if there is no impervious area to design for, why bother?
        return np.inf
    #size the system
    psystem = ddcv.retrieveDesign(dcv, "PB", soilK, [tarQ, tarTSS, tarTP, tarTN, 100])
    
    if psystem == np.inf:       #if the system cannot be designed, it will return infinity
        return np.inf
    
    system_area = Aimp * psystem
    
    #add extra area to the system (multipliers for batters)
    batter_multiplier = 1.3
    
    Areq = system_area * batter_multiplier
    
    if Areq > maxsize:          #if the final design exceeds the maximum allowable size, forget it!
        print "Warning, Maximum System Size Exceeded"
        return np.inf
    
    return Areq

#---RAINWATER TANKS [RT]--------------------------------------------------------
def design_RT(self, currentID):
    
    dcRT = [[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.5,2.0], \
            [0,45,59,70,78,81,86,90,91,95,97,98,99,99.9,100], \
            [0,40,49,56,61,69,71,78,81,82,85,88,90,91,96], \
            [0,37,41,48,51,58,60,65,69,71,73,78,80,84,90], \
            [0,34,39,42,48,50,54,59,60,62,67,69,70,76,81]]
    
    return True

#---SURFACE WETLANDS [WSUR]-----------------------------------------------------
def design_WSUR(Aimp, dcv, tarQ, tarTSS, tarTP, tarTN, soilK, maxsize ):
    #Design of Ponds & Lakes
    #   input: Imparea = Impervious Area to treat
    #          tarQ = Runoff reduction target
    #          tarTSS = TSS reduction target
    #          tarTP = TP reduction target
    #          tarTN = TN reduction target
    #          soilK = soil hydraulic conductivity
    #          maxsize = maximum allowable system size
    
    if Aimp == 0:   #if there is no impervious area to design for, why bother?
        return np.inf
    #size the system
    psystem = ddcv.retrieveDesign(dcv, "PB", soilK, [tarQ, tarTSS, tarTP, tarTN, 100])
    
    if psystem == np.inf:       #if the system cannot be designed, it will return infinity
        return np.inf
    
    system_area = Aimp * psystem
    
    #add extra area to the system (multipliers for batters)
    batter_multiplier = 1.3
    
    Areq = system_area * batter_multiplier
    
    if Areq > maxsize:          #if the final design exceeds the maximum allowable size, forget it!
        print "Warning, Maximum System Size Exceeded"
        return np.inf
    
    return Areq

#---SWALES & BUFFER STRIPS [SW]-------------------------------------------------
def design_SW(Aimp, dcv, tarQ, tarTSS, tarTP, tarTN, soilK, maxsize ):
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

