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

from .forms import CreateProductForm, CreateShippingForm

from User.models import UserDetails, AddressDetail


def home(request):
    products = Product.objects.all()
    return render(request, "Product/home.html", context={"products":products})


@login_required(login_url='/login')
def createProduct(request):
    user = request.user
    if request.method == "POST":
        pass

    productForm = CreateProductForm
    shippingForm = CreateShippingForm(user)
    return render(request, "Product/createProduct.html", context={"form": productForm, "shippingForm": shippingForm})