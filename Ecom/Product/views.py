from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,  get_object_or_404
from django.urls import reverse
from django.db.models import Max
from .models import *
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import decimal
from .forms import CreateProductForm, CreateShippingForm, CommentForm, CheckoutForm
from User.forms import AddressDetailForm

from User.models import UserDetails, AddressDetail

import json
from Paytm import Checksum


#needed for production transactions after kyc
MERCHANT_KEY = 'F2s_R6cQ!LNkXqQx'
#-----------------------------------


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

'''def searchCrit():
    for i in Product.objects.all():
        i.searchKeywords = i.subCategory.category.categoryType + ' ' + i.subCategory.subCategoryType + ' ' + i.title + ' ' + i.description
        i.save()
    print('done')
    return ('yes')'''

def search(request):
    if request.method == "POST":
        keyword  = request.POST["search"]
        products = Product.objects.filter(searchKeywords__icontains = keyword)
        return render(request, "Product/search.html", context={"products":products, "keyword":keyword})

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
            product.searchKeywords = product.subCategory.category.categoryType + ' ' + product.subCategory.subCategoryType + ' ' + product.title + ' ' + product.description
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

@login_required(login_url='user/login')
def orderHistory(request):
    user = request.user
    orderedProducts =  Order.objects.filter(user=user).filter(paymentRecieved=True).order_by("-updateDate")
    return render(request, "Product/orderHistory.html", context={"orderedProducts": orderedProducts,})


#PAYMETNS-------------------------------------------------------------

@login_required(login_url='user/login')
def checkout(request):
    #before filling the form
    user = request.user
    cartProducts =  Cart.objects.filter(user=user)
    totalAmount = 0
    for singleProduct in cartProducts:
        totalAmount += singleProduct.get_total_item_price()
    checkoutForm = CheckoutForm(user)

    if request.method == "POST":
        checkoutForm = CheckoutForm(user, request.POST,)
        productDetails = {"active":True}
        if checkoutForm.is_valid: 
            order = checkoutForm.save(commit=False)
            order.user = user
            order.amount = totalAmount
            order.productDetails = json.dumps(productDetails)
            order.save()
            for singleProduct in cartProducts:
                order.products.add(singleProduct.product)
                productDetails[str(singleProduct.product.id)] = {
                    "name" : str(singleProduct.product.title),
                    "quantity" : str(singleProduct.quantity),
                    "price" : str(singleProduct.product.price),
                    "supplier_name" : str(singleProduct.product.user.fullname),
                    "supplier_phone" : str(singleProduct.product.user.phonenumber),
                    "supplier_email" : str(singleProduct.product.user.email),
                }
            print(productDetails)
            order.productDetails = json.dumps(productDetails)
            order.save()
            
            #needs to change (Website, MID) after Legal Documentation for it to work
            param_dict = {
                'MID':'xubJEf88177726122713',
                'ORDER_ID':str(order.id),
                'TXN_AMOUNT':str(order.amount),
                'CUST_ID':str(user.email),
                'INDUSTRY_TYPE_ID':'Retail',
                'WEBSITE':'WEBSTAGING',
                'CHANNEL_ID':'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/handleRequest/',
        }
        
            param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
            return render(request, 'Product/paytm.html', {'param_dict': param_dict})

    return render(request, "Product/checkout.html", context={"checkoutForm":checkoutForm,"totalAmount": totalAmount})

@csrf_exempt
def handleRequest(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
            id = response_dict["ORDERID"]
            order = get_object_or_404(Order,id=id)
            order.paymentRecieved = True
            order.save()
            user = order.user
            cartProducts =  Cart.objects.filter(user=user)
            mess = "Your Order " + str(id) + " of Bill amount Rs." + str(order.amount) + " including - \n"
            for singleProduct in cartProducts:
                singleProduct.product.availableQt -= singleProduct.quantity
                singleProduct.product.save()
                mess += f"{singleProduct.product.title} x ({singleProduct.quantity}),\n "
                singleProduct.delete()

            #message for email after successful order
            mess += f"is placed Successfuly and will be deliver to - \n {order.deliveryAddress}!"
            send_mail('Successfull Order ID - ' + str(id), mess,'kartikay252081075@gmail.com', [user.email],fail_silently=False,) 
            
            login(request, user)
            messages.success(request, "Order Successful")
            return HttpResponseRedirect(reverse("home"))
        else:
            print('order was not successful because' + response_dict['RESPMSG'])

        return HttpResponseRedirect(reverse("home"))


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