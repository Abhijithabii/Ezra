from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name="home"),


    path('register/', views.register, name='register'),
    path('verifyotp/<int:user_id>/', views.verify_otp, name='verifyotp'),
    path('resend-otp/<int:user_id>/', views.resend_otp, name='resend_otp'),


    path('login/',views.user_login,name="login"),
    path('resetpass/<int:user_id>/', views.reset_password, name='resetpass'),
    path('forgotpass/', views.forgot_password, name='forgotpass'),


    path('logout/',views.user_logout,name="logout_user"),
    #shop view
    # new
    # path('userproduct/',views.userproduct,name="userproduct"),
    # old
    path('userproduct/<int:id>/',views.userproduct,name="userproduct"),
    path('search/',views.search,name="search"),
    path('singleproduct/<int:id>/',views.singleproduct,name="singleproduct"),

    #userprofile
    path('updateprofile',views.updateprofile,name="updateuserprofile"),
    #changing password of a authenticated user
    path('changepass/',views.changepassword,name="changepassword"),
    path('userprofile/',views.userprofile,name="userprofile"),
    path('useraddress/',views.address_book,name="useraddress"),
    path('addaddress/<int:id>/',views.add_address,name="add_address"),
    path('edit-address/<int:address_id>/', views.edit_address, name='edit_address'),
    path('dlt-address/<int:address_id>/', views.delete_address, name='delete_address'),
    path('usertotalorderview/',views.user_total_orderview,name="usertotalorderview"),
    path('usersingleorder/<int:id>/',views.user_single_orderview,name="usersingleorderview"),
    path('cancelorder/<int:id>/',views.cancelorder,name="cancelorder"),
    path('returnorder/<int:id>/',views.return_order,name="returnorder"),
    

    path('error/',views.error_404,name='error'),

]
