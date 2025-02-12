from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import *
from .models import *
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings

# ------------------- Login ---------------------

def bank_login(req):
    if 'user' in req.session:
        return redirect(home)
    if 'bank' in req.session:
        return redirect(adprf)
    if req.method=='POST':
        uname=req.POST['uname']
        password=req.POST['password']
        data=authenticate(username=uname,password=password)
        if data:
            if data.is_superuser:
                login(req,data)
                req.session['bank']=uname
                return redirect(adhome)
            else:
                login(req,data)
                req.session['user']=uname
                req.session['user1']= data.id
                return redirect(home)
        else:
            messages.warning(req,"Invalid uname or password")
            return redirect(bank_login)
    else:
        return render(req,'login/login.html')

def bank_logout(req):
    req.session.flush()          
    logout(req)
    return redirect(bank_login)



# ----------------- Admin ----------------------

def adhome(req):
    return render(req,'admin/adhome.html')

def adprf(req):
    return render(req,'admin/adprofile.html')


# --------------- Users ------------------------ 

def home(req):
    return render(req,'users/index.html')

def openacc(req):
    if req.method == 'POST':
        fullname = req.POST['fullname']
        phone = req.POST['phone']
        address = req.POST['address']
        accountType = req.POST['accountType']
        photo = req.FILES['photo']
        proof = req.FILES['proof']
        email = req.POST['email']
        if User.objects.filter(email=email).exists():
            messages.warning(req, "Email already registered")
            return redirect('register')
        otp = get_random_string(length=6, allowed_chars='0123456789')
        req.session['otp'] = otp
        req.session['email'] = email
        req.session['fullname'] = fullname
        req.session['phone'] = phone
        req.session['address'] = address
        req.session['photo'] = photo
        req.session['proof'] = proof
        send_mail(
                'Your OTP Code',
                f'Your OTP is: {otp}',
                settings.EMAIL_HOST_USER, [email]
            )
        messages.success(req, "OTP sent to your email")
        return redirect(accotp)
    return render(req,'users/openacc.html')

def accotp(req):
    if req.method == 'POST':
        otp = req.POST['otp']
        if otp == req.session['otp']:
            email = req.session['email']
            fullname = req.session['fullname']
            phone = req.session['phone']
            address = req.session['address']
            photo = req.session['photo']
            proof = req.session['proof']
            account_number = f"111{phone}"
            Openacc.objects.create(
                accountnumber=account_number,email=email,fullname=fullname,phone=phone,address=address,photo=photo,proof=proof
            )    
            messages.success(req, "Account created successfully")
            return redirect(bank_login)
        else:
            messages.warning(req, "Invalid OTP")
            return redirect(accotp)
    return render(req,'users/accotp.html')


def money(req):
    return render(req,'users/money.html')

def mini(req):
    return render (req,'users/mini.html')