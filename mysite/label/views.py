from asyncio.windows_events import NULL
from django.http import HttpResponse
import requests
import json
import pandas as pd
import os 
from django.core.files.base import File

from django.views.generic.edit import  UpdateView
from .forms import OrderB2CForm

import mimetypes
from django.shortcuts import redirect


from django.shortcuts import get_object_or_404


from .FormatLabels.FormatLabel import FormatLabel
from .DataLabels.DataLabel import Label
# from .Email.Email import Mail
from .FunctionPackages import make_dic_from_Optima, country_to_2chars
from .FunctionVP import campaign_to_dic
from .FunctionBZC import zpl_to_pdf_bzc
from .functionOrders import checkFactoryApproval,checkClientApproval,addClientData
from .factory import updater_factory_info
from .models import Client,Furniture, Order, OrderB2C, OrderProduct, Package, PackageFromClient,Transporter, Campaign,Factory

from django.http import JsonResponse

from django.core.mail import EmailMessage

def index(request):
    return HttpResponse("hi")

def fetchoutofcollection(request):
    request_url = 'http://pim.besolux.com/pimcore-graphql-webservices/outofcollection?apikey=b0860326999c15f5b1e9618062ab7217'
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
        after+=100
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
                    f.outOfCollection = True
                    #more structure
                # try:
                    if child["fabrics"]== None:
                        f.fabric = ""
                        f.color = ""
                    elif  child["fabrics"][0]["series"]!= None and child["fabrics"][0]['color'] != None:
                        f.fabric = child["fabrics"][0]["series"]
                        f.color = child["fabrics"][0]['color']["name"]

                    elif child["fabrics"][0]["series"] != None and child["fabrics"][0]['color'] == None:
                        f.fabric = child["fabrics"][0]["series"]
                        f.color = ""

                    elif child["fabrics"][0]["series"] == None and child["fabrics"][0]['color'] != None:
                        f.fabric = ""
                        f.color = child["fabrics"][0]['color']["name"]

                    else:
                        return HttpResponse(child["besoLuxRef"])
                    f.save()
                    print(child["besoLuxRef"])
                    # except:
                    #     if child["besoLuxRef"] != "CXL_CHSET2_76_F10_LYS1":
                    #         return HttpResponse(child["besoLuxRef"])
                

    return HttpResponse("Add and update data from PIM")

def fetchpimcore(request):
    request_url = 'http://pim.besolux.com/pimcore-graphql-webservices/IT_LOGISTIC?apikey=808e344746070e84579d8dd2c3ba18cd'
    after=0
    while True:
        print(after)
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
                    f.outOfCollection = False
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

def existOfdescriptionClients(value):
    clients = Client.objects.all()
    for client in clients:
        if client.descriptionToFind in value:
            return client
    return False

