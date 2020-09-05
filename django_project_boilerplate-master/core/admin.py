from django.contrib import admin
from .models import Item,Order,OrderItem,Address,Payment,Coupon

class OrderAdmin(admin.ModelAdmin):
     list_display=['user','ordered','being_delivered','received','refund_requested','refund_granted','billing_address','shipping_address','payment','coupon']
     list_display_link=['user','billing_address','shipping_address','payment','coupon']
     list_filter=['user','ordered','being_delivered','received','refund_requested','refund_granted']
     search_field=['user__username','ref_code']
     # actions=[make_refund_accepted]
     
  
class AddressAdmin(admin.ModelAdmin):
     list_display=['user','street_address','apartment_address','country','zip','address_type','default']
     list_filter=['country','default','address_type']
     search_fields=['user','street_address','apartment_address','zip']
       
admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order,OrderAdmin)
admin.site.register(Payment)
admin.site.register(Address)
admin.site.register(Coupon)
