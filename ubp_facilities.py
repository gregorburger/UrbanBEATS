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
from pyvibe import *
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
        self.blockcityin = VectorDataIn
        self.facilities = VectorDataIn
        self.patchcityin = VectorDataIn
        self.planningrules = VectorDataIn
        self.addParameter(self, "blockcityin", VIBe2.VECTORDATA_IN)
        self.addParameter(self, "facilities", VIBe2.VECTORDATA_OUT)
        self.addParameter(self, "patchcityin", VIBe2.VECTORDATA_IN)
        self.addParameter(self, "planningrules", VIBe2.VECTORDATA_IN)
    
    
    def run(self):
        #Get Vector Data
        blockcityin = self.blockcityin.getItem()
        facilities = self.facilities.getItem()
        patchcityin = self.patchcityin.getItem()
        planningrules = self.planningrules.getItem()
        
        map_attr = blockcityin.getAttributes("MapAttributes")   #GET map attributes
        
        #Get some Parameters
        blocks_num = map_attr.getAttribute("NumBlocks")     #number of blocks to loop through
        blocks_size = map_attr.getAttribute("BlockSize")    #size of block
        map_w = map_attr.getAttribute("WidthBlocks")        #num of blocks wide
        map_h = map_attr.getAttribute("HeightBlocks")       #num of blocks tall
        input_res = map_attr.getAttribute("InputReso")      #resolution of input data
        urbansimdata = map_attr.getStringAttribute("UrbanSimData")
        
        
        #--------------------------------------------------------------------------------#
        #       DISASSEMBLE PLANNING RULES INTO USABLE FORMAT FROM PREVIOUS MODULE       #
        #--------------------------------------------------------------------------------#
        
        plan_gen = planningrules.getAttributes("GeneralRules")
        
        maximperv = plan_gen.getAttribute("maximperv")                          #DOUBLE -- maximum site imperviousness [%]
        maxsitecover = plan_gen.getAttribute("maxsitecover")                    #DOUBLE -- maximum site cover [%]
        lcality_mun_trans = plan_gen.getAttribute("locality_mun_trans")         #BOOL -- locality map for municipal & transport?
        
        #===-----------------

        plan_facilities = planningrules.getAttributes("FacilitiesRules")
        
        mun_explicit = plan_facilities.getAttribute("mun_explicit")             #BOOL
        edu_school = plan_facilities.getAttribute("edu_school")                 #BOOL
        edu_uni = plan_facilities.getAttribute("edu_uni")                       #BOOL  
        edu_lib = plan_facilities.getAttribute("edu_lib")                       #BOOL
        
        civ_hospital = plan_facilities.getAttribute("civ_hospital")             #BOOL
        civ_clinic = plan_facilities.getAttribute("civ_clinic")                 #BOOL
        civ_police = plan_facilities.getAttribute("civ_police")                 #BOOL
        civ_fire = plan_facilities.getAttribute("civ_fire")                     #BOOL
        civ_jail = plan_facilities.getAttribute("civ_jail")                     #BOOL
        civ_worship = plan_facilities.getAttribute("civ_worship")               #BOOL
        civ_leisure = plan_facilities.getAttribute("civ_leisure")               #BOOL
        civ_museum = plan_facilities.getAttribute("civ_museum")                 #BOOL
        civ_zoo = plan_facilities.getAttribute("civ_zoo")                       #BOOL
        civ_stadium = plan_facilities.getAttribute("civ_stadium")               #BOOL
        civ_racing = plan_facilities.getAttribute("civ_racing")                 #BOOL
        civ_cemetery = plan_facilities.getAttribute("civ_cemetery")             #BOOL
        
        sut_waste = plan_facilities.getAttribute("sut_waste")                   #BOOL
        sut_gas = plan_facilities.getAttribute("sut_gas")                       #BOOL
        sut_electricity = plan_facilities.getAttribute("sut_electricity")       #BOOL
        sut_water = plan_facilities.getAttribute("sut_water")                   #BOOL
        sut_lgoffice = plan_facilities.getAttribute("sut_lgoffice")             #BOOL
        
        trans_explicit = plan_facilities.getAttribute("trans_explicit")         #BOOL
        trans_airport = plan_facilities.getAttribute("trans_airport")           #BOOL
        trans_comseaport = plan_facilities.getAttribute("trans_comseaport")     #BOOL
        trans_indseaport = plan_facilities.getAttribute("trans_indseaport")     #BOOL
        trans_busdepot = plan_facilities.getAttribute("trans_busdepot")         #BOOL
        trans_railterminal = plan_facilities.getAttribute("trans_railterminal") #BOOL
        
        #===-----------------
        
        plan_nonres = planningrules.getAttributes("NonResRules")
        
        lscape_hsbal = plan_nonres.getAttribute("lscape_hsbal")                 #DOUBLE -- balance between hard & soft landscapes
        lscape_avgimp_dced = plan_nonres.getAttribute("lscape_avgimp_dced")     #DOUBLE -- avg. imperviousness disconnected
        
        #===-----------------
        
        plan_space = planningrules.getAttributes("SpacesRules")
        
        w_comfootpath_min = plan_space.getAttribute("w_comfootpath_min")        #DOUBLE
        w_comfootpath_max = plan_space.getAttribute("w_comfootpath_max")        #DOUBLE
        w_comnaturestrip_min = plan_space.getAttribute("w_comnaturestrip_min")  #DOUBLE
        w_comnaturestrip_max = plan_space.getAttribute("w_comnaturestrip_max")  #DOUBLE
        w_comfootpath_med = plan_space.getAttribute("w_comfootpath_med")        #BOOL -- to simplify things, just use median footpath width?
        w_comnaturestrip_med = plan_space.getAttribute("w_comnaturestrip_med")  #BOOL -- to simplify things, just use median naturestrip width?
        
        w_collectlane_min = plan_space.getAttribute("w_collectlane_min")        #DOUBLE
        w_collectlane_max = plan_space.getAttribute("w_collectlane_max")        #DOUBLE
        w_collectlane_med = plan_space.getAttribute("w_collectlane_med")        #BOOL
        collect_crossfall = plan_space.getAttribute("collect_crossfall")        #DOUBLE
        
        
        #--------------------------------------------------------------------------------#
        #       BEGIN LOOPING ACROSS ALL BLOCKS IN MAP                                   #
        #--------------------------------------------------------------------------------#
        
        for i in range(int(blocks_num)):
            currentID = i + 1
            currentAttList = blockcityin.getAttributes("BlockID"+str(currentID))        #attribute list of current block structure
            currentPatchList = patchcityin.getAttributes("PatchDataID"+str(currentID))
            facilities_attr = Attribute()
            facilities_attr.setAttribute("BlockID", currentID)
            block_AActive = blocks_size * blocks_size * (currentAttList.getAttribute("Activity")/100)

            #--------------------------------------------------------------------------------#
            #            CONDITIONAL CHECK TO SEE IF CURRENT BLOCK IS RELEVANT               #
            #--------------------------------------------------------------------------------#
            block_status = currentAttList.getAttribute("Status")
            tot_facilities_area = currentAttList.getAttribute("ALUC_Edu") + currentAttList.getAttribute("ALUC_HnC") \
                + currentAttList.getAttribute("ALUC_SnU") + currentAttList.getAttribute("ALUC_Tr")
            if block_status == 0 or tot_facilities_area == 0:           #2 conditions to skip: (1) status = 0, (2) no facilities
                print "BlockID"+str(currentID)+" is not active or has no relevant facilities area"
                continue
            #IF NOT SKIPPED, PLAN URBAN FORM
            facilities_attr.setAttribute("HasFacilities", 1)
            #--------------------------------------------------------------------------------#
            #            SETUP DATA - RETRIEVE FROM BLOCKCITY AND SAMPLE VALUES              #
            #--------------------------------------------------------------------------------#
            
            Edu_area_tot = float(currentAttList.getAttribute("ALUC_Edu"))       #Area of Education facilities
            HnC_area_tot = float(currentAttList.getAttribute("ALUC_HnC"))       #Area of Health & Community
            SnU_area_tot = float(currentAttList.getAttribute("ALUC_SnU"))       #Area of Services & Utilities
            
            mun_Atotal = Edu_area_tot + HnC_area_tot + SnU_area_tot             #Total Municipal Area
            
            tr_area_tot = float(currentAttList.getAttribute("ALUC_Tr"))         #Area of other transport facilities
            
            
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
                facilities_attr.setAttribute("MunATot", mun_Atotal)
                facilities_attr.setAttribute("MunAimp", mun_Aimp)
                facilities_attr.setAttribute("MunAeimp", mun_Aeimp)
                facilities_attr.setAttribute("MunAperv", mun_Aperv)
                facilities_attr.setAttribute("MunAroof", mun_Aroof)
                facilities_attr.setAttribute("MunTIF", mun_TIF)
                facilities_attr.setAttribute("MunEIF", mun_EIF)
            
            if tr_area_tot == 0:
                pass
            else:
                facilities_attr.setAttribute("TrATot", tr_area_tot)
                facilities_attr.setAttribute("TrAimp", tr_Aimp)
                facilities_attr.setAttribute("TrAeimp", tr_Aeimp)
                facilities_attr.setAttribute("TrAperv", tr_Aperv)
                facilities_attr.setAttribute("TrAroof", tr_Aroof)
                facilities_attr.setAttribute("TrTIF", tr_TIF)
                facilities_attr.setAttribute("TrEIF", tr_EIF)
                
            #-----------------------------------------------------------------#
            #        Write all updated Attribute Lists to the output          #
            #-----------------------------------------------------------------#
                
            facilities.setAttributes("BlockID"+str(currentID),facilities_attr)
            
            #FOR LOOP END (Repeat for next BlockID)
            
        #END OF MODULE
    
            