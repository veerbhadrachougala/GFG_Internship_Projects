from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views import View
from .models import Product, Cart, Customer, Orderedplaced, Coupon
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.models import User
from decimal import Decimal
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from xhtml2pdf import pisa

# -------------All Product Lists-----------------#

def productList(request):
    products_man = Product.objects.filter(category='man')
    products_women = Product.objects.filter(category='women')
    products_kids = Product.objects.filter(category='kids')
    products_electronics = Product.objects.filter(category='electronics')
    
    context = {
        'products_man': products_man,
        'products_women': products_women,
        'products_kids': products_kids,
        'products_electronics': products_electronics,
        # 'products_mobiles': products_mobiles,
    }
    return render(request, 'index.html', context)


# -------------User Loginr-----------------#

def Login(request):
    if request.method == "POST":
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        user = authenticate(request,username = phone, password = password)
        if user is not None:
            login(request,user)
            return redirect('Home')
        else:
            return HttpResponse("mobile number & password is incorrect!!!")
        
    return render(request,'login.html')


# -------------User Register-----------------#

def Register(request):
    if request.method == "POST":
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')

        if confirmpassword != password:
            return HttpResponse("Your Password and Confirm Password are not matching")
        else:
            existing_user = User.objects.filter(username=phone).first()
            if existing_user:
                return redirect('login')

            new_user = User.objects.create_user(phone, email, password)
            new_user.save()

            my_user = Customer.objects.create(User=new_user, phone=phone, email=email)
            my_user.save()

            return redirect('login')

    return render(request, 'register.html')

# -------------user Logout function-----------------#

def Log_out(request):
    logout(request)
    return redirect('Home')

# -------------Product Detail view -----------------#

class ProductDetailsView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        item_already_in_cart = Cart.objects.filter(product=product, user=request.user).exists()

        context = {
            'products': product,
            'item_already_in_cart':item_already_in_cart
        }
        return render(request, 'product-details.html',context)
  

# -------------User Adding the items to cart-----------------#

def addToCart(request):
    if request.method == 'GET':
        product_id = request.GET.get('product_id')
        product_instance = Product.objects.get(pk=product_id)

        if request.user.is_authenticated:
            user = request.user

            existing_cart_item = Cart.objects.filter(user=user, product=product_instance).first()

            if existing_cart_item:
                existing_cart_item.quantity += 1
                existing_cart_item.save()
            else:
                new_cart_item = Cart(user=user, product=product_instance)
                new_cart_item.save()

        return redirect('cart')


# -------------Cart item functions-----------------#

def cart(request):
    if request.user.is_authenticated:
        user = request.user
        user_cart = Cart.objects.filter(user=user)
        amount = Decimal('0.0')
        delivery_charge = Decimal('00.0')
        total_amount = Decimal('0.0')  
        discount = Decimal('0.0')
        cart_products = [cart_item for cart_item in user_cart]
        if cart_products:
            for cart_item in cart_products:
                temp_amount = cart_item.quantity * cart_item.product.price
                amount += temp_amount

            if amount < 1000:
                delivery_charge = Decimal('50.0')
            elif amount >= 1000:
                delivery_charge = Decimal('0.0')

            total_amount = amount + delivery_charge
            if total_amount >= 2000:
                discount = total_amount * Decimal('0.2') # 20% == (0.2)
                total_amount -= discount
        context = {
            'carts': user_cart,
            'Totalamount': total_amount,
             'Amount': amount,
             'delivery_charge': delivery_charge,
             'Discount': discount
        }
        return render(request, 'cart.html', context)
    else:
        return redirect('login')
  

# -----------Total quantity of the cart to display on the base.html cart icon------------#

def cartTotalQuantity(request):
    if request.user.is_authenticated:
        user = request.user
        cart_quantity = Cart.objects.filter(user=user).count()
        return JsonResponse({'cart_quantity': cart_quantity})
    else:
        return JsonResponse({'cart_quantity': 0})


# -------------To increase the item quantity in cart -----------------#

