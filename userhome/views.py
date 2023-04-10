from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from adminhome.models import Category, Product, ProductImage,  ProductVarient
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from.models import UserProfile, Address, Banner
from .forms import UserProfileForm, UserForm
from shop.models import *
from django.core.paginator import Paginator
import razorpay
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
import myproject.settings

# from django.views import View
# from .forms import CustomerProfileForm
# Create your views here.

def home(request):
    product = Product.objects.all().order_by('-id')[:8]
    banner = Banner.objects.all()
    category = Category.objects.all()
    context = {
        'banner':banner,
        'product':product,
        'category':category,
    }
    return render(request, 'home.html',context)


def register(request):

    user = None
    if request.method == 'POST':
        # Get form data
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        # Check if email already exists
        if User.objects.filter(username=email).exists():
            messages.error(request, 'Email already exists')
            return redirect(register)

        # # Check if username already exists
        # if User.objects.filter(username=username).exists():
        #     messages.error(request, 'Username already exists')
        #     return redirect('register')

        # Check if password and confirm password match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect(register)
        
        else:

        # Generate OTP
            otp = get_random_string(length=6, allowed_chars='1234567890')
        
        # Save user details to database
            user = User.objects.create_user(username=email, password=password, first_name=username)
        
        # Send OTP to user email
            subject = 'OTP for account verification'
            message = f'Your OTP for account verification is {otp}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email,]
            send_mail(subject, message, email_from, recipient_list)


         # Create UserProfile object for the user
            UserProfile.objects.create(user=user)
            Wallet.objects.create(user=user)
            
        # Save OTP to database
            user.profile.otp = otp
            user.profile.save()
        
        # Redirect to OTP verification page
            return redirect('verifyotp', user.id)
            

    return render(request, 'register.html')


