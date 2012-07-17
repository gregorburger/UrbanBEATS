# -*- coding: utf-8 -*-

from pyvibe import *

class VecDataAttributePrinter(Module):
    def __init__(self):
        Module.__init__(self)
        self.vector_data_name = "specify_name"
        self.filename = "Attributes.txt"
        self.blockcityin = VectorDataIn
        self.addParameter(self, "blockcityin", VIBe2.VECTORDATA_IN)
        self.addParameter(self, "vector_data_name", VIBe2.STRING)
        self.addParameter(self, "filename", VIBe2.STRING)
    
    def run(self):
        f = open(self.filename, 'w')
        f.write("Complete Vector Data Attributes List for: "+str(self.vector_data_name)+"\n\n")
        
        blockcityin = self.blockcityin.getItem()
        att_groups = blockcityin.getAttributeNames()
        for i in range(len(att_groups)):
            f.write ("Category: "+str(att_groups[i])+"\n")
            att_names = blockcityin.getAttributes(att_groups[i]).getAttributeNames()
            for j in range(len(att_names)):
                f.write ("\t"+str(att_names[j])+"\n")
        
        f.close()
    