import pandas as pd

from .dics import FID,OID

def order_to_ID(nameOfOrder):
    print(nameOfOrder)
    set = nameOfOrder.split("/")

    if len(set)==4:
        code = OID[ set[0] ] + str( set[1][-1:] ) + str( set[2][-3:] ) + FID[ set[3] ]
        return code

    elif len(set)==5:
        code = OID[ set[0] ] + str( set[3][-1:] ) + str( set[1][-3:] ) + FID[ set[4] ]
        return code
    
    else:
        raise ValueError("out of schema Order")

def number_to_3chars(value):
    if type(value)==int:
        value=str(value)

    if len(value) == 1:
        return("00" + str(value))
    elif len(value) == 2:
        return("0" + str(value))
    elif len(value) == 3:
        return(str(value))
    else:
        raise ValueError("len more than 3")

def make_code(order,ordN,qty,pack):
    segment1 = order_to_ID(order)
    segment2 = number_to_3chars(ordN)
    segment3 = number_to_3chars(qty)
    segment4 = str(pack)
    return(segment1+segment2+segment3+segment4)

def make_dic_from_Optima():
    path = "Optima_raport"
    df=pd.read_excel(path+"\\"+"Rpt.xlsx")
    orders=df["ORDER"].unique()
    dic={}
    for i in orders:
        df1=df[df["ORDER"]==i].reset_index(inplace=False)
        description = df1.loc[0,"PO"]
        country = df1.loc[0,"COUNTRY"]
        df1=df1[["REF","QTY","LP"]]
        df1=df1.set_index('LP').transpose()

        dicOfOrder=df1.to_dict()
        dic[i]={
            "country":country,
            "description":description,
            "order":dicOfOrder
        }
    return(dic)

#ISO 3166-1 Alpha-2 code
def country_to_2chars(nameOfCountry):
    if nameOfCountry!= nameOfCountry:
        return None
    elif len(nameOfCountry) > 2:
        if nameOfCountry.upper() in ["NIEMCY", "GERMANY"]:
            return "DE"
        elif nameOfCountry.upper() in ["SWITZERLAND", "SZWAJCARIA"]:
            return "CH"
        elif nameOfCountry.upper() in ["AUSTRIA", "ÖSTERREICH", "AUT", "OSTERREICH"]:
            return "AT"
        elif nameOfCountry.upper() in ["POLSKA", "POLAND"]:
            return "PL"
        elif nameOfCountry.upper() in ["FRANCJA", "FRANCE"]:
            return "FR"
        elif nameOfCountry.upper() in ["LITWA"]:
            return "LT"
        elif nameOfCountry.upper() in ["ITALY"]:
            return "IT"
        elif nameOfCountry.upper() in ["HISZPANIA", "SPAIN"]:
            return "ES"
        elif nameOfCountry.upper() in ["HOLANDIA"]:
            return "NL"
        else:
            return None
    elif nameOfCountry == "AU":
        return None
    elif len(nameOfCountry) == 2:
        return nameOfCountry
    else:
        return None