import pandas as pd

def to_xlsx(setOfDataLabel,name):

    counter = 0
    dict={}
    for i in setOfDataLabel:
        dict[counter]={
            "CLIENT":i.factoryRef,
            "REF":i.besoRef,
            "QTY":i.qty,
            "PACK":i.pack,
            "ORDER":i.order,
            "SERIA":"",
            "ID":""
        }
    df = pd.DataFrame.from_dict(dict)
    df.to_excel("excel_label"+"\\"+"etykiety_"+ name+".xlsx")  

