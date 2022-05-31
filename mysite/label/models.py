from django.db import models
from zmq import TYPE

from .FunctionPackages import make_code

# Create your models here.

class Factory(models.Model):
    shortcut = models.CharField(max_length =3, unique=True)
    name = models.CharField(max_length =100)
    CHOICES = (
        ('10x20', 'Standard'),
        ('A4', 'Big Standard'),
    )
    typeOfLabel = models.CharField(max_length=300, choices = CHOICES)

    orderRequirement = models.BooleanField(default = False)
    labelInfoRequirement = models.BooleanField(default = False)
    labelCodeRequirement = models.BooleanField(default = False)
    factoryReferenceRequirement = models.BooleanField(default = False)

    def __str__(self):
       return '{}'.format(self.shortcut)

class Order(models.Model):
    name = models.CharField(max_length=20,unique=True)
    factory = models.ForeignKey(Factory, on_delete = models.CASCADE,null=True)
    description = models.CharField(max_length=500)
    country = models.CharField(max_length=20)
    #do usuniecia
    is_made = models.BooleanField(default = False)
    is_sent = models.BooleanField(default = False)
    factory_info = models.CharField(max_length=20)
    #do usuniecia
    attention = models.BooleanField(default = False)
    factoryApproval = models.BooleanField(default = False)
    clientApproval = models.BooleanField(default = False)
    label = models.FileField(upload_to = "Label_file" ,null=True)

    def __str__(self):
       return '{}'.format(self.name)

class OrderB2C(Order):
    nameOfClient = models.CharField(max_length=100, blank = True)
    surnameOfClient = models.CharField(max_length=100, blank = True)
    street = models.CharField(max_length=100,blank = True)
    numberOfStreet = models.IntegerField(blank = True, default = 0)
    numberofFlat = models.IntegerField(blank = True, default = 0)
    city = models.CharField(max_length=100,blank = True)
    code = models.CharField(max_length=100,blank = True)
    email = models.CharField(max_length=100,blank = True)
    phone = models.CharField(max_length=100,blank = True)
    dropshippingApproval = models.CharField(max_length=100, default= False)

class Furniture(models.Model):
    besoRef = models.CharField(max_length=50, unique=True)
    factoryRef = models.CharField(max_length=50, default = "")
    brand = models.CharField(blank = True, max_length=50, default = "")
    ean = models.IntegerField(blank = True, default = 0)
    fabric = models.CharField(max_length = 50)
    color = models.CharField(blank = True, max_length = 50, default = "")
    full = models.CharField(blank = True, max_length = 300, default = "")
    legsPlacement = models.CharField(blank = True, max_length = 50, default = "")
    packagesQuantity = models.IntegerField(blank = True, default = 0)
    outOfCollection = models.BooleanField(default = False)

    def __str__(self):
       return '{}'.format(self.besoRef)

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete = models.CASCADE)
    furniture = models.ForeignKey(Furniture, on_delete = models.CASCADE)
    quantity = models.IntegerField(default = 1)
    ordinalNumber = models.IntegerField(default = 1)

    class Meta:
        unique_together = ('order', 'furniture')

    def __str__(self):
       return '{}--{}:{}'.format(self.order, str(self.quantity), self.furniture)
    
    @classmethod
    def create(cls, name, ordN, ref,qty):
        order = Order.objects.get(name = name)
        furniture = Furniture.objects.get(besoRef = ref)
        orderProduct = cls(order = order, furniture = furniture, quantity = qty, ordinalNumber = ordN)
        orderProduct.save()
        for i in range(qty):
            for j in range(furniture.packagesQuantity):
                package = Package.create(i+1,j+1,ordN, name,ref)
                package.save()
        return(orderProduct)

class Transporter(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
       return '{}'.format(self.name)

class Client(models.Model):
    name = models.CharField(max_length = 200)
    transporter = models.ForeignKey(Transporter, on_delete = models.CASCADE, null = True)
    is_campaign = models.BooleanField(default = False)
    type = models.CharField(max_length =200)
    #dodanie opcji 1-casual, 2-typ westwing, 3-typ VP, 4-typ courier
    def __str__(self):
       return '{}'.format(self.name)

class Campaign(models.Model):
    name = models.CharField(max_length = 20)
    client = models.ForeignKey(Client, on_delete = models.CASCADE, null=True)
    
    def __str__(self):
       return '{}'.format(self.name)

class PackageFromClient(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete = models.CASCADE)
    furniture = models.ForeignKey(Furniture, on_delete = models.CASCADE)
    pack = models.IntegerField(default = 1)

    number = models.CharField(default = "", max_length=20, unique = True)

    def __str__(self):
       #return '{} {}:{}_{}'.format(self.campaign, self.transporter, self.furniture.besoRef, str(self.pack))
        return str(self.number)

class Package(models.Model):
    orderProduct = models.ForeignKey(OrderProduct, on_delete = models.CASCADE)
    ordinalNumber = models.IntegerField()
    quantity = models.IntegerField()
    pack = models.IntegerField()
    packageFromClient = models.ForeignKey(PackageFromClient, on_delete = models.SET_NULL, blank = True, null = True)
    codeBeso = models.IntegerField(default = 1, unique = True)
    codeFactory = models.CharField(max_length=50)
    infoFactory = models.CharField(max_length=50)
    
    def __str__(self):
        return(str(self.codeBeso))

    @classmethod
    def create(cls, qty, pack, ordN, name, besoRef):
        order = Order.objects.get(name = name)
        furniture = Furniture.objects.get(besoRef = besoRef)
        orderProduct = OrderProduct.objects.get(order = order, furniture = furniture)
        codeBeso = make_code(order.name,ordN,qty,pack)
        package = cls(ordinalNumber = ordN, quantity = qty, pack = pack, orderProduct = orderProduct, codeBeso = codeBeso)

        return package