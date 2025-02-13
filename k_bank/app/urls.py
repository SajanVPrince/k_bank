from django.urls import path
from . import views

urlpatterns = [

# ---------------LOGIN ----------

    path('login',views.bank_login,name="bank_login"),
    path('logout',views.bank_logout),

# ------------- ADMIN ------------

    path('adhome',views.adhome),
    path('adprf',views.adprf),
    path('viewapp',views.viewappli),
    path('approve/<int:id>',views.approve, name='approve'),
    path('reject/<int:id>',views.reject,name='reject'),
    

# ---------users------------------

    path('',views.home),
    path('home',views.home,name="home"),
    path('openacc',views.openacc,name="openacc"),
    path('verify',views.accotp,name="accotp"),
    path('money',views.money),
    path('mini',views.mini),


    
]