from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


PAYMENT_CHOICES=(('S','Stripe'),('P','Paypal'))

# class CheckoutForm(forms.Form):
#     street_address=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'1234 Main Street'}))
#     apartment_address=forms.CharField(required=False,widget=forms.TextInput(attrs={'placeholder':'Apartment or Suite'}))
#     country = CountryField(blank_label='(select country)').formfield(
#                                             widget=CountrySelectWidget( attrs={'class':'custom-select d-block w-100','id':'zip'})) 
#     zip=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
#     same_shipping_address=forms.BooleanField(widget=forms.CheckboxInput())
#     save_info=forms.BooleanField(widget=forms.CheckboxInput())
#     payment_option=forms.ChoiceField(widget=forms.RadioSelect(),choices=PAYMENT_CHOICES)  


class CheckoutForm(forms.Form):
    shipping_address=forms.CharField(required=False)
    shipping_address2=forms.CharField(required=False)
    # street_address=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'1234 Main Street'}))
    # apartment_address=forms.CharField(required=False,widget=forms.TextInput(attrs={'placeholder':'Apartment or Suite'}))
    shipping_country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(
             attrs={'class':'custom-select d-block w-100','id':'zip'})) 
    
    billing_address=forms.CharField(required=False)
    billing_address2=forms.CharField(required=False)
    billing_country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(
             attrs={'class':'custom-select d-block w-100','id':'zip'})) 
    billing_zip=forms.CharField(required=False)
    
    shipping_zip=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    same_billing_address=forms.BooleanField(required=False)
    
    set_default_shipping=forms.BooleanField(required=False)
    use_default_shipping=forms.BooleanField(required=False)
    
    set_default_billing=forms.BooleanField(required=False)
    use_default_billing=forms.BooleanField(required=False)
  
    payment_option=forms.ChoiceField(widget=forms.RadioSelect(),choices=PAYMENT_CHOICES)

class PaymentForm(forms.Form):
    stripeToken = forms.CharField(required=False)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)
    
class Coupon(forms.Form):
    code=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control',
                                                       'placeholder':'Promo Code',
                                                       'aria-label':'Recipients username',
                                                       'aria-describedby':'basic-addon2 '}))    

class RefundForm(forms.Form):
    ref_code=forms.CharField()
    message=forms.CharField(widget=forms.Textarea(attrs={'rows':4}))
    email=forms.EmailField()     