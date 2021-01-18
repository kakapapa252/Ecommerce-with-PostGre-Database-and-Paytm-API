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
import decimal
from .forms import CreateProductForm, CreateShippingForm

from User.models import UserDetails, AddressDetail


def home(request):
    products = Product.objects.all()
    return render(request, "Product/home.html", context={"products":products})


@login_required(login_url='/login')
def createProduct(request):
    user = request.user
    if request.method == "POST":
        productForm = CreateProductForm(request.POST, request.FILES)
        shippingForm = CreateShippingForm(user, request.POST)
        if productForm.is_valid and shippingForm.is_valid:
            shippingDetail = shippingForm.save(commit=False)
            shippingDetail.save()
            product = productForm.save(commit=False)
            product.user = user
            try:
                incTax = request.POST["incTax"]
                product.incTax = True
            except:
                product.incTax = False
                product.price += product.price*decimal.Decimal(0.18)
            
            try:
                refundable = request.POST["refundable"]
                product.refundable = True
            except:
                product.refundable = False
                product.refund_period = 0
            product.shippingDetail = shippingDetail
            product.save()
            messages.success(request, f"Created!")
            return HttpResponseRedirect(reverse("home"))
        else:
            messages.error(request, "Error Detected")
            return HttpResponseRedirect(reverse("home"))

    productForm = CreateProductForm
    shippingForm = CreateShippingForm(user)
    return render(request, "Product/createProduct.html", context={"form": productForm, "shippingForm": shippingForm})