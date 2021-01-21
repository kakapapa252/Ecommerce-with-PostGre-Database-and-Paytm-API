from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,  get_object_or_404
from django.urls import reverse
from django.db.models import Max
from .models import *
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PhoneDetailForm, AddressDetailForm, SubscriptionDetailForm

from Product.views import home

def index(request):
    return HttpResponseRedirect('/')


#Subscription-------------------------------------
def subscribe(request):
    user = request.user
    if request.method == "POST":
        user = request.user
        messages.success(request, f"Subscribed")
        return HttpResponseRedirect(reverse("index"))
    else:
        form = SubscriptionDetailForm
        return render(request, "User/subscribe.html", context={"form": form})

#login register logout---------------------
def login_view(request):
    if request.method == "POST":
        emailf  = request.POST["username"]
        if '@' in emailf:
            pass
        else:
            try:
                emailf = User.objects.get(phonenumber=emailf).email
            except:
                return render(request, "User/login.html", {
                "message": "Invalid Email or Phone."
            })
        # Attempt to sign user in
        password = request.POST["password"]
        
        user = authenticate(request, email=emailf, password=password)
        # Check if authentication successful
        if user is not None:
            mess = "You've Logged in shop- " + str(emailf) + '!'
            send_mail('Successful Login', mess,'kartikay252081075@gmail.com', [user.email],fail_silently=False,)

            login(request, user)
            #print(str(request.user.is_superuser))
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "User/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "User/login.html")

@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

def register(request):
    if request.method == "POST":
        fullname = request.POST["username"]
        email = request.POST["email"]
        phonenumber = request.POST["phonenumber"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "User/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(fullname, email, phonenumber, password)
            user.save()
        except:
            return render(request, "User/register.html", {
                "message": "Email or Phone already taken. (Please enter all fields.)"
            })
        #create user detail object
        userDetail = UserDetails(user=user)
        userDetail.save()
        #add phone number as defualt phone
        phType = PhoneTypes.objects.get(phType="Primary").phType 
        phoneDetail = PhoneDetail(phoneNum=phonenumber)
        phoneDetail.save()
        #add phonedetail t0 userDetail
        userDetail.phones.add(phoneDetail)
        #send email of successful registration
        mess = "You've Registered successfully to Shop with Email - " + str(email) + ' and Mobile ' + str(phonenumber) + '!'
        send_mail('Successful Registration', mess,'kartikay252081075@gmail.com', [user.email],fail_silently=False,)

        login(request, user)
        messages.success(request, f"Registered")
        return HttpResponseRedirect(reverse("subscribe"))
    else:
        return render(request, "User/register.html")

@login_required(login_url='/login')
def changePassword(request):
    user = request.user
    if request.method == "POST":
        current_password = request.POST["current_password"]
        new_password = request.POST["new_password"]
        confirmation = request.POST["confirmation"]
        userf = authenticate(request, email=user.email, password=current_password)
        if userf is not None:
            if new_password != confirmation:
                return render(request, "User/changePassword.html", {"message": "Passwords must match."})
            else:
                user.set_password(new_password)
                user.save()
                login(request, user)
                mess = "You've Registered successfully Changed Password to - " + str(new_password)
                send_mail('Successful Password Change', mess,'kartikay252081075@gmail.com', [user.email],fail_silently=False,)
                messages.success(request, f"Password Changed")
                return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "User/changePassword.html", {"message": "Check Current Password."})
    else:
        return render(request, "User/changePassword.html")


#phonebook-------------------------------------
@login_required(login_url='/login')
def phoneDetailView(request):
    userDetail = UserDetails.objects.get(user=request.user)
    phoneDetails = userDetail.phones.all()
    return render(request, "User/phoneView.html", context={"phones":phoneDetails,})

@login_required(login_url='/login')
def createPhone(request):
    if request.method == "POST":
        form = PhoneDetailForm(request.POST)
        if form.is_valid():
            phoneDetail = form.save(commit=False) 
            phoneDetail.save()
            messages.success(request, f"Created!")
            userDetail = UserDetails.objects.get(user=request.user)
            userDetail.phones.add(phoneDetail)

            return HttpResponseRedirect(reverse("phoneDetailView"))
        else:
            messages.error(request, "Error Detected")
            return HttpResponseRedirect(reverse("createPhone"))

    form = PhoneDetailForm
    return render(request, "User/createPhone.html", context={"form": form})

