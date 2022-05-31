import django_filters
from .models import Furniture, Order, Campaign, PackageFromClient

class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = {
            'name': ['contains'],
            'description': ['contains'],
            'country': ['exact'],
            'is_made': ['exact'],
            'factoryApproval': ['exact'],
            'clientApproval': ['exact'],
        }

class FurnitureFilter(django_filters.FilterSet):
    class Meta:
        model = Furniture
        fields = {
            'besoRef': ['contains'],
            'factoryRef': ['contains'],
            'brand': ['contains'],
            'ean': ['contains'],
            'fabric': ['contains'],
            'color': ['contains'],
            'full': ['contains'],
            'legsPlacement': ['contains'],
            'packagesQuantity': ['exact'],
            'outOfCollection': ['exact'],
        }

class CampaignFilter(django_filters.FilterSet):
    client = django_filters.CharFilter(field_name='client__name', lookup_expr='icontains')
    class Meta:
        model = Campaign
        fields = {
            'name': ['contains'],
        }

class PackageFromClientFilter(django_filters.FilterSet):
    transporter = django_filters.CharFilter(field_name='transporter__name', lookup_expr='icontains')
    furniture = django_filters.CharFilter(field_name='furniture__besoRef', lookup_expr='icontains')
    class Meta:
        model = PackageFromClient
        fields = {
            'pack': ['contains'], 
            'number': ['contains'],
        }