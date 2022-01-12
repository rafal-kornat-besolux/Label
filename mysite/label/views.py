from django.http import HttpResponse
import requests
import json
import pandas as pd
import os 

from django.shortcuts import get_object_or_404
from django_tables2 import SingleTableView
from .Tables import FurnitureTable, OrderTable, OrderProductTable, PackageTable

from .FormatLabels.FormatLabel import FormatLabel
from .DataLabels.DataLabel import Label
# from .Email.Email import Mail
from .FunctionPackages import make_dic_from_Optima, country_to_2chars
from .FunctionVP import campaign_to_dic
from .FunctionBZC import zpl_to_pdf_bzc
from .Factory import updater_factory_info
from .models import Furniture, Order, OrderProduct, Package, PackageFromClient,Transporter, Campaign

from django.core.mail import EmailMessage

def index(request):
    return HttpResponse("hi")

def fetchpimcore(request):
    request_url = 'http://pim.besolux.com/pimcore-graphql-webservices/graphql?apikey=e1323dd9c2c04563240eddc9d4583799'
    after=0
    while True:
        query = """query {
            getProductListing(first:100, after: """+str(after)+""",filter: "{\\"isParent\\": {\\"$like\\" : \\"parent\\"}}") {
                edges {
                node {
                    besoLuxRef
                    producersReference
                    brandRel
                    fColor
                    legsPlacement
                    packagesQuantity
                    children (objectTypes:["variant"]) {
                    ...on object_Product {
                        besoLuxRef
                        producersReference
                        ean
                        titleForLabels
                        fabrics {
                        ...on object_Fabric {
                            series
                            color {
                            ...on object_FabricColor {
                                name(language:"en")
                            }
                            }
                        }
                        }
                    }
                    }
                }
                }
            }
            }
            """
        r = requests.post(request_url, json={'query': query})

        if len(r.text)<45:
            break

        try:
            json_data = json.loads(r.text)
        except:
            return HttpResponse(r.text)

        for parent in json_data["data"]["getProductListing"]["edges"]:
            for child in parent['node']["children"]:
                f = Furniture.objects.filter(besoRef = child["besoLuxRef"])
                k=0
                l=0
                if f.exists():
                    
                    f = f.first()
                    #info from parent
                    f.brand = parent['node']['brandRel']
                    f.legsPlacement = parent['node']['legsPlacement']
                    f.packagesQuantity = parent['node']['packagesQuantity']
                    #info from child
                    f.factoryRef = child["producersReference"]
                    f.ean = child["ean"]
                    f.full = child["titleForLabels"]
                    f.factoryRef = child["producersReference"]
                    #more structure
                    if child["fabrics"]== None:
                        f.fabric = ""
                        f.color = ""
                        k=1
                    elif  child["fabrics"][0]["series"]!= None and child["fabrics"][0]['color'] != None:
                        f.fabric = child["fabrics"][0]["series"]
                        f.color = child["fabrics"][0]['color']["name"]
                        k=2
                    elif child["fabrics"][0]["series"] != None and child["fabrics"][0]['color'] == None:
                        f.fabric = child["fabrics"][0]["series"]
                        f.color = ""
                        k=3
                    elif child["fabrics"][0]["series"] == None and child["fabrics"][0]['color'] != None:
                        f.fabric = ""
                        f.color = child["fabrics"][0]['color']["name"]
                        k=4
                    else:
                        return HttpResponse(child["besoLuxRef"]+"   k="+str(k)+" l="+str(l)+str(child["fabrics"]))

                else:
                    
                    if child["fabrics"] == None:
                        fabric = ""
                        color = ""
                        l=1
                    elif  child["fabrics"][0]["series"] != None and child["fabrics"][0]['color'] != None:
                        fabric = child["fabrics"][0]["series"]
                        color = child["fabrics"][0]['color']["name"]
                        l=2

                    elif child["fabrics"][0]["series"] != None and child["fabrics"][0]['color'] == None:
                        fabric = child["fabrics"][0]["series"]
                        color = ""
                        l=3
                    elif child["fabrics"][0]["series"] == None and child["fabrics"][0]['color'] != None:
                        fabric = ""
                        color = child["fabrics"][0]['color']["name"]
                        l=4
                    else:
                        return HttpResponse(child["besoLuxRef"]+"   k="+str(k)+" l="+str(l)+str(child["fabrics"]))

                    f = Furniture(
                        #info from parent
                        brand = parent['node']['brandRel'],
                        legsPlacement = parent['node']['legsPlacement'],
                        packagesQuantity = parent['node']['packagesQuantity'],
                        #info from child
                        besoRef = child["besoLuxRef"],
                        factoryRef = child["producersReference"],
                        ean = child["ean"],
                        full = child["titleForLabels"],
                        #more structure
                        fabric = fabric,
                        color = color
                        )
                # try:
                #     f.save()
                # except:
                #     return HttpResponse(child["besoLuxRef"]+"   k="+str(k)+" l="+str(l))

                f.save()
    
    
        after +=100
        
    return HttpResponse("Add and update data from PIM")