@login_required(login_url='/login')
def deletePhone(request, id):
    try:
        userDetail = UserDetails.objects.get(user=request.user)
        phone = get_object_or_404(PhoneDetail,id=id)
        if ((phone in userDetail.phones.all()) or request.user.is_superuser) and phone.phType.id != 1:
            phone.delete()
            messages.success(request, f"Removed")
            return HttpResponseRedirect(reverse("phoneDetailView"))
        else:
            messages.error(request, f"Unable to Remove.")
            return HttpResponseRedirect(reverse("phoneDetailView"))
    except:
        messages.error(request, f"Unable to Remove.")
        return HttpResponseRedirect(reverse("phoneDetailView"))


#adressbook------------------------------------------
@login_required(login_url='/login')
def addressDetailView(request):
    userDetail = UserDetails.objects.get(user=request.user)
    addressDetails = userDetail.addresses.all()
    return render(request, "User/addressView.html", context={"addresses":addressDetails,})

@login_required(login_url='/login')
def createAdrress(request):
    if request.method == "POST":
        form = AddressDetailForm(request.POST)
        try:
            isPrim = request.POST["isPrimary"]
            isPrimary = True
        except:
            isPrimary = False

        if form.is_valid():
            userDetail = UserDetails.objects.get(user=request.user)

            #turning rest of the isPrimary == False if new entry is true
            if isPrimary == True:
                try:
                    addressPrimary = userDetail.addresses.get(isPrimary=True)
                    addressPrimary.isPrimary = False
                    addressPrimary.save()
                except:
                    pass

            addressDetail = form.save(commit=False) 
            addressDetail.isPrimary = isPrimary
            
            addressDetail.save()
            messages.success(request, f"Created!")  
            
            userDetail.addresses.add(addressDetail)

            return HttpResponseRedirect(reverse("addressDetailView"))
        else:
            messages.error(request, "Error Detected")
            return HttpResponseRedirect(reverse("createAddress"))

    form = AddressDetailForm
    return render(request, "User/createAddress.html", context={"form": form})

@login_required(login_url='/login')
def deleteAddress(request, id):
    try:
        userDetail = UserDetails.objects.get(user=request.user)
        address = get_object_or_404(AddressDetail,id=id)
        if (address in userDetail.addresses.all()) or request.user.is_superuser:
            address.delete()
            messages.success(request, f"Removed")
        else:
            messages.error(request, f"Unable to Remove.")
        return HttpResponseRedirect(reverse("addressDetailView"))
    except:
        messages.error(request, f"Unable to Remove.")
        return HttpResponseRedirect(reverse("addressDetailView"))

@login_required(login_url='/login')
def updateAddress(request, id):
    address = get_object_or_404(AddressDetail,id=id)
    form = AddressDetailForm(request.POST or None, instance= address)
    if request.method == "POST":
        if form.is_valid():
            address = form.save(commit= False)
            address.save()
            messages.success(request, "You successfully Edited")
            return HttpResponseRedirect(reverse("addressDetailView"))
        else:
            messages.error(request, f"Unable to Edit.")
            return render(request, "User/updateAddress.html", context={"form": form, "helper":address})

    else:
        form = AddressDetailForm
        return render(request, "User/updateAddress.html", context={"form": form, "helper":address})

@login_required(login_url='/login')
def setPrimaryAddress(request, id):
    userDetail = UserDetails.objects.get(user=request.user)
    address = get_object_or_404(AddressDetail,id=id)
    if (address in userDetail.addresses.all()) or request.user.is_superuser:
        # make isPrimary = False for all other entries
        try:
            addressPrimary = userDetail.addresses.get(isPrimary=True)
            addressPrimary.isPrimary = False
            addressPrimary.save()
        except:
            pass
        
        address.isPrimary = True
        address.save()
        messages.success(request, f"Success")
    else:
        messages.error(request, f"Unable to Set Primary.")
    return HttpResponseRedirect(reverse("addressDetailView"))

