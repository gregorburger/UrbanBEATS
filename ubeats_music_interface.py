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
def createMUSICmsf(path, name):
    f = open(str(path)+str(name)+".msf", 'w')
    return f

def writeMUSICheader(f,climatepath):
    path = "C:\\Program Files\\eWater\\MUSIC 5 SL\\Template\\Melbourne 1959 6 Minute.mlb"
    #path = climatepath
    f.write("====================================================================================\n")
    f.write("DESCRIPTION\n")
    f.write("UrbanBEATS Output, MUSIC File Input\n")
    f.write("====================================================================================\n")
    f.write("VersionNumber,200,{MUSIC Setup File version number}\n")
    f.write("------------------------------------------------------------------------------------\n")
    f.write("MeteorologicalTemplate,"+path+",{MLB Filename}\n")
    f.write("------------------------------------------------------------------------------------\n")
    f.write("====================================================================================\n")
    return True

def writeMUSICcatchmentnode(f, ID, nodepart, ncount, x, y, area, imp, parameter_list):
    #f = filename variables, ID = block ID, nodepart = lot/street/treat/untreat x = x-coordinate of block, y = y-coordinate of block
    f.write("Node Type,UrbanSourceNode,{Node Type}\n")
    f.write("Node Name,BlockID"+str(ID)+str(nodepart)+",{Node Name}\n")
    f.write("Node ID,"+str(ncount)+",{Node ID}\n")
    f.write("Coordinates,"+str(x)+":"+str(y)+",{Coordinates}{X:Y}\n")
    f.write("General - Location,BlockID"+str(ID)+str(nodepart)+",\n")
    f.write("General - Notes,,\n")
    f.write("General - Fluxes - Daily,,\n")
    f.write("General - Fluxes - Sub-Daily,,\n")
    f.write("Areas - Total Area (ha),"+str(area)+",{ha}\n")
    f.write("Areas - Impervious (%),"+str(imp*100)+",{%}\n")
    f.write("Areas - Pervious (%),"+str((1-imp)*100)+",{%}\n")
    f.write("Rainfall-Runoff - Impervious Area - Rainfall Threshold (mm/day),"+str(parameter_list[0])+",{mm/day}\n")
    f.write("Rainfall-Runoff - Pervious Area - Soil Storage Capacity (mm),"+str(parameter_list[1])+",{mm}\n")
    f.write("Rainfall-Runoff - Pervious Area - Initial Storage (% of Capacity),"+str(parameter_list[2])+",{% of Capacity}\n")
    f.write("Rainfall-Runoff - Pervious Area - Field Capacity (mm),"+str(parameter_list[3])+",{mm}\n")
    f.write("Rainfall-Runoff - Pervious Area - Infiltration Capacity Coefficient - a,"+str(parameter_list[4])+",\n")
    f.write("Rainfall-Runoff - Pervious Area - Infiltration Capacity Exponent - b,"+str(parameter_list[5])+",\n")
    f.write("Rainfall-Runoff - Groundwater Properties - Initial Depth (mm),"+str(parameter_list[6])+",{mm}\n")
    f.write("Rainfall-Runoff - Groundwater Properties - Daily Recharge Rate (%),"+str(parameter_list[7])+",{%}\n")
    f.write("Rainfall-Runoff - Groundwater Properties - Daily Baseflow Rate (%),"+str(parameter_list[8])+",{%}\n")
    f.write("Rainfall-Runoff - Groundwater Properties - Daily Deep Seepage Rate (%),"+str(parameter_list[9])+",{%}\n")
    f.write("Total Suspended Solids - Base Flow Concentration - Mean (log mg/L),1.1,{log mg/L}\n")
    f.write("Total Suspended Solids - Base Flow Concentration - Std Dev (log mg/L),0.17,{log mg/L}\n")
    f.write("Total Suspended Solids - Base Flow Concentration - Estimation Method,1,{Index from 0 to 1 for \"Mean\" | \"Stochastically generated\"}\n")
    f.write("Total Suspended Solids - Base Flow Concentration - Serial Correlation (R squared),0,{R squared}\n")
    f.write("Total Suspended Solids - Storm Flow Concentration - Mean (log mg/L),2.2,{log mg/L}\n")
    f.write("Total Suspended Solids - Storm Flow Concentration - Std Dev (log mg/L),0.32,{log mg/L}\n")
    f.write("Total Suspended Solids - Storm Flow Concentration - Estimation Method,1,{Index from 0 to 1 for \"Mean\" | \"Stochastically generated\"}\n")
    f.write("Total Suspended Solids - Storm Flow Concentration - Serial Correlation (R squared),0,{R squared}\n")
    f.write("Total Phosphorus - Base Flow Concentration - Mean (log mg/L),-0.82,{log mg/L}\n")
    f.write("Total Phosphorus - Base Flow Concentration - Std Dev (log mg/L),0.19,{log mg/L}\n")
    f.write("Total Phosphorus - Base Flow Concentration - Estimation Method,1,{Index from 0 to 1 for \"Mean\" | \"Stochastically generated\"}\n")
    f.write("Total Phosphorus - Base Flow Concentration - Serial Correlation (R squared),0,{R squared}\n")
    f.write("Total Phosphorus - Storm Flow Concentration - Mean (log mg/L),-0.45,{log mg/L}\n")
    f.write("Total Phosphorus - Storm Flow Concentration - Std Dev (log mg/L),0.25,{log mg/L}\n")
    f.write("Total Phosphorus - Storm Flow Concentration - Estimation Method,1,{Index from 0 to 1 for \"Mean\" | \"Stochastically generated\"}\n")
    f.write("Total Phosphorus - Storm Flow Concentration - Serial Correlation (R squared),0,{R squared}\n")
    f.write("Total Nitrogen - Base Flow Concentration - Mean (log mg/L),0.32,{log mg/L}\n")
    f.write("Total Nitrogen - Base Flow Concentration - Std Dev (log mg/L),0.12,{log mg/L}\n")
    f.write("Total Nitrogen - Base Flow Concentration - Estimation Method,1,{Index from 0 to 1 for \"Mean\" | \"Stochastically generated\"}\n")
    f.write("Total Nitrogen - Base Flow Concentration - Serial Correlation (R squared),0,{R squared}\n")
    f.write("Total Nitrogen - Storm Flow Concentration - Mean (log mg/L),0.42,{log mg/L}\n")
    f.write("Total Nitrogen - Storm Flow Concentration - Std Dev (log mg/L),0.19,{log mg/L}\n")
    f.write("Total Nitrogen - Storm Flow Concentration - Estimation Method,1,{Index from 0 to 1 for \"Mean\" | \"Stochastically generated\"}\n")
    f.write("Total Nitrogen - Storm Flow Concentration - Serial Correlation (R squared),0,{R squared}\n")
    f.write("------------------------------------------------------------------------------------\n")
    return True

