from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser

from django.utils import timezone
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, fullname, email, phonenumber, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, fullname=fullname, phonenumber=phonenumber, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, fullname, email, phonenumber, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(fullname, email, phonenumber, password, **extra_fields)


class User(AbstractUser):
    username = None
    fullname = models.CharField(max_length=200,blank=False,null=False, default='SuperUser')
    email = models.EmailField(_('email address'), unique=True, primary_key=True)
    phonenumber =  PhoneNumberField(null=False, blank=False, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname', "phonenumber"]
    objects = CustomUserManager()

    def __str__(self):
        return(self.email)




# This model contains all the phone types like CELL, HOME, OFFICE , etc
class PhoneTypes(models.Model):
    id = models.AutoField(primary_key=True)
    phType = models.CharField(max_length=20,blank=False,null=False)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return(self.phType)


# This model contains the details of phone numbers which users 
class PhoneDetail(models.Model):
    id =models.AutoField(primary_key=True)
    phType = models.ForeignKey(PhoneTypes,default=1, on_delete=models.PROTECT, null = True)
    #countryCode = models.IntegerField(max_length=7,default=91,null=False)
    phoneNum = PhoneNumberField(null=False, blank=False)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return(str(self.phoneNum))



#billing/shipping(for supplier)/recieving
class AddressTypes(models.Model):
    id = models.AutoField(primary_key=True)
    addType = models.CharField(max_length=20,blank=False,null=False)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return(self.addType)

class AddressDetail(models.Model):
    id = models.AutoField(primary_key=True)
    addType = models.ForeignKey(AddressTypes,on_delete=models.PROTECT)
    addressLine1 = models.CharField(max_length=200,blank=False,null=False)
    addressLine2 = models.CharField(max_length=200,blank=False,null=False)

    addressLine3 = models.CharField(max_length=200,blank=True,null=True)
    addressLine4 = models.CharField(max_length=200,blank=True,null=True)
    addressLine5 = models.CharField(max_length=200,blank=True,null=True)
    
    city = models.CharField(max_length=50,blank=False,null=False)
    state = models.CharField(max_length=50,blank=False,null=False)

    zipCode = models.PositiveIntegerField(max_length=6,blank=False,null=False)
    zip4 = models.PositiveIntegerField(max_length=4,blank=True,null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6,blank=True,null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6,blank=True,null=True)
    isPrimary = models.BooleanField(default=False)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return(self.addressLine1+ ", " + self.addressLine2 + ", " + self.city + ", " + self.state)

#subsrcip price
class SubscriptionTypes(models.Model):
    id = models.AutoField(primary_key=True)
    subType = models.CharField(max_length=200,blank=False,null=False,)
    subPrice = models.DecimalField(max_digits=10,decimal_places=2)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return(self.subType + ' Price : ' + str(self.subPrice))

class SubscriptionPeriods(models.Model):
    id = models.AutoField(primary_key=True)
    subPeriod = models.IntegerField(blank=False,null=False,)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return(str(self.subPeriod) + ' Months')

#subtype = ad , --
#expiration period subtype in a new class
class SubscriptionDetail(models.Model):
    id = models.AutoField(primary_key=True)
    subType = models.ForeignKey(SubscriptionTypes,on_delete=models.PROTECT)
    subPeriod = models.ForeignKey(SubscriptionPeriods,on_delete=models.PROTECT)
    createDate = models.DateTimeField(auto_now_add=True)
    renewDate = models.DateTimeField(auto_now=True)
    gracePeriod = models.IntegerField(default=0, null=False)
    isExpired = models.BooleanField(default=False, null=False)

    def __str__(self):
        return(str(self.subType) + ' ' + str(self.id))


#======================Payment Reference Field=============
#Cash on Delivery, Debit Card, Credit Card, PayTm
'''class PaymentTypes(models.Model): # R
    id = models.AutoField(primary_key=True)
    types = models.CharField(max_length=20,blank=False,null=False,)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return(self.types)

class PaymentItem(models.Model): # R
    id = models.AutoField(primary_key=True)
    key =  models.CharField(max_length=200, blank=False,null=False)
    valueType =  models.CharField(max_length=1,blank=False,null=False)
    maxLength = models.IntegerField(null=False)

    def __str__(self):
        return(str(self.id))


class PaymentDetail(models.Model): # R
    id = models.AutoField(primary_key=True)
    types = models.ForeignKey(PaymentTypes,on_delete=models.CASCADE)
    paymentItems = models.ManyToManyField(PaymentItem)

    def __str__(self):
        return('Payment Detail id - ' + str(self.id))

class ClientPaymentDetail(models.Model):
    id = models.AutoField(primary_key=True)
    types = models.ManyToManyField(PaymentTypes,on_delete=models.CASCADE)

    
    def __str__(self):
        return('Payment Detail id - ' + str(self.id))

class ClientPaymentItems(models.Model):
    id = models.AutoField(primary_key=True)
    paymentItem = models.ForeignKey(PaymentItem)
    clientPaymentDetail = models.ForeignKey(ClientPaymentDetail)
    value =  models.CharField(max_length=1000,blank=False,null=False)
    
    def __str__(self):
        return(str(self.id))'''
    

#===========================================================

class UserDetails(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    subscriptions = models.ForeignKey(SubscriptionDetail, on_delete=models.DO_NOTHING, null = True, blank= True)
    addresses = models.ManyToManyField(AddressDetail)
    phones = models.ManyToManyField(PhoneDetail)
    #payments = models.ManyToManyField(ClientPaymentDetail)

    def __str__(self):
        return("Details for User : " + str(self.user))