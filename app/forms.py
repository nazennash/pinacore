from django import forms
from .models import User
from phonenumber_field.widgets import PhoneNumberPrefixWidget


class RegisterForm(forms.ModelForm):
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ["phone_number",]
        widgets = {
            'phone': PhoneNumberPrefixWidget(initial='US'),
        }

class VerifyForm(forms.ModelForm):
    number = forms.CharField(label='Code',widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ["number",]


CATEGORY_CHOICES = (
    'PCS,PCS'
)

class RequestForm(forms.Form):
    item = forms.CharField(label="Item",widget=forms.TextInput(attrs={'class':'form-control'}))
    item_desc = forms.CharField(label="Description",widget=forms.TextInput(attrs={'class':'form-control'}))
    quantity = forms.IntegerField(label="Quantity",widget=forms.TextInput(attrs={'class':'form-control'}))
    # quantity = forms.CharField(widget=forms.IntegerField(attrs={'class':'form-control'}))
    # item_measure = forms.CharField(choices=forms.CATEGORY_CHOICES)