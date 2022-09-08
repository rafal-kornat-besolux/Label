from label.models import Package


class Label:
    def __init__(self, package):
        #From model Package
        self.qty = package.quantity
        self.pack = package.pack
        self.ordN = package.ordinalNumber
        self.uniqueBesoCode = package.codeBeso
        self.uniquefactoryCode = package.codeFactory
        self.infoFactory = package.infoFactory

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


        #From model Factory
        self.typeOfLabel = package.orderProduct.order.factory.typeOfLabel
        self.orderRequirement = package.orderProduct.order.factory.orderRequirement
        self.labelInfoRequirement = package.orderProduct.order.factory.labelInfoRequirement
        self.labelCodeRequirement = package.orderProduct.order.factory.labelCodeRequirement
        self.factoryReferenceRequirement = package.orderProduct.order.factory.factoryReferenceRequirement
        
        #From model Client
        self.clientName = package.orderProduct.order.client.name
        self.typeClient = package.orderProduct.order.client.type
        self.transporter = package.orderProduct.order.client.transporter
        
        #From model PackageFromClient
        if package.orderProduct.order.client.is_campaign == True:
            self.campaign = package.packageFromClient.campaign
            self.packageFromClient = package.packageFromClient.number
