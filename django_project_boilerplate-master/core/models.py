from django.db import models
from django.shortcuts import reverse
from django.conf import settings
from django.db.models import Sum
from django_countries.fields import CountryField
import datetime
from django.db.models.signals import post_save


LABEL_CATEGORY=(('d','danger'),('s','secondary'),('p','primary'))

CATEGORY_FIELD=(('S','Shirt'),('O','OutWear'),('SW','SportsWear'))

# COLOR=(('12','blue'),('13','red'),('14','gray'),('15','black'))
ADDRESS_CHOICES=(('B','Billing'),('S','Shipping'))


class UserProfile(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    stripe_customer_id=models.CharField(max_length=50,blank=True,null=True)
    one_click_purchasing=models.BooleanField(default=False)

    def __str__(self):
        self.user.username


class Item(models.Model):
    title=models.CharField(max_length=200)
    label=models.CharField(choices=LABEL_CATEGORY,max_length=2)
    description=models.TextField()
    category=models.CharField(choices=CATEGORY_FIELD,max_length=2)
    # color=models.CharField(choices=COLOR,max_length=10)
    price =models.FloatField()
    discount_price=models.FloatField(null=True,blank=True)
    slug = models.SlugField()
    # quantity=models.IntegerField(default=1)
    image=models.ImageField()

    def get_absolute_url(self):
        return reverse("core:product", kwargs={'slug': self.slug})

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={'slug':self.slug})

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={'slug':self.slug})

    def __str__(self):
        return self.title


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,blank=True, null=True)
    quantity= models.IntegerField(default=1)
    item = models.ForeignKey(Item, on_delete=models.CASCADE,null=True)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of {self.item.title} {self.item.slug}"

    def get_total_price(self):
        return self.quantity*self.item.price

    def get_discount_price(self):
        return self.quantity*self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_price() - self.get_discount_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_discount_price()
        self.get_total_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=30,blank=True,null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey('Address',related_name='billing_address',on_delete=models.SET_NULL,blank=True,null=True)
    shipping_address = models.ForeignKey('Address',related_name='shipping_address',on_delete=models.SET_NULL,blank=True,null=True)
    payment = models.ForeignKey('Payment',on_delete=models.SET_NULL,blank=True,null=True)
    coupon = models.ForeignKey('Coupon',on_delete=models.SET_NULL,blank=True,null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total=0
        for order_item in self.items.all():
            total+=order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple =False)
    zip = models.CharField(max_length=10)
    address_type = models.CharField(max_length=1,choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural='Addresses'

class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=30)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,blank=True,null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        self.user.username

class Coupon(models.Model):
    code=models.CharField(max_length=15)
    amount=models.FloatField()

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return f"{self.pk}"

def user_profile_receiver(sender,instance ,created, *args, **kwargs):
    if created:
        userprofile=UserProfile.objects.create(user=instance)

post_save.connect(user_profile_receiver,sender=settings.AUTH_USER_MODEL)





