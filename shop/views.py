from django.shortcuts import render ,redirect, get_object_or_404
from .models import CartItem, wishlist, Coupon, UserCoupon, Order, OrderProduct,Payment
from userhome.models import Address
from adminhome.models import Product, ProductVarient
from django.contrib import messages
from userhome.views import user_login
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
import datetime
import random

from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
# from django.db.models import Q

from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required




# view cart of without looged in users
def viewcart(request):
    current_user = request.user

    if current_user.is_authenticated:
        items = CartItem.objects.filter(user_id=current_user.id).order_by('id')
        cart_items = []
        for cart_item in items:
            product = get_object_or_404(Product, id=cart_item.product_id)
            varient = ProductVarient.objects.get(id=cart_item.provar_id)
            quantity = cart_item.quantity
            price = product.price * quantity
            cart_items.append({'product': product, 'quantity': quantity,'varient':varient ,'price': price})
    else:
        cart = request.session.get('cart', {})
        print('im in cart')
        print(cart)
        cart_items = []
        for item_id, item_data in cart.items():
            product_id, varient_id = item_id.split('-')  # Split the item_id to get the product_id and variant_id
            if not varient_id:
                print('viewcart')
            print(product_id)
            print(varient_id)
            product = get_object_or_404(Product, id=product_id)
            if varient_id:
                varient = ProductVarient.objects.get(id=varient_id)
            else:
                varient = ProductVarient.objects.filter(proname=product).first()
            quantity = item_data['quantity']
            price = product.price * quantity
            cart_items.append({'product': product, 'quantity': quantity, 'varient': varient, 'price': price})

    total = sum(item['price'] for item in cart_items)
    context = {'cart_items': cart_items, 'total': total}

    return render(request, 'shop/viewcart.html', context)

    




# add to cart without logged in using session

def addtocart(request, varient_id):
    if request.user.is_authenticated:
        current_user = request.user
    else:
        current_user = None

    quantity = request.POST.get('quantity')
    if quantity is None:
        product_quantity = 1
    else:
        product_quantity= int(quantity)
    if request.method == 'POST':
        varient_id = request.POST.get('varient_id')
        varient = ProductVarient.objects.get(id=varient_id)
        
    else:
        varient = ProductVarient.objects.get(id=varient_id)
        
    product = varient.proname.name
    print(product,'----------product in add cart---------')
    product_id = varient.proname.id

    if current_user:
        item_exists = CartItem.objects.filter(user_id=current_user.id,product_id=product_id,provar_id=varient.id).exists()
        if (item_exists):
            item=CartItem.objects.get(product_id=product_id,user_id=current_user.id,provar_id=varient.id)
            quantity_expected=item.quantity + product_quantity
            if varient.varstock>quantity_expected:

                item.quantity = item.quantity + product_quantity
                item.save()
                messages.success(request,  f"{product} are added to Cart.")
            else:

                item.quantity = varient.varstock
                item.save()
                messages.info(request,  f"{varient.varstock} items left. All of them are added to Cart.")
        else:
            if(varient.varstock>=product_quantity):
                item = CartItem.objects.create(user_id=current_user.id, product_id=product_id,provar_id=varient.id,quantity=product_quantity)
                messages.success(request, f"{product} added to cart!")
            else:
                product_quantity = varient.varstock
                item = CartItem.objects.create(user_id=current_user.id, product_id=product_id,provar_id=varient.id,quantity=product_quantity)
                messages.info(request,  f"{varient.varstock} items left. All of them are added to Cart.")
    else:
        cart = request.session.get('cart', {})
        item_id = str(product_id)  # Use product ID only
        if varient_id:
            item_id += f"-{varient_id}"  # Add variant ID if it exists
        else:
            varient_id = varient.id
            print('varient kitty')
            print(varient_id)
            item_id += f"-{varient_id}"  # Add variant ID if it exists
        print('im in else of varient id')
        print('addcart')
        print(item_id)
        if item_id in cart:
            quantity_expected = cart[item_id]['quantity'] + product_quantity
            if varient.varstock > quantity_expected:
                cart[item_id]['quantity'] += product_quantity
                messages.success(request, f"{product} added to cart!")
            else:
                cart[item_id]['quantity'] = varient.varstock
                messages.info(request,  f"{varient.varstock} items left. All of them are added to Cart.")
        else:
            if varient.varstock >= product_quantity:
                cart[item_id] = {'quantity': product_quantity, 'varient_id': varient_id}
                messages.success(request, f"{product} added to cart!")
            else:
                product_quantity = varient.varstock
                cart[item_id] = {'quantity': product_quantity, 'varient_id': varient_id}
                messages.info(request,  f"{varient.varstock} items left. All of them are added to Cart.")
        request.session['cart'] = cart

    return redirect(viewcart)