def plusCart(request,product_id):
    # if request.method == 'POST':
    #     product_id = request.POST.get('product_id')
        print(product_id)
        try:
            cart_item = Cart.objects.get(product_id=product_id, user=request.user)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Cart item not found'})

        cart_item.quantity += 1
        cart_item.save()

        amount = Decimal('0.0')  
        delivery_charge = Decimal('70.0')
        total_amount = Decimal('0.0')  

        cart_products = Cart.objects.filter(user=request.user)
        for p in cart_products:
            temp_amount = p.quantity * p.product.price
            amount += Decimal(temp_amount)  

        if amount < 1000:
            delivery_charge = Decimal('50.0')
        elif amount >= 1000:
            delivery_charge = Decimal('0.0')

        total_amount = amount + delivery_charge
        if total_amount >= 2000:
            discount = total_amount * Decimal('0.2') # 20% == (0.2)
            total_amount -= discount

        data = {
            'amount': amount,
            'delivery_charge': delivery_charge,
            'Discount':discount,
            'totalamount': total_amount,
            'carts': cart_products
        }

        return render(request, 'cart.html', data)
    

# -------------To decrease the item quantity in cart -----------------#

def minusCart(request, product_id):
    # if request.method == 'POST':
    #     product_id = request.POST.get('product_id')
        print(product_id)
        c = Cart.objects.get(Q(product=product_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()

        amount = Decimal('0.0') 
        delivery_charge = Decimal('0.0') 
        total_amount = Decimal('0.0') 

        cart_products = Cart.objects.filter(user=request.user)
        for p in cart_products:
            temp_amount = p.quantity * p.product.price
            amount += Decimal(temp_amount)  

        if amount < 1000:
            delivery_charge = Decimal('50.0')
        elif amount >= 1000:
            delivery_charge = Decimal('0.0')

        total_amount = amount + delivery_charge
        if total_amount >= 2000:
            discount = total_amount * Decimal('0.2') # 20% == (0.2)
            total_amount -= discount

        data = {
            'amount': amount,
            'delivery_charge': delivery_charge,
            'Discount':discount,
            'totalamount': total_amount,
            'carts': cart_products
        }

        return render(request, 'cart.html', data)


# -------------To Remove the particular item in cart -----------------#

def removeCart(request, product_id):
    # if request.method == 'POST':
    #     product_id = request.POST.get('product_id') 
        c = Cart.objects.get(Q(product=product_id) & Q(user=request.user))
        c.delete()

        amount = Decimal('0.0')  
        delivery_charge = Decimal('0.0')  
        total_amount = Decimal('0.0')  

        cart_products = Cart.objects.filter(user=request.user)
        for p in cart_products:
            temp_amount = p.quantity * p.product.price
            amount += Decimal(temp_amount)  

        if amount < 1000:
            delivery_charge = Decimal('50.0')
        elif amount >= 1000:
            delivery_charge = Decimal('0.0')

        total_amount = amount + delivery_charge

        if total_amount >= 2000:
            discount = total_amount * Decimal('0.2') # 20% == (0.2)
            total_amount -= discount

        data = {
            'amount': amount,
            'delivery_charge': delivery_charge,
            'Discount':discount,
            'totalamount': total_amount,
            'carts': cart_products
        }
        return render(request, 'cart.html', data)


# -------------Checkout Page to place the order || Getting the data from the checkout form storing that data into ordrePlaced model -----------------#

@csrf_exempt
def apply_coupon(request):
    if request.method == 'POST':
        # user = request.user
        coupon_code = request.POST.get("coupon_code")
        print(coupon_code)

        amount = Decimal('0.0')
        delivery_charge = Decimal('0.0')
        total_amount = Decimal('0.0')
        discount = Decimal('0.0')

        cart_items = Cart.objects.filter(user=request.user) 
        for cp in cart_items:
            temp_amount = (cp.quantity * cp.product.price)
            amount += Decimal(temp_amount)      

        if amount < 1000:
            delivery_charge = Decimal('50.0')   
        else:
            delivery_charge = Decimal('0.0')

        total_amount = amount + delivery_charge

        if total_amount >= 2000:
            discount = total_amount * Decimal('0.2')
            print(discount,'discvbbnnmm')
            total_amount -= discount
            print(total_amount)

        coupon = Coupon.objects.get(code=coupon_code)
        print(coupon)
        # if coupon == coupon_code:
        discount += coupon.discount_price
        print('coupon discount + --------',discount)
        total_amount = amount - discount
        print('coupon---------------',total_amount)
        # if coupon_code:
        #     try:
        #         coupon = Coupon.objects.get(code=coupon_code)
        #         if coupon.is_valid():
        #             discount = discount + coupon.discount_price
        #             total_amount = amount - discount
        #     except ObjectDoesNotExist:
        #         pass
        print(amount)
        print(delivery_charge)
        print(discount)
        print(total_amount)
        # Prepare the response data
        response_data = {
            'sub_total': amount,
            'delivery_charge': delivery_charge,
            'discount': discount,
            'total': total_amount,
        }
        return JsonResponse(response_data)


@login_required(login_url='login')
def checkout(request):
    user = request.user

    amount = Decimal('0.0')
    delivery_charge = Decimal('0.0')
    total_amount = Decimal('0.0')
    discount = Decimal('0.0')

    cart_items = user.cart_set.all()
    for cp in cart_items:
        temp_amount = (cp.quantity * cp.product.price)
        amount += Decimal(temp_amount)      

    if amount < 1000:
        delivery_charge = Decimal('50.0')   
    else:
        delivery_charge = Decimal('0.0')

    total_amount = amount + delivery_charge


    if total_amount >= 2000:
        discount = total_amount * Decimal('0.2')
        total_amount -= discount

    context = {
        'Amount': amount,
        'Totalamount': total_amount,
        'Cartitems': cart_items,
        'Discount': discount,
        'delivery_charge': delivery_charge
    }

    if cart_items and request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        state_name = request.POST.get('state')
        district = request.POST.get('district')
        city = request.POST.get('city')
        address = request.POST.get('address')
        pin = request.POST.get('pin')

        amount = int('0')
        delivery_charge = int('0')

        for cart_item in cart_items:
            temp_amount = (cart_item.quantity * cart_item.product.price)
            amount += int(temp_amount)

            if amount < 1000:
                delivery_charge = int('50')
                amount = amount + delivery_charge
            else:
                delivery_charge = int('0')

            total_amount = amount + delivery_charge


            if total_amount >= 2000:
                discount = amount * Decimal('0.2') # 20% == (0.2)
                amount = amount - int(discount)

            # Saving the order
            Orderedplaced.objects.create(
                User=user,
                product=cart_item.product,
                customerName=name,
                email=email,
                phone=phone,
                state=state_name,
                district=district,
                city=city,
                address=address,
                pin=pin,
                quantity=cart_item.quantity,
                amount=amount
            )

        # Delete cart
        cart_items.delete()
        return redirect('myOrders')

    return render(request, 'checkout.html', context)



# -------------Orders page to show the all ordered items for particular user -----------------#

def orders(request):
    myOrders = Orderedplaced.objects.filter(User=request.user)
    return render(request, 'myOrders.html',{'myOrders':myOrders})


# -------------Search function to search the items -----------------#

def search_view(request):
    search = request.GET.get('search')
    results = None

    if search:
        results = Product.objects.filter( Q(name__icontains = search) |  Q(category__icontains = search) ) # Search by product name or category 


    context = {
        'search': search,
        'results': results,
    }

    return render(request, 'search.html', context)


def cancel_order(request, order_id):
    try:
        order = Orderedplaced.objects.get(pk=order_id)

        if order.status != 'Delivered':
            order.status = 'Canceled'
            order.save()

    except Orderedplaced.DoesNotExist:
        print("There is no ---Orderedplaced--- model or table in ur database...")

    return redirect('myOrders')            


def render_to_pdf(template_path, context_dict):
    template = render(None, template_path, context_dict)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Invoice.pdf"'

    # Creating PDF
    pisa_status = pisa.CreatePDF(
        template.getvalue(),
        dest=response
    )

    if pisa_status.err:
        return HttpResponse('We had some errors with code %s <pre>%s</pre>' % (pisa_status.err, html))

    return response

def generate_pdf(request):
    # Define your template path and context data
    template_path = 'Invoice.html'
    context = {
        # Add your context data here if needed
    }
    # Generate and return the PDF response
    return render_to_pdf(template_path, context)
    


















