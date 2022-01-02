from django.http import HttpResponse
import requests
import json
import pandas as pd
import os 

from django.shortcuts import get_object_or_404
from django_tables2 import SingleTableView
from .Tables import OrderTable, OrderProductTable, PackageTable

from .FormatLabels.FormatLabel import FormatLabel
from .DataLabels.DataLabel import Label

from .FunctionPackages import make_dic_from_Optima, country_to_2chars
from .FunctionVP import campaign_to_dic
from .FunctionBZC import zpl_to_pdf_bzc
from .models import Furniture, Order, OrderProduct, Package, PackageFromClient,Transporter, Campaign

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
    dic = make_dic_from_Optima()
    for nameOfOrder in dic:
        name=nameOfOrder.replace("_","/")

        order = Order.objects.filter(name = name)
        if order.exists()==False:
            try:
                country = country_to_2chars(dic[nameOfOrder]["country"])
                if country == None:
                    return HttpResponse("Problem with country: "+str(dic[nameOfOrder]["country"])+" from oreder: "+name)

                ord=Order(
                    name = name,
                    description = dic[nameOfOrder]["description"],
                    country = country
                )
                ord.save()
            except:
                return HttpResponse(dic[nameOfOrder]["description"]+name)

            for i in dic[nameOfOrder]["order"]:
                ref = dic[nameOfOrder]["order"][i]["REF"]
                qty = dic[nameOfOrder]["order"][i]["QTY"]
                ordProduct = OrderProduct.create(name,i,ref,qty)
                ordProduct.save()
        elif order.exists()==True:
            country = country_to_2chars(dic[nameOfOrder]["country"])
            if country == None:
                return HttpResponse("Problem with country: "+str(dic[nameOfOrder]["country"])+" from oreder: "+name)

            order.country = country
            order.description = dic[nameOfOrder]["description"]
            order.save()
            for i in dic[nameOfOrder]["order"]:
                ref = dic[nameOfOrder]["order"][i]["REF"]
                qty = dic[nameOfOrder]["order"][i]["QTY"]
                furniture = Furniture.objects.filter(besoRef = ref)
                ordProduct = OrderProduct.objects.filter(
                    order = order,
                    furniture = furniture,
                    quantity = qty,
                    ordinalNumber = i)
                if ordProduct.exists() == False:
                    return HttpResponse("Problem with:"+order.name+" " + i +" "+ ref+" "+qty)


            
    return HttpResponse("Add orders")

def make_label(request):
    setorder=["CDE/2021/000434/STX","CDE/2021/000444/MBS","CDE/2021/000289/DAS"]
    for a in setorder:
        x = Package.objects.filter(order=Order.objects.get(name=a))
        set=[]
        for i in x:
            z=Label(i)
            set.append(z)

        FormatLabel(set,a.replace("/","_"))
    

    

    return HttpResponse("done")

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

def conect_VP(request,nameOfCampaign):
    orders = Order.objects.filter(description__contains = nameOfCampaign)
    if orders.exists() == False:
        return HttpResponse("Data from campaign "+nameOfCampaign+" from optima has not been entered.")
    orderProducts = OrderProduct.objects.filter(order__in = orders)
    packages = Package.objects.filter(orderProduct__in = orderProducts)

    campVP = Campaign.objects.get(name = nameOfCampaign)
    packagesVP = PackageFromClient.objects.filter(campaign = campVP)

    # for i in packages:
    #     furniture = i.furniture
    #     qty = i.qty
    #     pack = i.pack
    #     try:
    #         transporter = TransporterVP.objects.get(name=type_transport(i.order.description))
    #     except:
    #         return HttpResponse(i.order.description)
    #     campaign = CampaignVP.objects.get(name="MAZZINI20")
    #     packVP = PackageVP.objects.get(
    #         furniture = furniture,
    #         campaignVP = campaign,
    #         transporter = transporter,
    #         rep = qty,
    #         pack = pack
    #       )
    #     i.VP = packVP
    #     i.save()

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

        for i in range(len(df["ref"])):
            if df.loc[i,"ref"]==dfVP.loc[i,"ref"] and df.loc[i,"transporter"]==dfVP.loc[i,"transporter"] and df.loc[i,"pack"]==dfVP.loc[i,"pack"]:
                check_connection+=1
            else:
                return HttpResponse("Incorrect connection.")

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
            return HttpResponse("Incorrect connection.")#+str(len(packages))+" , VP ="+str(len(packagesVP)))
    else:
        return HttpResponse("Parcel difference. Optima ="+str(len(packages))+" , VP ="+str(len(packagesVP)))

def VP_label(request,campaign):
    setorder=Order.objects.filter(description__contains = campaign)
    for a in setorder:
        orderProducts = OrderProduct.objects.filter(order=a)
        x = Package.objects.filter(orderProduct__in = orderProducts)
        set=[]
        for i in x:
            z=Label(i)
            set.append(z)

        FormatLabel(set,a.name.replace("/","_"),campaign)    

    return HttpResponse("done")

def add_tranporter(request):
    for i in ["POST_AT","VIR_FR", "ADER", "ASM", "COLISSIMO", "DHL_DE", "GLS", "HOMEDEL_DE", "NOVATI", "SPERRGUT_DE"]:
        transporter = Transporter(
            name = i
        )   
        transporter.save()
    return HttpResponse("add transporters")

def bzc(request,):
    dict=zpl_to_pdf_bzc("104087")

    for i in dict:
        print(i)
    return HttpResponse("bzc done")

# class OrderList(ListView):
#     model = Order

#     def get(self, request, *args, **kwargs): 
#         orders = Order.objects.all()
#         context  = {'orders':orders}
#         return render(request, 'Template/order_list.html', context)

#     def post(self, request, *args, **kwargs): 
#         pass

class OrderShow(SingleTableView):
    model = Order
    queryset = Order.objects.all()
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