#working addcartitem
def addcartitem(request,product_id,varient_id):
    product = get_object_or_404(Product, id=product_id)
    varient= get_object_or_404(ProductVarient, id=varient_id)
    if request.user.is_authenticated:
        current_user=request.user
        item=CartItem.objects.get(user_id=current_user.id, product=product,provar=varient)
        item.quantity = item.quantity + 1
        if (varient.varstock>item.quantity):
            item.save()
        else:
            messages.warning(request,"Product Out Of Stock...! Can't be added to cart")

           
            
    else:
        cart = request.session.get('cart', {})
        item_id = f"{product.id}-{varient_id}"
        cart[item_id]['quantity'] += 1
        if (varient.varstock>cart[item_id]['quantity']):
            request.session['cart'] = cart
           
        else:
            messages.warning(request,"Product Out Of Stock...! Can't be added to cart")

    return redirect(viewcart)


#for checking ajax
# def addcartitem(request):
#     if request.method == 'POST':
#         if request.user.is_authenticated:
#             current_user=request.user
#             prod_id  = request.POST.get('product_id')
#             var_id = request.POST.get('varient_id')
#             product = Product.objects.get(id=prod_id)
#             varient= ProductVarient.objects.get(id=var_id)
#             item=CartItem.objects.get(user_id=current_user.id, product=product,provar=varient)
#             item.quantity = int(request.POST.get('product_qty'))
#             if (varient.varstock>item.quantity):
#                 item.save()
#                 return JsonResponse({'status':"Updated successfully"})
#             else:
#                 return JsonResponse({'status':"Product Out Of Stock...! Can't be added to cart"})
            
#         else:
#             return JsonResponse({'status':"Please log in to continue"})
        




def removecartitem(request,product_id,varient_id):
    product = get_object_or_404(Product, id=product_id)
    varient= get_object_or_404(ProductVarient, id=varient_id)
    if request.user.is_authenticated:
        current_user = request.user
        cart_item = CartItem.objects.get(user_id=current_user.id, product=product,provar=varient)
        print(cart_item)
        if cart_item.quantity == 1:
            cart_item.delete()  # remove the item from the cart if the quantity is 1
        else:
            cart_item.quantity -= 1
            cart_item.save()  # decrement the quantity by 1
        return redirect(viewcart)
    else:
        cart = request.session.get('cart', {})
        item_id = f"{product_id}-{varient_id}"
        if cart[item_id]['quantity'] == 1:
            del cart[item_id]
        else:
            cart[item_id]['quantity'] -= 1

        request.session['cart'] = cart   
        return redirect(viewcart)


def removecartproduct(request, product_id, varient_id):
    current_user = request.user
    product = get_object_or_404(Product, id=product_id)
    varient = get_object_or_404(ProductVarient, id=varient_id)
    cart_item = CartItem.objects.filter(user_id=current_user.id, product_id=product.id, provar=varient).first()
    if cart_item:
        cart_item.delete()
    else:
        if 'cart' in request.session:
            cart = request.session['cart']
            item_key = f'{product.id}-{varient.id}'
            if item_key in cart:
                del cart[item_key]
                request.session['cart'] = cart
    messages.success(request, "Item has been removed from your cart.")
    return redirect(viewcart)




@never_cache
@login_required(login_url='login')
def userwishlist(request):
    user = request.user
    witems=wishlist.objects.filter(user_id=user.id)
    context={
        'witems':witems,
    }
    return render(request,'shop/wishlist.html',context)

@never_cache
@login_required(login_url='login')
def add_to_wishlist(request,varient_id):
    if request.user.is_authenticated:
        product = ProductVarient.objects.get(id=varient_id)
        
        user = request.user
        if wishlist.objects.filter(provar=product,user_id=user.id).exists():
            messages.info(request, "Product already exist in wishlist")
            return redirect(userwishlist)
            
        else:
            wishlist.objects.create(provar=product,user_id=user.id)
            messages.success(request,"Product added to wishlist")
            return redirect(userwishlist)
            
    else:
        messages.warning(request, "Please log in to add items to wishlist.")
        return redirect(user_login)

