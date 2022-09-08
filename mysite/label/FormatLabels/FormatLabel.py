from PyPDF2 import PdfFileWriter
from .Combining import combining_universal_10x20, combining_dropshiping_10x20, combining_dropshiping_A4, combining_universal_A4
from .Export import to_xlsx
import os

def case_writer(writer,label):
    nameOfOrder = label.order.replace("/","_")

    if os.path.exists("done_label\\"+nameOfOrder) == False:
        os.mkdir("done_label\\"+nameOfOrder)

    if label.orderRequirement == True:
        with open("done_label\\"+nameOfOrder+"\\" + label.typeOfLabel+" "+ label.factory_info +" etykiety_" + nameOfOrder + ".pdf", 'wb') as f:
            writer.write(f)
    else:
        with open("done_label\\"+nameOfOrder+"\\" + label.typeOfLabel + " etykiety_" + nameOfOrder + ".pdf", 'wb') as f:
            writer.write(f)

class FormatLabel:
    is_made=0
    
    def __init__(self,setOfDataLabel):
        writer = PdfFileWriter()
    
        if setOfDataLabel[0].typeClient == "Casual" and setOfDataLabel[0].typeOfLabel == "10x20":
            writer = combining_universal_10x20(writer,setOfDataLabel)
            case_writer(writer,setOfDataLabel[0])
            self.is_made=1
        elif setOfDataLabel[0].typeClient == "Casual" and setOfDataLabel[0].typeOfLabel == "A4":
            writer = combining_universal_A4(writer,setOfDataLabel)
            case_writer(writer,setOfDataLabel[0])
            self.is_made=1
        elif setOfDataLabel[0].typeClient == "CasualOneInformation":
            pass
        elif setOfDataLabel[0].typeClient == "DropshippingOutside" and setOfDataLabel[0].typeOfLabel == "10x20":
            pass
            # writer = combining_dropshiping_10x20(writer,setOfDataLabel,extra,client)
            # case_writer(writer,setOfDataLabel[0])
            # self.is_made=1
        elif setOfDataLabel[0].typeClient == "DropshippingOutside" and setOfDataLabel[0].typeOfLabel == "A4":
            pass
            # writer = combining_dropshiping_A4(writer,setOfDataLabel,extra,client)
            # case_writer(writer,setOfDataLabel[0])
            # self.is_made=1        
        elif setOfDataLabel[0].typeClient == "Dropshipping":
            pass
        else:
            return None
