import os
import tempfile

import pandas as pd
import datetime

from sre_constants import AT_END
from .models import  Order, Factory
from .client.clientType import CWR

from datetime import datetime

from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext

def checkFactoryApproval(allOrders):
    for order in allOrders:
        orderRequirement = order.factory.orderRequirement
        labelInfoRequirement = order.factory.labelInfoRequirement
        labelCodeRequirement = order.factory.labelCodeRequirement
        factoryReferenceRequirement = order.factory.factoryReferenceRequirement
        
        if orderRequirement == False and labelInfoRequirement == False and factoryReferenceRequirement == False and labelCodeRequirement== False and factoryReferenceRequirement == False:
            order.factoryApproval = True
            order.save()

def checkClientApproval(allOrders):
    for order in allOrders:
        print(order.name)
        print(order.client)
        if order.client==None:
            order.clientApproval = True
            order.save()
        elif order.client.type == "Casual":
            order.clientApproval = True
            order.save()

def shiping_schedule():
    site_url = "https://besolux.sharepoint.com/sites/SharePoint-Logistics"
    ctx = ClientContext(site_url).with_credentials(UserCredential("rafal.k@Besolux.onmicrosoft.com", "Bun19822"))


    file_url = "/sites/SharePoint-Logistics/Shared Documents/SHIPPING_SCHEDULE_2022_v2.xlsx"

    download_path = os.path.join(tempfile.mkdtemp(), os.path.basename(file_url))
    with open(download_path, "wb") as local_file:
        file = ctx.web.get_file_by_server_relative_path(file_url).download(local_file).execute_query()
    return download_path

def datafromSheet(df,order):
    indexArray = df[df["OPTIMAORDERNUMBER"] == order.name].index
    print(order.name)
    
    if len(indexArray) == 1:
        indexOfArray = indexArray[0]
    else:
        print(indexArray)
            
    dataClient = df.loc[indexOfArray,"NAME"]
    dataC = dataClient.split(" ")
    if len(dataC)==2:
        name = dataC[0]
        surname = dataC[1]
    elif len(dataC)==1:
        name = dataC[0]
        surname = ""
    elif len(dataC)>2:
        name =  dataC[0]
        surname = ""
        for d in dataC[1:]:
            surname = surname + d +" "

    street = df.loc[indexOfArray,"STREET"]
    numberOfBuilding = df.loc[indexOfArray,"NUMBER BUILDING"]
    numberOfHouse = df.loc[indexOfArray,"NUMBER HOUSE"]
    city = df.loc[indexOfArray,"CITY"]
    postal = df.loc[indexOfArray,"POSTAL"]
    email = df.loc[indexOfArray,"EMAIL"]
    phone = df.loc[indexOfArray,"PHONE"]

    production= df.loc[indexOfArray,"PRODUCTION DATE YY/MM/DD"]
    dropshipingPartner = df.loc[indexOfArray,"DROPSHIPPING PARTNER"]
    if name==name:
        order.nameOfClient = name
    if surname== surname:
        order.surnameOfClient = surname
    if street==street:
        order.street = street
    if numberOfBuilding==numberOfBuilding:
        order.numberOfStreet = numberOfBuilding
    if numberOfHouse==numberOfHouse:
        order.numberofFlat = numberOfHouse
    if city==city:
        order.city = city
    if postal == postal:
        order.code = postal
    if email==email:
        order.email = email
    if phone==phone:
        order.phone = phone
    print(type(production))
    if type(production)==datetime:
        order.productionDate = production
    else:
        order.productionDate = datetime.strptime(production, "%d.%m.%Y")
    order.dropshipingPartner = dropshipingPartner

    return order

def check_Agediss(order):
    #city
    if order.city != order.city:
        return "no city",order
    #postal code
    elif order.code != order.code:
        return "no code",order
    elif type(order.code)== str and "-" in order.code:
        order.code = order.code.replace("-","")
    #phone
    elif order.phone != order.phone:
        return "no phone",order        
    elif order.nameOfClient != order.nameOfClient:
        return "no name of Client",order
    

    return "OK",order
    
def addClientData(allOrders):
    downloading_file = shiping_schedule()
    df_SS_FR = pd.read_excel(downloading_file, sheet_name="Dropshipping FR")
    df_SS_PL = pd.read_excel(downloading_file, sheet_name="Polska")
    df_SS_EU = pd.read_excel(downloading_file, sheet_name="EU")
    df_SS_DEU = pd.read_excel(downloading_file, sheet_name="Dropshipping EU")
    df_SS_courier = pd.read_excel(downloading_file, sheet_name="Courier")

    ordersInDropshipingFR = df_SS_FR["OPTIMAORDERNUMBER"].tolist()
    ordersInPolska = df_SS_PL["OPTIMAORDERNUMBER"].tolist()
    for order in allOrders:
        # check if order in Dropshipping FR
        if order.name in ordersInDropshipingFR:
            df = df_SS_FR
            order = datafromSheet(df,order)
            text,order = check_Agediss(order)
            print(text)
            if text == "OK":
                order.correctnessOfData = True
                order.save()
