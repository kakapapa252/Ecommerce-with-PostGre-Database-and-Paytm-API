from django.db import models
from django.utils import timezone

from User.models import *
# Create your models here.
#====================== Product =============================

#======================Payment Reference Field=============
#Cash on Delivery, Debit Card, Credit Card, PayTm
class PaymentTypes(models.Model):
    _id = models.AutoField(primary_key=True)
    types = models.CharField(max_length=20,blank=False,null=False,)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return(self.types)

class PaymentItem(models.Model):
    _id = models.AutoField(primary_key=True)
    key =  models.CharField(max_length=200, blank=False,null=False)
    value =  models.CharField(max_length=200,blank=False,null=False)
    maxLength = models.IntegerField(null=False,default=1000)

    def __str__(self):
        return(self.key)


class PaymentDetail(models.Model):
    _id = models.AutoField(primary_key=True)
    types = models.ForeignKey(PaymentTypes,on_delete=models.CASCADE)
    paymentItems = models.ManyToManyField(PaymentItem)

    def __str__(self):
        return('Payment Detail id - ' + str(self._id))
#===========================================================


# Eg Category Electronics
class Category(models.Model):
    _id = models.AutoField(primary_key=True)
    categoryType = models.CharField(max_length=20,blank=False,null=False,)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return(self.categoryType)

# Eg SubCategory TV, Refrigerator, AC
class SubCategory(models.Model):
    _id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category,blank=False,null=False, on_delete=models.PROTECT)
    subCategoryType = models.CharField(max_length=20,blank=False,null=False,)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return(self.subCategoryType)

#images for product
class Thumbnail(models.Model):
    _id = models.AutoField(primary_key=True)
    thumbnail = models.ImageField(null=False)
    thumbnailDetail = models.CharField(max_length=200, blank=True,null=True)
    isFirst = models.BooleanField(default=False,null=False)
    createDate = models.DateTimeField(auto_now_add=True)
    #isDeleted = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        return("Thumbnail id - " + str(self._id))

class ShippingTypes(models.Model):
    _id = models.AutoField(primary_key=True)
    shippingType = models.CharField(max_length=20,blank=False,null=False,)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return(self.shippingType)

class ShippingDetails(models.Model):
    _id = models.AutoField(primary_key=True)
    shippingType = models.ForeignKey(ShippingTypes, on_delete=models.PROTECT, null = False)
    shippingAdresses = models.ForeignKey(AddressDetail, on_delete=models.CASCADE, null = False)
    shippingPrice = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return('ShippingDetail Id - ' + str(self._id))

class PackageDetails(models.Model):
    _id = models.AutoField(primary_key=True)
    fragile = models.BooleanField(default=False)
    height = models.DecimalField(max_digits=10,decimal_places=2,null = False, blank=False)
    width = models.DecimalField(max_digits=10,decimal_places=2,null = False, blank=False)
    depth = models.DecimalField(max_digits=10,decimal_places=2,null = False, blank=False)
    weight = models.DecimalField(max_digits=10,decimal_places=2,null = False, blank=False)

    def __str__(self):
        return('PackageDetails ID - '+str(self._id))

class Product(models.Model):
    _id = models.AutoField(primary_key=True)
    shippingDetail = models.ForeignKey(ShippingDetails, null = False, on_delete = models.PROTECT)
    paymentDetail = models.ForeignKey(PaymentDetail, on_delete=models.PROTECT,)
    thumbnails = models.ForeignKey(Thumbnail, on_delete=models.DO_NOTHING,)

    subCategory = models.ForeignKey(SubCategory,on_delete=models.DO_NOTHING, null = False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = False)
    packageDetail = models.ForeignKey(PackageDetails, on_delete=models.PROTECT, null=True, blank= True)

    title = models.CharField(max_length=200, blank=False,null=False)
    searchCriteria = models.CharField(max_length=200, blank=True,null=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    incTax = models.BooleanField(default=False)

    # Fee can be included in UserOrder Instead
    #fee = models.DecimalField(max_digits=10,decimal_places=2) 
    availableQt = models.PositiveIntegerField(null=False, blank=False, default= 0)
    refundable = models.BooleanField(default=False)
    refund_period = models.IntegerField(null=True, blank=True)
    description = models.TextField()
    inProcessQt = models.IntegerField(null=False, blank=False,default=0)
    soldQt = models.IntegerField(null=False, blank=False,default=0)

    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return(self.title)
    
class Cart(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	product = models.ForeignKey(Product,on_delete=models.CASCADE)
	added_date = models.DateTimeField(default=timezone.now())

	def __str__(self):
		return (f"This product {self.product.title} has id: {self.product._id} added by {self.user}")

class Comments(models.Model):
    _id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, null=False,on_delete=models.CASCADE)
    description = models.TextField()
    createDate = models.DateTimeField(auto_now_add=True)
    isDeleted = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        return(self.product + '| Comment ID - ' + str(self._id) )

class UserOrder(models.Model):
    _id = models.AutoField(primary_key=True)
    paymentDetail = models.ForeignKey(PaymentDetail, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, null=False,on_delete=models.DO_NOTHING)
    deliveryAddress = models.ForeignKey(AddressDetail,on_delete=models.DO_NOTHING)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    shippingPrice = models.DecimalField(max_digits=10,decimal_places=2)
    tax = models.DecimalField(max_digits=10,decimal_places=2,null = True, blank=True)
    fee = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    paymentRecieved = models.BooleanField(null=False ,blank= False,default=False)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)
    # Address and Phone and Email Detail by Kartik

    def __str__(self):
        return('OrderId - ' + str(self._id) + ' User - ' + str(self.user) + ' Item - '+ str(self.product))
    

