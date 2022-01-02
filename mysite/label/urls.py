from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('orders', views.OrderShow.as_view(), name='orders'),
    path('info/<int:pk>/', views.OrderProductShow.as_view(), name='order_details'),
    path('info_pack/<int:pk>/', views.PackageShow.as_view(), name='order_details_packages'),
    path('fetchpimcore', views.fetchpimcore, name='fetchpimcore'),
    path("optima", views.make_order_from_Optima, name='make_order_from_Optima'),
    path("label", views.make_label, name='make_label'),
    path("vp/<str:name>", views.import_package_VP, name="import_package_VP"),
    path("vplabel/<str:campaign>", views.VP_label, name="VP_label"),
    path("transporter", views.add_tranporter, name="add_tranporter"),
    path("bzc", views.bzc, name="bzc"),
    path("conect/<str:nameOfCampaign>", views.conect_VP, name="conect_VP")
]