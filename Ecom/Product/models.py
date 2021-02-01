from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from User.models import *

# Create your models here.
#====================== Product =============================

# Eg Category Electronics
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    categoryType = models.CharField(max_length=20,blank=False,null=False,)
    thumbnail = models.ImageField(null=True, blank=True)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return(self.categoryType)

# Eg SubCategory TV, Refrigerator, AC
class SubCategory(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category,blank=False,null=False, on_delete=models.PROTECT)
    thumbnail = models.ImageField(null=True, blank=True)
    subCategoryType = models.CharField(max_length=20,blank=False,null=False,)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return(self.subCategoryType)

#images for product
'''class Thumbnail(models.Model):
    _id = models.AutoField(primary_key=True)
    thumbnail = models.ImageField(null=False)
    thumbnailDetail = models.CharField(max_length=200, blank=True,null=True)
    isFirst = models.BooleanField(default=False,null=False)
    createDate = models.DateTimeField(auto_now_add=True)
    #isDeleted = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        return("Thumbnail id - " + str(self._id))'''

class ShippingTypes(models.Model):
    id = models.AutoField(primary_key=True)
    shippingType = models.CharField(max_length=20,blank=False,null=False,)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return(self.shippingType)

class ShippingDetails(models.Model):
    id = models.AutoField(primary_key=True)
    shippingType = models.ManyToManyField(ShippingTypes)
    shippingAdresses = models.ManyToManyField(AddressDetail)
    shippingPrice = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return('ShippingDetail Id - ' + str(self.id))

class PackageDetails(models.Model):
    id = models.AutoField(primary_key=True)
    fragile = models.BooleanField(default=False)
    height = models.DecimalField(max_digits=10,decimal_places=2,null = False, blank=False)
    width = models.DecimalField(max_digits=10,decimal_places=2,null = False, blank=False)
    depth = models.DecimalField(max_digits=10,decimal_places=2,null = False, blank=False)
    weight = models.DecimalField(max_digits=10,decimal_places=2,null = False, blank=False)

    def __str__(self):
        return('PackageDetails ID - '+str(self.id))

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    
    subCategory = models.ForeignKey(SubCategory,on_delete=models.DO_NOTHING, null = False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = False)
    

    shippingDetail = models.ForeignKey(ShippingDetails, null = False, on_delete = models.PROTECT)
    #packageDetail = models.ForeignKey(PackageDetails, on_delete=models.PROTECT, null=True, blank= True)
    #paymentDetail = models.ForeignKey(PaymentDetail, on_delete=models.PROTECT,)

    title = models.CharField(max_length=200, blank=False,null=False)
    thumbnail1 = models.ImageField(null=False)
    thumbnail2= models.ImageField(null=True, blank=True)
    thumbnail3 = models.ImageField(null=True, blank=True)
    thumbnail4 = models.ImageField(null=True, blank=True)
    thumbnail5 = models.ImageField(null=True, blank=True)
    description = models.TextField()

    searchKeywords = models.TextField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    incTax = models.BooleanField(default=False)

    # Fee can be included in UserOrder Instead
    #fee = models.DecimalField(max_digits=10,decimal_places=2) 
    
    refundable = models.BooleanField(default=False)
    refund_period = models.IntegerField(null=True, blank=True, default= 0)
    
    availableQt = models.PositiveIntegerField(null=False, blank=False, default= 0)
    inProcessQt = models.IntegerField(null=False, blank=False,default=0)
    soldQt = models.IntegerField(null=False, blank=False,default=0)

    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return(self.title)
    
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=False,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f"Cart of {self.user}")

    def get_total_item_price(self):
        return self.quantity * self.product.price

class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, null=False,on_delete=models.CASCADE)
    description = models.TextField()
    createDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return(str(self.product) + '| Comment ID - ' + str(self.id) )

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    products = models.ManyToManyField(Product)
    productDetails = models.JSONField()
    deliveryAddress = models.ForeignKey(AddressDetail,on_delete=models.DO_NOTHING)
    deliveryPhonenumber = models.ForeignKey(PhoneDetail,on_delete=models.DO_NOTHING)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    shippingPrice = models.DecimalField(max_digits=10,decimal_places=2, default=0)
    #tax = models.DecimalField(max_digits=10,decimal_places=2,null = True, blank=True)
    #fee = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    paymentRecieved = models.BooleanField(null=False ,blank= False,default=False)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return("ID - " + str(self.id) + ' Ordering User - ' + str(self.user))
    