def writeMUSICnodeWSUR(f, ID, nodepart, ncount, x, y, parameter_list):
    #parameter_list = [50, 1, 50, 0, 200]                #[Asurface, EDD, Perm. Pool Vol, Exfil Rate, Pipe Diameter]
    f.write("Node Type,WetlandNode,{Node Type}\n")
    f.write("Node Name,WSUR"+str(ID)+str(nodepart)+",{Node Name}\n")
    f.write("Node ID,"+str(ncount)+",{Node ID}\n")
    f.write("Coordinates,"+str(x)+":"+str(y)+",{Coordinates}{X:Y}\n")
    f.write("General - Location,WSUR"+str(ID)+str(nodepart)+",\n")
    f.write("General - Notes,,\n")
    f.write("General - Fluxes,,\n")
    f.write("Stormwater Re-use - Use stored water for irrigation or other purpose,1,\n")
    f.write("Stormwater Re-use - Annual Demand (kL/yr) Scaled by Daily: PET,-9999,{kL/yr}\n")
    f.write("Stormwater Re-use - Annual Demand (kk/yr) Scaled by Daily: PET - Rain,-9999,{kk/yr}\n")
    f.write("Stormwater Re-use - Daily Demand (kL/day),-9999000,{kL/day}\n")
    f.write("Stormwater Re-use - User-defined distribution of Annual Demand (ML/yr),-9999,{ML/yr}\n")
    f.write("Stormwater Re-use - User-defined time series,,\n")
    f.write("Inlet Properties - Low Flow By-pass (cubic metres per sec),0,{cubic metres per sec}\n")
    f.write("Inlet Properties - High Flow By-pass (cubic metres per sec),100,{cubic metres per sec}\n")
    f.write("Inlet Properties - Inlet Pond Volume (cubic metres),0,{cubic metres}\n")
    f.write("Storage Properties - Surface Area (square metres),"+str(parameter_list[0])+",{square metres}\n") #----------------#BEGIN OF PARAMETER LIST
    f.write("Storage Properties - Extended Detention Depth (metres),"+str(parameter_list[1])+",{metres}\n")
    f.write("Storage Properties - Permanent Pool Volume (cubic metres),"+str(parameter_list[2])+",{cubic metres}\n")
    f.write("Storage Properties - Exfiltration Rate (mm/hr),"+str(parameter_list[3])+",{mm/hr}\n")
    f.write("Storage Properties - Evaporative Loss as % of PET,125,\n")
    f.write("Outlet Properties - Equivalent Pipe Diameter (mm),"+str(parameter_list[4])+",{mm}\n")
    f.write("Outlet Properties - Overflow Weir Width (metres),3,{metres}\n")
    f.write("Outlet Properties - Notional Detention Time (hrs),0.149022412970911,{hrs}\n")
    f.write("Advanced Properties - Orifice Discharge Coefficient,0.6,\n")
    f.write("Advanced Properties - Weir Coefficient,1.7,\n")
    f.write("Advanced Properties - Number of CSTR Cells,4,\n")
    f.write("Advanced Properties - Total Suspended Solids - k (m/yr),1500,{m/yr}\n")
    f.write("Advanced Properties - Total Suspended Solids - C* (mg/L),6,{mg/L}\n")
    f.write("Advanced Properties - Total Suspended Solids - C** (mg/L),6,{mg/L}\n")
    f.write("Advanced Properties - Total Phosphorus - k (m/yr),1000,{m/yr}\n")
    f.write("Advanced Properties - Total Phosphorus - C* (mg/L),0.06,{mg/L}\n")
    f.write("Advanced Properties - Total Phosphorus - C** (mg/L),0.06,{mg/L}\n")
    f.write("Advanced Properties - Total Nitrogen - k (m/yr),150,{m/yr}\n")
    f.write("Advanced Properties - Total Nitrogen - C* (mg/L),1,{mg/L}\n")
    f.write("Advanced Properties - Total Nitrogen - C** (mg/L),1,{mg/L}\n")
    f.write("Advanced Properties - Threshold Hydraulic Loading for C** (m/yr),3500,{m/yr}\n")
    f.write("Advanced Properties - User Defined Storage-Discharge-Height,,\n")
    f.write("------------------------------------------------------------------------------------\n")
    return True

