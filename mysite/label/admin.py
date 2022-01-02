from django.contrib import admin

from .models import Furniture, Order, OrderProduct, Package
from .models import Campaign, Transporter, PackageFromClient
# Register your models here.

admin.site.register(Furniture)
admin.site.register(OrderProduct)
admin.site.register(Order)
admin.site.register(Package)

admin.site.register(Campaign)
admin.site.register(Transporter)
admin.site.register(PackageFromClient)