def make_order_from_Optima(request):
    text=""
    dic = make_dic_from_Optima()
    for nameOfOrder in dic:
        name=nameOfOrder.replace("_","/")
        order = Order.objects.filter(name = name)
        country = country_to_2chars(dic[nameOfOrder]["country"])
        
        if country == None:
            text = text + "Problem with country "+ dic[nameOfOrder]["country"] + " from " + nameOfOrder + "\n\n"

        else:
            if order.exists()==False:
                ord=Order(
                    name = name,
                    description = dic[nameOfOrder]["description"],
                    country = country
                )
                ord.save()
                check = 0
                for i in dic[nameOfOrder]["order"]:
                    ref = dic[nameOfOrder]["order"][i]["REF"]
                    qty = dic[nameOfOrder]["order"][i]["QTY"]
                    furniture = Furniture.objects.filter(besoRef = ref)
                    if furniture.exists()==True:
                        ordProduct = OrderProduct.create(name,i,ref,qty)
                        ordProduct.save()
                    elif furniture.exists()==False:
                        text = text + "Problem with ref "+ ref + " in " + nameOfOrder + "\n\n"
                        check =1
                if check == 1:
                    ord.delete()

                        

            elif order.exists()==True:
                order=order.first()

                order.country = country
                order.description = dic[nameOfOrder]["description"]
                order.save()
                
                if len(dic[nameOfOrder]["order"]) !=len (OrderProduct.objects.filter(order = order)):

                    text = text + "Problem with order "+ nameOfOrder + ". Number of references : \n Optima:" + str(len(dic[nameOfOrder]["order"])) +"\n System:"+str(len(OrderProduct.objects.filter(order = order))) + "\n\n"
     
                else:
                    for i in dic[nameOfOrder]["order"]:
                        ref = dic[nameOfOrder]["order"][i]["REF"]
                        qty = dic[nameOfOrder]["order"][i]["QTY"]
                        furniture = Furniture.objects.get(besoRef = ref)
                        ordProduct = OrderProduct.objects.filter(
                            order = order,
                            furniture = furniture,
                            quantity = qty,
                            ordinalNumber = i)
                       
                        if ordProduct.exists() == False:
                            ordProduct = OrderProduct.objects.filter(
                            order = order,
                            furniture = furniture
                            )
                            if ordProduct.exists() == True: 
                                ordProduct = ordProduct.first()
                                if ordProduct.quantity != qty:
                                    text = text + "Problem with order "+ nameOfOrder + ". Change number od reference "+ ref +" : \n System:" + str(ordProduct.quantity) +"\n Optima:"+str(qty) + "\n\n"
                
                                elif ordProduct.ordinalNumber != i:
                                    text = text+  "Problem with order "+ nameOfOrder + ". Change ordinal number od reference "+ ref +" : \n System:" + str(ordProduct.ordinalNumber)  +"\n Optima:"+str(i) + "\n\n"
        
                            else:
                                text = text + "Problem with order "+ nameOfOrder + ". No reference "+ ref +" : in System, but we have in Optima." + "\n\n"

    if text != "":
        email = EmailMessage(
                'IT- Problems import order from Optima',
                text,
                'from@example.com',
                cc=["rafal.trachta@besolux.com","rafal.kornat@besolux.com"],
                headers={'Message-ID': 'foo'},
                                    )
        email.send()                    
                
    return HttpResponse("Add orders")

def label_campaign(request,campaign):
    undone = []
    campaign = Campaign.objects.get(name = campaign)
    client = campaign.client
    setorder = Order.objects.filter(description__contains = campaign)
    for a in setorder:
        orderProducts = OrderProduct.objects.filter(order=a)
        x = Package.objects.filter(orderProduct__in = orderProducts)
        set=[]
        for i in x:
            z=Label(i)
            set.append(z)
        
        label_pdf = FormatLabel(set,a.name.replace("/","_"),str(campaign),client)

        if label_pdf.is_made == 1:
            a.is_made = True
            a.save()
        else:
            undone.append(a)

    return HttpResponse("done")

