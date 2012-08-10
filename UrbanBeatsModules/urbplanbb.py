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
#from urbplanbbguic import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
#from pyvibe import *
import random
import math

class urbplanbb(Module):
    """Determines urban form of grid of blocks for model city by processing the
    individual land zoning classes along with the planning map, locality map and
    population input with local planning regulations/rules/geometries.
	
    The updated grid is output along with all parameters in two separate
    vector files: 
	- <description of inputs/outputs>
    
    Log of Updates made at each version:
    
    v0.8 update (March, 2012):
        - Split the planning into four separate modules with prefix ubp_
        - This has cut several hundred lines of code in urbplanbb.py
        - urbplansummary.py now active, will take the existing map from this module
            and add the additional planning data to it
        - urbplanbb's sole purpose at the moment is to process information from the GUI
    
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
        #inputs from previous modules and output vector data to next module
	'''        
	self.blockcityin = VectorDataIn
        self.blockcityout = VectorDataIn
        self.patchcityin = VectorDataIn
        self.existingblock = VectorDataIn
        self.patchcityout = VectorDataIn
        self.planningrules = VectorDataIn
	'''
        self.createParameter( "blockcityin", VIBe2.VECTORDATA_IN)
        self.createParameter( "existingblock", VIBe2.VECTORDATA_IN)
        self.createParameter( "blockcityout", VIBe2.VECTORDATA_OUT)
        self.createParameter( "patchcityin", VIBe2.VECTORDATA_IN)
        self.createParameter( "patchcityout", VIBe2.VECTORDATA_OUT)
        self.createParameter( "planningrules", VIBe2.VECTORDATA_OUT)
        '''
        self.reportin = VectorDataIn
        self.reportout = VectorDataIn
	'''        
	self.createParameter( "reportin", VIBe2.VECTORDATA_IN)
        self.createParameter( "reportout", VIBe2.VECTORDATA_OUT)
        
        #parameters for blocks analysis (these are contained in the GUI)
        
        ############################
        #GENERAL RULES PARAMETERS 
        ############################
        #--> Limits on Site Cover & Imperviousness
        self.maximperv = 80                     #maximum imperviousness allowed
        self.maxsitecover = 60                  #maximum site cover allowed
        self.createParameter("maximperv", DOUBLE, "")
        self.createParameter("maxsitecover", DOUBLE, "")
        #--> Spatial Details & Metrics
        self.locality_mun_trans = False
        self.createParameter("locality_mun_trans", BOOL, "")
        #self.district_age_infer = False
        #self.createParameter( "district_age_infer", BOOL,"")
        #--> Building Block Dynamics
        #parameters coming soon!!!
        
        
        ############################
        #RESIDENTIAL PARAMETERS
        ############################
        #(includes all residential land uses of varying density)
        self.occup_avg = 2.67                   #average occupancy (house)
        self.occup_max = 5                      #maximum occupancy (house)
        self.person_space = 84                  #space per person [sqm]
        self.extra_comm_area = 10               #extra space for communal area
        self.createParameter("occup_avg", DOUBLE,"")
        self.createParameter("occup_max", DOUBLE,"")
        self.createParameter("person_space", DOUBLE)
        self.createParameter("extra_comm_area", DOUBLE,"")
        
        self.setback_f_min = 2                  #minimum front setback
        self.setback_f_max = 9                  #maximum front setback
        self.setback_s_min = 1                  #minimum side setback (applies to rear as well)
        self.setback_s_max = 2                  #maximum side setback (applies to rear as well)
        self.createParameter("setback_f_min", DOUBLE,"")
        self.createParameter("setback_f_max", DOUBLE,"")
        self.createParameter("setback_s_min", DOUBLE,"")
        self.createParameter("setback_s_max", DOUBLE,"")
        
        self.carports_max = 2                   #max number of carports
        self.garage_incl = False                #include garage? YES/NO
        self.w_driveway_min = 2.6               #minimum driveway width [m]
        self.patio_area_max = 2                 #maximum patio area [sqm]
        self.patio_covered = False              #is patio covered by roof?
        self.floor_num_max = 2                  #maximum number of floors
        self.floor_autobuild = True             #autobuild floors?
        self.createParameter("carports_max", DOUBLE,"")
        self.createParameter("garage_incl", BOOL,"")
        self.createParameter("w_driveway_min",DOUBLE,"")
        self.createParameter("patio_area_max",DOUBLE,"")
        self.createParameter("patio_covered", BOOL,"")
        self.createParameter("floor_num_max", DOUBLE,"")
        self.createParameter("floor_autobuild",BOOL,"")
        
        self.occup_flat_avg = 1.5               #average occupancy of apartment
        self.commspace_indoor = 10              #communal space % indoor
        self.commspace_outdoor = 5              #communal space % outdoor
        self.flat_area_max = 90                 #maximum apartment size [sqm]
        self.setback_HDR_avg = 1                #average setback for HDR site
        self.setback_HDR_auto = True            #determine setback for HDR automatically?
        self.createParameter("occup_flat_avg", DOUBLE,"")
        self.createParameter("commspace_indoor",DOUBLE,"")
        self.createParameter("commspace_outdoor",DOUBLE,"")
        self.createParameter("flat_area_max", DOUBLE,"")
        self.createParameter("setback_HDR_avg",DOUBLE,"")
        self.createParameter("setback_HDR_auto",BOOL,"")
                
        self.roof_connected = "Direct"          #how is the roof connected to drainage? Direct/Disconnected/Varied?
        self.imperv_prop_dced = 10              #proportion of impervious area disconnected
        self.createParameter("roof_connected", STRING,"")
        self.createParameter("imperv_prop_dced",DOUBLE,"")
        
        
        #############################
        #Non-Residential Parameters 
        #############################
        #(includes Trade, Office/Rescom, Light Industry, Heavy Industry, Education, Health & Comm, Serv & Util)
        #--> Commercial & Industrial Zones :: Employment Details
        self.employment_data = "D"              #'D' = direct input, 'P' = population-derived
        self.employment_rad = 1                 #consider employment radius of 1km
        self.employment_rate = 90               #employment rate for region in %
        self.employment_adjust = 1.2            #employment adjustment factor for future growth
        self.com_spacevary_check = False        #True/False checkbox to vary required floor space
        self.createParameter("employment_data", STRING,"")
        self.createParameter( "employment_rad", DOUBLE,"")
        self.createParameter("employment_rate", DOUBLE,"")
        self.createParameter("employment_adjust",DOUBLE,"")
        self.createParameter("com_spacevary_check",BOOL,"")
        #--> variables for areas (appearing in the subdialog box urbplanbbc1_gui)
        self.Atrad_cc = 10              #Trade sqm/employee at city centre
        self.Atrad_uf = 10              #Trade sqm/employee at urban fringe
        self.Aoff_cc = 10               #Offices sqm/employee at city centre
        self.Aoff_uf = 10               #Offices sqm/employee at urban fringe
        self.Alind_cc = 10              #Light industry sqm/employee at city centre
        self.Alind_uf = 10              #Light industry sqm/employee at urban fringe
        self.Ahind_cc = 10              #Heavy industry sqm/employee at city centre
        self.Ahind_uf = 10              #Heavy industry sqm/employee at urban fringe
        self.ddecay_type = "L"          #distance decay relationship
        self.createParameter("Atrad_cc", DOUBLE,"")
        self.createParameter("Atrad_uf", DOUBLE,"")
        self.createParameter("Aoff_cc", DOUBLE,"")
        self.createParameter("Aoff_uf", DOUBLE,"")
        self.createParameter("Alind_cc", DOUBLE,"")
        self.createParameter("Alind_uf", DOUBLE,"")
        self.createParameter("Ahind_cc", DOUBLE,"")
        self.createParameter("Ahind_uf", DOUBLE,"")
        self.createParameter("ddecay_type",STRING,"")
        
        
        #--> Commercial & Industrial Zones :: Site Layout and Building Form
        self.com_fsetback_min = 1               #minimum front setback [m]
        self.com_setback_auto = False           #determine setback automatically?
        self.com_floors_max = 3                 #maximum allowable floors
        self.createParameter(self, "com_fsetback_min", DOUBLE,"")
        self.createParameter(self, "com_setback_auto", BOOL,"")
        self.createParameter(self, "com_floors_max", DOUBLE,"")
        
        #--> Commercial & Industrial Zones :: Car Parking and Service Area
        self.com_carpark_dmin = 17              #minimum depth of frontage parking area [m]
        self.com_carparkW = 2.6                 #minimum width of one parking lot
        self.com_carparkD = 4                   #minimum depth of one parking lot
        self.com_carpark_avgimp = 90               #avg. imperviousness of parking area
        self.com_carpark_share = False          #share carparks if multiple zones?
        self.com_service_dmin = 17              #minimum depth of service area
        self.createParameter( "com_carpark_dmin", DOUBLE,"")
        self.createParameter( "com_carparkW", DOUBLE,"")
        self.createParameter( "com_carparkD", DOUBLE,"")
        self.createParameter( "com_carpark_avgimp",DOUBLE,"")
        self.createParameter( "com_carpark_share", BOOL,"")
        self.createParameter( "com_service_dmin", DOUBLE,"")
        
        #--> Commercial & Industrial Zones :: Service/Access Road
        self.access_perp = False                #access road aligned perpendicular
        self.access_parall = False              #access road aligned parallel
        self.access_cds = False                 #access road cul-de sacs
        self.access_parall_medwidth = 1         #median width if access rd aligned parallel
        self.access_cds_circlerad = 27          #turning circle radius in cul-de-sac
        self.access_ped_include = False         #include pedestrian paths along service roads?
        self.createParameter( "access_perp", BOOL,"")
        self.createParameter( "access_parall",BOOL,"")
        self.createParameter( "access_cds", BOOL,"")
        self.createParameter( "access_parall_medwidth", DOUBLE,"")
        self.createParameter( "access_cds_circlerad", DOUBLE,"")
        self.createParameter( "access_ped_include", BOOL,"")
        
        #--> Commercial & Industrial Zones :: Landscaping
        self.lscape_hsbal = 0                   #balance between hard & soft landscapes
        self.lscape_avgimp_dced = 0.1           #avg. imperviousness disconnected
        self.createParameter( "lscape_hsbal", DOUBLE,"")
        self.createParameter( "lscape_avgimp_dced", DOUBLE,"")
        
        #--> Municipal Facilities
        self.mun_explicit = False
        self.edu_school = False
        self.edu_uni = False
        self.edu_lib = False
        self.createParameter( "mun_explicit", BOOL,"")
        self.createParameter("edu_school", BOOL,"")
        self.createParameter("edu_uni", BOOL,"")
        self.createParameter("edu_lib", BOOL,"")
        #--> Parameters to customise different facilities
        #coming soon!
        
        self.civ_hospital = False
        self.civ_clinic = False
        self.civ_police = False
        self.civ_fire = False
        self.civ_jail = False
        self.civ_worship = False
        self.civ_leisure = False
        self.civ_museum = False
        self.civ_zoo = False
        self.civ_stadium = False
        self.civ_racing = False
        self.civ_cemetery = False
        self.createParameter( "civ_hospital", BOOL,"")
        self.createParameter( "civ_clinic", BOOL,"")
        self.createParameter( "civ_police", BOOL,"")
        self.createParameter( "civ_fire", BOOL,"")
        self.createParameter( "civ_jail", BOOL,"")
        self.createParameter( "civ_worship", BOOL,"")
        self.createParameter( "civ_leisure", BOOL,"")
        self.createParameter( "civ_museum", BOOL,"")
        self.createParameter( "civ_zoo", BOOL,"")
        self.createParameter( "civ_stadium", BOOL,"")
        self.createParameter( "civ_racing", BOOL,"")
        self.createParameter( "civ_cemetery", BOOL,"")
        #--> Parameters to customise different facilities
        #coming soon!
        
        self.sut_waste = False
        self.sut_gas = False
        self.sut_electricity = False
        self.sut_water = False
        self.sut_lgoffice = False
        self.createParameter( "sut_waste", BOOL,"")
        self.createParameter( "sut_gas", BOOL,"")
        self.createParameter( "sut_electricity", BOOL,"")
        self.createParameter( "sut_water", BOOL,"")
        self.createParameter( "sut_lgoffice", BOOL,"")
        #--> Parameters to customise different facilities
        #coming soon!
        
        ############################
        #Transport Parameters
        ############################
        #(includes Roads, Transport)
        #--> Residential Pedestrian
        self.w_resfootpath_min = 1
        self.w_resfootpath_max = 3
        self.w_resnaturestrip_min = 1
        self.w_resnaturestrip_max = 3
        self.w_resfootpath_med = True          #to simplify things, just use median footpath width?
        self.w_resnaturestrip_med = True       #to simplify things, just use median naturestrip width?
        self.createParameter( "w_resfootpath_min", DOUBLE,"")
        self.createParameter( "w_resfootpath_max", DOUBLE,"")
        self.createParameter( "w_resnaturestrip_min", DOUBLE,"")
        self.createParameter( "w_resnaturestrip_max", DOUBLE,"")
        self.createParameter( "w_resfootpath_med", BOOL,"")
        self.createParameter( "w_resnaturestrip_med", BOOL,"")
        
        #--> Commercial Pedestrian
        self.w_comfootpath_min = 1
        self.w_comfootpath_max = 3
        self.w_comnaturestrip_min = 1
        self.w_comnaturestrip_max = 3
        self.w_comfootpath_med = True          #to simplify things, just use median footpath width?
        self.w_comnaturestrip_med = True       #to simplify things, just use median naturestrip width?
        self.createParameter( "w_comfootpath_min", DOUBLE,"")
        self.createParameter( "w_comfootpath_max", DOUBLE,"")
        self.createParameter( "w_comnaturestrip_min", DOUBLE,"")
        self.createParameter( "w_comnaturestrip_max", DOUBLE,"")
        self.createParameter( "w_comfootpath_med", BOOL,"")
        self.createParameter( "w_comnaturestrip_med", BOOL,"")
        
        #--> Local Access/Service/Collector Roads
        self.w_collectlane_min = 3            
        self.w_collectlane_max = 5           
        self.w_collectlane_med = True       #to simplify things, just use median collector lane width?
        self.collect_crossfall = 3
        self.createParameter( "w_collectlane_min", DOUBLE,"")
        self.createParameter( "w_collectlane_max", DOUBLE,"")
        self.createParameter( "w_collectlane_med", BOOL,"")
        self.createParameter( "collect_crossfall", DOUBLE,"")
        
        #--> Arterials/District Distributors/Dual Carriageways
        self.w_artlane_min = 3
        self.w_artlane_max = 5
        self.w_artlane_med = False
        self.w_artmedian = 3
        self.artmedian_reserved = False
        self.art_crossfall = 3
        self.createParameter( "w_artlane_min", DOUBLE,"")
        self.createParameter( "w_artlane_max", DOUBLE,"")
        self.createParameter( "w_artlane_med", BOOL,"")
        self.createParameter( "w_artmedian", DOUBLE,"")
        self.createParameter( "artmedian_reserved", BOOL,"")
        self.createParameter( "art_crossfall", DOUBLE,"")
        
        #--> Highways/Freeways/Motorways
        self.w_hwylane_avg = 3
        self.w_hwymedian = 3
        self.hwy_buffered = False
        self.hwymedian_reserved = False
        self.hwy_crossfall = 3
        self.createParameter( "w_hwylane_avg", DOUBLE,"")
        self.createParameter( "w_hwymedian", DOUBLE,"")
        self.createParameter( "hwy_buffered", BOOL,"")
        self.createParameter( "hwymedian_reserved", BOOL,"")
        self.createParameter( "hwy_crossfall", DOUBLE,"")
        
        #--> Other Transportation
        self.trans_explicit = False
        self.trans_airport = False
        self.trans_comseaport = False
        self.trans_indseaport = False
        self.trans_busdepot = False
        self.trans_railterminal = False
        self.createParameter( "trans_explicit", BOOL,"")
        self.createParameter( "trans_airport", BOOL,"")
        self.createParameter( "trans_comseaport", BOOL,"")
        self.createParameter( "trans_indseaport", BOOL,"")
        self.createParameter( "trans_busdepot", BOOL,"")
        self.createParameter( "trans_railterminal", BOOL,"")
        #--> Detailed parameters for individual facilities
        #coming soon!
        
        
        ############################
        #Open Space Parameters
        ############################
        #(includes Parks & Garden, Reserves & Floodways)
        #--> Parks, Squares & Gardens :: General
        self.pg_clustering_degree = 1           #degree of clustering, 0=low, 1=medium, 2=high
        self.pg_greengrey_ratio = 0             #balance between green and grey spaces -10=fully grey, +10=fully green
        self.pg_linear_threshold = 1            #ratio threshold to consider open space as "linear"
        self.createParameter( "pg_clustering_degree", DOUBLE,"")
        self.createParameter( "pg_greengrey_ratio", DOUBLE,"")
        self.createParameter( "pg_linear_threshold", DOUBLE,"")
        
        #--> Parks, Squares & Gardens :: Green Space Configuration
        self.pg_footpath_cross = False
        self.pg_footpath_circle = False
        self.pg_footpath_perimeter = False
        self.pg_circle_radius = 10              #radius of circle footpath if chosen [% of park width]
        self.pg_circle_accesses = 4             #no. of access routes from boundary to circle
        self.pg_perimeter_setback = 10          #setback of perimeter footpath if chosen [% of park width]
        self.pg_perimeter_accesses = 4          #no. of access routes from boundary to perimeter footpath
        self.pg_footpath_avgW = 1               #average width of the footpath
        self.pg_footpath_impdced = 0.9          #avg. prop of imperviousness disconnected from footpath
        self.pg_footpath_varyW = False          #vary the width of the footpath?
        self.pg_footpath_multiply = False       #multiply footpaths if green space is classed as linear?
        self.createParameter( "pg_footpath_cross", BOOL,"")
        self.createParameter( "pg_footpath_circle", BOOL,"")
        self.createParameter( "pg_footpath_perimeter", BOOL,"")
        self.createParameter( "pg_circle_radius", DOUBLE,"")
        self.createParameter( "pg_circle_accesses", DOUBLE,"")
        self.createParameter( "pg_perimeter_setback", DOUBLE,"")
        self.createParameter( "pg_perimeter_accesses", DOUBLE,"")
        self.createParameter( "pg_footpath_avgW", DOUBLE,"")
        self.createParameter( "pg_footpath_impdced", DOUBLE,"")
        self.createParameter( "pg_footpath_varyW", BOOL,"")
        self.createParameter( "pg_footpath_multiply", BOOL,"")
        
        #--> Reserves & Floodways
        self.rfw_partialimp_check = False               #assume the area is partially impervious
        self.rfw_partialimp = 5                         #set the partially impervious value [%]
        self.rfw_areausable_check = False               #restrict some of the usable area
        self.rfw_areausable = 10                        #set the amount of area that can be used [%]
        self.createParameter( "rfw_partialimp_check", BOOL,"")
        self.createParameter( "rfw_partialimp", DOUBLE,"")
        self.createParameter( "rfw_areausable_check", BOOL,"")
        self.createParameter( "rfw_areausable", DOUBLE,"")
        
        
        ############################
        #Others Parameters
        ############################
        #(includes Unclassified and Undeveloped)
        #--> Unclassified Land
        self.unc_merge = True
        self.unc_unc2square = True
        self.unc_unc2square_weight = 0
        self.unc_unc2park = True
        self.unc_unc2park_weight = 0
        self.unc_unc2road = False
        self.unc_unc2road_weight = 0
        self.unc_landmark = False
        self.unc_landmark_threshold = 40
        self.unc_landmark_avgimp = 40
        self.unc_landmark_otherwater = False
        self.createParameter( "unc_merge", BOOL,"")
        self.createParameter( "unc_unc2square", BOOL,"")
        self.createParameter( "unc_unc2square_weight", DOUBLE,"")
        self.createParameter( "unc_unc2park", BOOL,"")
        self.createParameter( "unc_unc2park_weight", DOUBLE,"")
        self.createParameter( "unc_unc2road", BOOL,"")
        self.createParameter( "unc_unc2road_weight", DOUBLE,"")
        self.createParameter( "unc_landmark", BOOL,"")
        self.createParameter( "unc_landmark_threshold", DOUBLE,"")
        self.createParameter( "unc_landmark_avgimp", DOUBLE,"")
        self.createParameter( "unc_landmark_otherwater", BOOL,"")
        
        #--> Undeveloped Land
        self.und_whattodo = "N"                 #what to do with this land? N= do not touch, Y = allow
        self.und_allowspace = 20                #allowable space to be used for technologies
        self.und_autodeterminetype = True       #automatically determine type based on distance from city centre
        self.createParameter( "und_whattodo", STRING,"")
        self.createParameter( "und_allowspace", DOUBLE,"")
        self.createParameter( "und_autodeterminetype", BOOL,"")
        
        #------------------------------------------
        #END OF INPUT PARAMETER LIST
        
        
    def run(self):
        #Link input vectors with local variables
        blockcityin = self.blockcityin.getItem()                #incoming vector data from delinblocks
        blockcityout = self.blockcityout.getItem()              #outgoing vector data to next module
        existingblock = self.existingblock.getItem()            #incoming existing vector data from previous module
        patchcityin = self.patchcityin.getItem()
        patchcityout = self.patchcityout.getItem()
        planningrules = self.planningrules.getItem()
        
        map_attr = blockcityin.getAttributes("MapAttributes")   #GET map attributes

        #get data needed to being for loop analysis
        blocks_num = map_attr.getAttribute("NumBlocks")     #number of blocks to loop through
        blocks_size = map_attr.getAttribute("BlockSize")    #size of block
        map_w = map_attr.getAttribute("WidthBlocks")        #num of blocks wide
        map_h = map_attr.getAttribute("HeightBlocks")       #num of blocks tall
        input_res = map_attr.getAttribute("InputReso")      #resolution of input data
        urbansimdata = map_attr.getStringAttribute("UrbanSimData")
        
        basins = map_attr.getAttribute("TotalBasins")
        for i in range(int(basins)):
            currentID = i+1
            basin_attr = blockcityin.getAttributes("BasinID"+str(currentID))
            blockcityout.setAttributes("BasinID"+str(currentID), basin_attr)
        
        #SAMPLING RANGE ADJUSTMENT
        #if parameter range median boxes were checked, adjust these parameters to reflect that
        if self.w_resfootpath_med == True:
            self.w_resfootpath_min = int((self.w_resfootpath_min+self.w_resfootpath_max)/2)
            self.w_resfootpath_max = self.w_resfootpath_min
        if self.w_resnaturestrip_med == True:
            self.w_resnaturestrip_min = int((self.w_resnaturestrip_min+self.w_resnaturestrip_max)/2)
            self.w_resnaturestrip_max = self.w_resnaturestrip_min
        if self.w_collectlane_med == True:
            self.w_collectlane_min = int((self.w_collectlane_min+self.w_collectlane_max)/2)
            self.w_collectlane_max = self.w_collectlane_min
        
        #CONVERSIONS
        #convert percentages to proportions and proportions to percentages and adjust other necessary
        #parameters
        self.collect_crossfall = self.collect_crossfall/100     #convert to a proportion
        
        
        
                    ##############################################
                ##                                                  ##    
            ##                                                          ##   
        ##                                                                  ##        
        ######################################################################
        #        Determine which blocks need to be replaced/recreated        #
        #            THIS WILL BE IMPLEMENTED IN THE NEAR FUTURE             #
        #    <THE FOLLOWING IS CURRENTLY A PLACEHOLDER FOR THIS ALGORITHM>   #
        ######################################################################
        ##                                                                  ##
            ##                                                          ##
                ##                                                 ##
                    #############################################
            
        
        #--------------------------------------------------------------------------#
        #        TRANSFER PLANNING RULES INTO VECTOR FORMAT TO NEXT MODULE         #
        #--------------------------------------------------------------------------#
        #Planning rules to be transferred as strings that are splitted in the next module
        #these are grouped into a few useful groups and written to the planning rules vector
        
        #Groups for General
        plan_gen = Attribute()
        
        plan_gen.setAttribute("maximperv", self.maximperv)
        plan_gen.setAttribute("maxsitecover", self.maxsitecover)
        plan_gen.setAttribute("locality_mun_trans", self.locality_mun_trans)
        
        planningrules.setAttributes("GeneralRules", plan_gen)
        
        #Groups for RES
        plan_res = Attribute()
        
        plan_res.setAttribute("occup_avg", self.occup_avg)
        plan_res.setAttribute("occup_max", self.occup_max)
        plan_res.setAttribute("person_space", self.person_space)
        plan_res.setAttribute("extra_comm_area", self.extra_comm_area)
        
        plan_res.setAttribute("setback_f_min", self.setback_f_min)
        plan_res.setAttribute("setback_f_max", self.setback_f_max)
        plan_res.setAttribute("setback_s_min", self.setback_s_min)
        plan_res.setAttribute("setback_s_max", self.setback_s_max)
        
        plan_res.setAttribute("carports_max", self.carports_max)
        plan_res.setAttribute("garage_incl", self.garage_incl)
        plan_res.setAttribute("w_driveway_min", self.w_driveway_min)
        plan_res.setAttribute("patio_area_max", self.patio_area_max)
        plan_res.setAttribute("patio_covered", self.patio_covered)
        plan_res.setAttribute("floor_num_max", self.floor_num_max)
        plan_res.setAttribute("floor_autobuild", self.floor_autobuild)
        
        plan_res.setAttribute("occup_flat_avg", self.occup_flat_avg)
        plan_res.setAttribute("commspace_indoor", self.commspace_indoor)
        plan_res.setAttribute("commspace_outdoor", self.commspace_outdoor)
        plan_res.setAttribute("flat_area_max", self.flat_area_max)
        plan_res.setAttribute("setback_HDR_avg", self.setback_HDR_avg)
        plan_res.setAttribute("setback_HDR_auto", self.setback_HDR_auto)
        plan_res.setAttribute("roof_connected", self.roof_connected)
        plan_res.setAttribute("imperv_prop_dced", self.imperv_prop_dced)
        
        planningrules.setAttributes("ResidentialRules", plan_res)
        
        #Groups for NonRES
        plan_nonres = Attribute()
        
        plan_nonres.setAttribute("employment_data", self.employment_data)
        plan_nonres.setAttribute("employment_rad", self.employment_rad)
        plan_nonres.setAttribute("employment_rate", self.employment_rate)
        plan_nonres.setAttribute("employment_adjust", self.employment_adjust)
        plan_nonres.setAttribute("com_spacevary_check", self.com_spacevary_check)
        
        plan_nonres.setAttribute("Atrad_cc", self.Atrad_cc)
        plan_nonres.setAttribute("Atrad_uf", self.Atrad_uf)
        plan_nonres.setAttribute("Aoff_cc", self.Aoff_cc)
        plan_nonres.setAttribute("Aoff_uf", self.Aoff_uf)
        plan_nonres.setAttribute("Alind_cc", self.Alind_cc)
        plan_nonres.setAttribute("Alind_uf", self.Alind_uf)
        plan_nonres.setAttribute("Ahind_cc", self.Ahind_cc)
        plan_nonres.setAttribute("Ahind_uf", self.Ahind_uf)
        plan_nonres.setAttribute("ddecay_type", self.ddecay_type)
        
        plan_nonres.setAttribute("com_fsetback_min", self.com_fsetback_min)
        plan_nonres.setAttribute("com_setback_auto", self.com_setback_auto)
        plan_nonres.setAttribute("com_floors_max", self.com_floors_max)
        
        plan_nonres.setAttribute("com_carpark_dmin", self.com_carpark_dmin)
        plan_nonres.setAttribute("com_carparkW", self.com_carparkW)
        plan_nonres.setAttribute("com_carparkD", self.com_carparkD)
        plan_nonres.setAttribute("com_carpark_avgimp", self.com_carpark_avgimp)
        plan_nonres.setAttribute("com_carpark_share", self.com_carpark_share)
        plan_nonres.setAttribute("com_service_dmin", self.com_service_dmin)
        
        plan_nonres.setAttribute("access_perp", self.access_perp)
        plan_nonres.setAttribute("access_parall", self.access_parall)
        plan_nonres.setAttribute("access_cds", self.access_cds)
        plan_nonres.setAttribute("access_parall_medwidth", self.access_parall_medwidth)
        plan_nonres.setAttribute("access_cds_circlerad", self.access_cds_circlerad)
        plan_nonres.setAttribute("access_ped_include", self.access_ped_include)
        
        plan_nonres.setAttribute("lscape_hsbal", self.lscape_hsbal)
        plan_nonres.setAttribute("lscape_avgimp_dced", self.lscape_avgimp_dced)
        
        planningrules.setAttributes("NonResRules", plan_nonres)
        
        #Groups for Facilities
        plan_facilities = Attribute()
        
        plan_facilities.setAttribute("mun_explicit", self.mun_explicit)
        plan_facilities.setAttribute("edu_school", self.edu_school)
        plan_facilities.setAttribute("edu_uni", self.edu_uni)
        plan_facilities.setAttribute("edu_lib", self.edu_lib)
        
        plan_facilities.setAttribute("civ_hospital", self.civ_hospital)
        plan_facilities.setAttribute("civ_clinic", self.civ_clinic)
        plan_facilities.setAttribute("civ_police", self.civ_police)
        plan_facilities.setAttribute("civ_fire", self.civ_fire)
        plan_facilities.setAttribute("civ_jail", self.civ_jail)
        plan_facilities.setAttribute("civ_worship", self.civ_worship)
        plan_facilities.setAttribute("civ_leisure", self.civ_leisure)
        plan_facilities.setAttribute("civ_museum", self.civ_museum)
        plan_facilities.setAttribute("civ_zoo", self.civ_zoo)
        plan_facilities.setAttribute("civ_stadium", self.civ_stadium)
        plan_facilities.setAttribute("civ_racing", self.civ_racing)
        plan_facilities.setAttribute("civ_cemetery", self.civ_cemetery)
        
        plan_facilities.setAttribute("sut_waste", self.sut_waste)
        plan_facilities.setAttribute("sut_gas", self.sut_gas)
        plan_facilities.setAttribute("sut_electricity", self.sut_electricity)
        plan_facilities.setAttribute("sut_water", self.sut_water)
        plan_facilities.setAttribute("sut_lgoffice", self.sut_lgoffice)
        
        plan_facilities.setAttribute("trans_explicit", self.trans_explicit)
        plan_facilities.setAttribute("trans_airport", self.trans_airport)
        plan_facilities.setAttribute("trans_comseaport", self.trans_comseaport)
        plan_facilities.setAttribute("trans_indseaport", self.trans_indseaport)
        plan_facilities.setAttribute("trans_busdepot", self.trans_busdepot)
        plan_facilities.setAttribute("trans_railterminal", self.trans_railterminal)
        
        planningrules.setAttributes("FacilitiesRules", plan_facilities)
        
        #Groups for OpenSpaces
        plan_spaces = Attribute()
        #PARKS, RESERVES GROUP
        plan_spaces.setAttribute("pg_clustering_degree", self.pg_clustering_degree)
        plan_spaces.setAttribute("pg_greengrey_ratio", self.pg_greengrey_ratio)
        plan_spaces.setAttribute("pg_linear_threshold", self.pg_linear_threshold)
        
        plan_spaces.setAttribute("pg_footpath_cross", self.pg_footpath_cross)
        plan_spaces.setAttribute("pg_footpath_circle", self.pg_footpath_circle)
        plan_spaces.setAttribute("pg_footpath_perimeter", self.pg_footpath_perimeter)
        plan_spaces.setAttribute("pg_circle_radius", self.pg_circle_radius)
        plan_spaces.setAttribute("pg_circle_accesses", self.pg_circle_accesses)
        plan_spaces.setAttribute("pg_perimeter_setback", self.pg_perimeter_setback)
        plan_spaces.setAttribute("pg_perimeter_accesses", self.pg_perimeter_accesses)
        plan_spaces.setAttribute("pg_footpath_avgW", self.pg_footpath_avgW)
        plan_spaces.setAttribute("pg_footpath_impdced", self.pg_footpath_impdced)
        plan_spaces.setAttribute("pg_footpath_varyW", self.pg_footpath_varyW)
        plan_spaces.setAttribute("pg_footpath_multiply", self.pg_footpath_multiply)
        
        plan_spaces.setAttribute("rfw_partialimp_check", self.rfw_partialimp_check)
        plan_spaces.setAttribute("rfw_partialimp", self.rfw_partialimp)
        plan_spaces.setAttribute("rfw_areausable_check", self.rfw_areausable_check)
        plan_spaces.setAttribute("rfw_areausable", self.rfw_areausable)
        
        #UNCLASSIFIED GROUP
        plan_spaces.setAttribute("unc_merge", self.unc_merge)
        plan_spaces.setAttribute("unc_unc2square", self.unc_unc2square)
        plan_spaces.setAttribute("unc_unc2square_weight", self.unc_unc2square_weight)
        plan_spaces.setAttribute("unc_unc2park", self.unc_unc2park)
        plan_spaces.setAttribute("unc_unc2park_weight", self.unc_unc2park_weight)
        plan_spaces.setAttribute("unc_unc2road", self.unc_unc2road)
        plan_spaces.setAttribute("unc_unc2road_weight", self.unc_unc2road_weight)
        plan_spaces.setAttribute("unc_landmark", self.unc_landmark)
        plan_spaces.setAttribute("unc_landmark_threshold", self.unc_landmark_threshold)
        plan_spaces.setAttribute("unc_landmark_avgimp", self.unc_landmark_avgimp)
        plan_spaces.setAttribute("unc_landmark_otherwater", self.unc_landmark_otherwater)
        
        #UNDEVELOPED GROUP
        plan_spaces.setAttribute("und_whattodo", self.und_whattodo)
        plan_spaces.setAttribute("und_allowspace", self.und_allowspace)
        plan_spaces.setAttribute("und_autodeterminetype", self.und_autodeterminetype)
                
        #ROADS & HIGHWAYS GROUP
        plan_spaces.setAttribute("w_resfootpath_min", self.w_resfootpath_min)
        plan_spaces.setAttribute("w_resfootpath_max", self.w_resfootpath_max)
        plan_spaces.setAttribute("w_resnaturestrip_min", self.w_resnaturestrip_min)
        plan_spaces.setAttribute("w_resnaturestrip_max", self.w_resnaturestrip_max)
        plan_spaces.setAttribute("w_resfootpath_med", self.w_resfootpath_med)
        plan_spaces.setAttribute("w_resnaturestrip_med", self.w_resnaturestrip_med)
        
        plan_spaces.setAttribute("w_comfootpath_min", self.w_comfootpath_min)
        plan_spaces.setAttribute("w_comfootpath_max", self.w_comfootpath_max)
        plan_spaces.setAttribute("w_comnaturestrip_min", self.w_comnaturestrip_min)
        plan_spaces.setAttribute("w_comnaturestrip_max", self.w_comnaturestrip_max)
        plan_spaces.setAttribute("w_comfootpath_med", self.w_comfootpath_med)
        plan_spaces.setAttribute("w_comnaturestrip_med", self.w_comnaturestrip_med)
        
        plan_spaces.setAttribute("w_collectlane_min", self.w_collectlane_min)
        plan_spaces.setAttribute("w_collectlane_max", self.w_collectlane_max)
        plan_spaces.setAttribute("w_collectlane_med", self.w_collectlane_med)
        plan_spaces.setAttribute("collect_crossfall", self.collect_crossfall)
        
        plan_spaces.setAttribute("w_artlane_min", self.w_artlane_min)
        plan_spaces.setAttribute("w_artlane_max", self.w_artlane_max)
        plan_spaces.setAttribute("w_artlane_med", self.w_artlane_med)
        plan_spaces.setAttribute("w_artmedian", self.w_artmedian)
        plan_spaces.setAttribute("artmedian_reserved", self.artmedian_reserved)
        plan_spaces.setAttribute("art_crossfall", self.art_crossfall)
        
        plan_spaces.setAttribute("w_hwylane_avg", self.w_hwylane_avg)
        plan_spaces.setAttribute("w_hwymedian", self.w_hwymedian)
        plan_spaces.setAttribute("hwy_buffered", self.hwy_buffered)
        plan_spaces.setAttribute("hwymedian_reserved", self.hwymedian_reserved)
        plan_spaces.setAttribute("hwy_crossfall", self.hwy_crossfall)
        
        planningrules.setAttributes("SpacesRules", plan_spaces)
        
        #begin for loop
        for i in range(int(blocks_num)):
            currentID = i + 1
            currentAttList = blockcityin.getAttributes("BlockID"+str(currentID))        #attribute list of current block structure
            currentPatchList = patchcityin.getAttributes("PatchDataID"+str(currentID))
            #existingAttList = existingblock.getAttributes("BlockID"+str(currentID))    #attribute list of the existing block structure
            plist = blockcityin.getPoints("BlockID"+str(currentID))
            flist = blockcityin.getFaces("BlockID"+str(currentID))
            pnetlist = blockcityin.getPoints("NetworkID"+str(currentID))
            enetlist = blockcityin.getEdges("NetworkID"+str(currentID))
            network_attr = blockcityin.getAttributes("NetworkID"+str(currentID))
            
            #-----------------------------------------------------------------#
            #        DETERMINE WHETHER TO UPDATE CURRENT BLOCK AT ALL         #
            #-----------------------------------------------------------------#
            
            block_status = currentAttList.getAttribute("Status")
            if block_status == 0:
                print "BlockID"+str(currentID)+" is not active in simulation"
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
            
                #skips the for loop iteration to the next block, not more needs to be done
                continue
            
            print currentID
            
            #if <comparison between existing blocks and new blocks> condition TRUE:
            #   assign an attribute "UPDATE" or "DO NOT UPDATE" so that all future block modules can review this!
            #   blockcityout.setPoints("BlockID"+str(currentID),plist)
            #   blockcityout.setFaces("BlockID"+str(currentID), flist)
            #   blockcityout.setAttributes("BlockID"+str(currentID), existingAttList)
            #   continue        #no need to replace block urban form, therefore continue!        
            
            #-----------------------------------------------------------------#
            #        Write all updated Attribute Lists to the output          #
            #-----------------------------------------------------------------#
            
            blockcityout.setPoints("BlockID"+str(currentID),plist)
            blockcityout.setFaces("BlockID"+str(currentID),flist)
            blockcityout.setAttributes("BlockID"+str(currentID),currentAttList)
            blockcityout.setPoints("NetworkID"+str(currentID), pnetlist)
            blockcityout.setEdges("NetworkID"+str(currentID), enetlist)
            blockcityout.setAttributes("NetworkID"+str(currentID), network_attr)
            
            patchcityout.setPoints("PatchDataID"+str(currentID), plist)
            patchcityout.setFaces("PatchDataID"+str(currentID),flist)
            patchcityout.setAttributes("PatchDataID"+str(currentID), currentPatchList)
            
            #FOR LOOP END (Repeat for next BlockID)
            
        #Output vector update
        blockcityout.setAttributes("MapAttributes", map_attr)

    
    ########################################################
    #LINK WITH GUI                                         #
    ########################################################   
    
    def createInputDialog(self):
        form = activateurbplanbbGUI(self, QApplication.activeWindow())
        form.show()
        return True  
