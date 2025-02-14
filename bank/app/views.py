from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import *
from .models import *
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password 

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
    return render(req,'admin/approved.html',{'data':data})

def activate(req, id):
    approved = get_object_or_404(Approved, id=id)
    openacc= approved.account
    user = User.objects.create_user(
    username=openacc.accountnumber,
    password=make_password("12345678") 
    )
    user.save()
    bank = Bank.objects.create(
        account_number=openacc.accountnumber,
        balance=0
    )
    bank.save()
    approved.delete()
    return redirect('view_users')

def add_update(req):
    if req.method=='POST':
        title = req.POST['title']
        description = req.POST['dis']
        if title and description:
            data=Updates.objects.create(title=title, discription=description)
            data.save()
            messages.success(req,"Update added")
            return redirect(add_update)
        else:
            messages.warning(req,'Please fill all')
    return render(req, "admin/addupdates.html")

def viewup(req):
    data=Updates.objects.all()
    return render(req,'admin/viewupdate.html',{'data':data})

def delete_update(req,id):
    update = get_object_or_404(Updates, id=id)
    update.delete()
    return redirect(viewup)



# --------------- Users ------------------------ 

def home(req):
    data=Updates.objects.all()
    return render(req,'users/index.html',{'data':data})

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
            print(f"Email Error: {e}")  
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

def activateacc(req):
    if req.method == "POST":
        account = req.POST['accnu']
        if Availible.objects.filter(accountnumber=account).exists():
            req.session["account_number"] = account 
            return redirect(askemail)
        else:
            messages.error(req, "Invalid account number")
    return render(req,'users/activateacc.html')

def askemail(req):
    if req.method == "POST":
        email = req.POST['email']
        account_number = req.session.get("account_number")
        if Bank.objects.filter(email=email).exists():
            messages.error(req, "Email already in use. Try a different email.")
        else:
            try:
                otp = get_random_string(length=6, allowed_chars='0123456789')
                req.session['otp'] = otp
                req.session["email"] = email
                send_mail(
                    'Your OTP Code',
                    f'Your OTP is: {otp}',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
                messages.success(req, "OTP sent to your email")
                return redirect(verifyacc)
            except:
                messages.error(req,"OTP not sent")
    return render(req,'users/askemail.html')

# def verifyacc(req):
#     if req.method == "POST":
#         otp = req.POST['otp']
#         sotp = req.session.get("otp")
#         email = req.session.get("email")
#         if sotp and otp == sotp:
#             account_number = req.session.get("account_number")
#             if account_number:
#                 user = User.objects.create_user(
#                     username=account_number, 
#                     password="12345678"
#                 )
#                 bank=Bank.objects.create(
#                     username=user,
#                     accountnumber=account_number,
#                     balance=0,
#                     email=email
#                 )
#                 bank.save()
#                 user.save()
#                 messages.success(req, "Account activated successfully!")
#             messages.success(req, "OTP verified successfully!")
#             del req.session["otp"]  
#             del req.session["email"]
#             return redirect(confirm)  
#         else:
#             messages.error(req, "Invalid OTP. Please try again.")
#     return render(req,'users/verify.html')

def verifyacc(req):
    if req.method == "POST":
        otp = req.POST.get("otp")
        sotp = req.session.get("otp")
        email = req.session.get("email")

        if sotp and otp == sotp:
            account_number = req.session.get("account_number")

            if account_number:
                # Check if the user already exists
                user, created = User.objects.get_or_create(
                    username=account_number,
                    defaults={"password": "12345678"}  # Default password only if created
                )
                bank = Bank.objects.create(
                        username=user,  
                        accountnumber=account_number,
                        balance=0,
                        email=email
                )
                bank.save()
                messages.success(req, "Account activated successfully!")

                # Clear session data
                del req.session["otp"]
                del req.session["email"]
                del req.session["account_number"]

                return redirect(confirm)  # Redirect to confirmation page

        else:
            messages.error(req, "Invalid OTP. Please try again.")

    return render(req, "users/verify.html")

def confirm(req,):
    return render(req,'users/confirm.html')


def money(req):
    return render(req,'users/money.html')

def mini(req):
    return render (req,'users/mini.html')