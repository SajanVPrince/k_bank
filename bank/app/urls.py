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
    path('appapp',views.appapp),
    path('activate/<int:id>',views.activate),
    path('addup',views.add_update),
    path('viewup',views.viewup),
    path('deleteup/<int:id>',views.delete_update),
    

# ---------users------------------

    path('',views.home),
    path('home',views.home,name="home"),
    path('openacc',views.openacc,name="openacc"),
    path('verify',views.accotp,name="accotp"),
    path('money',views.money),
    path('mini',views.mini),
    path('actacc',views.activateacc),
    path('askemail',views.askemail),
    path('verifyacc',views.verifyacc),
    path('confirm',views.confirm)



    
]