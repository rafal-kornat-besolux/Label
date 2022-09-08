from django.urls import path

from . import views
from . import viewsClass

urlpatterns = [
    path('', views.index, name='index'),
    path('test', views.test, name='test'),
    path('fetchpimcore', views.fetchpimcore, name='fetchpimcore'),
    path('fetchout', views.fetchoutofcollection, name='fetchoutofcollection'),
    path("optima", views.make_order_from_Optima, name='make_order_from_Optima'),
    path("label", views.make_label, name='make_label'),
    path("approve", views.check_approval_status, name='check_approval_status'),

    path("transporter", views.add_tranporter, name="add_tranporter"),
    path("factory", views.factory, name="factory"),
    

    #dropshiping client
    path("vp/<str:name>", views.import_package_VP, name="import_package_VP"),
    path("bzc/<str:nameOfCampaign>", views.bzc, name="bzc"),
    #connect data Package and PackageFromClient
    path("connect/<str:nameOfCampaign>", views.connect_campaign, name="connect_campaign"),
    #make label dropshiping
    path("label/<str:campaign>", views.label_campaign, name="label_campaign"),

    path('download/<int:pk>', views.download_file, name="download_file"),



    # path('B2C/edit/<int:pk>', views.OfferUpdateFormView.as_view(), name='B2Cedit'),


    #class views
    path('furniture', viewsClass.FurnitureShow.as_view(), name='furniture'),
    path('orders', viewsClass.OrderShow.as_view(), name='orders'),
    path('B2C', viewsClass.OrderB2CShow.as_view(), name='B2Corders'),
    path('campaign', viewsClass.CampaignShow.as_view(), name='campaign'),
    path('info/<int:pk>/', viewsClass.OrderProductShow.as_view(), name='order_details'),
    path('info_pack/<int:pk>/', viewsClass.PackageShow.as_view(), name='order_details_packages'),
    path('info_pack_client/<int:pk>/', viewsClass.PackageFromClientShow.as_view(), name='order_from_client_details_packages'),
    

]