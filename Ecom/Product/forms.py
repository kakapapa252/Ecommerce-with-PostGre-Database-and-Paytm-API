from django import forms

from django.db.models import Q
from django.forms import ModelForm
from .models import Product, ShippingDetails, Comments, Order
from User.models import UserDetails

class CreateProductForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subCategory'].required = True
        self.fields['title'].required = True
        self.fields['description'].required = True
        self.fields['thumbnail1'].required = True
        self.fields['price'].required = True
        self.fields['availableQt'].required = True

    class Meta:
        model = Product
        fields = ['subCategory','title','description','thumbnail1','thumbnail2','thumbnail3','thumbnail4','thumbnail5','price','availableQt','refund_period']

class CreateShippingForm(ModelForm):

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['shippingType'].required = True
        if user:
            userDetails = UserDetails.objects.get(user=user)
            self.fields['shippingAdresses'].queryset = userDetails.addresses.all()
        self.fields['shippingAdresses'].required = True
        self.fields['shippingPrice'].required = True

    class Meta:
        model = ShippingDetails
        fields = ['shippingType','shippingAdresses','shippingPrice']


class CommentForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].label = 'Add Comment'
        self.fields['description'].required = True
    
    class Meta:
        model = Comments
        fields = ['description']


class CheckoutForm(ModelForm):

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            userDetails = UserDetails.objects.get(user=user)
            self.fields['deliveryAddress'].queryset = userDetails.addresses.all()
            userDetails = UserDetails.objects.get(user=user)
            self.fields['deliveryPhonenumber'].queryset = userDetails.phones.all()

        self.fields['deliveryAddress'].required = True
        self.fields['deliveryPhonenumber'].required = True
    class Meta:
        model = Order
        fields = ['deliveryAddress', 'deliveryPhonenumber']