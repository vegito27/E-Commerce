from django.urls import path, include
from rest_framework import routers
from .views import ( UserViewSet,
                     GroupViewSet,
                     home,
                     CheckOutView,
                     HomeView,
                     ItemDetailView,
                     add_to_cart,
                     remove_single_item_from_cart,
                     remove_from_cart,
                     OrderSummaryView,
                     remove_single_item_from_cart,
                     PaymentView,
                     AddCouponView,
                     RequestRefundView,
                     )

app_name="core"

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)


urlpatterns = [
    path('',HomeView.as_view(),name="home"),
    path('rest/', include(router.urls)),
    path('api/', include('rest_framework.urls', namespace='rest_framework')),
    path('order-summary/',OrderSummaryView.as_view(),name="order-summary"),
    path('checkout/',CheckOutView.as_view(),name="checkout"),
    path('product/<slug>/',ItemDetailView.as_view(),name="product"),
    path('add-to-cart/<slug>/',add_to_cart,name="add-to-cart"),
    path('add-coupon/<code>/',AddCouponView.as_view(),name="add-coupon"),
    path('remove-from-cart/<slug>/',remove_from_cart,name="remove-from-cart"),
    path('remove-single-item-from-cart/<slug>/', remove_single_item_from_cart,name="remove-single-item-from-cart"),
    path('payment/<payment_option>/',PaymentView.as_view(),name="payment"),
    path('request-refund/',RequestRefundView.as_view(),name="request-refund")
    
]