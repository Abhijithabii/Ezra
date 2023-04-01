from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Category, Product, ProductImage, ProductVarient
from shop.models import *
from shop.forms import CouponForm
from django.contrib import messages
from userhome.models import UserProfile, Banner
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.cache import cache_control
from django.db.models import  Sum
from datetime import datetime
from django.http import JsonResponse



import os
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.

def adminlogin(request):
    msg = None
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        try:
            if user.is_staff:
                login(request, user)
                messages.success(request,"User login successfully")
                return redirect(admindashboard)
            else:
                messages.success(request, "Invalid Credentials")
        except:
            messages.success(request,"Invalid Credentials")
    return render(request, 'adminside/adminlogin.html')


def adminlogout(request):
    logout(request)
    messages.success(request, "Logout Successfully")
    return redirect(adminlogin)



@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def adminhome(request):
    return render(request, 'adminside/admin_base.html')

@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admindashboard(request):
    user=User.objects.all().count()
    product=Product.objects.all().count()
    allcategory = Category.objects.all()
    category=allcategory.count()
    order=Order.objects.all().count()
    coupons=Coupon.objects.all().count()
    total_income = Payment.objects.aggregate(Sum('amount_paid'))['amount_paid__sum']
    refunded = Payment.objects.filter(refund_id=None)
    refund_income = refunded.aggregate(Sum('amount_paid'))['amount_paid__sum']
    print(refund_income)
    # total_income = Payment.objects.filter(refund_id__isnull=False).aggregate(Sum('amount_paid'))['amount_paid__sum']

    # revenue from cash on delivery when the product is delivered
    # cod_sum = Payment.objects.filter(payment_method='COD', order__status='Delivered').aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    # revenue of all cash on delivery when the product is ordered
    cod_sum = Payment.objects.filter(payment_method='COD' ).aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    cod_sum = round(cod_sum,2)
    # Calculate the payment sum for Razorpay
    razorpay_sum = Payment.objects.filter(payment_method='Paid by Razorpay').aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    # payment_percentages = calculateNumberOfOrdersByPaymentMethod()

    
            
    context={
        'user':user,
        'product':product,
        'category':category,
        'order':order,
        'coupons':coupons,
        'total_income' :total_income,
        'razorpay_sum':razorpay_sum,
        'cod_sum':cod_sum,
        'allcategory':allcategory,

    }
    return render(request, 'adminside/admindashboard.html',context)

@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def add_categories(request):
    if request.method == 'POST':
        name = request.POST['name']
        image1 = request.FILES.get('image')
        if Category.objects.filter(name__iexact=name.lower().replace(' ', '')).exists():
            messages.info(request, "Category already exists")

        else:
            Category.objects.create(name=name,image=image1)
            messages.success(request, "Category added successfully")
            return redirect(viewcategory)
    return render(request,'adminside/add_category.html')


@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def viewcategory(request):
    category = Category.objects.all().order_by('id')
    dict_user={
        'categories':category
    }
    return render(request, 'adminside/view_category.html', dict_user)

@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def editcategory(request, pid):
    category = Category.objects.get(id=pid)
    if request.method == 'POST':
        name = request.POST['name']
        image = request.FILES.get('image')
        print(image)
        # if Category.objects.filter(name__iexact=name.lower().replace(' ', '')).exists():
        #     messages.info(request,"Category name already exists")
            
        # else:
        category.name = name
        if image is not None:
            category.image = image
        category.save()
        messages.success(request,'Category edited successfully')
        return redirect(viewcategory)
      
    return render(request, 'adminside/edit_category.html', locals())



@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def delete_category(request, pid):
    category = Category.objects.get(id=pid)
    category.delete()
    messages.info(request,'Category deleted successfully')
    return redirect(viewcategory)



#product wise functions
@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def addproduct(request):
    category = Category.objects.all()
    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        categ = request.POST['categories']
        desc = request.POST['desc']
        images = request.FILES.getlist('image')
        catobj = Category.objects.get(id=categ)
        if price.isdigit():
            product = Product.objects.create(name=name, price=price, category=catobj, description=desc)
            product.save()
            for image in images:
                ProductImage.objects.create(product=product, images=image)
            messages.success(request, "Product Added")
            return redirect(viewproduct)
        else:
            messages.warning(request,"Please Enter a valid quantity")
            return redirect(addproduct)

    return render(request, 'adminside/add_product.html',locals())



