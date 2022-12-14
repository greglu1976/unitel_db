from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('reports/', views.reports),
    path('reports/getreport/', views.get_report),
    path('reports/show/', views.show),
    path('lntypes/', views.lntypes),
    path('lntypes/show/', views.show),

]