@never_cache
@login_required(login_url='login')
def remove_from_wishlist(request,varient_id):
    user = request.user
    wishItem=wishlist.objects.get(provar_id=varient_id,user_id=user.id)
    wishItem.delete()
    return redirect(userwishlist)


def checkout(request, address_id=None):
    if request.user.is_authenticated:
        subtotal=0
        quantity=0
        amountToBePaid =0
        msg=''
        cart_items=None
        coupon_discount = 0
        coupon_code = ''
        discount = False
        coupon = ''
        if address_id:
            addresses = Address.objects.filter(id=address_id, user_id=request.user)
        else:
            addresses = Address.objects.filter(user_id=request.user)
        # selected_address = addresses.first() if selected_address else None
        user=User.objects.get(id=request.user.id)
        cart_items=CartItem.objects.filter(user=user, provar__varstock__gt=0)
        for cart_item in cart_items:
            subtotal+=(cart_item.product.price*cart_item.quantity)
            quantity+=cart_item.quantity
        grand_total = subtotal+70
        amountToBePaid = grand_total
        if ('couponCode' in request.POST):
            coupon_code = request.POST.get('couponCode')
            try:
                coupon = Coupon.objects.get(code = coupon_code)
                grand_total = request.POST['grand_total']
                coupon_discount = 0
                if (coupon.active):
                    try:
                        instance = UserCoupon.objects.get(user=request.user, coupon=coupon)
                    except ObjectDoesNotExist:
                        instance = None
                    # instance = UserCoupon.objects.get(user = request.user ,coupon = coupon)
                    if(instance):
                        pass
                    else:
                        instance = UserCoupon.objects.create(user = request.user ,coupon = coupon)
                    if(not instance.used):
                        if float(grand_total) >= float(instance.coupon.min_value):
                            coupon_discount = ((float(grand_total) * float(instance.coupon.discount))/100)
                            amountToBePaid = float(grand_total) - coupon_discount
                            amountToBePaid = format(amountToBePaid, '.2f')
                            coupon_discount = format(coupon_discount, '.2f')
                            messages.info(request, 'Coupon Applied successfully')
                            discount=True
                        else:
                            messages.info(request,'This coupon is only applicable for orders more than ₹'+ str(instance.coupon.min_value)+ '\- only!')
                    else:
                        messages.info(request,'Coupon is already used')
                else:
                    messages.info(request, "Coupon is not Active!")
            except:
                messages.info(request,"Invalid Coupon Code!")
        else:
            try:
                instance = UserCoupon.objects.get(user=request.user, used= False)
                instance.delete()
            except ObjectDoesNotExist:
                instance = None

    else:
        messages.warning(request, "Please log in for payments.")
        return redirect(user_login)
    # except ObjectDoesNotExist:
    #     pass

    context={
        'subtotal':subtotal,
        'quantity':quantity,
        'cart_items':cart_items,
        'grand_total':grand_total,
        'user':user,
        'amountToBePaid':amountToBePaid,
        'msg':msg,
        'coupon':coupon,
        'coupon_discount':coupon_discount,
        'discount':discount,
        'AllAddress':addresses,
        # 'selected_address':selected_address
    }


    return render(request,'shop/checkout.html',context)




def confirm_order(request):
    if request.method == 'POST':
        try:
            newAddress_id = request.POST.get('selected_addresses')
            if not newAddress_id:
                messages.error(request, "Please add an address to make orders")
                return redirect(checkout)
            else:
                address  = Address.objects.get(id = newAddress_id)
            subtotal = request.POST.get('subtotal')
            grand_total = request.POST.get('grand_total')
            amountToBePaid = request.POST.get('amountToBePaid')
            coupon_discount = request.POST.get('coupon_discount')
            couponCode =  request.POST.get('couponCode')
            payment_method = request.POST.get('payment_method')


            
            cartitems=CartItem.objects.filter(user=request.user,  provar__varstock__gt=0)
            cart_items = []
            for items in cartitems :
                varient = ProductVarient.objects.get(id=items.provar.id)
                print(varient)
                product = get_object_or_404(Product, id=items.product_id)
                quantity = items.quantity
                price = product.price * quantity
                cart_items.append({'product': product, 'quantity': quantity,'varient':varient, 'price': price})

        except ObjectDoesNotExist:
            pass
    
    
        context={
            'addressSelected':address,
            'subtotal':subtotal,
            'grand_total':grand_total,
            'amountToBePaid':amountToBePaid,
            'coupon_discount':coupon_discount,
            'payment_method':payment_method,
            'cart_items':cart_items,
            'couponCode':couponCode,
            # 'cartitems':cartitems,
        }
    return render(request, 'shop/orderconfirmation.html',context)