def make_label(request):
    setorder = Order.objects.filter(is_made = False).exclude(description__contains = "VP").exclude(description__contains = "BZC")
    done = []
    for a in setorder:
        orderProducts = OrderProduct.objects.filter(order=a)
        x = Package.objects.filter(orderProduct__in = orderProducts)
        set=[]
        for i in x:
            z=Label(i)
            set.append(z)

        label_pdf = FormatLabel(set,a.name.replace("/","_"),factory_info = a.factory_info)
        
        if label_pdf.is_made == 1:
            a.is_made = True
            a.save()
        else:
            done.append(a)

    text="Zamowienia(NIE VP, NIE BZC) bez etykiet:\n\n"
    for i in done:
        text += "Zamowienie: " + str(i.name) + " Opis: " +  str(i.description)  + "\n"

    # campaings = Campaign.objects.all()
    # text += "\n\nZamowienia VP, BZC bez etykiet:\n\n"
    # for campaign in campaings:
    #     undone = label_campaign(campaign.name)
    #     for i in undone:
    #         text += "Zamowienie: " + str(i.name) + " Opis: " +  str(i.description)  + "\n"

    email = EmailMessage(
                'IT- Problems with labels',
                text,
                'from@example.com',
                cc=["rafal.trachta@besolux.com","rafal.kornat@besolux.com"],
                headers={'Message-ID': 'foo'},
                                    )
    email.send()  
    
    return HttpResponse("we did: " + str(text))

def import_package_VP(request,name):
    if  os.path.isdir("working_labels/VP"+"\\"+name):
        campaign = Campaign.objects.filter(name = name)
        if campaign.exists():
            return HttpResponse("Campaign "+name+" exists.")
        else:
            campaignVP = Campaign(
                name = name,
                client = "VP")
            campaignVP.save()

            dicofCampaign = campaign_to_dic(name)

            for i in dicofCampaign:
                transporter = Transporter.objects.get(name = dicofCampaign[i]["Transporter"])
                furniture = Furniture.objects.get(besoRef = dicofCampaign[i]["ref"])
                packVP = PackageFromClient(
                    campaign = campaignVP,
                    transporter = transporter,
                    furniture = furniture,
                    pack = dicofCampaign[i]["pack"],
                    number = dicofCampaign[i]["Parcel number"]
                )
                packVP.save()
            
            return HttpResponse("Add VP packages- campaign "+ name)
    else:
        return HttpResponse("Campaign "+ name+" has not folder.")

def type_transport(x):
    for i in ["POST_AT","VIR_FR", "ADER", "ASM", "COLISSIMO", "DHL_DE", "GLS", "HOMEDEL_DE", "NOVATI", "SPERRGUT_DE"]:
        if i in x:
            index = x.index(" ")
            index2 = x.index(" ", index+1)
            campaign = x[index:index2]
            campaign = campaign.replace(" ", "")
            return i
    if "BZC" in x:
        return "VIR_FR"

def connect_campaign(request,nameOfCampaign):
    orders = Order.objects.filter(description__contains = nameOfCampaign)
    if orders.exists() == False:
        return HttpResponse("Data from campaign "+nameOfCampaign+" from optima has not been entered.")
    orderProducts = OrderProduct.objects.filter(order__in = orders)
    packages = Package.objects.filter(orderProduct__in = orderProducts)

    campVP = Campaign.objects.get(name = nameOfCampaign)
    packagesVP = PackageFromClient.objects.filter(campaign = campVP)

    if len(packages)==len(packagesVP):
        #check conection VP Optima
        check_connection = 0
        dic={}
        for i in packages:
            dic[i.codeBeso]={
                "ref":i.orderProduct.furniture.besoRef,
                "transporter":type_transport(i.orderProduct.order.description),
                "qty":i.quantity,
                "pack":i.pack
            }
        df = pd.DataFrame.from_dict(dic)
        df = df.transpose()
        df = df.sort_values(by=["ref","transporter", "pack", "qty"])
        df=df.reset_index()
        dicVP={}
        for j in packagesVP:
            dicVP[j.number]={
                "ref":j.furniture.besoRef,
                "transporter":j.transporter.name,
                "pack":j.pack
            }
        dfVP = pd.DataFrame.from_dict(dicVP)
        dfVP = dfVP.transpose()
        dfVP = dfVP.sort_values(by=["ref","transporter","pack"])
        dfVP = dfVP.reset_index()

        campaign_html = dfVP.to_html()
        order_html = df.to_html()

        for i in range(len(df["ref"])):
            if df.loc[i,"ref"]==dfVP.loc[i,"ref"] and df.loc[i,"transporter"]==dfVP.loc[i,"transporter"] and df.loc[i,"pack"]==dfVP.loc[i,"pack"]:
                check_connection+=1
            else:
                return HttpResponse("Incorrect connection.\n"+campaign_html+"\n"+order_html)

        if check_connection == len(packages):

            for i in range(len(df["index"])):
                code = df.loc[i,"index"]
                number = dfVP.loc[i,"index"]
                package = Package.objects.get(codeBeso = code)
                
                packageVP = PackageFromClient.objects.get(number = number)
                

                package.packageFromClient = packageVP
                package.save()

            return HttpResponse(True)
        else:
            return HttpResponse("Incorrect connection.\n")#+"\n"+order_html)
    else:
        return HttpResponse("Parcel difference. Optima ="+str(len(packages))+" , VP ="+str(len(packagesVP)))