def writeMUSICnodePB(f, ID, nodepart, ncount, x, y, parameter_list):
    #parameter_list = [50, 2, 50, 0, 300]        #[Asurface, EDD, Perm. Pool Vol, Exfil Rate, Pipe Diameter]
    f.write("Node Type,PondNode,{Node Type}\n")
    f.write("Node Name,PB"+str(ID)+str(nodepart)+",{Node Name}\n")
    f.write("Node ID,"+str(ncount)+",{Node ID}\n")
    f.write("Coordinates,"+str(x)+":"+str(y)+",{Coordinates}{X:Y}\n")
    f.write("General - Location,PB"+str(ID)+str(nodepart)+",\n")
    f.write("General - Notes,,\n")
    f.write("General - Fluxes,,\n")
    f.write("Stormwater Re-use - Use stored water for irrigation or other purpose,1,\n")
    f.write("Stormwater Re-use - Annual Demand (kL/yr) Scaled by Daily: PET,-9999,{kL/yr}\n")
    f.write("Stormwater Re-use - Annual Demand (kk/yr) Scaled by Daily: PET - Rain,-9999,{kk/yr}\n")
    f.write("Stormwater Re-use - Daily Demand (kL/day),-9999000,{kL/day}\n")
    f.write("Stormwater Re-use - User-defined distribution of Annual Demand (ML/yr),-9999,{ML/yr}\n")
    f.write("Stormwater Re-use - User-defined time series,,\n")
    f.write("Inlet Properties - Low Flow By-pass (cubic metres per sec),0,{cubic metres per sec}\n")
    f.write("Inlet Properties - High Flow By-pass (cubic metres per sec),100,{cubic metres per sec}\n")
    f.write("Storage and Infiltration Properties - Surface Area (square metres),"+str(parameter_list[0])+",{square metres}\n") #----------------#BEGIN OF PARAMETER LIST
    f.write("Storage and Infiltration Properties - Extended Detention Depth (metres),"+str(parameter_list[1])+",{metres}\n")
    f.write("Storage and Infiltration Properties - Permanent Pool Volume (cubic metres),"+str(parameter_list[2])+",{cubic metres}\n")
    f.write("Storage and Infiltration Properties - Exfiltration Rate (mm/hr),"+str(parameter_list[3])+",{mm/hr}\n")
    f.write("Storage and Infiltration Properties - Evaporative Loss as % of PET,100,\n")
    f.write("Outlet Properties - Equivalent Pipe Diameter (mm),"+str(parameter_list[3])+",{mm}\n")
    f.write("Outlet Properties - Overflow Weir Width (metres),2,{metres}\n")
    f.write("Outlet Properties - Notional Detention Time (hrs),0.0936664522315673,{hrs}\n")
    f.write("Advanced Properties - Orifice Discharge Coefficient,0.6,\n")
    f.write("Advanced Properties - Weir Coefficient,1.7,\n")
    f.write("Advanced Properties - Number of CSTR Cells,2,\n")
    f.write("Advanced Properties - Total Suspended Solids - k (m/yr),400,{m/yr}\n")
    f.write("Advanced Properties - Total Suspended Solids - C* (mg/L),12,{mg/L}\n")
    f.write("Advanced Properties - Total Suspended Solids - C** (mg/L),12,{mg/L}\n")
    f.write("Advanced Properties - Total Phosphorus - k (m/yr),300,{m/yr}\n")
    f.write("Advanced Properties - Total Phosphorus - C* (mg/L),0.09,{mg/L}\n")
    f.write("Advanced Properties - Total Phosphorus - C** (mg/L),0.09,{mg/L}\n")
    f.write("Advanced Properties - Total Nitrogen - k (m/yr),40,{m/yr}\n")
    f.write("Advanced Properties - Total Nitrogen - C* (mg/L),1,{mg/L}\n")
    f.write("Advanced Properties - Total Nitrogen - C** (mg/L),1,{mg/L}\n")
    f.write("Advanced Properties - Threshold Hydraulic Loading for C** (m/yr),3500,{m/yr}\n")
    f.write("Advanced Properties - User Defined Storage-Discharge-Height,,\n")
    f.write("------------------------------------------------------------------------------------\n")
    return True