def sendmails(request):
    user = User.objects.all()
    for user in user:
        if user.is_superuser:
            pass
        else:
            cart_item = CartItem.objects.filter(user=user)
            if cart_item:
                # Send email to user email
                subject = 'from ezra furnitures'
                message = 'products are going to finish.purchase fast to get discounts'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [user.username,]
                send_mail(subject, message, email_from, recipient_list)
    return render(request, 'shop/viewcart.html')





def calculateCartTotal(request):
   cart_items   = CartItem.objects.filter(user=request.user, provar__varstock__gt=0)
   if not cart_items:
       pass
    #   return redirect('product_management:productlist',0)
   else:
      total = 0
      tax=0
      grand_total=0
      for cart_item in cart_items:
         total  += (cart_item.product.price * cart_item.quantity)
         tax = 70
         grand_total = tax + total
   return total, tax, grand_total


def placeOrder(request):
    if request.method =='POST':
        if ('couponCode' in request.POST):
           instance = checkCoupon(request)
        cart_items   = CartItem.objects.filter(user=request.user,  provar__varstock__gt=0)
        if not cart_items:
           return redirect('userproduct',0)
        newAddress_id = request.POST.get('addressSelected')
        address  = Address.objects.get(id = newAddress_id)
        newOrder =Order()
        newOrder.user=request.user
        newOrder.address = address
        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        mt = int(datetime.date.today().strftime('%m'))
        d = datetime.date(yr,mt,dt)
        current_date = d.strftime("%Y%m%d")
        rand = str(random.randint(1111111,9999999))
        order_number = current_date + rand
        newPayment = Payment()
        if('payment_id' in request.POST ):
           newPayment.payment_id = request.POST.get('payment_id')
           newPayment.paid = True
        else:
           newPayment.payment_id = order_number
           payment_id  =order_number
        newPayment.payment_method = request.POST.get('payment_method')
        newPayment.customer = request.user
        newPayment.save()
        newOrder.payment = newPayment
        total, tax, grand_total = calculateCartTotal(request)
        newOrder.order_total = grand_total
        if(instance):
           if(instance.used == False):
               if float(grand_total) >= float(instance.coupon.min_value):
                   coupon_discount = ((float(grand_total) * float(instance.coupon.discount))/100)
                   print(coupon_discount)
                   amountToBePaid = float(grand_total) - coupon_discount
                   amountToBePaid = format(amountToBePaid, '.2f')
                   coupon_discount = format(coupon_discount, '.2f')
                   newOrder.order_discount = coupon_discount
                   newOrder.paid_amount = amountToBePaid
                   instance.used = True
                   newOrder.paid_amount = amountToBePaid
                   newPayment.amount_paid = amountToBePaid
                   instance.save()
               else:
                   msg='This coupon is only applicable for orders more than ₹'+ str(instance.coupon.min_value)+ '\- only!'
           else:
               newOrder.paid_amount = grand_total
               newPayment.amount_paid = grand_total
               newOrder.discount=0
               msg = 'Coupon is not valid'
        else:
           newOrder.paid_amount = grand_total
           newPayment.amount_paid = grand_total
           msg = 'Coupon not Added'
        newPayment.save()
        newOrder.payment = newPayment
        order_number = 'EZRA'+ order_number
        newOrder.order_number =order_number
     #to making order number unique
        while Order.objects.filter(order_number=order_number) is None:
           order_number = 'EZRA'+order_number
        newOrder.tax=tax
        newOrder.save()
        newPayment.order_id = newOrder.id
        newPayment.save()
        newOrderItems = CartItem.objects.filter(user=request.user, provar__varstock__gt=0)
        for item in newOrderItems:
            OrderProduct.objects.create(
               order = newOrder,
               customer=request.user,
               varient = item.provar,
               product=item.product,
               product_price=item.product.price,
               quantity=item.quantity
           )
            product_varient = item.provar
            product_varient.varstock -= item.quantity
            product_varient.save()
        
            
            # #TO DECRESE THE QUANTITY OF PRODUCT FROM CART
            # orderproduct = Product.objects.filter(id=item.product_id).first()
            # if(orderproduct.stock<=0):
            #    messages.warning(request,'Sorry, Product out of stock!')
            #    orderproduct.is_available = False
            #    orderproduct.save()
            #    item.delete()
            #    return redirect('order_management:cart')
            # elif(orderproduct.stock < item.quantity):
            #    messages.success(request,  f"{orderproduct.stock} only left in cart.")
            #    return redirect('order_management:cart')
            # else:
            #    orderproduct.stock -=  item.quantity
            # orderproduct.save()
        if(instance):
           instance.order = newOrder
           instance.save()
        # TO CLEAR THE USER'S CART
        cart_item=CartItem.objects.filter(user=request.user, provar__varstock__gt=0)
        cart_item.delete()
        messages.success(request,'Order Placed Successfully')

        payMode =  request.POST.get('payment_method')
        if (payMode == "Paid by Razorpay" ):
           return JsonResponse ({'status':"Your order has been placed successfully"})
        elif (payMode == "COD" ):
           request.session['my_context'] = {'payment_id':payment_id}
           return redirect('ordercomplete')
    return redirect(checkout)


