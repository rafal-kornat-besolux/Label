import pandas as pd
import os
import math
from .models import Order, OrderProduct, Package
from django.core.mail import EmailMessage

path_BEX = "working_labels\\Factory\\BEX"

def order_to_name_BEX(order):
    set=order.split("/")
    number=str(int(set[2]))
    return set[0]+number

def info_from_BEX(file):
    df= pd.read_excel(path_BEX+"\\"+file)

    table = []
    for i in df["Unnamed: 4"]:
        if (i != i) == False:
            table.append(i)

    dict={}
    
    for i in range(int(len(table)/2)):
        dict[table[2*i+1]]=table[2*i]

    text = file.split(" ")
    car_number = text[0]
    return car_number , dict

def case_BEX():
    text=""
    setOfOrder = Order.objects.filter(factory_info = "None").filter(name__contains = "BEX")
    for order in setOfOrder:
        orderProducts = OrderProduct.objects.filter(order = order)
        setPackages = Package.objects.filter(orderProduct__in = orderProducts)
        text_to_find = order_to_name_BEX(order.name)
        file_list = os.listdir(path_BEX)
        for file in file_list:
            if text_to_find in file:
                car_number, dict = info_from_BEX(file)
                check = 0
                for pack in setPackages:
                    try:
                        pack.infoFactory = dict[pack.orderProduct.furniture.besoRef]
                        pack.save()
                        check += 1
                    except:
                        text = text + "Problem dla zamowienia"+order.name +" dla ref "+ pack.orderProduct.furniture.besoRef+"\n\n"
                
                if check == len(setPackages):
                    order.factory_info = car_number
                    order.save()
                else:
                    text = text + "Problem dla zamowienia"+order.name +" nie dla wszystkich referencji znlazlo z mapowanie \n\n"
            else:
                text = text + "Problem dla zamowienia"+order.name +" nie ma pliku z BENIXA \n\n"
    return text

def updater_factory_info():
    text=""

    #case BEX
    text= text + case_BEX()

    if text != "":
        email = EmailMessage(
                    'IT- Problems with Facotries IMPORT DATA',
                    text,
                    'from@example.com',
                    cc=["rafal.trachta@besolux.com","rafal.kornat@besolux.com"],
                    headers={'Message-ID': 'foo'},
                                        )
        email.send()