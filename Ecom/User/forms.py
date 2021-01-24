from django import forms

from django.db.models import Q
from django.forms import ModelForm
from .models import *


class PhoneDetailForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phType'].label = "Type"
        self.fields['phType'].required = True
        self.fields['phType'].queryset = PhoneTypes.objects.filter(~Q(id=1))

        self.fields['phoneNum'] = forms.CharField(label="Phone Number", widget=forms.TextInput(attrs={'placeholder': "Add '+countrycode' before number" }))
        self.fields['phoneNum'].required = True

    class Meta:
        model = PhoneDetail
        fields = ['phType','phoneNum']


class AddressDetailForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['addType'].label = "Type"
        self.fields['addType'].required = True
        self.fields['addressLine1'].required = True
        self.fields['addressLine2'].required = True
        self.fields['city'].required = True
        self.fields['state'].required = True
        self.fields['zipCode'].required = True


    class Meta:
        model = AddressDetail
        fields = ['addType','addressLine1','addressLine2','zipCode','city',"state"]

class SubscriptionDetailForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subType'].required = True
        self.fields['subPeriod'].required = True


    class Meta:
        model = SubscriptionDetail
        fields = ['subType','subPeriod']