def writeMUSICnodeIS(f, ID, nodepart, ncount, x, y, parameter_list):
    #parameter_list = [10, 0.2, 10, 14, 1, 100]                  #[pond_area, EDD, filter area, unlined filter perimeter, depth, exfil rate]
    f.write("Node Type,InfiltrationSystemNodeV4,{Node Type}\n")
    f.write("Node Name,IS"+str(ID)+str(nodepart)+",{Node Name}\n")
    f.write("Node ID,"+str(ncount)+",{Node ID}\n")
    f.write("Coordinates,"+str(x)+":"+str(y)+",{Coordinates}{X:Y}\n")
    f.write("General - Location,IS"+str(ID)+str(nodepart)+",\n")
    f.write("General - Notes,,\n")
    f.write("General - Fluxes,,\n")
    f.write("Inlet Properties - Low Flow By-pass (cubic metres per sec),0,{cubic metres per sec}\n")
    f.write("Inlet Properties - High Flow By-pass (cubic metres per sec),100,{cubic metres per sec}\n")
    f.write("Storage and Infiltration Properties - Pond Surface Area (square metres),"+str(parameter_list[0])+",{square metres}\n")
    f.write("Storage and Infiltration Properties - Extended Detention Depth (metres),"+str(parameter_list[1])+",{metres}\n")
    f.write("Storage and Infiltration Properties - Filter Area (square metres),"+str(parameter_list[2])+",{square metres}\n")
    f.write("Storage and Infiltration Properties - Unlined Filter Media Perimeter (metres),"+str(parameter_list[3])+",{metres}\n")
    f.write("Storage and Infiltration Properties - Depth of Infiltration Media (metres),"+str(parameter_list[4])+",{metres}\n")
    f.write("Storage and Infiltration Properties - Exfiltration Rate (mm/hr),"+str(parameter_list[5])+",{mm/hr}\n")
    f.write("Storage and Infiltration Properties - Evaporative Loss as % of PET,100,\n")
    f.write("Outlet Properties - Overflow Weir Width (metres),2,{metres}\n")
    f.write("Advanced Properties - Weir Coefficient,1.7,\n")
    f.write("Advanced Properties - Number of CSTR Cells,1,\n")
    f.write("Advanced Properties - Total Suspended Solids - k (m/yr),400,{m/yr}\n")
    f.write("Advanced Properties - Total Suspended Solids - C* (mg/L),12,{mg/L}\n")
    f.write("Advanced Properties - Total Suspended Solids - C** (mg/L),12,{mg/L}\n")
    f.write("Advanced Properties - Total Phosphorus - k (m/yr),300,{m/yr}\n")
    f.write("Advanced Properties - Total Phosphorus - C* (mg/L),0.09,{mg/L}\n")
    f.write("Advanced Properties - Total Phosphorus - C** (mg/L),0.09,{mg/L}\n")
    f.write("Advanced Properties - Total Nitrogen - k (m/yr),40,{m/yr}\n")
    f.write("Advanced Properties - Total Nitrogen - C* (mg/L),1,{mg/L}\n")
    f.write("Advanced Properties - Total Nitrogen - C** (mg/L),1,{mg/L}\n")
    f.write("Advanced Properties - Threshold Hydraulic Loading for C** (m/yr),3500,{m/yr}\n")
    f.write("Advanced Properties - Porosity of Infiltration Media,0.35,\n")
    f.write("Advanced Properties - Horizontal Flow Coefficient,3,\n")
    f.write("Advanced Properties - User Defined Storage-Discharge-Height,,\n")
    f.write("------------------------------------------------------------------------------------\n")
    return True