@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def viewproduct(request):
    product = Product.objects.all().order_by('id')
    varient = ProductVarient.objects.all()


    paginator = Paginator(product, 6)
    page_numebr = request.GET.get('page')
    page_obj = paginator.get_page(page_numebr)
    dict_prod = {
        'product' : product,
        'page_obj': page_obj,
        'varient':varient
    }
    return render(request, 'adminside/view_product.html',dict_prod)



@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def editproduct(request, pid):
    product = Product.objects.get(id=pid)
    category = Category.objects.all()
    images = ProductImage.objects.filter(product=product)
    if request.method == "POST":
        name = request.POST['name']
        price = request.POST['price']
        cat = request.POST['category']
        desc = request.POST['desc']
        catobj = Category.objects.get(id=cat)
        if price.isdigit():
            # Update product attributes
            Product.objects.filter(id=pid).update(name=name, price=price, category=catobj, description=desc)

        
        else:
            messages.warning(request,"Enter a valid quantity")
            return redirect(editproduct,pid)

        
        # Get the new images uploaded during editing
        new_images = request.FILES.getlist('images')

        # Add the new images to the product
        for image in new_images:
            ProductImage.objects.create(product=product, images=image)
       
        messages.success(request, "Product Updated")
        return redirect(viewproduct)
    return render(request, 'adminside/edit_product.html', locals())

@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def delete_image(request, iid):
    image = ProductImage.objects.get(id=iid)
    image_path = os.path.join(settings.MEDIA_ROOT, str(image.images))
    os.remove(image_path)
    product_id = image.product.id if image.product else None
    image.delete()
    if product_id:
        return HttpResponseRedirect(reverse(editproduct, args=[product_id]))
    else:
        return HttpResponseRedirect(reverse(viewproduct))
    print(f"DEBUG: iid={iid}, image={image}, image_path={image_path}, product_id={product_id}")


# def delete_image(request, iid):
#     image = ProductImage.objects.get(id=iid)
#     image_path = os.path.join(settings.MEDIA_ROOT, str(image.images))
#     os.remove(image_path)
#     product_id = image.product.id if image.product else None
#     image.delete()
#     response_data = {"success": True}
#     return JsonResponse(response_data)



@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def deleteproduct(request, pid):
    product = Product.objects.get(id=pid)
    product.delete()
    messages.success(request, "Product Deleted")
    return redirect(viewproduct)


# varient
@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def viewvarient(request):
    varient = ProductVarient.objects.all().order_by('id')
    context = {
        'varient':varient,
    }

    return render(request, 'adminside/view_varient.html',context)



@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def addvarient(request):
    products = Product.objects.all()
    if request.method == 'POST':
        product_id = request.POST['product']
        prod_varientname = request.POST['varname']
        stock = request.POST['stock']
        product = Product.objects.get(id=product_id)
        if stock.isdigit():
             # if ProductVarient.objects.filter(varientname__iexact=prod_varientname.lower().replace(' ', '')).exists(): 
            #     messages.warning(request,'The varient name with the same product already exists')
            # else:
            productvarient = ProductVarient.objects.create(varientname=prod_varientname,varstock=stock,proname=product)
            productvarient.save()
            messages.success(request, 'varient added successfully')
            return redirect(viewvarient)
            
        else:
            messages.warning(request,'Enter a valid Quantity')
           
    context = {
       'products': products,
    }
    return render(request, 'adminside/add_varient.html', context)


@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def editvarient(request,id):
    product = Product.objects.all()
    provarient = ProductVarient.objects.get(id=id)
    if request.method == 'POST':
        name = request.POST['products']
        varname = request.POST['varname']
        stock = request.POST['stock']
        if stock.isdigit():
            ProductVarient.objects.filter(id=id).update(varientname=varname,varstock=stock,proname=name)
            messages.success(request, ' varient edited successfully')
            return redirect(viewvarient)
            
        else:
            messages.warning(request,"Enter a valid quantity")
    context = {
        'product':product,
        'provarient':provarient,
    }
    return render(request,'adminside/edit_varient.html',context)



@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def deleteverient(request,id):
    productvar = ProductVarient.objects.get(id=id)
    productvar.delete()
    messages.success(request, "Product Deleted")
    return redirect(viewvarient)