def make_order_from_Optima(request):
    problems = []
    dic = make_dic_from_Optima()
    for nameOfOrder in dic:
        name = nameOfOrder.replace("_","/")
        order = Order.objects.filter(name = name)
        country = country_to_2chars(dic[nameOfOrder]["country"])
        #to do if factory not exists
        if "SAV" in name or "CLM" in name:
            problems.append([ "Order SAV ", nameOfOrder ])
        elif "ATT" in name or "ATL" in name:
            problems.append([ "Order ATL, ATT", nameOfOrder ])
        elif Factory.objects.filter(shortcut = name[-3:]).count()==0:
            problems.append([ "we can not find a factory",name[-3:]+ " from " + nameOfOrder ])
        elif existOfdescriptionClients(dic[nameOfOrder]["description"]) == False and ("B2C" in name) == False:
            problems.append([ "we can not find a client, Problem with description ", dic[nameOfOrder]["description"] + " from " + nameOfOrder ])
        elif country == None:
            try:
                problems.append([ "Problem with country ", dic[nameOfOrder]["country"] + " from " + nameOfOrder ])
            except:
                problems.append([ "Probably no country ",  nameOfOrder ])
        elif "ORD" in name or "CDE" in name:
            if order.exists()==False:
                ord=Order(
                    name = name,
                    description = dic[nameOfOrder]["description"],
                    country = country,
                    factory = Factory.objects.get(shortcut = name[-3:]),
                    client = existOfdescriptionClients(dic[nameOfOrder]["description"])
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
                        problems.append([ "Problem with ref ", ref + " in " + nameOfOrder ])
                        check =1
                if check == 1:
                    ord.delete()

            elif order.exists()==True:
                order=order.first()

                order.country = country
                order.description = dic[nameOfOrder]["description"]
                order.factory = Factory.objects.get(shortcut = name[-3:])
                order.client = existOfdescriptionClients(dic[nameOfOrder]["description"])
                order.save()
                
                if len(dic[nameOfOrder]["order"]) !=len (OrderProduct.objects.filter(order = order)):
                    problems.append([ "Problem with order "+nameOfOrder, "Number of references : In Optima:" + str(len(dic[nameOfOrder]["order"])) +", but in System:"+str(len(OrderProduct.objects.filter(order = order))) ])
     
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
                                    problems.append([ "Problem with order "+nameOfOrder, "Change number od reference "+ ref +" : System:" + str(ordProduct.quantity) +"Optima:"+str(qty) ])
    
                                elif ordProduct.ordinalNumber != i:
                                    problems.append([ "Problem with order "+nameOfOrder,"Change ordinal number od reference "+ ref +" : System:" + str(ordProduct.ordinalNumber)  +" Optima:"+str(i) ])

                            else:
                                problems.append([ "Problem with order "+nameOfOrder, "No reference "+ ref +" : in System, but we have in Optima." ])
        elif "B2C" in name:
            order = OrderB2C.objects.filter(name = name)
            if order.exists()==False:
                ord=OrderB2C(
                    name = name,
                    description = dic[nameOfOrder]["description"],
                    country = country,
                    factory = Factory.objects.get(shortcut = name[-3:]),
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
                        problems.append([ "Problem with ref ", ref + " in " + nameOfOrder ])
                        check =1
                if check == 1:
                    ord.delete()

            elif order.exists()==True:
                order=order.first()

                order.country = country
                order.description = dic[nameOfOrder]["description"]
                order.factory = Factory.objects.get(shortcut = name[-3:])
                order.save()
                
                if len(dic[nameOfOrder]["order"]) !=len (OrderProduct.objects.filter(order = order)):
                    problems.append([ "Problem with order "+nameOfOrder, "Number of references : In Optima:" + str(len(dic[nameOfOrder]["order"])) +", but in System:"+str(len(OrderProduct.objects.filter(order = order))) ])
     
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
                                    problems.append([ "Problem with order "+nameOfOrder, "Change number od reference "+ ref +" : System:" + str(ordProduct.quantity) +"Optima:"+str(qty) ])
    
                                elif ordProduct.ordinalNumber != i:
                                    problems.append([ "Problem with order "+nameOfOrder,"Change ordinal number od reference "+ ref +" : System:" + str(ordProduct.ordinalNumber)  +" Optima:"+str(i) ])

                            else:
                                problems.append([ "Problem with order "+nameOfOrder, "No reference "+ ref +" : in System, but we have in Optima." ])
        
    
    df_html = pd.DataFrame(problems,columns=["type of problem","content of the problem"]).to_html()
    return HttpResponse(df_html)

def label_campaign(request,campaign):
    undone = []
    campaign = Campaign.objects.get(name = campaign)
    
    client = campaign.client

    setorder = Order.objects.filter(description__contains = campaign.name)
    print(setorder)
    for a in setorder:
        orderProducts = OrderProduct.objects.filter(order=a)
        x = Package.objects.filter(orderProduct__in = orderProducts)
        set=[]
        for i in x:
            z=Label(i)
            set.append(z)
        
        label_pdf = FormatLabel(set,a.name.replace("/","_"),str(campaign.name),client)

        if label_pdf.is_made == 1:
            a.is_made = True
            a.save()
        else:
            undone.append(a)

    return HttpResponse("done")

def make_label(request):
    setorder = Order.objects.exclude(is_made = True).filter(clientApproval = True).filter(factoryApproval = True)
    print(setorder)
    done = []
    for order in setorder:
        orderProducts = OrderProduct.objects.filter(order=order)
        x = Package.objects.filter(orderProduct__in = orderProducts)
        set=[]
        for i in x:
            z=Label(i)
            set.append(z)

        label_pdf = FormatLabel(set)
        
        if label_pdf.is_made == 1:
            order.is_made = True
            with open("done_label\\"+ order.name.replace("/","_")+"\\"+order.factory.typeOfLabel+" etykiety_" + order.name.replace("/","_") + ".pdf", 'rb') as f:
                order.label=  File(f,"done_label\\"+ order.name.replace("/","_")+"\\"+"10x20 etykiety_" + order.name.replace("/","_") + ".pdf")
                order.save()
        else:
            done.append(order)
    
    return HttpResponse("we did: " + str(done))

def download_file(request,pk):
    order = Order.objects.get(pk=pk)
    # check if label is done
    if order.label != None:
        filename = order.label.name.split('/')[-1]
        response = HttpResponse(order.label, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response
    else:
        return HttpResponse("There are no labels to order "+ order.name)

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
    
    setOfOrders=[
       "ORD/2021/000020/BSO",
"ORD/2021/000021/BSO",
"ORD/2021/000022/BSO",
        ]
    orderob = Order.objects.filter(name__in = setOfOrders)
    orderprodob = OrderProduct.objects.filter(order__in = orderob)
    packob = Package.objects.filter(orderProduct__in = orderprodob)
    text=""
    for pack in packob:
        text = text +str(pack.packageFromClient)+","
    return HttpResponse("tata:"+text)

def factory(request):
    updater_factory_info()
    return HttpResponse("done")

def check_approval_status(request):
    allOrders = Order.objects.all()
    checkFactoryApproval(allOrders)
    checkClientApproval(allOrders)
    allOrdersB2C = OrderB2C.objects.all()
    checkFactoryApproval(allOrdersB2C)
    # checkClientApproval(allOrdersB2C)
    addClientData(allOrdersB2C)
    print("test")
    return HttpResponse("done")


# class OfferUpdateFormView(UpdateView):
#     model = OrderB2C
#     template_name = 'form.html'
#     form_class = OrderB2CForm
 
#     def form_valid(self, form):
#         form.save()
#         return redirect("")