def writeMUSICnodeBF(f, ID, nodepart, ncount, x, y, parameter_list):
    #parameter_list = [0.2, 10, 10, 14, 100, 0.5, 0]             #EDD, Asystem, FilterArea, UnlinedPerimeter, ksat, depth, exfil rate]
    f.write("Node Type,BioRetentionNodeV4,{Node Type}\n")
    f.write("Node Name,BF"+str(ID)+str(nodepart)+",{Node Name}\n")
    f.write("Node ID,"+str(ncount)+",{Node ID}\n")
    f.write("Coordinates,"+str(x)+":"+str(y)+",{Coordinates}{X:Y}\n")
    f.write("General - Location,BF"+str(ID)+str(nodepart)+",\n")
    f.write("General - Notes,,\n")
    f.write("General - Fluxes,,\n")
    f.write("Inlet Properties - Low Flow By-pass (cubic metres per sec),0,{cubic metres per sec}\n")
    f.write("Inlet Properties - High Flow By-pass (cubic metres per sec),100,{cubic metres per sec}\n")
    f.write("Storage Properties - Extended Detention Depth (metres),"+str(parameter_list[0])+",{metres}\n")
    f.write("Storage Properties - Surface Area (square metres),"+str(parameter_list[1])+",{square metres}\n")
    f.write("Filter and Media Properties - Filter Area (square metres),"+str(parameter_list[2])+",{square metres}\n")
    f.write("Filter and Media Properties - Unlined Filter Media Perimeter (metres),"+str(parameter_list[3])+",{metres}\n")
    f.write("Filter and Media Properties - Saturated Hydraulic Conductivity (mm/hr),"+str(parameter_list[4])+",{mm/hr}\n")
    f.write("Filter and Media Properties - Filter Depth (metres),"+str(parameter_list[5])+",{metres}\n")
    f.write("Filter and Media Properties - TN Content of Filter Media (mg/kg),800,{mg/kg}\n")
    f.write("Filter and Media Properties - Orthophosphate Content of Filter Media (mg/kg),80,{mg/kg}\n")
    f.write("Infiltration Properties - Exfiltration Rate (mm/hr),"+str(parameter_list[6])+",{mm/hr}\n")
    f.write("Lining Properties - Base Lined,0,\n")
    f.write("Vegetation Properties - Vegetation Properties,0,{Index from 0 to 2 for \"Vegetated with Effective Nutrient Removal Plants\" | \"Vegetated with Ineffective Nutrient Removal Plants\" | \"Unvegetated\"}\n")
    f.write("Outlet Properties - Overflow Weir Width (metres),2,{metres}\n")
    f.write("Outlet Properties - Underdrain Present,1,\n")
    f.write("Outlet Properties - Submerged Zone With Carbon Present,1,\n")
    f.write("Outlet Properties - Submerged Zone Depth (metres),0.45,{metres}\n")
    f.write("Advanced Properties - Total Suspended Solids - k (m/yr),8000,{m/yr}\n")
    f.write("Advanced Properties - Total Suspended Solids - C* (mg/L),20,{mg/L}\n")
    f.write("Advanced Properties - Total Phosphorus - k (m/yr),6000,{m/yr}\n")
    f.write("Advanced Properties - Total Phosphorus - C* (mg/L),0.13,{mg/L}\n")
    f.write("Advanced Properties - Total Nitrogen - k (m/yr),500,{m/yr}\n")
    f.write("Advanced Properties - Total Nitrogen - C* (mg/L),1.4,{mg/L}\n")
    f.write("Advanced Properties - Filter Media Soil Type,1,{Index from 0 to 4 for \"Sand\" | \"Loamy Sand\" | \"Sandy Loam\" | \"Silt Loam\" | \"Loam\"}\n")
    f.write("Advanced Properties - Weir Coefficient,1.7,\n")
    f.write("Advanced Properties - Number of CSTR Cells,3,\n")
    f.write("Advanced Properties - Porosity of Filter Media,0.35,\n")
    f.write("Advanced Properties - Porosity of Submerged Zone,0.35,\n")
    f.write("Advanced Properties - Horizontal Flow Coefficient,3,\n")
    f.write("------------------------------------------------------------------------------------\n")
    return True

