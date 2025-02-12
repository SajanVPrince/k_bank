from django.urls import path
from . import views

urlpatterns = [

# ---------------LOGIN ----------

    path('login',views.bank_login),
    path('logout',views.bank_logout),

# ------------- ADMIN ------------

    path('adhome',views.adhome),
    path('adprf',views.adprf),

    

# ---------users------------------

    path('',views.home),
    path('openacc',views.openacc),
    path('money',views.money),
    path('mini',views.mini),


    
]