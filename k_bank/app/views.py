from django.shortcuts import render,redirect,get_object_or_404
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

def viewappli(req):
    data = Openacc.objects.all()
    return render(req,'admin/viewappli.html',{'data':data})

def reject(req,id):
    data=Openacc.objects.filter(id=id)
    data.delete()
    return redirect(viewappli)

def approve(req,id):
    data = get_object_or_404(Openacc, id=id)
    Approved.objects.create(account=data)
    send_mail(
        'Account Approved',
        'Your account has been approved. Please visit the branch.',
        settings.EMAIL_HOST_USER,
        [data.email],
        fail_silently=False
    )
    data.delete()
    return redirect(viewappli)

def appapp(req):
    data = Approved.objects.all()
    return render(req,'admin/appapp.html',{'data':data})

def activate(request, id):


    return redirect('view_users')


# --------------- Users ------------------------ 

def home(req):
    return render(req,'users/index.html')

def openacc(req):
    if req.method == 'POST':
        fullname = req.POST['fullname']
        phone = req.POST['phone']
        address = req.POST['address']
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

        try:
            send_mail(
                'Your OTP Code',
                f'Your OTP is: {otp}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            messages.success(req, "OTP sent to your email")
        except Exception as e:
            print(f"Email Error: {e}")  # Check for errors in the console
            messages.error(req, "Failed to send OTP. Check email settings.")

        return redirect(accotp)
    
    return render(req, 'users/openacc.html')

def accotp(req):
    if req.method == 'POST':
        otp = req.POST['otp']
        if otp == req.session.get('otp', ''):
            email = req.session.get('email')
            fullname = req.session.get('fullname')
            phone = req.session.get('phone')
            address = req.session.get('address')
            account_number = f"111{phone}"
            Openacc.objects.create(
                accountnumber=account_number, email=email, fullname=fullname, phone=phone, address=address
            )
            req.session.pop('otp', None)
            req.session.pop('email', None)
            req.session.pop('fullname', None)
            req.session.pop('phone', None)
            req.session.pop('address', None)

            messages.success(req, "Account created successfully")
            return redirect('home') 
        else:
            messages.warning(req, "Invalid OTP. Please try again.")
            return redirect('accotp')
    
    return render(req, 'users/accotp.html')



def money(req):
    return render(req,'users/money.html')

def mini(req):
    return render (req,'users/mini.html')