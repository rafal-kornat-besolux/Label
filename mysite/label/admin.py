from django.contrib import admin

from .models import Furniture, Order, OrderProduct, Package, Client, OrderB2C
from .models import Campaign, Transporter, PackageFromClient, Factory
# Register your models here.

admin.site.register(Furniture)
admin.site.register(OrderProduct)
admin.site.register(Order)
admin.site.register(OrderB2C)
admin.site.register(Package)
admin.site.register(Factory)
admin.site.register(Client)
admin.site.register(Campaign)
admin.site.register(Transporter)
admin.site.register(PackageFromClient)
