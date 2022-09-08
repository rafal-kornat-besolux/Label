from .filters import OrderFilter, OrderB2CFilter, FurnitureFilter, CampaignFilter,  PackageFromClientFilter
from .tables import FurnitureTable, OrderTable, OrderB2CTable, OrderProductTable, PackageTable, CampaignTable, PackageFromClientTable
from .models import Furniture, Order, OrderB2C, OrderProduct, Package, PackageFromClient, Campaign

from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django_tables2 import SingleTableView

class FurnitureShow(SingleTableMixin, FilterView):
    model = Furniture
    queryset = Furniture.objects.all()
    table_class = FurnitureTable
    template_name = "order2.html"

    filterset_class = FurnitureFilter

class OrderShow(SingleTableMixin, FilterView):
    model = Order
    queryset = Order.objects.all()
    table_class = OrderTable
    template_name = "order2.html"

    filterset_class = OrderFilter

class OrderB2CShow(SingleTableMixin, FilterView):
    model = OrderB2C
    queryset = OrderB2C.objects.all()
    table_class = OrderB2CTable
    template_name = "order2.html"

    filterset_class = OrderB2CFilter

class CampaignShow(SingleTableMixin, FilterView):
    model = Campaign
    queryset = Campaign.objects.all()
    table_class = CampaignTable
    template_name = "order2.html"

    filterset_class = CampaignFilter

class PackageFromClientShow(SingleTableMixin, FilterView):
    model = PackageFromClient
    table_class = PackageFromClientTable
    template_name = "order2.html"

    filterset_class = PackageFromClientFilter

    def get_queryset(self):
        pk = self.kwargs['pk']
        campaign = Campaign.objects.get(pk=pk)
        return PackageFromClient.objects.filter(campaign=campaign)

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