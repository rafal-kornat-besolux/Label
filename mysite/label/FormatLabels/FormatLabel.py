from PyPDF2 import PdfFileWriter
from .Combining import combining_universal_10x20, combining_dropshiping_10x20, combining_dropshiping_A4 

set_10x20 =  ["STX", "DAS", "MGR", "CHX", "MBS", "BEX", "GIB",
     "MLE", "ANG","SOB","BSO","DOL","GAL","ZAM","CHB"]

class FormatLabel:

    def __init__(self,setOfDataLabel,name,extra=""):

        writer = PdfFileWriter()
        if setOfDataLabel[0].type_label == 1:
            writer = combining_universal_10x20(writer,setOfDataLabel)
            with open("done_label"+"\\"+"10x20 etykiety_" + name+".pdf", 'wb') as f:
                writer.write(f)
        elif setOfDataLabel[0].type_label == 2:
            if setOfDataLabel[0].order[-3:] in set_10x20:
                writer = combining_dropshiping_10x20(writer,setOfDataLabel,extra)
                with open("done_label"+"\\"+"10x20 etykiety_" + name+".pdf", 'wb') as f:
                    writer.write(f)
            else:
                writer = combining_dropshiping_A4(writer,setOfDataLabel,extra)
                with open("done_label"+"\\"+"A4 etykiety_" + name+".pdf", 'wb') as f:
                    writer.write(f)
                
        elif setOfDataLabel[0].type_label == 0:
            pass           
        else:
            return None
