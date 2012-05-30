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
import subprocess

class peformance_assessment(Module):
    """Writes the XML file input of the CityDrain3 simulation and calls the program
    This module is not accompanied by a GUI, rather, it is solely responsible for managing
    the CityDrain3 simulation (and other future interfaces).
	
	Several outputs are provided from this script.
	- blockcity
            The up-to-date block-based city representation. A grid of blocks created
            through the previous scripts in the BPM
        - performance indicators
            A comprehensive list of performance indicators for the city/blocks
            depending on the parameter. Local parameters are written into the
            block grid
        - inputs:
            Up to date block-size

    v0.75 update (October 2011):
        - Linked the delineated network from delinblocks.py into the XML writer
        - Added coordinates to the CityDrain3 file so that viewing the file will show
        catchment outline.
        Future work:
            - Add EPANET and other Model compatibility
            - Update the CityDrain3 Modules to contain more sub-models that can be called
            - Update the XML creation process to include new CD3 Modules
            - Update the attributes list to include new CD3 Modules
    
    v0.5 update (August 2011):
        - Added a fork into the program depending on whether the simulation is embedded
        in DAnCE4Water or whether it stands by itself
        - The new fork writes CityDrain3 attributes to a separate vector output in string
        format, which is broken up by the internal CityDrain3 Module.
        - Added first bits of parameter inputs into the CityDrain3 XML writing section.
        
    v0.5 first (July 2011):
        - Created code to write the XML file for a simple set of blocks in the landscape
        - Tested simple tool on CityDrain3
	
	@ingroup DAnCE4Water, CityDrain3
	@author Peter M Bach
	"""
    def __init__(self):
        Module.__init__(self)
        self.blockcityin = VectorDataIn
        self.blockcityout = VectorDataIn
        self.perf_indicators = VectorDataIn
        
        self.addParameter(self, "blockcityin", VIBe2.VECTORDATA_IN)
        self.addParameter(self, "blockcityout", VIBe2.VECTORDATA_OUT)
        self.addParameter(self, "perf_indicators", VIBe2.VECTORDATA_OUT)
    
    def run(self):
        blockcityin = self.blockcityin.getItem()
        blockcityout = self.blockcityout.getItem()
        perf_indicators = self.perf_indicators.getItem()
        
        map_attr = blockcityin.getAttributes("MapAttributes")
        cd3simulation_config = blockcityin.getAttributes("CD3simulation_config")
        
        #get data needed to being for loop analysis
        blocks_num = map_attr.getAttribute("NumBlocks")     #number of blocks to loop through
        blocks_size = map_attr.getAttribute("BlockSize")    #size of block
        map_w = map_attr.getAttribute("WidthBlocks")        #num of blocks wide
        map_h = map_attr.getAttribute("HeightBlocks")       #num of blocks tall
        input_res = map_attr.getAttribute("InputReso")      #resolution of input data
        
        #get CityDrain Simulation Details
        cd3_exe_location = cd3simulation_config.getStringAttribute("CD3ExePath")
        rain_fname = cd3simulation_config.getStringAttribute("RainPath")
        evap_fname = cd3simulation_config.getStringAttribute("EvapPath")
        solar_fname = cd3simulation_config.getStringAttribute("SolarPath")
        rain_dt = cd3simulation_config.getAttribute("Rain_dt")*60
        
        #get and convert scaling factors string attribute into matrix 
        #(NOTE THAT THE VALUES ARE STILL STRINGS,USE FLOAT TO CONVERT THOSE)
        rsf_matrix = cd3simulation_config.getStringAttribute("rsf_matrix").split("*|*")
        esf_matrix = cd3simulation_config.getStringAttribute("esf_matrix").split("*|*")
        ssf_matrix = cd3simulation_config.getStringAttribute("ssf_matrix").split("*|*")
        
        #BEGIN PERF ASSESSMENT BASED ON OPTION D4W or BPM
        if cd3simulation_config.getStringAttribute("CD3SimType") == "BPM":
            mapscale = 5
        #######################################################################
        ### SIMULATION TYPE - BPM - Write the XML file manually and run CD3 ###
        #######################################################################
            
            #creates the CityDrain3 xml file from scratch
            f = open("C:\\dance4watercd3pa.xml", 'w')
            
            #BLOCK to define file details
            f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
            f.write("<citydrain version=\"1.0\">\n")
            f.write("\t<pluginpath path=\"nodes\"/>\n")
            f.write("\t<pythonmodule module=\"C:/Users/Peter M Bach/Documents/VIBe2 Development/Modules/__d4wBPM/CD3 Nodes/dance4waterCD3.py\"/>\n")
            
            #BLOCK to define <simulation> details
            f.write("\t<simulation class=\"DefaultSimulation\">\n")
            f.write("\t\t<time start=\"1959-Jan-01 00:00:00\" stop=\"1959-Dec-31 23:00:00\" dt=\""+str(int(rain_dt))+"\">\n")          #this will need to be replaced in future with ppa_gui's new date/time feature
            f.write("\t\t\t<flowdefinition>\n")
            f.write("\t\t\t\t<flow name=\"Q\"/>\n")
            f.write("\t\t\t\t<climatic name=\"Evap\"/>\n")
            #f.write("\t\t\t\t<climatic name=\"Solar\"/>\n")
            f.write("\t\t\t\t<concentration name=\"TN\"/>\n")
            f.write("\t\t\t\t<concentration name=\"TP\"/>\n")
            f.write("\t\t\t\t<concentration name=\"TSS\"/>\n")
            f.write("\t\t\t</flowdefinition>\n")
            f.write("\t\t</time>\n")
            f.write("\t</simulation>\n")
            
            #BLOCK to define <model> details
            f.write("\t<model>\n")
            f.write("\t\t<nodelist>\n")
            
            #LOOP FOR <nodelist>
            for i in range(int(blocks_num)):
                currentID = i + 1
                currentAttList = blockcityin.getAttributes("BlockID"+str(currentID))        #attribute list of current block structure
                
                if currentAttList.getAttribute("Status") == 0:
                    continue
                
                #define the incoming JUNCTION node
                f.write("\t\t\t<node id=\"D4Wj"+str(currentID)+"\" class=\"D4Wjunction\"/>\n")
                #write info to cd3attribute list:
                cd3_attr = Attribute()
                cd3_attr.setAttribute("BlockID", currentID)
                cd3_attr.setAttribute("NodeName", "D4Wj"+str(currentID))
                cd3_attr.setAttribute("NodeType", "J")                          #Node Types: C=catchment, R=rain, E=evap, S=solar, T=treatment, Q=quality, J=junction, F = FileOut
                cd3_attr.setAttribute("Centre_x", currentAttList.getAttribute("Centre_x"))
                cd3_attr.setAttribute("Centre_y", currentAttList.getAttribute("Centre_y"))
                blockcityout.setAttributes("CityDrain3_ID"+str(currentID)+"J", cd3_attr)
                cd3_ports = Attribute()
                cd3_ports.setAttribute("Port1", 0)
                cd3_ports.setAttribute("Port2", 0)
                cd3_ports.setAttribute("Port3", 0)
                cd3_ports.setAttribute("Port4", 0)
                cd3_ports.setAttribute("Port5", 0)
                cd3_ports.setAttribute("Port6", 0)
                cd3_ports.setAttribute("Port7", 0)
                cd3_ports.setAttribute("Port8", 0)
                blockcityout.setAttributes("CityDrain3_ID"+str(currentID)+"JP", cd3_ports)
                
                #define the RAIN_READ Node
                f.write("\t\t\t<node id=\"Rain"+str(currentID)+"\" class=\"IxxRainRead_v2\">\n")
                f.write("\t\t\t\t<parameter name=\"rain_file\" type=\"string\" value=\""+str(rain_fname)+"\"/>\n")
                f.write("\t\t\t</node>\n")    
                #write info to cd3attribute list:
                cd3_attr = Attribute()
                cd3_attr.setAttribute("BlockID", currentID)
                cd3_attr.setAttribute("NodeName", "Rain"+str(currentID))
                cd3_attr.setAttribute("NodeType", "R")                          
                cd3_attr.setAttribute("Centre_x", currentAttList.getAttribute("Centre_x"))
                cd3_attr.setAttribute("Centre_y", currentAttList.getAttribute("Centre_y"))
                blockcityout.setAttributes("CityDrain3_ID"+str(currentID)+"R", cd3_attr)
                
                #define the CATCHMENT Node
                f.write("\t\t\t<node id=\"BlockID_"+str(currentID)+"\" class=\"D4Wcatchment\">\n")
                f.write("\t\t\t\t<parameter name=\"Imp\" type=\"double\" value=\"0.72999999999999998\"/>\n")
                f.write("\t\t\t\t<parameter name=\"muskK\" type=\"double\" value=\"30\"/>\n")
                f.write("\t\t\t\t<parameter name=\"Spervmax\" type=\"double\" value=\"18\"/>\n")
                f.write("\t\t\t\t<parameter name=\"catchment_area\" type=\"double\" value=\"100\"/>\n")
                f.write("\t\t\t\t<parameter name=\"theta\" type=\"double\" value=\"0.25\"/>\n")
                f.write("\t\t\t\t<parameter name=\"route_method\" type=\"int\" value=\"1\"/>\n")
                f.write("\t\t\t</node>\n")
                #write info to cd3attribute list:
                cd3_attr = Attribute()
                cd3_attr.setAttribute("BlockID", currentID)
                cd3_attr.setAttribute("NodeName", "BlockID_"+str(currentID))
                cd3_attr.setAttribute("NodeType", "C")                          
                cd3_attr.setAttribute("Centre_x", currentAttList.getAttribute("Centre_x"))
                cd3_attr.setAttribute("Centre_y", currentAttList.getAttribute("Centre_y"))
                blockcityout.setAttributes("CityDrain3_ID"+str(currentID)+"C", cd3_attr)
                
                #define WATER_QUALITY node
                f.write("\t\t\t<node id=\"WQ"+str(currentID)+"\" class=\"D4W_WQ\">\n")
                f.write("\t\t\t\t<parameter name=\"TN_BF_mean\" type=\"double\" value=\"0.32000000000000001\"/>\n")
                f.write("\t\t\t\t<parameter name=\"TN_BF_stdev\" type=\"double\" value=\"0.12\"/>\n")
                f.write("\t\t\t\t<parameter name=\"TN_SF_mean\" type=\"double\" value=\"0.41999999999999998\"/>\n")
                f.write("\t\t\t\t<parameter name=\"TN_SF_stdev\" type=\"double\" value=\"0.19\"/>\n")
                f.write("\t\t\t\t<parameter name=\"TP_BF_mean\" type=\"double\" value=\"-0.81999999999999995\"/>\n")
                f.write("\t\t\t\t<parameter name=\"TP_BF_stdev\" type=\"double\" value=\"0.19\"/>\n")
                f.write("\t\t\t\t<parameter name=\"TP_SF_mean\" type=\"double\" value=\"-0.45000000000000001\"/>\n")
                f.write("\t\t\t\t<parameter name=\"TP_SF_stdev\" type=\"double\" value=\"0.25\"/>\n")
                f.write("\t\t\t\t<parameter name=\"TSS_BF_mean\" type=\"double\" value=\"1.1000000000000001\"/>\n")
                f.write("\t\t\t\t<parameter name=\"TSS_BF_stdev\" type=\"double\" value=\"0.17000000000000001\"/>\n")
                f.write("\t\t\t\t<parameter name=\"TSS_SF_mean\" type=\"double\" value=\"2.2000000000000002\"/>\n")
                f.write("\t\t\t\t<parameter name=\"TSS_SF_stdev\" type=\"double\" value=\"0.32000000000000001\"/>\n")
                f.write("\t\t\t</node>\n")
                #write info to cd3attribute list:
                cd3_attr = Attribute()
                cd3_attr.setAttribute("BlockID", currentID)
                cd3_attr.setAttribute("NodeName", "WQ"+str(currentID))
                cd3_attr.setAttribute("NodeType", "Q")
                cd3_attr.setAttribute("Centre_x", currentAttList.getAttribute("Centre_x"))
                cd3_attr.setAttribute("Centre_y", currentAttList.getAttribute("Centre_y"))
                blockcityout.setAttributes("CityDrain3_ID"+str(currentID)+"Q", cd3_attr)
                
                #output box if downstrID == 0
                if currentAttList.getAttribute("downstrID") == -1:
                    f.write("\t\t\t<node id=\"FOut"+str(currentID)+"\" class=\"FileOut\">\n")
                    f.write("\t\t\t\t<parameter name=\"out_file_name\" type=\"string\" value=\"block"+str(currentID)+"output.txt\"/>\n")
                    f.write("\t\t\t</node>\n")
                    cd3_attr = Attribute()
                    cd3_attr.setAttribute("BlockID", currentID)
                    cd3_attr.setAttribute("NodeName", "FOut"+str(currentID))
                    cd3_attr.setAttribute("NodeType", "F")
                    cd3_attr.setAttribute("Centre_x", currentAttList.getAttribute("Centre_x"))
                    cd3_attr.setAttribute("Centre_y", currentAttList.getAttribute("Centre_y"))
                    blockcityout.setAttributes("CityDrain3_ID"+str(currentID)+"F", cd3_attr)
                    
            f.write("\t\t</nodelist>\n")
            f.write("\t\t<connectionlist>\n")
            connection_counter = 0

            #PART A - connect modules within Blocks
            for i in range(int(blocks_num)):
                currentID = i + 1
                currentAttList = blockcityin.getAttributes("BlockID"+str(currentID))        #attribute list of current block structure
                
                if currentAttList.getAttribute("Status") == 0:
                    continue
                
                if currentAttList.getAttribute("downstrID") == -1:
                    fout_exist = True
                else:
                    fout_exist = False
                
                #connect junction with catchment
                f.write("\t\t\t<connection id=\""+str(connection_counter)+"\">\n")
                f.write("\t\t\t\t<source node=\"D4Wj"+str(currentID)+"\" port=\"out\"/>\n")
                f.write("\t\t\t\t<sink node=\"BlockID_"+str(currentID)+"\" port=\"upstream\"/>\n")
                f.write("\t\t\t</connection>\n")
                connection_counter += 1
                #connect rain with catchment
                f.write("\t\t\t<connection id=\""+str(connection_counter)+"\">\n")
                f.write("\t\t\t\t<source node=\"Rain"+str(currentID)+"\" port=\"out\"/>\n")
                f.write("\t\t\t\t<sink node=\"BlockID_"+str(currentID)+"\" port=\"raindata\"/>\n")
                f.write("\t\t\t</connection>\n")
                connection_counter += 1
                #connect catchment with water quality, surface
                f.write("\t\t\t<connection id=\""+str(connection_counter)+"\">\n")
                f.write("\t\t\t\t<source node=\"BlockID_"+str(currentID)+"\" port=\"downstream\"/>\n")
                f.write("\t\t\t\t<sink node=\"WQ"+str(currentID)+"\" port=\"in\"/>\n")
                f.write("\t\t\t</connection>\n")
                connection_counter += 1
                #connect catchment with water quality, subsurface
                f.write("\t\t\t<connection id=\""+str(connection_counter)+"\">\n")
                f.write("\t\t\t\t<source node=\"BlockID_"+str(currentID)+"\" port=\"downstream_sub\"/>\n")
                f.write("\t\t\t\t<sink node=\"WQ"+str(currentID)+"\" port=\"ssin\"/>\n")
                f.write("\t\t\t</connection>\n")
                connection_counter += 1
                #connect WQ with FileOut if there is one present
                if fout_exist == True:
                    f.write("\t\t\t<connection id=\""+str(connection_counter)+"\">\n")
                    f.write("\t\t\t\t<source node=\"WQ"+str(currentID)+"\" port=\"out\"/>\n")
                    f.write("\t\t\t\t<sink node=\"FOut"+str(currentID)+"\" port=\"in\"/>\n")
                    f.write("\t\t\t</connection>\n")
                    connection_counter += 1
                
            #PART B - connect blocks with each other at the junctions!    
            output_node_counter = 0
            for i in range(int(blocks_num)):
                currentID = i + 1
                currentAttList = blockcityin.getAttributes("BlockID"+str(currentID))        #attribute list of current block structure
                
                if currentAttList.getAttribute("Status") == 0:
                    continue
                
                downstreamJ = currentAttList.getAttribute("downstrID")
                
                ##POSSIBILITY NO. 1 == Block has a downstream block to flow into
                if int(downstreamJ) > 0:
                    #connect to the corresponding blocks
                    #determine what port of that junction node to connect to:
                    downstrCD3AttList = blockcityout.getAttributes("CityDrain_ID"+str(int(downstreamJ))+"JP")        #get the attributes list for connecting junction node
                    port_found = 0      #while it is zero, no port will have been found!
                    port_counter = 0
                    while port_found == 0:
                        port_counter += 1
                        if int(port_counter) == 9:   #all ports tried, something must be wrong, we raise this problem and break
                            print "Maximum ports exceeded, error!"
                            break
                        if downstrCD3AttList.getAttribute("Port"+str(port_counter)) == 0:
                            f.write("\t\t\t<connection id=\""+str(connection_counter)+"\">\n")
                            f.write("\t\t\t\t<source node=\"WQ"+str(currentID)+"\" port=\"out\"/>\n")
                            f.write("\t\t\t\t<sink node=\"D4Wj"+str(int(downstreamJ))+"\" port=\"in"+str(port_counter)+"\"/>\n")
                            f.write("\t\t\t</connection>\n")
                            downstrCD3AttList.setAttribute("Port"+str(port_counter), 1)
                            blockcityout.setAttributes("CityDrain3_ID"+str(int(downstreamJ))+"JP", downstrCD3AttList)
                            connection_counter += 1
                            port_found = 1
                        else:
                            pass                #port is taken, cannot connect here, must try the next port
                        
                
                ##POSSIBILITY NO. 2 == Block was a local sink and had to be unblocked
