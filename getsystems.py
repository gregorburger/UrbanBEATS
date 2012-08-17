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
from osgeo import ogr, osr
import sys

class GetSystems(Module):
    """Loads the Points Shapefile and transfers all relevant information about water management systems into
    a suitable data management structure for use in implementation modules
        
    Inputs: Either project path or exact filename
	- Obtain file directly from a filename or from an ongoing simulation? - Boolean
            Filename: specify path
            Ongoing simulation: specify project path (it is likely the program will load a text file with information on how to grab the shapefile)
    Outputs: Vector Data containing block attributes (these are used in later modules as a comparison with the newly entered data)
    
    Log of Updates made at each version:
    
    v0.80 (March 2012):
        - First created. Imports a systems shape file, containing points of each system
        - Future work: To make sure the projection is adjusted if the file was not created by UrbanBEATS
        
    
	@ingroup UrbanBEATS
	@author Peter M Bach
	"""

    def __init__(self):
        Module.__init__(self)
        self.ubeats_file = 1            #Was this file created by UrbanBEATS or is it man-made?
        self.ongoing_sim = 0            #Is this module part of an ongoing simulation?
        self.path_name = "C:/UBEATS/Replicate100/0_SCreekTest1-500msys-1970_points.shp"          #specify C-drive as default value
        self.system_list = VectorDataIn
        self.addParameter(self, "ubeats_file", VIBe2.BOOL)
        self.addParameter(self, "ongoing_sim", VIBe2.BOOL)
        self.addParameter(self, "path_name", VIBe2.STRING)
        self.addParameter(self, "system_list", VIBe2.VECTORDATA_OUT)
        
    def run(self):
        system_list = self.system_list.getItem()
        sys_global = Attribute()                       #write all general attributes in here
        
        #Get the correct driver (we are working with ESRI Shapefiles)
        driver = ogr.GetDriverByName('ESRI Shapefile')
        
        #Use the following file for testing: C:/UBEATS/0_UrbanBEATS-SC-500m_points.shp
        #self.path_name = "C:/UBEATS/Replicate100/0_SCreekTest1-500msys-1970_points.shp"
        save_file = "ubeats_out.shp"
        if self.ongoing_sim == True:
            file_name = self.path_name + save_file
        else:
            file_name = self.path_name
        
        print file_name
        
        #open data source, check if it exists otherwise quit.
        dataSource = driver.Open(file_name, 0)
        if dataSource is None:
            print "Error, could not open "+file_name
            sys.exit(1)
        
        layer = dataSource.GetLayer()
        total_systems = layer.GetFeatureCount()
        spatialRef = layer.GetSpatialRef()
        print "Spatial Reference (Proj4): " + str(spatialRef.ExportToProj4())
        
        #Perform some comparison to make sure that the projection of the loaded file is identical to that of the final desired format
        #Code...
        #...
        
        #Set global attributes
        sys_global.setAttribute("TotalSystems", total_systems)
        
        system_type_matrix = ['BF', 'SW', 'WSUR', 'PB', 'IS']               
        system_type_numeric = [2463, 7925, 9787, 7663, 4635]                #Think Telephone Buttons :) ('Biof', 'Swal', 'WSUR', 'Pond', 'Infl')
        scale_matrix = ['L', 'S', 'N', 'P']
        
        #Loop through each feature and grab all the relevant information
        for i in range(int(total_systems)):
            feature = layer.GetFeature(i)
            sys_attr = Attribute()
            
            #System Location and scale (BlockID)
            sys_attr.setAttribute("Location", feature.GetFieldAsInteger("Location"))
            scale_code = feature.GetFieldAsInteger("ScaleN")
            scale = scale_matrix[scale_code]
            sys_attr.setAttribute("ScaleN", scale_code)
            sys_attr.setAttribute("Scale", str(scale))
            
            #Loop through all systems and grab the attributes
            #System TypeN (Type Numeric, translates the code into string)
            type_code = feature.GetFieldAsInteger("TypeN")
            sys_attr.setAttribute("TypeN", type_code)
            print type_code
            
            type = system_type_matrix[system_type_numeric.index(type_code)]
            sys_attr.setAttribute("Type", type)
            
            #Design Details
            Asystem = feature.GetField("SysArea")
            sys_attr.setAttribute("SysArea", Asystem)
            
            deg = feature.GetField("Degree")
            sys_attr.setAttribute("Degree", deg)
            
            sysstatus = feature.GetField("Status")
            sys_attr.setAttribute("Status", sysstatus)
            
            yearbuilt = feature.GetField("Year")
            sys_attr.setAttribute("Year", yearbuilt)
            
            sys_qty = feature.GetField("Qty")
            sys_attr.setAttribute("Qty", sys_qty)
            
            sys_eafact = feature.GetField("EAFact")
            sys_attr.setAttribute("EAFact", sys_eafact)
            
            sys_imptreated = feature.GetField("ImpT")
            sys_attr.setAttribute("ImpT", sys_imptreated)
            
            sys_impcurrent = feature.GetField("CurImpT")
            sys_attr.setAttribute("CurImpT", sys_impcurrent)
            
            #Save the Attributes List & Destroy the feature to free up memory
            system_list.setAttributes("System"+str(i), sys_attr)
            feature.Destroy()
        
        #Destroy the shapefile to free up memory
        dataSource.Destroy()
        
        #output the vector file by setting the final Global Attributes
        system_list.setAttributes("GlobalSystemAttributes", sys_global)
        
        #END OF MODULE
    