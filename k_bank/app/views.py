from django.shortcuts import render

# Create your views here.
 
def home(req):
    return render(req,'users/index.html')

def money(req):
    return render(req,'users/money.html')

def mini(req):
    return render (req,'users/mini.html')