def checkCoupon(request):
   try:
      coupon_code = request.POST['couponCode']
      coupon = Coupon.objects.get(code = coupon_code)
      try:
         instance = UserCoupon.objects.get(user=request.user, coupon=coupon)
      except ObjectDoesNotExist:
         instance = None
         if(instance):
            pass
         else:
            instance = UserCoupon.objects.create(user = request.user ,coupon = coupon)
   except:
      instance = None
   return instance




def razorPayCheck(request):
   total=0
   coupon_discount =0
   amountToBePaid = 0
   current_user=request.user
   cart_items=CartItem.objects.filter(user_id=current_user.id, provar__varstock__gt=0)
   print(cart_items)
   if cart_items:
      for cart_item in cart_items:
         total+=(cart_item.product.price*cart_item.quantity)
      tax=70
      grand_total=total+tax
      grand_total = round(grand_total,2)
      try:
         instance = UserCoupon.objects.get(user=request.user, used=False)
         coupon = instance.coupon.code
         if float(grand_total) >= float(instance.coupon.min_value):
            coupon_discount = ((float(grand_total) * float(instance.coupon.discount))/100)
            amountToBePaid = float(grand_total) - coupon_discount
            amountToBePaid = format(amountToBePaid, '.2f')
            coupon_discount = format(coupon_discount, '.2f')
      except ObjectDoesNotExist:
         instance = None
         amountToBePaid = grand_total
         coupon_discount = 0
         coupon =None
      return JsonResponse({
         'grand_total' : grand_total,
         'coupon': coupon,
         'coupon_discount':coupon_discount,
         'amountToBePaid':amountToBePaid
      })
   else:
      return redirect('userproduct',0)
   

def orderComplete(request):
    product_items = []
    total=0
    if ('payment_id' in request.GET):
      payment_id = request.GET.get('payment_id')
      print(payment_id,'------------------Paymentid---------')
      payment = Payment.objects.get(payment_id=payment_id)

    else:
      try:
         my_context = request.session.get('my_context', {})
         payment_id = my_context['payment_id']
         payment = Payment.objects.get(payment_id=payment_id)
      except:
         user=request.user
         payment = Payment.objects.filter(customer=user, payment_method ='COD').order_by('-created_at').first()

    order_details = Order.objects.get(payment=payment)
    print( order_details)
    orderitems = OrderProduct.objects.filter(order=order_details.id)
    for order_item in orderitems:
            product = Product.objects.get(id=order_item.product.id)
            quantity = order_item.quantity
            price = order_item.product_price * quantity
            total += price
            print(total)
            product_items.append({
                'product': product,
                'quantity': quantity,
                'price': price,
            })
    context={
        'total':total,
        'order': order_details,
        'orderitems':orderitems,
        'product_items': product_items,
    }

    return render(request,'shop/ordersuccess.html',context)


