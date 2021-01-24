from django.contrib import admin
from .models import *
# Register your models here.



admin.site.register(Category)
admin.site.register(SubCategory)

admin.site.register(ShippingTypes)
admin.site.register(ShippingDetails)
admin.site.register(PackageDetails)
admin.site.register(Product)
admin.site.register(Comments)
admin.site.register(Cart)
admin.site.register(Order)