def verify_otp(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        otp = request.POST['otp']
        if len(otp) == 6:
            if user.profile.otp == otp:
                user.profile.is_verified = True
                user.profile.otp = ''
                user.profile.save()
                messages.success(request, 'Account has been verified')
                return redirect(user_login)
            else:
                messages.error(request, 'Invalid OTP')
                return redirect('verifyotp', user_id)
        else:
            messages.error(request, 'enter correct otp')

    return render(request, 'verify_otp.html', {'user': user})


def resend_otp(request, user_id):
    user = User.objects.get(id=user_id)

    # Generate new OTP
    otp = get_random_string(length=6, allowed_chars='1234567890')

    # Send new OTP to user email
    subject = 'New OTP for account verification'
    message = f'Your new OTP for account verification is {otp}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.username,]
    send_mail(subject, message, email_from, recipient_list)

    # Save new OTP to database
    user.profile.otp = otp
    user.profile.save()

    messages.success(request, 'New OTP has been sent to your email')
    return redirect('verifyotp', user_id)





def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(username=email).exists():
            user = User.objects.get(username=email)
            otp = get_random_string(length=6, allowed_chars='1234567890')
            user.profile.otp = otp
            user.profile.save()
            subject = 'OTP for password reset'
            message = f'Your OTP for password reset is {otp}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email,]
            send_mail(subject, message, email_from, recipient_list)
            return redirect('resetpass', user.id)
        else:
            messages.error(request, 'Email does not exist')
            return redirect(forgot_password)
    return render(request, 'forgot_password.html')




def reset_password(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        otp = request.POST['otp']
        if user.profile.otp == otp:
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']
            if password == confirm_password:
                user.set_password(password)
                user.profile.otp = ''
                user.profile.save()
                user.save()
                messages.success(request, 'Password reset successful. Please login.')
                return redirect('login')
            else:
                messages.error(request, 'Passwords does not match')
        else:
            messages.error(request, 'Invalid OTP')
    return render(request, 'reset_password.html', {'user': user})


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "User login successfully")
            
            # Transfer cart items from session to user's cart
            cart = request.session.get('cart', {})
            if cart:
                for item_id, item_data in cart.items():
                    product_id, varient_id = item_id.split('-')  # Split the item_id to get the product_id and variant_id
                    if CartItem.objects.filter(user=user, product_id=product_id, provar_id=varient_id).exists():
                        item = CartItem.objects.get(user=user, product_id=product_id, provar_id=varient_id)
                        item.quantity += item_data['quantity']
                        item.save()
                    else:
                        CartItem.objects.create(user=user, product_id=product_id, provar_id=varient_id, quantity=item_data['quantity'])
                del request.session['cart']
            
            return redirect(home)
        
        else:
             messages.info(request, 'Invalid Username or password')

    return render(request, 'login.html', locals())


def user_logout(request):
    logout(request)
    messages.info(request, "Logout Successfully")
    return redirect('home')

# def userproduct(request):
#     allcategory = Category.objects.all()
#     product = Product.objects.all()
#     varient = ProductVarient.objects.all()
#     cat_id = request.GET.get('catid')
#     vari_id = request.GET.get('varientid')
#     print(vari_id)
#     if cat_id:
#         product = Product.objects.filter(category=cat_id)

#     elif vari_id:
#         product = Product.objects.filter(varient_name=vari_id)
#     else:
#         product = Product.objects.all()
#     context = {
#         'allcategory':allcategory,
#         'product':product,
#         'varient':varient,
#     }
#     return render(request, 'user_product.html',context)

# def userproduct(request, id):
#     if id == 0 :
#         product = Product.objects.all()
        
#     else:
#         category = Category.objects.get(id=id)
#         varient_id = request.GET.get('varientid')
#         if varient_id:
#             product = Product.objects.filter(category=category, varname_id=varient_id)
#         else:
#             product = Product.objects.filter(category=category)

#     paginator = Paginator(product, 6)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     allcategory = Category.objects.all()
#     varient = ProductVarient.objects.all()

#     context = {
#         'product': product,
#         'allcategory': allcategory,
#         'page_obj': page_obj,
#         'varient': varient,
#     }
#     return render(request, 'user_product.html', context)


def userproduct(request, id):
    # normal working in varients
    if id == 0:
        product = Product.objects.all()
        
    else:
        category = Category.objects.get(id=id)
        product = Product.objects.filter(category=category)

    
    paginator = Paginator(product, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    allcategory = Category.objects.all()
    varient = ProductVarient.objects.all()

    context = {
        'product': product,
        'allcategory': allcategory,
        'page_obj': page_obj,
        'varient': varient,
    }
    return render(request, 'user_product.html', context)
 

# def searchproduct(request):
#     if 'se' in request.GET:
#         se = request.GET['se']
#         obj = Product.objects.filter(name__startswith=se)

#     else:
#         obj = Product.objects.all()
#         dict_userin={
#             'newuser' : obj
    
#         }

#     return redirect(request, 'user_product.html',dict_userin)


def singleproduct(request, id):
    prod = Product.objects.get(id=id)
    images = ProductImage.objects.filter(product_id=id)
    provar = prod.variants.all()
    if request.method == 'POST':
        newvarient_id = request.POST.get('selectedwish')
        varient = ProductVarient.objects.get(id=newvarient_id)
        
        print(newvarient_id,'----------------------')
        print(varient,'----------------------')
        v= render_to_string('varient.html',{'varient':varient})
        return JsonResponse({'data':v})
        
    context =  {
        'prod':prod ,
        'images':images,
        'provar':provar,
        }
    return render(request, 'user_singleprod_details.html', context)



# class UpdateUserProfile(View):
#     def get(self, request):
#         form = CustomerProfileForm()
#         return render(request, 'updateuserprofile.html', locals())
    
#     def post(self, request):
#         form = CustomerProfileForm(request.POST)
#         if form.is_valid:
#             user = request.user
#             mobile = form.cleaned_data['mobile']
#             address = form.cleaned_data['address']
#             image = form.cleaned_data['image']
#             district = form.cleaned_data['district']
#             state = form.cleaned_data['state']
#             pincode = form.cleaned_data['pincode']


#             reg = UserProfile(user=user,mobile=mobile,address=address,image=image,district=district,state=state,pincode=pincode)
#             reg.save()
#             messages.success(request, "PROFILE updated successfully")

#         else:
#             messages.warning(request, "invalid input")

@never_cache
@login_required(login_url='login')
def updateprofile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    user_form = UserForm(instance=request.user)
    profile_form = UserProfileForm(instance=user_profile)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile = profile_form.save()
            if 'image' in request.FILES:
                profile.image = request.FILES['image']
            user_profile = profile.save()
            messages.info(request, 'Updated Successfully')
            return redirect(userprofile)

    return render(request, 'updateuserprofile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
        



    
    # return render(request, 'userprofile.html')



@never_cache
@login_required(login_url='login')
def userprofile(request):
    totalcart = CartItem.objects.filter(user=request.user).count()
    totalwishlist = wishlist.objects.filter(user=request.user).count()
    totalorder = Order.objects.filter(user=request.user).count()
    orders = Order.objects.filter(user=request.user).order_by('-id')[:2]
    userwallet = Wallet.objects.get(user=request.user)
    
    return render(request, 'userprofile.html',locals())



@never_cache
@login_required(login_url='login')
def changepassword(request):
    if request.method == 'POST':
        oldpass = request.POST['currentpassword']
        newpass = request.POST['newpassword']
        confirm_newpass = request.POST['confirmpassword']
        user = authenticate(username=request.user.username, password=oldpass)
        if user:
            if oldpass == newpass:
                messages.warning(request, 'oldpassword and new password should not be same')

            elif newpass == confirm_newpass:
                user.set_password(newpass)
                user.save()
                messages.success(request, "Password Changed")
                return redirect(user_login)
            else:
                messages.success(request, "Password not matching")
                return redirect(changepassword)
        else:
            messages.success(request, "Invalid Password")
            return redirect(changepassword)
        
    return render(request, 'changepassword.html')



@never_cache
@login_required(login_url='login')
def address_book(request):
    addresses = Address.objects.filter(user=request.user)

    # if request.method == 'POST':
    #     selected_addresses = request.POST.getlist('selected_addresses')
    #     if not selected_addresses:
    #         messages.warning(request, 'No addresses were selected.')
    #     else:
    #         Address.objects.filter(id__in=selected_addresses).delete()
    #         messages.success(request, 'The selected addresses have been deleted.')
    #     return redirect(address_book)

    return render(request, 'address_book.html', {'addresses': addresses,})



@never_cache
@login_required(login_url='login')
def add_address(request,id):
    state = ['Kerala', 'AndraPradesh', 'Karnataka', 'Tamilnadu']
    city = ['Kannur','Kozhikkode','Ernakulam','Thiruvananthapuram','Banglore','Hubli','Hydrabad','Coimbator','Madurai']
    if Address.objects.filter(user=request.user).count() >= 5:
        messages.success(request, 'Cannot create more than 5 addresses,Please remove an address to add a new one')
        if id == 0:
            return redirect('checkout')
        else:
            return redirect(address_book)
        
    else:
        if request.method == 'POST':
            address = Address(
                user=request.user,
                firstname=request.POST['firstname'],
                lastname=request.POST['lastname'],
                phone=request.POST['phone'],
                email=request.POST['email'],
                address_line_1=request.POST['address_line_1'],
                address_line_2=request.POST.get('address_line_2', ''),
                # phone=request.POST['phone'],
                city=request.POST['city'],
                state=request.POST['state'],
                pincode=request.POST['pincode']
            )
            address.save()
            address_id = address.id
            if id == 0:
                messages.success(request,"Address added successfully")
                return redirect('checkout')
            else:
                messages.success(request,"Address added successfully")
                return redirect(address_book)
        else:
            context = {
                'state': state,
                'city': city,
            }

    # pass the address_id to the template
    # context['address_id'] = id
    
    return render(request, 'add_address.html',context)



@never_cache
@login_required(login_url='login')
def edit_address(request, address_id):
    state = ['Kerala', 'AndraPradesh', 'Karnataka', 'Tamilnadu']
    city = ['Kannur','Kozhikkode','Ernakulam','Thiruvananthapuram','Banglore','Hubli','Hydrabad','Coimbator','Madurai']
    newaddress = Address.objects.get(id= address_id)
    print(newaddress)
    if request.method == 'POST':
        newaddress.firstname=request.POST['firstname']
        newaddress.lastname=request.POST['lastname']
        newaddress.email=request.POST['email']
        newaddress.address_line_1=request.POST['address_line_1']
        newaddress.address_line_2=request.POST.get('address_line_2', '')
        newaddress.phone=request.POST['phone']
        newaddress.city=request.POST['city']
        newaddress.state=request.POST['state']
        newaddress.pincode=request.POST['pincode']
        newaddress.save()
        messages.success(request,"Your Address successfully edited")
        return redirect(address_book)
    
    context = {
        'state': state,
        'city' : city,
        'newaddress' : newaddress
    }

    return render(request, 'edit_address.html',context)



@never_cache
@login_required(login_url='login')
def delete_address(request, address_id):
    address = Address.objects.get(id=address_id)
    address.delete()
    messages.info(request, 'Address deleted successfully')
    return redirect(address_book)



# user order details
@never_cache
@login_required(login_url='login')
def user_total_orderview(request):
    orders=Order.objects.filter(user=request.user).order_by('-id')
    paginator = Paginator(orders, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context ={
        'orders':orders,
        'page_obj':page_obj,
    }
    return render(request, 'usertotalorderview.html',context)



@never_cache
@login_required(login_url='login')
def user_single_orderview(request,id):
    order =Order.objects.filter(id=id,user=request.user).first()
    orderitems = OrderProduct.objects.filter(order=order)
    # test = Order.objects.get(id=id, status='Cancelled')
    # if request.method == 'POST':
    #     order_id = request.POST.get('order_id')
    #     if order_id:
    #         order_to_cancel = Order.objects.get(id=order_id)
    #         if order_to_cancel.status != 'Cancelled' and order_to_cancel.status != 'Delivered' and order_to_cancel.status != 'Returned':
    #             order_to_cancel.status = 'Cancelled'
    #             order_to_cancel.save()
    #             messages.success(request, "Order Cancelled")

    #         elif order_to_cancel.status == 'Delivered':
    #             messages.error(request, "This order has already been Delivered.")

    #         elif order_to_cancel.status == 'Returned':
    #             messages.error(request, "This order has already been Returned.")
    #         elif order_to_cancel.status == 'Cancelled':
    #             messages.error(request, "This order has already been Cancelled.")

    #     return redirect('usersingleorderview', order_id)
    context={
        'order': order,
        'orderitems':orderitems,
        # 'test':test,
    }
    return render(request, 'usersingleorder.html', context)



@never_cache
@login_required(login_url='login')
def cancelorder(request,id):
    client = razorpay.Client(auth=(myproject.settings.API_KEY, myproject.settings.RAZORPAY_SECRET_KEY))
    order = Order.objects.get(id=id,user=request.user)
    payment=order.payment
    msg=''
    if (payment.payment_method == 'Paid by Razorpay'):
        payment_id = payment.payment_id
        amount = payment.amount_paid
        amount=amount*100
        print(amount)
        print('ttttttttttttttttttttttttttttttttttt')
        captured_amount = client.payment.capture(payment_id,amount)
        print(captured_amount)

        if captured_amount['status'] == 'captured' :
            refund_data = {
            "payment_id": payment_id,
            "amount": amount,  # amount to be refunded in paise
            "currency": "INR",
         }
        else:
            msg = "Your bank has not completed the payment yet."
         # If the payment is not captured, return an error message and don't attempt a refund
            orderitems = OrderProduct.objects.filter(order=order)
            context={
            'order': order,
            'orderitems':orderitems,
            'msg':msg
         }
            return render(request,'usersingleorder.html',context)
        refund = client.payment.refund(payment_id, refund_data)
        print(refund)
        if refund is not None:
            current_user=request.user
            order.refund_completed = True
            order.status = 'Cancelled'
            payment = order.payment
            payment.refund_id = refund['id']
            payment.save()
            order.save()
            messages.success(request,"Your order has been successfully cancelled and amount has been refunded!")
            mess=f'Hello\t{current_user.first_name},\nYour order has been canceled,Money will be refunded with in 1 hour\nThanks!'
            send_mail(
                        "EZRA Furnitures - Order Cancelled",
                        mess,
                        settings.EMAIL_HOST_USER,
                        [current_user.username],
                        fail_silently = False
                     )
        else :
            messages.success(request,"Your order is not cancelled because the refund couldnot be  completed now. Please try again later. If the issue continues, CONTACT THE SUPPORT TEAM!")
            pass
    else :
        if(payment.paid):
            order.refund_completed = True
            order.status = 'Cancelled'
            messages.success(request,"YOUR ORDER HAS BEEN SUCCESSFULLY CANCELLED!")
            order.save()
        else:
            order.status = 'Cancelled'
            order.save()
            msg ="Your payment has not been recieved yet. But the order has been cancelled.!"
    orderitems = OrderProduct.objects.filter(order=order)
    context={
        'order': order,
        'orderitems':orderitems,
        'msg':msg
    }
    return render(request,'usersingleorder.html',context)


def search(request):
    keyword = request.GET.get('keyword')
    print(keyword)
    products = Product.objects.filter(Q(description__icontains=keyword) | Q(name__icontains=keyword)).order_by('created')
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    allcategory = Category.objects.all() 
    varient = ProductVarient.objects.all()
    context = {
        'product': products,
        'keyword' : keyword,
        'allcategory' : allcategory,
        'page_obj': page_obj,
        'varient':varient,
        
        
    }
    return render(request, 'user_product.html', context)



@never_cache
@login_required(login_url='login')
def return_order(request,id):
    order = Order.objects.get(id=id, user=request.user)
    print(order,'return order')
    userwallet = Wallet.objects.get(user=request.user)
    if order.payment.payment_method == 'COD':
        print('if in return order')
        print(order.paid_amount)
        userwallet.balance = userwallet.balance+order.paid_amount
        print(userwallet.balance)
        order.is_returned = True
    order.status = 'Returned'
    order.save()
    userwallet.save()
   

    orderitems = OrderProduct.objects.filter(order=order)
    context={
        'order': order,
        'orderitems':orderitems,
    }
    return render(request,'usersingleorder.html',context)


#custom 404 page

def error_404(request):
    return render(request, '404.html')






