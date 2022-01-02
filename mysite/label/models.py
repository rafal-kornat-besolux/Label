from django.db import models

from .FunctionPackages import make_code

# Create your models here.
class Order(models.Model):
    name = models.CharField(max_length=20,unique=True)
    description = models.CharField(max_length=500)
    country = models.CharField(max_length=20)

    def __str__(self):
       return '{}'.format(self.name)

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


class Campaign(models.Model):
    name = models.CharField(max_length=20)
    client = models.CharField(max_length=20)
    
    def __str__(self):
       return '{}'.format(self.name)

class Transporter(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
       return '{}'.format(self.name)

class PackageFromClient(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete = models.CASCADE)
    transporter = models.ForeignKey(Transporter, on_delete = models.CASCADE)
    furniture = models.ForeignKey(Furniture, on_delete = models.CASCADE)
    pack = models.IntegerField(default = 1)

    number = models.IntegerField(default = 1, unique = True)

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
    codeFactory = models.IntegerField(default = 0)
    
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