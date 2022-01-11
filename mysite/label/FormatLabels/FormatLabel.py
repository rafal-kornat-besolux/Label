from PyPDF2 import PdfFileWriter
from .Combining import combining_universal_10x20, combining_dropshiping_10x20, combining_dropshiping_A4, combining_universal_A4
from .Export import to_xlsx

set_10x20 =  ["STX", "DAS", "MGR", "CHX", "MBS", "BEX", "GIB",
     "MLE","SOB","BSO","DOL","GAL","ZAM","CHB"]
set_specific = ["ANG"]

class FormatLabel:
    is_made=0

    def __init__(self,setOfDataLabel,name,extra = "",client = ""):
        writer = PdfFileWriter()
        if setOfDataLabel[0].type_label == 1:
            if setOfDataLabel[0].order[-3:] in set_10x20:
                writer = combining_universal_10x20(writer,setOfDataLabel)
                with open("done_label"+"\\"+"10x20 etykiety_" + name + ".pdf", 'wb') as f:
                    writer.write(f)
                self.is_made=1
            else:
                writer = combining_universal_A4(writer,setOfDataLabel,extra)
                with open("done_label"+"\\"+"A4 etykiety_" + name + ".pdf", 'wb') as f:
                    writer.write(f)
                self.is_made=1
        elif setOfDataLabel[0].type_label == 2:
            if setOfDataLabel[0].order[-3:] in set_10x20:
                writer = combining_dropshiping_10x20(writer,setOfDataLabel,extra,client)
                with open("done_label"+"\\"+"10x20 etykiety_" + name + ".pdf", 'wb') as f:
                    writer.write(f)
                self.is_made=1
            else:
                writer = combining_dropshiping_A4(writer,setOfDataLabel,extra,client)
                with open("done_label"+"\\"+"A4 etykiety_" + name + ".pdf", 'wb') as f:
                    writer.write(f)
                self.is_made=1
        elif setOfDataLabel[0].type_label == 0:
            pass           
        elif setOfDataLabel[0].type_label == 1.5:
            to_xlsx(setOfDataLabel,name)
        else:
            return None
