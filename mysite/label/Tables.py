import django_tables2 as tables
from django_tables2.utils import A
from .models import Furniture, Order, OrderProduct, Package

class FurnitureTable(tables.Table):
    class Meta:
        model = Furniture
        template_name = "django_tables2/bootstrap-responsive.html"
        fields = ('besoRef','factoryRef', 'brand','ean','fabric', 'color','full','legsPlacement', 'packagesQuantity',)
        
class OrderTable(tables.Table):
    # download = DownloadLinkColumn('downloadexcel', text='Download', args=[A("pk")], orderable=False)
    # summary = tables.LinkColumn('offerdetail', text='Summary', args=[A("pk")], orderable=False)
    Details = tables.LinkColumn('order_details', text='Details', args=[A("pk")], orderable=False)
    Package = tables.LinkColumn('order_details_packages', text='Package', args=[A("pk")], orderable=False)
    # edit = tables.LinkColumn('offeredit', text='Edit', args=[A("pk")], orderable=False)
    # delete = tables.LinkColumn('offerdelete', text='Delete', args=[A("pk")], orderable=False)
    class Meta:
        model = Order
        template_name = "django_tables2/bootstrap-responsive.html"
        fields = ('name','description', 'country','is_made' ,)

class OrderProductTable(tables.Table):
    class Meta:
        model = OrderProduct
        template_name = "django_tables2/bootstrap-responsive.html"
        fields = ('ordinalNumber','furniture', 'quantity',)

class PackageTable(tables.Table):
    class Meta:
        model = Package
        template_name = "django_tables2/bootstrap-responsive.html"

        fields = ('codeBeso','ordinalNumber', 'quantity','pack','orderProduct.furniture','packageFromClient','infoFactory',)