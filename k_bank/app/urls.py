from django.urls import path
from . import views

urlpatterns = [

    path('',views.home),
    path('money',views.money),
    path('mini',views.mini),


    
]