@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def manageuser(request):
    user = User.objects.all().order_by('id')[1:]

    return render(request, 'adminside/manage_user.html', {'user': user})



@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def blockuser(request, id):
    user = get_object_or_404(User, id=id)
    if user.is_active:
        user.is_active = False
        messages.success(request, "user has been blocked.")
    else:
        user.is_active = True
        messages.success(request, "user has been unblocked.")
    user.save()
    return redirect(manageuser)



# coupon side functions
@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def view_coupons(request):
    coupons = Coupon.objects.all()
    return render(request,'adminside/view_coupon.html',{'coupons':coupons})


@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def add_coupons(request):
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(view_coupons)
    else:
        form = CouponForm()
    return render(request, 'adminside/add_coupon.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def edit_coupon(request, pid):
    coupon = Coupon.objects.get(id=pid)

    if request.method == "POST":
        form = CouponForm(request.POST, instance=coupon)
        if form.is_valid():
            form.save()
            messages.success(request, "Coupon Updated")
            return redirect(view_coupons)
    else:
        form = CouponForm(instance=coupon)
        messages.error(request, "fill all fields")

    return render(request, 'adminside/edit_coupon.html', {'form': form, 'coupon': coupon})



@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def delete_coupon(request, pid):
    coupon = Coupon.objects.get(id=pid)
    coupon.delete()
    messages.success(request, "Coupon Deleted")
    return redirect(view_coupons)

# bannerside functions


@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def viewbanner(request):
    banner = Banner.objects.all().order_by('id')
    context = {
        'banner':banner
    }
    return render(request, 'adminside/view_banner.html',context)



@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def addbanner(request):
    if request.method == 'POST':
        title = request.POST['title']
        desc = request.POST['desc']
        newimage = request.FILES['image']
        banner = Banner.objects.create(title=title,desc=desc,image=newimage)
        banner.save()
        messages.success(request, ' Banner added successfully')
        return redirect(viewbanner)

    return render(request, 'adminside/add_banner.html')

@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def editbanner(request, id):
    banner = Banner.objects.get(id=id)
    if request.method == 'POST':
        title = request.POST['title']
        desc = request.POST['desc']
        new_image = request.FILES.get('image')
        if new_image:
            # delete the old image
            if banner.image:
                banner.image.delete()
            # save the new image to the same path
            banner.image = new_image
        banner.title = title
        banner.desc = desc
        banner.save()

        messages.success(request, 'Banner edited successfully')
        return redirect('viewbanner')
    
    context = {'banner': banner}
    return render(request, 'adminside/edit_banner.html', context)



@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def deletebanner(request, id):
    banner = Banner.objects.get(id=id)
    banner.delete()
    messages.info(request, 'Banner deleted successfully')
    return redirect(viewbanner)



@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def manage_order(request):
    orders=Order.objects.all().order_by('-id')
    return render(request, 'adminside/manage_order.html', locals())


@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def manage_order_singleview(request, id):
    order =Order.objects.filter(id=id).first()
    print(order)
    orderitems = OrderProduct.objects.filter(order=order)
    print(orderitems)
    context = {
        'order':order,
        'orderitems':orderitems,
    }
    return render(request, 'adminside/manage_order_singleview.html',context)



@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def update_order(request, id):
    if request.method == 'POST':
        order = Order.objects.get(id=id)
        status = request.POST.get('status')
        if(status):
            order.status = status
            order.save()
        if status  == "Delivered":
            try:
                payment = Payment.objects.get(payment_id = order.order_number, status = False)
                print(payment)
                if payment.payment_method == 'Cash on Delivery':
                    payment.paid = True
                    payment.save()
            except:
                pass
    return redirect(manage_order)




@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def sales_report(request):
    orders = Order.objects.all().order_by('-id')
    today_date = datetime.now().strftime('%Y-%m-%d')

    if 'from_date' in request.GET and 'to_date' in request.GET:
        from_date = request.GET['from_date']
        to_date = request.GET['to_date']

        if to_date > today_date:
            messages.warning(request, "Please select a date up to today's date.")
        elif from_date > to_date:
            messages.warning(request, "The from date should be before than the To date")
        else:
            orders = orders.filter(created_at__range=[from_date, to_date])
            total_sales = orders.aggregate(Sum('paid_amount'))['paid_amount__sum']
            

    return render(request, 'adminside/sales_report.html', locals())

