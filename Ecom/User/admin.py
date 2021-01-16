from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(User)
admin.site.register(PhoneTypes)
admin.site.register(PhoneDetail)
admin.site.register(AddressTypes)
admin.site.register(AddressDetail)
admin.site.register(SubscriptionTypes)
admin.site.register(SubscriptionPeriods)
admin.site.register(SubscriptionDetail)

admin.site.register(UserDetails)


