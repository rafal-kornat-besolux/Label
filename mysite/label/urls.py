from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('test', views.test, name='test'),
    path('furniture', views.FurnitureShow.as_view(), name='furniture'),
    path('orders', views.OrderShow.as_view(), name='orders'),
    path('campaign', views.CampaignShow.as_view(), name='campaign'),
    path('info/<int:pk>/', views.OrderProductShow.as_view(), name='order_details'),
    path('info_pack/<int:pk>/', views.PackageShow.as_view(), name='order_details_packages'),
    path('info_pack_client/<int:pk>/', views.PackageFromClientShow.as_view(), name='order_from_client_details_packages'),
    path('fetchpimcore', views.fetchpimcore, name='fetchpimcore'),
    path('fetchout', views.fetchoutofcollection, name='fetchoutofcollection'),
    path("optima", views.make_order_from_Optima, name='make_order_from_Optima'),
    path("label", views.make_label, name='make_label'),
    

    path("transporter", views.add_tranporter, name="add_tranporter"),
    path("factory", views.factory, name="factory"),

    #dropshiping client
    path("vp/<str:name>", views.import_package_VP, name="import_package_VP"),
    path("bzc/<str:nameOfCampaign>", views.bzc, name="bzc"),
    #connect data Package and PackageFromClient
    path("connect/<str:nameOfCampaign>", views.connect_campaign, name="connect_campaign"),
    #make label dropshiping
    path("label/<str:campaign>", views.label_campaign, name="label_campaign")
]