#                elif downstreamJ == -1:
                    #connect sink to corresponding draining block
#                    drainJ = currentAttList.getAttribute("drainto_ID")
#                    downstrCD3AttList = blockcityout.getAttributes("CityDrain_ID"+str(drainJ)+"J")        #get the attributes list for connecting junction node
#                    port_found = 0      #while it is zero, no port will have been found!
#                    port_counter = 0
#                    while port_found == 0:
#                        port_counter += 1
#                        if port_counter == 9:   #all ports tried, something must be wrong, we raise this problem and break
#                            print "Maximum ports exceeded, error!"
#                            break
#                        if downstrCD3AttList.getAttribute("Port"+str(port_counter)) == 0:
#                            f.write("\t\t\t<connection id=\""+str(connection_counter)+"\">\n")
#                            f.write("\t\t\t\t<source node=\"WQ"+str(currentID)+"\" port=\"out\"/>\n")
#                            f.write("\t\t\t\t<sink node=\"D4Wj"+str(drainJ)+"\" port=\"in"+str(port_counter)+"\"/>\n")
#                            f.write("\t\t\t</connection>\n")
#                            downstrCD3AttList.setAttribute("Port"+str(port_counter),1)
#                            blockcityout.setAttributes("CityDrain3_ID"+str(drainJ)+"J", downstrCD3AttList)
#                            connection_counter += 1
#                            port_found = 1
#                        else:
#                            pass                #port is taken, cannot connect here, must try the next port
                        
                
                
                
#                ##POSSIBILITY NO. 3 == Block is an outlet and will be connected to an output file
#                else: 
#                    #connect to output node
#                    output_node_counter += 1
                    
                    
            f.write("\t\t</connectionlist>\n")
            f.write("\t\t<gui>\n")
            
            #LOOP FOR <gui> - sets the coordinates of each CityDrain3 Node
            for i in range(int(blocks_num)):
                currentID = i + 1
                currentAttList = blockcityin.getAttributes("BlockID"+str(currentID))        #attribute list of current block structure
                if currentAttList.getAttribute("Status") == 0:
                    continue
                x = currentAttList.getAttribute("Centre_x")*mapscale
                y = currentAttList.getAttribute("Centre_y")*mapscale
                if blockcityout.getAttributes("CityDrain3_ID"+str(currentID)+"C").getAttribute("BlockID") != 0:           #Does catchment node exist? If it doesn't then Block ID is 0
                    nname = blockcityout.getAttributes("CityDrain3_ID"+str(currentID)+"C").getStringAttribute("NodeName")
                    f.write("\t\t\t<nodeposition id=\""+nname+"\" x=\""+str(x)+"\" y=\"-"+str(y)+"\"/>\n")                      #if it exists, draw it! Catchmnent in centre
                if blockcityout.getAttributes("CityDrain3_ID"+str(currentID)+"J").getAttribute("BlockID") != 0:             #Junctions to the left
                    nname = blockcityout.getAttributes("CityDrain3_ID"+str(currentID)+"J").getStringAttribute("NodeName")
                    f.write("\t\t\t<nodeposition id=\""+nname+"\" x=\""+str(x-300)+"\" y=\"-"+str(y)+"\"/>\n")
                if blockcityout.getAttributes("CityDrain3_ID"+str(currentID)+"Q").getAttribute("BlockID") != 0:             #Water quality to the right
                    nname = blockcityout.getAttributes("CityDrain3_ID"+str(currentID)+"Q").getStringAttribute("NodeName")
                    f.write("\t\t\t<nodeposition id=\""+nname+"\" x=\""+str(x+400)+"\" y=\"-"+str(y)+"\"/>\n")
                if blockcityout.getAttributes("CityDrain3_ID"+str(currentID)+"R").getAttribute("BlockID") != 0:             #Rainfall top left
                    nname = blockcityout.getAttributes("CityDrain3_ID"+str(currentID)+"R").getStringAttribute("NodeName")
                    f.write("\t\t\t<nodeposition id=\""+nname+"\" x=\""+str(x-300)+"\" y=\"-"+str(y+200)+"\"/>\n")
                if blockcityout.getAttributes("CityDrain3_ID"+str(currentID)+"F").getAttribute("BlockID") != 0:             #Rainfall top left
                    nname = blockcityout.getAttributes("CityDrain3_ID"+str(currentID)+"F").getStringAttribute("NodeName")
                    f.write("\t\t\t<nodeposition id=\""+nname+"\" x=\""+str(x+400)+"\" y=\"-"+str(y-200)+"\"/>\n")
                
                
                
            f.write("\t\t</gui>\n")
            f.write("\t</model>\n")
            f.write("</citydrain>\n") #FINAL LINE TO CLOSE <citydrain> section
            f.close() #save and close xml file
            
            
            #CALL CITYDRAIN3.exe
