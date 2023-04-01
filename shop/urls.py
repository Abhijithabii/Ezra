from . import views
from django.urls import path
                                            
urlpatterns = [
    path('', views.viewcart, name="viewcart"),
    path('addtocart/<int:varient_id>/', views.addtocart, name='addtocart'),
    #plus cart using ajax
    # path('pluscart/', views.plus_cart,name='pluscart'),
    path('addcartitem/<int:product_id>/<int:varient_id>/',views.addcartitem,name='addcartitem'),
    path('removecartitem/<int:product_id>/<int:varient_id>/',views.removecartitem,name='removecartitem'),
    path('removecartproduct/<int:product_id>/<int:varient_id>/',views.removecartproduct,name='removecartproduct'),

    #wishlist urls 
    path('wishlist/',views.userwishlist,name='userwishlist'),
    path('addwishlist/<int:varient_id>/',views.add_to_wishlist,name='add_to_wishlist'),
    path('removewishlist/<int:varient_id>/',views.remove_from_wishlist,name='remove_from_wishlist'),

    path('checkout/',views.checkout,name='checkout'),
    path('orderconfirm/',views.confirm_order,name='orderconfirm'),
    path('sendmails/',views.sendmails, name='sendmail'),
    path('placeorder/',views.placeOrder,name='ordersuccess'),
    path('ordercomplete/',views.orderComplete,name="ordercomplete"),
    path('proceed_to_pay/',views.razorPayCheck,name="razorpaycheck"),
]