def writeMUSICnodeSW(f, ID, nodepart, ncount, x, y, parameter_list):
    #parameter_list = [100,3,1,5,0.5,0.25,0]                     #[length, bedslope, Wbase, Wtop, depth, veg.height, exfilrate]
    f.write("Node Type,SwaleNode,{Node Type}\n")
    f.write("Node Name,SW"+str(ID)+str(nodepart)+",{Node Name}\n")
    f.write("Node ID,"+str(ncount)+",{Node ID}\n")
    f.write("Coordinates,"+str(x)+":"+str(y)+",{Coordinates}{X:Y}\n")
    f.write("General - Location,SW"+str(ID)+str(nodepart)+",\n")
    f.write("General - Notes,,\n")
    f.write("General - Fluxes,,\n")
    f.write("Inlet Properties - Low Flow By-pass (cubic metres per sec),0,{cubic metres per sec}\n")
    f.write("Storage Properties - Length (metres),"+str(parameter_list[0])+",{metres}\n")
    f.write("Storage Properties - Bed Slope (%),"+str(parameter_list[1])+",{%}\n")
    f.write("Storage Properties - Base Width (metres),"+str(parameter_list[2])+",{metres}\n")
    f.write("Storage Properties - Top Width (metres),"+str(parameter_list[3])+",{metres}\n")
    f.write("Storage Properties - Depth (metres),"+str(parameter_list[4])+",{metres}\n")
    f.write("Storage Properties - Vegetation Height (metres),"+str(parameter_list[5])+",{metres}\n")
    f.write("Storage Properties - Exfiltration Rate (mm/hr),"+str(parameter_list[6])+",{mm/hr}\n")
    f.write("Advanced Properties - Number of CSTR Cells,10,\n")
    f.write("Advanced Properties - Total Suspended Solids - k (m/yr),8000,{m/yr}\n")
    f.write("Advanced Properties - Total Suspended Solids - C* (mg/L),20,{mg/L}\n")
    f.write("Advanced Properties - Total Suspended Solids - C** (mg/L),14,{mg/L}\n")
    f.write("Advanced Properties - Total Phosphorus - k (m/yr),6000,{m/yr}\n")
    f.write("Advanced Properties - Total Phosphorus - C* (mg/L),0.13,{mg/L}\n")
    f.write("Advanced Properties - Total Phosphorus - C** (mg/L),0.13,{mg/L}\n")
    f.write("Advanced Properties - Total Nitrogen - k (m/yr),500,{m/yr}\n")
    f.write("Advanced Properties - Total Nitrogen - C* (mg/L),1.4,{mg/L}\n")
    f.write("Advanced Properties - Total Nitrogen - C** (mg/L),1.4,{mg/L}\n")
    f.write("Advanced Properties - Threshold Hydraulic Loading for C** (m/yr),3500,{m/yr}\n")
    f.write("------------------------------------------------------------------------------------\n")
    return True