def add_tranporter(request):
    for i in ["POST_AT","VIR_FR", "ADER", "ASM", "COLISSIMO", "DHL_DE", "GLS", "HOMEDEL_DE", "NOVATI", "SPERRGUT_DE"]:
        transporter = Transporter(
            name = i
        )   
        transporter.save()
    return HttpResponse("add transporters")

def bzc(request,nameOfCampaign):
    dict=zpl_to_pdf_bzc(nameOfCampaign)
    #"104087"

    for i in dict:
        print(i)

    campaignBZC = Campaign.objects.filter(name = nameOfCampaign)
    if campaignBZC.exists():
        return HttpResponse("Campaign "+nameOfCampaign+" exists.")
    else:
        campaignBZC = Campaign(
            name = nameOfCampaign,
            client = "BZC")
        campaignBZC.save()

        for i in dict:
                transporter = Transporter.objects.get(name = "VIR_FR")
                furniture = Furniture.objects.get(besoRef = dict[i]["REF"])
                packBZC = PackageFromClient(
                    campaign = campaignBZC,
                    transporter = transporter,
                    furniture = furniture,
                    pack = dict[i]["PACK"],
                    number = dict[i]["ID"]
                )
                packBZC.save()

    return HttpResponse("bzc done")

def test(request):
    # df=pd.read_excel("Optima_raport"+"//"+"22_BSO.xlsx")
    
    # order = Order.objects.get(name = "ORD/2021/000022/BSO")
    # orderProduct = OrderProduct.objects.filter(order = order)
    # packages = Package.objects.filter(orderProduct__in = orderProduct)
    # df2 =pd.DataFrame()
    # for i in packages:
    #     df2=df2.append({"ref":i.orderProduct.furniture.besoRef,"pack":i.pack,"quantity":i.quantity,"codeBeso":i.codeBeso}, ignore_index=True)
    # print(df2.columns)
    # df2 = df2.sort_values(by = ["ref","quantity"]).reset_index(drop=True)
    # df = df.sort_values(by = ["ref","qty"]).reset_index(drop=True)

    # for i in range(len(df["ref"])):
    #     packages = Package.objects.get(codeBeso = df2.loc[i,"codeBeso"])
    #     packages.infoFactory = df.loc[i,"code"]
    #     packages.save()

    orders=Package.objects.all()
    for order in orders:
        order.codeFactory = "None"
        order.infoFactory = "None"
        order.save()
    return HttpResponse("done")

def factory(request):
    updater_factory_info()
    return HttpResponse("done")

class FurnitureShow(SingleTableView):
    model = Furniture
    queryset = Furniture.objects.all()
    table_class = FurnitureTable
    template_name = "order.html"

class OrderShow(SingleTableView):
    model = Order
    queryset = Order.objects.all()
    table_class = OrderTable
    template_name = "order.html"

class OrderNoShow(SingleTableView):
    model = Order
    queryset = Order.objects.filter(is_made = False)
    table_class = OrderTable
    template_name = "order.html"

class OrderProductShow(SingleTableView):
    model = OrderProduct
    table_class = OrderProductTable
    template_name = "order.html"
    def get_queryset(self):
        pk = self.kwargs['pk']
        order = Order.objects.get(pk=pk)
        return OrderProduct.objects.filter(order=order)

class PackageShow(SingleTableView):
    model = Package
    table_class = PackageTable
    template_name = "order.html"
    def get_queryset(self):
        pk = self.kwargs['pk']
        order = Order.objects.get(pk=pk)
        orderProduct = OrderProduct.objects.filter(order = order)
        return Package.objects.filter(orderProduct__in = orderProduct)