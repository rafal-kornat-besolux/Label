from label.models import Package
from .B2B import function_B2B
from .Factory import factories_specifications


class Label:

    def __init__(self, package):
        #From model Package
        self.qty = package.quantity
        self.pack = package.pack
        self.ordN = package.ordinalNumber
        self.uniqueBesoCode = package.codeBeso
        self.uniquefactoryCode = package.codeFactory
        

        #From model OrderProduct
        #From model Order
        self.order = package.orderProduct.order.name
        self.description = package.orderProduct.order.description
        self.country = package.orderProduct.order.country

        #From model OrderProduct
        #From model Furniture
        self.besoRef = package.orderProduct.furniture.besoRef
        self.factoryRef = package.orderProduct.furniture.factoryRef
        self.brand = package.orderProduct.furniture.brand
        self.ean = package.orderProduct.furniture.ean
        self.fabric = package.orderProduct.furniture.fabric
        self.color = package.orderProduct.furniture.color
        self.full = package.orderProduct.furniture.full
        self.legsPlacement = package.orderProduct.furniture.legsPlacement
        self.packagesQuantity = package.orderProduct.furniture.packagesQuantity

        

        self.type_label = 0
        
        # 1 - universal
        # 2 - VP
        self.factory_details = 0


        self.client = ""

        if package.infoFactory != "None":
            self.infoFactory = package.infoFactory
        else:
            self.infoFactory = ""
        
        if package.codeFactory != "None":
            self.codeFactory = package.codeFactory
        else:
            self.codeFactory = ""
        
        self = factories_specifications(self,package)

        if self.factory_details == 1:
 
            if function_B2B(self.description) != False:
                self.description = function_B2B(self.description)
                self.type_label = 1
            elif self.order[:3]=="ORD" and ("VP" in self.description):
                
                #print(package.packageFromClient)
                self.client = package.packageFromClient.number
                self.type_label = 2
            elif self.order[:3]=="ORD" and ("BZC" in self.description):
                
                #print(package.packageFromClient)
                self.client = package.packageFromClient.number
                self.type_label = 2  
        else:
            print(self.factory_details)

        

            
        



        