def writeMUSIClink(f, upN, downN):
    f.write("Link Name,Drainage Link,\n")
    f.write("Source Node ID,"+str(upN)+",{The is the ID of the upstream node}\n")
    f.write("Target Node ID,"+str(downN)+",{This is the ID of the downstream node}\n")
    f.write("Routing,Not Routed,{either \"Not Routed\" or \"Routed\"}\n")
    f.write("Muskingum K,30,{no value required for no routing or \"numerical value\" for routed}\n")
    f.write("Muskingum Theta,0.25,{no value required for no routing or \"numerical value\" for routed. Must be between 0.1 and 0.49}\n")
    f.write("------------------------------------------------------------------------------------\n")
    return True

def writeMUSICjunction(f, ID, ncount, x, y):
    f.write("Node Type,JunctionNode,{Node Type}\n")
    f.write("Node Name,Block"+str(ID)+"J,{Node Name}\n")
    f.write("Node ID,"+str(ncount)+",{Node ID}\n")
    f.write("Coordinates,"+str(x)+":"+str(y)+",{Coordinates}{X:Y}\n")
    f.write("General - Location,Block"+str(ID)+"J,\n")
    f.write("General - Notes,,\n")
    f.write("------------------------------------------------------------------------------------\n")
    return True

def writeMUSICreceiving(f, ID, ncount, x, y):
    f.write("Node Type,ReceivingNode,{Node Type}\n")
    f.write("Node Name,Receiving Node,{Node Name}\n")
    f.write("Node ID,"+str(ncount)+",{Node ID}\n")
    f.write("Coordinates,"+str(x)+":"+str(y)+",{Coordinates}{X:Y}\n")
    f.write("General - Location,Receiving Node,\n")
    f.write("General - Notes,,\n")
    f.write("------------------------------------------------------------------------------------\n")
    return True

def writeMUSICfooter(f):
    f.write("====================================================================================\n")
    f.close()
    return True
