# -*- coding: utf-8 -*-
"""
@file
@author  Christian Urich <christianurich@gmail.com>
@author  Peter M Bach <peterbach@gmail.com>
@version 0.5
@section LICENSE

This file is part of VIBe2
Copyright (C) 2011  Christian Urich, Peter M Bach

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

import osgeo.ogr, osgeo.osr
import os
from pyvibe import *

class ExportGISShapeFile(Module):
    """Exports any Vector Data format in VIBe2 to an ESRI shape file with UTM projection (Projection can be provided in Proj4 format)
        This module is modified from the original VIBe2 "ExportToShapeFile.py" script to be compatible with UrbanBEATS' data management
    
    Inputs: Either project path or exact filename
	- Specify an identifier (Name) in your vector data list that allows program to identify features in the collection
        - Specify a filename (Filename)
        - Check boxes indicate whether a shapefile is exported for all Polygons (faces), lines or points, only select those features that follow the identifier (Name)
        - Coordinate system is provided as a string input in Proj4 format (see OsGeo documentation for more information)
        - Offset X and Y can be used to scale the output map to its original coordinates. These can be obtained from a GIS program. If the scripts preceding
            this module work within standard Cartesian coordinates with Global Origin at (0,0), then X and Y should represent the xmin and ymin of map extents
            
    Outputs: ESRI Shapefile that is saved to VIBe's bin folder
    
    Log of Updates made at each version:
    
    v0.80 (May 2012):
        - Modified from ExportToShapeFile from VIBe2's original modules
        - Future work: Will implement directory option to save this to any directory
        
        @ingroup VIBe2
	@ingroup DAnCE4Water
	@original author Christian Urich
	@author Peter M Bach
	"""
        
	def __init__(self):
		Module.__init__(self)
		
		self.addDescription("Exports VIBe2 VectorData to ESRI Shapefiles")                
		
		self.vecin = VectorDataIn();
		self.Points = True
		self.Lines = True
		self.Faces = True
		self.FileName = "ShapeFile"
		self.Name = ""
		self.CoordinateSystem = "+proj=utm +zone=55 +south +ellps=WGS84 +datum=WGS84 +units=m +no_defs +towgs84=0,0,0"
		self.offsetX = 0
		self.offsetY = 0
		
		
		self.addParameter(self, "Name", VIBe2.STRING, "Name that is Exported e.g. Path_ all elements that start with Path_ are exported")
		self.addParameter(self, "FileName", VIBe2.STRING, "Filename the Filename is extended by the type e.g. Filename_points")
		self.addParameter(self, "Points", VIBe2.BOOL, "Option if points are exported")
		self.addParameter(self, "Lines", VIBe2.BOOL, "Option if lines are exported")
		self.addParameter(self, "Faces", VIBe2.BOOL, "Option if faces are exported")
		self.addParameter(self, "vecin", VIBe2.VECTORDATA_IN)
		self.addParameter(self, "CoordinateSystem", VIBe2.STRING)
		self.addParameter(self, "offsetX", VIBe2.DOUBLE)
		self.addParameter(self, "offsetY", VIBe2.DOUBLE)
		
		
	def run(self):
		if self.Points:
			self.exportPoints()  
		if self.Faces:                       
			self.exportFaces()
		if self.Lines:
			self.exportPolyline()             

	def exportFaces(self):
		spatialReference = osgeo.osr.SpatialReference()
		spatialReference.ImportFromProj4(self.CoordinateSystem)
		
		#Init Shape Files
		driver = osgeo.ogr.GetDriverByName('ESRI Shapefile')
		if os.path.exists(str(self.getInternalCounter()) + "_" +self.FileName+'_faces.shp'): os.remove(str(self.getInternalCounter()) + "_" +self.FileName+'_faces.shp')
		shapeData = driver.CreateDataSource(str(self.getInternalCounter())+"_" +self.FileName+'_faces.shp')
		
		layer = shapeData.CreateLayer('layer1', spatialReference, osgeo.ogr.wkbPolygon)
		layerDefinition = layer.GetLayerDefn()               
		AttributeList = []
		attr = []
		hasAttribute = False
		#Get Data 

		names_tot = self.vecin.getItem().getFaceNames()
		
		names = []
		for i in range(len(names_tot)): 
			n = str(names_tot[i])
			if n.find(str(self.Name)) == 0 or self.Name == "":
				names.append(n)
				
		attr_tmp = self.vecin.getItem().getAttributeNames()
		for i in range(len( attr_tmp)):
			attr.append(attr_tmp[i])
		for i in range(len(names)): 
			#Append Attributes
			if names[i] in attr:
				alist = self.vecin.getItem().getAttributes(names[i]).getAttributeNames()   
				#Check if attribute exists             
				for j in range(len(alist)):
					hasAttribute = True                                  
					if (alist[j] in AttributeList) == False:
						fielddef = osgeo.ogr.FieldDefn(alist[j], osgeo.ogr.OFTReal)
						layer.CreateField(fielddef)
						layerDefinition = layer.GetLayerDefn()  
						log(alist[j])
						AttributeList.append(alist[j]) 
			
			plist = self.vecin.getItem().getPoints(names[i])
			flist = self.vecin.getItem().getFaces(names[i])

			for j in range(len(flist)):
					
				line = osgeo.ogr.Geometry(osgeo.ogr.wkbPolygon)
				ring = osgeo.ogr.Geometry(osgeo.ogr.wkbLinearRing)
				pointIDs = flist[j].getIDs()
				for k in range(len(pointIDs)):
					p = Point
					p = plist[pointIDs[k]];
					ring.AddPoint(p.getX()+self.offsetX,p.getY()+self.offsetY)
				line.AddGeometry(ring)

				featureIndex = 0
				feature = osgeo.ogr.Feature(layerDefinition)
				feature.SetGeometry(line)
				feature.SetFID(featureIndex)  
				#Append Attributes
				if hasAttribute:        
					for k in range(len(alist)):
						value = self.vecin.getItem().getAttributes(names[i]).getAttribute(alist[k])
						feature.SetField(alist[k],value)
				layer.CreateFeature(feature)    
		shapeData.Destroy()               
               
	def exportPoints(self):
		spatialReference = osgeo.osr.SpatialReference()
		spatialReference.ImportFromProj4(self.CoordinateSystem)
		
		#Init Shape Files
		driver = osgeo.ogr.GetDriverByName('ESRI Shapefile')
		if os.path.exists(str(self.getInternalCounter())+"_" +self.FileName+'_points.shp'): os.remove(str(self.getInternalCounter())+"_" +self.FileName+'_points.shp')
		shapeData = driver.CreateDataSource(str(self.getInternalCounter())+"_" +self.FileName+'_points.shp')
		
		layer = shapeData.CreateLayer('layer1', spatialReference, osgeo.ogr.wkbPoint)
		#osgeo.ogr.wkbPolygon()
		layerDefinition = layer.GetLayerDefn()               
		AttributeList = []
		attr = []
		hasAttribute = False
		
		fielddef = osgeo.ogr.FieldDefn("Z", osgeo.ogr.OFTReal)
		layer.CreateField(fielddef)
		layerDefinition = layer.GetLayerDefn()  
		AttributeList.append("Z") 
		
		#Get Data 
		names_tot = self.vecin.getItem().getPointsNames()
		names = []
		for i in range(len(names_tot)): 
			n = str(names_tot[i])
			if n.find(str(self.Name)) == 0 or self.Name == "": 
				names.append(n)
		attr_tmp = self.vecin.getItem().getAttributeNames()
		for i in range(len( attr_tmp)):
			attr.append(attr_tmp[i])
		for i in range(len(names)): 
			#Append Attributes
			if names[i] in attr:
				alist = self.vecin.getItem().getAttributes(names[i]).getAttributeNames()   
				#Check if attribute exists             
				for j in range(len(alist)):
					hasAttribute = True                            
					if (alist[j] in AttributeList) == False:
						fielddef = osgeo.ogr.FieldDefn(alist[j], osgeo.ogr.OFTReal)
						layer.CreateField(fielddef)
						layerDefinition = layer.GetLayerDefn()  
						log(alist[j])
						AttributeList.append(alist[j])
				  
				
					
			#Addend Points
			plist = self.vecin.getItem().getPoints(names[i])
			for j in range(len(plist)):    
				point = osgeo.ogr.Geometry(osgeo.ogr.wkbPoint)
				point.SetPoint(0, plist[j].getX()+self.offsetX,  plist[j].getY()+self.offsetY)
				featureIndex = 0
				feature = osgeo.ogr.Feature(layerDefinition)
				feature.SetGeometry(point)
				feature.SetFID(featureIndex) 
				feature.SetField("Z", plist[j].getZ())
				#Append Attributes
				if hasAttribute:      
					for k in range(len(alist)):
						value = self.vecin.getItem().getAttributes(names[i]).getAttribute(alist[k])
						feature.SetField(alist[k],value)
				layer.CreateFeature(feature)    
		shapeData.Destroy()
		
	def exportPolyline(self):
		spatialReference = osgeo.osr.SpatialReference()
		spatialReference.ImportFromProj4(self.CoordinateSystem)
		
		#Init Shape Files
		driver = osgeo.ogr.GetDriverByName('ESRI Shapefile')
		if os.path.exists(str(self.getInternalCounter())+"_" +self.FileName+'_lines.shp'): os.remove(str(self.getInternalCounter())+"_" +self.FileName+'_lines.shp')
		shapeData = driver.CreateDataSource(str(self.getInternalCounter())+"_" + self.FileName+'_lines.shp')
		
		layer = shapeData.CreateLayer('layer1', spatialReference, osgeo.ogr.wkbLineString)
		layerDefinition = layer.GetLayerDefn()               
		AttributeList = []
		attr = []
		hasAttribute = False
		#Get Data 
		names_tot = self.vecin.getItem().getEdgeNames()
		names = []
		for i in range(len(names_tot)): 
			n = str(names_tot[i])
			if n.find(str(self.Name)) == 0 or self.Name == "":
				names.append(n)
		attr_tmp = self.vecin.getItem().getAttributeNames()
		for i in range(len( attr_tmp)):
			attr.append(attr_tmp[i])
		for i in range(len(names)): 
			#Append Attributes
			if names[i] in attr:
				alist = self.vecin.getItem().getAttributes(names[i]).getAttributeNames()   
				#Check if attribute exists             
				for j in range(len(alist)):
					hasAttribute = True                                  
					if (alist[j] in AttributeList) == False:
						fielddef = osgeo.ogr.FieldDefn(alist[j], osgeo.ogr.OFTReal)
						layer.CreateField(fielddef)
						layerDefinition = layer.GetLayerDefn()  
						log(alist[j])
						AttributeList.append(alist[j]) 
			
			plist = self.vecin.getItem().getPoints(names[i])
			flist = self.vecin.getItem().getEdges(names[i])

			for j in range(len(flist)):
					
				line = osgeo.ogr.Geometry(osgeo.ogr.wkbLineString)
				edge = flist[j]
				p1 = Point
				p1 = plist[edge.getID1()];
				p2 = Point
				p2 = plist[edge.getID2()];
				line.AddPoint(p1.getX()+self.offsetX, p1.getY()+self.offsetY)
				line.AddPoint(p2.getX()+self.offsetX, p2.getY()+self.offsetY)

				featureIndex = 0
				feature = osgeo.ogr.Feature(layerDefinition)
				feature.SetGeometry(line)
				feature.SetFID(featureIndex)  
				#Append Attributes
				if hasAttribute:        
					for k in range(len(alist)):
						value = self.vecin.getItem().getAttributes(names[i]).getAttribute(alist[k])
						feature.SetField(alist[k],value)
				layer.CreateFeature(feature)    
		shapeData.Destroy()               
	   
