from . import views
from django.urls import path

urlpatterns = [
    path('', views.adminlogin, name="adminlogin"),
    path('adminbase/',views.adminhome,name="adminhome"),
    path('adminlogout',views.adminlogout,name="adminlogout"),
    path('admindashboard/',views.admindashboard,name="admindashboard"),
    path('addcategory/',views.add_categories,name="add_categories"),
    path('viewcategory/',views.viewcategory,name="viewcategory"),
    path('editcategory/<int:pid>/',views.editcategory,name="editcategory"),
    path('deletecategory/<int:pid>/',views.delete_category,name="deletecategory"),
    path('addproduct/',views.addproduct,name="addproduct"),
    # path('addimage/<int:id>/',views.addimages,name="addimage"),
    path('viewproduct/',views.viewproduct,name="viewproduct"),
    path('editproduct/<int:pid>/',views.editproduct,name="editproduct"),
    path('delete-image/<int:iid>/', views.delete_image, name='deleteimage'),
    path('deleteproduct/<int:pid>/',views.deleteproduct,name="deleteproduct"),
    path('manageuser',views.manageuser,name="manageuser"),
    path('blockuser/<int:id>/',views.blockuser,name="blockuser"),

    path('viewvarient/',views.viewvarient,name='viewvarient'),
    path('addvarient/',views.addvarient,name='addvarient'),
    path('editvarient/<int:id>/',views.editvarient,name='editvarient'),
    path('dltvarient/<int:id>/',views.deleteverient,name='dltvarient'),

    # coupon urls
    path('viewcoupon/',views.view_coupons,name="viewcoupon"),
    path('addcoupon/',views.add_coupons,name="addcoupon"),
    path('editcoupon/<int:pid>/',views.edit_coupon,name="editcoupon"),
    path('deletecoupon/<int:pid>/',views.delete_coupon,name="deletecoupon"),

    # banner urls
    path('viewbanner/',views.viewbanner,name="viewbanner"),
    path('addbanner/',views.addbanner,name="addbanner"),
    path('editbanner/<int:id>/',views.editbanner,name="editbanner"),
    path('deletebanner/<int:id>/',views.deletebanner,name="deletebanner"),

    # ordermanagement
    path('manageorder/',views.manage_order,name="manageorder"),
    path('manageordersingleview/<int:id>/',views.manage_order_singleview,name="manageordersingleview"),
    path('updateorder/<int:id>/',views.update_order,name='updateorder'),
    

    path('salesreport',views.sales_report,name="salesreport"),
    # path('generatereport',views.generate_report,name="generate_report"),
]
