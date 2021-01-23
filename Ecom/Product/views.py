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
from .forms import CreateProductForm, CreateShippingForm, CommentForm

from User.models import UserDetails, AddressDetail

# different shop views -----------------------------------------------------------------------
def home(request):
    products = Product.objects.all()
    return render(request, "Product/home.html", context={"products":products})

def category(request):
    categories = Category.objects.all()
    return render(request, "Product/categories.html", context={"categories":categories})


def subCategory(request,id):
    category = Category.objects.get(id=id)
    subCategories = SubCategory.objects.filter(category=category)
    return render(request, "Product/subCategories.html", context={"subCategories":subCategories, "cat":category.categoryType})

def subCategoryProducts(request,id):
    subCategory = SubCategory.objects.get(id=id)
    products = Product.objects.filter(subCategory=subCategory)
    return render(request, "Product/subCategoryProducts.html", context={"products":products, "subCat":subCategory})



def productPage(request,id):
    product = get_object_or_404(Product, id=id)
    user = request.user
    commentForm = CommentForm
    comments = Comments.objects.filter(product=product)

    if request.method == "POST":
        commentForm = CommentForm(request.POST,)     
        if commentForm.is_valid():
            try:
                comment_exists = Comments.objects.get(product=product,user=user,description=commentForm["description"].value())
            except:
                comment = commentForm.save(commit=False)
                comment.user = user
                comment.product = product
                comment.save()
            return render(request,"Product/productPage.html", 
                        context={"product":product ,"commentForm": commentForm, "comments": comments})

        else:
            return render(request,"Product/productPage.html", 
                        context={"product":product ,"commentForm": commentForm, "comments": comments})
            

    return render(request,"Product/productPage.html", 
                context={"product":product ,"commentForm": commentForm, "comments": comments})


# logged in features-------------------------------------------------------------
@login_required(login_url='user/login')
def createProduct(request):
    user = request.user
    if request.method == "POST":
        productForm = CreateProductForm(request.POST, request.FILES)
        shippingForm = CreateShippingForm(user, request.POST)
        if productForm.is_valid and shippingForm.is_valid:
            shippingDetail = shippingForm.save(commit=False)
            shippingDetail.save()
            shippingForm.save_m2m()
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

@login_required(login_url='user/login')
def addToCart(request,id):
    product = get_object_or_404(Product,id=id)
    user = request.user
    cartItem ,created = Cart.objects.get_or_create(product = product, user = user,)
    if created:
        messages.success(request, f"Added To Cart") 
        cartItem.save()
    else:
        cartItem.quantity += 1
        cartItem.save()
        messages.success(request, f"Added Quantity") 

    return HttpResponseRedirect(reverse("cart"))

@login_required(login_url='user/login')
def removeFromCart(request,id):
    product = get_object_or_404(Product,id=id)
    user = request.user
    cartItem = Cart.objects.get(product = product, user = user,)
    if cartItem.quantity > 1:
        cartItem.quantity -= 1
        messages.success(request, f"Reduced Quantity") 
        cartItem.save()
    else:
        messages.success(request, f"Removed from Cart") 
        cartItem.delete()
        
    return HttpResponseRedirect(reverse("cart"))


@login_required(login_url='user/login')
def cart(request):
    user = request.user
    cartProducts =  Cart.objects.filter(user=user)
    cartSubTotal = 0
    for cartp in cartProducts:
        cartSubTotal += cartp.get_total_item_price()
    return render(request, "Product/cart.html", context={"cartProducts": cartProducts, "cartSubTotal":cartSubTotal})


#PAYMETNS-------------------------------------------------------------






























#preprocessors----------------------------------------------------
def cartCount(request):
    user = request.user
    cartCount = 0
    try:
        if user is not None:
            cart = Cart.objects.filter(user=user)
            for i in cart:
                cartCount += i.quantity
        return cartCount
    except:
        return cartCount

def categoryDropdown(request):
    categories = Category.objects.all()
    return categories