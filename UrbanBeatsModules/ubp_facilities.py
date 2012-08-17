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
#from pyvibe import *
from pydynamind import *
import random
import math

class ubp_facilities(Module):
    """Description of class
	
    Description of Inputs & Outputs 
	- <description of inputs/outputs>
    
    Log of Updates made at each version:
    
    v0.80 (March 2012):
        - Created ubp_facilities.py
        - Contains the code that used to be in urbplanbb.py for Municipal and Other Transport facilities
        - Now handles the these districts that urbplanbb.py initially did for more modularity
    
	@ingroup DAnCE4Water
	@author Peter M Bach
	"""
    def __init__(self):
        Module.__init__(self)
        #input/output data - each planning module has as input BLOCKS, PATCHES, RULES
        #                  - each planning module has as output: updated BLOCKS
        #                  - PATCHES are passed on from UrbplanBB straight through (not modified)
	self.blocks = View("Block",FACE,READ)
	self.blocks.getAttribute("BlockID")

	self.mapattributes = View("Mapattributes",COMPONENT,READ)
    	self.mapattributes.getAttribute("NumBlocks")
	self.mapattributes.getAttribute("BlockSize")
	self.mapattributes.getAttribute("WidthBlocks")
	self.mapattributes.getAttribute("HeightBlocks")
	self.mapattributes.getAttribute("InputReso")	

	self.planGen = View("PlanGen",COMPONENT,READ)
	self.planGen.getAttribute("maximperv")
	self.planGen.getAttribute("maxsitecover")
	self.planGen.getAttribute("locality_mun_trans")
	
	self.planFacilities = View("PlanFacilities",COMPONENT,READ)
	self.planFacilities.getAttribute("mun_explicit")           
        self.planFacilities.getAttribute("edu_school")             
        self.planFacilities.getAttribute("edu_uni")                  
        self.planFacilities.getAttribute("edu_lib")                
        
        self.planFacilities.getAttribute("civ_hospital")           
        self.planFacilities.getAttribute("civ_clinic")             
        self.planFacilities.getAttribute("civ_police")             
        self.planFacilities.getAttribute("civ_fire")               
        self.planFacilities.getAttribute("civ_jail")               
        self.planFacilities.getAttribute("civ_worship")               
        self.planFacilities.getAttribute("civ_leisure")              
        self.planFacilities.getAttribute("civ_museum")               
        self.planFacilities.getAttribute("civ_zoo")                  
        self.planFacilities.getAttribute("civ_stadium")              
        self.planFacilities.getAttribute("civ_racing")               
        self.planFacilities.getAttribute("civ_cemetery")             
        
        self.planFacilities.getAttribute("sut_waste")                   
        self.planFacilities.getAttribute("sut_gas")                     
        self.planFacilities.getAttribute("sut_electricity")      
        self.planFacilities.getAttribute("sut_water")            
        self.planFacilities.getAttribute("sut_lgoffice")         
        
        self.planFacilities.getAttribute("trans_explicit")       
        self.planFacilities.getAttribute("trans_airport")        
        self.planFacilities.getAttribute("trans_comseaport")    
        self.planFacilities.getAttribute("trans_indseaport")    
        self.planFacilities.getAttribute("trans_busdepot")      
        self.planFacilities.getAttribute("trans_railterminal") 

	self.planNonres = View("PlanNonres",COMPONENT,READ)
        self.planNonres.getAttribute("lscape_hsbal")                 
        self.planNonres.getAttribute("lscape_avgimp_dced")	   	

	self.planSpaces = View("PlanSpaces",COMPONENT,READ)
	self.planSpaces.getAttribute("w_comfootpath_min")
	self.planSpaces.getAttribute("w_comfootpath_max")
	self.planSpaces.getAttribute("w_comnaturestrip_min")
	self.planSpaces.getAttribute("w_comnaturestrip_max")
	self.planSpaces.getAttribute("w_comfootpath_med")
	self.planSpaces.getAttribute("w_comnaturestrip_med")
	self.planSpaces.getAttribute("w_collectlane_min")
	self.planSpaces.getAttribute("w_collectlane_max")
	self.planSpaces.getAttribute("w_collectlane_med")
	self.planSpaces.getAttribute("collect_crossfall")


	self.facilitiesAttr = View("Facilities",COMPONENT,WRITE)
	self.facilitiesAttr.addAttribute("BlockID")
	self.facilitiesAttr.addAttribute("HasFacilities")
	self.facilitiesAttr.addAttribute("MunATot")
	self.facilitiesAttr.addAttribute("MunAimp")
	self.facilitiesAttr.addAttribute("MunAeimp")
	self.facilitiesAttr.addAttribute("MunAperv")
	self.facilitiesAttr.addAttribute("MunAroof")
	self.facilitiesAttr.addAttribute("MinTIF")
	self.facilitiesAttr.addAttribute("MinEIF")
	self.facilitiesAttr.addAttribute("TrATot")
	self.facilitiesAttr.addAttribute("TrAimp")
	self.facilitiesAttr.addAttribute("TrAeimp")
	self.facilitiesAttr.addAttribute("TrAperv")
	self.facilitiesAttr.addAttribute("TrAroof")
	self.facilitiesAttr.addAttribute("TrTIF")
	self.facilitiesAttr.addAttribute("TrEIF")

	#Datastream
	datastream = []
	datastream.append(self.blocks)
	datastream.append(self.mapattributes)
	datastream.append(self.planGen)
	datastream.append(self.planFacilities)
	datastream.append(self.planNonres)
	datastream.append(self.facilitiesAttr)
	datastream.append(self.planSpaces)
	self.addData("City", datastream)
	self.BLOCKIDtoUUID = {}

    def getBlockUUID(self, blockid,city):
	try:
		key = self.BLOCKIDtoUUID[blockid]
	except KeyError:
		key = ""
	return city.getFace(key)


    def initBLOCKIDtoUUID(self, city):
	blockuuids = city.getUUIDsOfComponentsInView(self.blocks)
        for blockuuid in blockuuids:
            block = city.getFace(blockuuid)
            ID = int(round(block.getAttribute("BlockID").getDouble()))
	    self.BLOCKIDtoUUID[ID] = blockuuid

    def run(self):
        city = self.getData("City")
	self.initBLOCKIDtoUUID(city)
	

	#Get Vector Data        
	strvec = city.getUUIDsOfComponentsInView(self.mapattributes)        
	map_attr = city.getComponent(strvec[0])  #GET map attributes
        
        #Get some Parameters
        blocks_num = map_attr.getAttribute("NumBlocks").getDouble()     #number of blocks to loop through
        blocks_size = map_attr.getAttribute("BlockSize").getDouble()    #size of block
        map_w = map_attr.getAttribute("WidthBlocks").getDouble()        #num of blocks wide
        map_h = map_attr.getAttribute("HeightBlocks").getDouble()       #num of blocks tall
        input_res = map_attr.getAttribute("InputReso").getDouble()      #resolution of input data

        
        
        #--------------------------------------------------------------------------------#
        #       DISASSEMBLE PLANNING RULES INTO USABLE FORMAT FROM PREVIOUS MODULE       #
        #--------------------------------------------------------------------------------#
	strvec = city.getUUIDsOfComponentsInView(self.planGen)        
	plan_gen = city.getComponent(strvec[0])
        
        maximperv = plan_gen.getAttribute("maximperv").getDouble()                          #DOUBLE -- maximum site imperviousness [%]
        maxsitecover = plan_gen.getAttribute("maxsitecover").getDouble()                    #DOUBLE -- maximum site cover [%]
        lcality_mun_trans = bool(plan_gen.getAttribute("locality_mun_trans"))         	    #BOOL -- locality map for municipal & transport?
        
        #===-----------------
	strvec = city.getUUIDsOfComponentsInView(self.planFacilities)    
        plan_facilities = city.getComponent(strvec[0])
        
        mun_explicit = bool(plan_facilities.getAttribute("mun_explicit"))             #BOOL
        edu_school = bool(plan_facilities.getAttribute("edu_school"))                 #BOOL
        edu_uni = bool(plan_facilities.getAttribute("edu_uni"))                       #BOOL  
        edu_lib = bool(plan_facilities.getAttribute("edu_lib"))                       #BOOL
        
        civ_hospital = bool(plan_facilities.getAttribute("civ_hospital"))             #BOOL
        civ_clinic = bool(plan_facilities.getAttribute("civ_clinic"))                 #BOOL
        civ_police = bool(plan_facilities.getAttribute("civ_police"))                 #BOOL
        civ_fire = bool(plan_facilities.getAttribute("civ_fire"))                     #BOOL
        civ_jail = bool(plan_facilities.getAttribute("civ_jail"))                     #BOOL
        civ_worship = bool(plan_facilities.getAttribute("civ_worship"))               #BOOL
        civ_leisure = bool(plan_facilities.getAttribute("civ_leisure"))               #BOOL
        civ_museum = bool(plan_facilities.getAttribute("civ_museum"))                 #BOOL
        civ_zoo = bool(plan_facilities.getAttribute("civ_zoo"))                       #BOOL
        civ_stadium = bool(plan_facilities.getAttribute("civ_stadium"))               #BOOL
        civ_racing = bool(plan_facilities.getAttribute("civ_racing"))                 #BOOL
        civ_cemetery = bool(plan_facilities.getAttribute("civ_cemetery"))             #BOOL
        
        sut_waste = bool(plan_facilities.getAttribute("sut_waste"))                   #BOOL
        sut_gas = bool(plan_facilities.getAttribute("sut_gas"))                       #BOOL
        sut_electricity = bool(plan_facilities.getAttribute("sut_electricity"))       #BOOL
        sut_water = bool(plan_facilities.getAttribute("sut_water"))                   #BOOL
        sut_lgoffice = bool(plan_facilities.getAttribute("sut_lgoffice"))             #BOOL
        
        trans_explicit = bool(plan_facilities.getAttribute("trans_explicit"))         #BOOL
        trans_airport = bool(plan_facilities.getAttribute("trans_airport"))           #BOOL
        trans_comseaport = bool(plan_facilities.getAttribute("trans_comseaport"))     #BOOL
        trans_indseaport = bool(plan_facilities.getAttribute("trans_indseaport"))     #BOOL
        trans_busdepot = bool(plan_facilities.getAttribute("trans_busdepot"))         #BOOL
        trans_railterminal = bool(plan_facilities.getAttribute("trans_railterminal")) #BOOL
        
        #===-----------------
        
	strvec = city.getUUIDsOfComponentsInView(self.planNonres)
        plan_nonres = city.getComponent(strvec[0])
        
        lscape_hsbal = plan_nonres.getAttribute("lscape_hsbal").getDouble()                 #DOUBLE -- balance between hard & soft landscapes
        lscape_avgimp_dced = plan_nonres.getAttribute("lscape_avgimp_dced").getDouble()     #DOUBLE -- avg. imperviousness disconnected
        
        #===-----------------
        
	strvec = city.getUUIDsOfComponentsInView(self.planSpaces)
        plan_space = city.getComponent(strvec[0])
        
        w_comfootpath_min = plan_space.getAttribute("w_comfootpath_min").getDouble()         #DOUBLE
        w_comfootpath_max = plan_space.getAttribute("w_comfootpath_max").getDouble()         #DOUBLE
        w_comnaturestrip_min = plan_space.getAttribute("w_comnaturestrip_min").getDouble()   #DOUBLE
        w_comnaturestrip_max = plan_space.getAttribute("w_comnaturestrip_max").getDouble()   #DOUBLE
        w_comfootpath_med = bool(plan_space.getAttribute("w_comfootpath_med"))        	     #BOOL -- to simplify things, just use median footpath width?
        w_comnaturestrip_med = bool(plan_space.getAttribute("w_comnaturestrip_med"))  	     #BOOL -- to simplify things, just use median naturestrip width?
        
        w_collectlane_min = plan_space.getAttribute("w_collectlane_min").getDouble()         #DOUBLE
        w_collectlane_max = plan_space.getAttribute("w_collectlane_max").getDouble()         #DOUBLE
        w_collectlane_med = bool(plan_space.getAttribute("w_collectlane_med"))   	     #BOOL
        collect_crossfall = plan_space.getAttribute("collect_crossfall").getDouble()         #DOUBLE
        
        
        #--------------------------------------------------------------------------------#
        #       BEGIN LOOPING ACROSS ALL BLOCKS IN MAP                                   #
        #--------------------------------------------------------------------------------#
        
        for i in range(int(blocks_num)):
            currentID = i + 1
            currentAttList = self.getBlockUUID(currentID,city)#blockcityin.getAttributes("BlockID"+str(currentID))        #attribute list of current block structure
            #currentPatchList = patchcityin.getAttributes("PatchDataID"+str(currentID))
            facilities_attr = Component()
	    city.addComponent(facilities_attr,self.facilitiesAttr)
            facilities_attr.addAttribute("BlockID", currentID)
            block_AActive = blocks_size * blocks_size * (currentAttList.getAttribute("Activity").getDouble()/100)

            #--------------------------------------------------------------------------------#
            #            CONDITIONAL CHECK TO SEE IF CURRENT BLOCK IS RELEVANT               #
            #--------------------------------------------------------------------------------#
            block_status = currentAttList.getAttribute("Status").getDouble()
	    landclassvec = currentAttList.getAttribute("Area_Landclass").getDoubleVector()
 
            tot_facilities_area = landclassvec[5] + landclassvec[6] \
                + landclassvec[7] + landclassvec[9]
            if block_status == 0 or tot_facilities_area == 0:           #2 conditions to skip: (1) status = 0, (2) no facilities
                print "BlockID"+str(currentID)+" is not active or has no relevant facilities area"
                continue
            #IF NOT SKIPPED, PLAN URBAN FORM
            facilities_attr.addAttribute("HasFacilities", 1)
            #--------------------------------------------------------------------------------#
            #            SETUP DATA - RETRIEVE FROM BLOCKCITY AND SAMPLE VALUES              #
            #--------------------------------------------------------------------------------#
            
            Edu_area_tot = float(landclassvec[5])       #Area of Education facilities
            HnC_area_tot = float(landclassvec[6])       #Area of Health & Community
            SnU_area_tot = float(landclassvec[7])       #Area of Services & Utilities
            
            mun_Atotal = Edu_area_tot + HnC_area_tot + SnU_area_tot             #Total Municipal Area
            
            tr_area_tot = float(landclassvec[9])         #Area of other transport facilities
            
            
            #--------------------------------------------------------------------------------#
            #            PIECE TOGETHER URBAN FORM                                           #
            #--------------------------------------------------------------------------------#
            
            ### MUNICIPAL >> ===========================================================================#
            
            #v0.75 simple solution for now:
                #   - assume education and civic buildings occupy maximum site cover and maximum imperviousness
                #   - assume services & utility occupies 50% imperviousness and half the max site cover
                #   - calculate only imperviousness, roof area and the fractions of total area and write these to attributes
            
            if mun_Atotal == 0:
                pass
            else:
                mun_Aimp = maximperv/100*(Edu_area_tot + HnC_area_tot)+0.5*(SnU_area_tot)
                mun_Aeimp = mun_Aimp * lscape_avgimp_dced
                mun_Aperv = mun_Atotal - mun_Aimp
                mun_Aroof = maxsitecover/100 *(Edu_area_tot + HnC_area_tot) + maxsitecover/200 * (SnU_area_tot)
                mun_TIF = mun_Aimp/mun_Atotal
                mun_EIF = mun_Aeimp/mun_Atotal
                
            
            ### OTHER TRANSPORTATION >> ===========================================================================#
            
            #v0.75 - Simple Solution
            #   - assume transport infrastructure has max imperviousness and site cover
            
            if tr_area_tot == 0:
                pass
            else:
                tr_Aimp = maximperv/100*tr_area_tot
                tr_Aeimp = tr_area_tot * lscape_avgimp_dced
                tr_Aperv = tr_area_tot - tr_Aimp
                tr_Aroof = maxsitecover/100 *tr_area_tot
                tr_TIF = tr_Aimp/tr_area_tot
                tr_EIF = tr_Aeimp/tr_area_tot
                
            
            #--------------------------------------------------------------------------------#
            #            TALLY UP INFO AND WRITE TO OUTPUT                                   #
            #--------------------------------------------------------------------------------#
            
            if mun_Atotal == 0:
                pass
            else:
                facilities_attr.addAttribute("MunATot", mun_Atotal)
                facilities_attr.addAttribute("MunAimp", mun_Aimp)
                facilities_attr.addAttribute("MunAeimp", mun_Aeimp)
                facilities_attr.addAttribute("MunAperv", mun_Aperv)
                facilities_attr.addAttribute("MunAroof", mun_Aroof)
                facilities_attr.addAttribute("MunTIF", mun_TIF)
                facilities_attr.addAttribute("MunEIF", mun_EIF)
            
            if tr_area_tot == 0:
                pass
            else:
                facilities_attr.addAttribute("TrATot", tr_area_tot)
                facilities_attr.addAttribute("TrAimp", tr_Aimp)
                facilities_attr.addAttribute("TrAeimp", tr_Aeimp)
                facilities_attr.addAttribute("TrAperv", tr_Aperv)
                facilities_attr.addAttribute("TrAroof", tr_Aroof)
                facilities_attr.addAttribute("TrTIF", tr_TIF)
                facilities_attr.addAttribute("TrEIF", tr_EIF)
                
            #-----------------------------------------------------------------#
            #        Write all updated Attribute Lists to the output          #
            #-----------------------------------------------------------------#
                
            #facilities.setAttributes("BlockID"+str(currentID),facilities_attr)
            
            #FOR LOOP END (Repeat for next BlockID)
            
        #END OF MODULE
    
            