#            print "Calling CityDrain3"
#            subprocess.call([str(cd3_exe_location), "-mC:\\dance4watercd3.xml"])
            
            #BEGIN GETTING RESULTS FROM CITYDRAIN
    #        result_file = open("Results.txt", 'r')
    #        result_time_seris = open("Time_Series.txt", 'r')
            for i in range(int(blocks_num)):
                currentID = i + 1
                currentAttList = blockcityin.getAttributes("BlockID"+str(currentID))        #attribute list of current block structure
                plist = blockcityin.getPoints("BlockID"+str(currentID))
                flist = blockcityin.getFaces("BlockID"+str(currentID))
                blockcityout.setPoints("BlockID"+str(currentID),plist)
                blockcityout.setFaces("BlockID"+str(currentID),flist)
                blockcityout.setAttributes("BlockID"+str(currentID), currentAttList)
            
        else:    
        
        ######################################################################################
        ### SIMULATION TYPE - D4W - Write the output attributes list for VIBe2 to interpret###
        ######################################################################################
            
            #loop through blocks, create CityDrain3_IDx Attribute lists in the attributes table
            currentCD3ID = 0
            for i in range(int(blocks_num)):
                currentID = i + 1
                currentCD3ID += 1
                currentAttList = blockcityin.getAttributes("BlockID"+str(currentID))        #attribute list of current block structure
                currentParList = blockcityin.getAttributes("BlockID"+str(currentID)+"_params")
                plist = blockcityin.getPoints("BlockID"+str(currentID))
                flist = blockcityin.getFaces("BlockID"+str(currentID))
            
                #Find out for current block how many CityDrain3 entries are required
                #(To Do at a later stage) - probably ONE block and ONE for each point/edge probably outside this loop
                cd3_attr = Attribute()
                cd3_attr.setAttribute("CityDrain3_ID", currentCD3ID)
                cd3_attr.setAttribute("BlockID", currentID)
                cd3_attr.setAttribute("Type", "Block")
                cd3_attr.setAttribute("Filename", "simplecatchment.xml")
                cd3_attr.setAttribute("Receiving", 0)
                cd3_attr.setAttribute("CD3ATTR*|*D4Wcatchment*|*catchment_area", blocks_size*blocks_size/10000)
                cd3_attr.setAttribute("CD3ATTR*|*D4Wcatchment*|*Spervmax", currentParList.getAttribute("Spervmax"))
                cd3_attr.setAttribute("CD3ATTR*|*D4Wcatchment*|*Simpmax", currentParList.getAttribute("Simpmax"))
                cd3_attr.setAttribute("CD3ATTR*|*D4Wcatchment*|*muskK", currentParList.getAttribute("muskK"))
                cd3_attr.setAttribute("CD3ATTR*|*D4Wcatchment*|*theta", currentParList.getAttribute("muskTheta"))
                cd3_attr.setAttribute("CD3ATTR*|*D4Wcatchment*|*route_method", currentParList.getAttribute("route_method"))
                cd3_attr.setAttribute("CD3ATTR*|*D4Wcatchment*|*Imp", currentAttList.getAttribute("ResEIF"))
                cd3_attr.setAttribute("CD3ATTR*|*IxxRainRead*|*rain_file", rain_fname)
                blockcityout.setAttributes("CityDrain3_ID"+str(currentCD3ID), cd3_attr)
            
                blockcityout.setPoints("BlockID"+str(currentID),plist)
                blockcityout.setFaces("BlockID"+str(currentID),flist)
                blockcityout.setAttributes("BlockID"+str(currentID),currentAttList)
            
        #Output vector update
        blockcityout.setAttributes("MapAttributes", map_attr)
        

        