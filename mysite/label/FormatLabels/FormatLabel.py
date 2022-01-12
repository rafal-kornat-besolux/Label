from PyPDF2 import PdfFileWriter
from .Combining import combining_universal_10x20, combining_dropshiping_10x20, combining_dropshiping_A4, combining_universal_A4
from .Export import to_xlsx

set_10x20 =  ["STX", "DAS", "MGR", "CHX", "MBS", "BEX", "GIB",
     "MLE","SOB","BSO","DOL","GAL","ZAM","CHB"]
set_specific = ["ANG"]

def case_writer(writer,name,factory_info):

    if "BEX" in name:
        car_number = factory_info
        with open("done_label"+"\\"+"10x20 "+ car_number +" etykiety_" + name + ".pdf", 'wb') as f:
            writer.write(f)
    else:
        with open("done_label"+"\\"+"10x20 etykiety_" + name + ".pdf", 'wb') as f:
            writer.write(f)

class FormatLabel:
    is_made=0

    def __init__(self,setOfDataLabel,name,extra = "",client = "",factory_info = "None"):
        writer = PdfFileWriter()
        if setOfDataLabel[0].type_label == 1:
            if setOfDataLabel[0].order[-3:] in set_10x20:
                writer = combining_universal_10x20(writer,setOfDataLabel)
                case_writer(writer,name,factory_info)
                self.is_made=1
            else:
                writer = combining_universal_A4(writer,setOfDataLabel,extra)
                case_writer(writer,name,factory_info)
                self.is_made=1
        elif setOfDataLabel[0].type_label == 2:
            if setOfDataLabel[0].order[-3:] in set_10x20:
                writer = combining_dropshiping_10x20(writer,setOfDataLabel,extra,client)
                case_writer(writer,name,factory_info)
                self.is_made=1
            else:
                writer = combining_dropshiping_A4(writer,setOfDataLabel,extra,client)
                case_writer(writer,name,factory_info)
                self.is_made=1
        elif setOfDataLabel[0].type_label == 0:
            pass           
        elif setOfDataLabel[0].type_label == 1.5:
            to_xlsx(setOfDataLabel,name)
        else:
            return None
