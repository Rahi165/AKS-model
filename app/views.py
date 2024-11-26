from django.shortcuts import render, redirect
from django.views import View
from .models import (Product,OrderPlaced,Customer,Cart)
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class ProductView(View):
    def get(self, request):
        totalitems = 0
        topwears = Product.objects.filter(category = 'TW')
        bottomwears = Product.objects.filter(category = 'BW')
        mobiles = Product.objects.filter(category = 'M')
        laptops = Product.objects.filter(category = 'L')
        totalitems = len(Cart.objects.filter(user=request.user))
        return render(request,'app/home.html', {
            'tp':topwears,
            'mobiles':mobiles, 
            'bottomwears':bottomwears,
            'laptops': laptops,
            'totalitems':totalitems,
            })

class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        item_already_in_cart = Cart.objects.filter(Q(product=product.id)&Q(user=request.user)).exists()
        return render(request,'app/productdetail.html',{'product':product,'item_already_in_cart':item_already_in_cart})

def add_to_cart(request):
    user = request.user
    prod_id = request.GET.get('prod_id')
    product = Product.objects.get(id=prod_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')

def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 80.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity*p.product.discounted_price)
                amount += tempamount
                total_amount = amount+shipping_amount
            return render(request, 'app/addtocart.html',{'cart':cart,'tamount' : total_amount,'amount' : amount})
        else:
            return render(request,'app/emptycart.html')
        
def plus_cart(request):
    if request.method == 'GET':
            prod_id = request.GET.get('prod_id')
       
            c = Cart.objects.get(Q(product_id=prod_id) & Q(user=request.user))  
            c.quantity += 1
            c.save()

            amount = 0.0
            shipping_amount = 80.0
            cart_products = Cart.objects.filter(user=request.user)

            for p in cart_products:
                temp_amount = (p.quantity * p.product.discounted_price) 
                amount += temp_amount
            
            total_amount = amount + shipping_amount
            
            data = {
                "quantity": c.quantity,
                "amount": amount,
                "tamount": total_amount
            }
            return JsonResponse(data)
        
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        c = Cart.objects.get(Q(product_id=prod_id) & Q(user=request.user))  
        quantity = c.quantity  # Store the quantity before deleting
        c.delete()
        amount = 0.0
        shipping_amount = 80.0
        cart_products = Cart.objects.filter(user=request.user)

        for p in cart_products:
            temp_amount = (p.quantity * p.product.discounted_price) 
            amount += temp_amount
            
        total_amount = amount + shipping_amount
            
        data = {
            "quantity": quantity,  # Return the quantity removed
            "amount": amount,
            "tamount": total_amount
        }
        return JsonResponse(data)
   
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
            
        c = Cart.objects.get(Q(product_id=prod_id) & Q(user=request.user))  
        c.quantity -= 1
        c.save()

        amount = 0.0
        shipping_amount = 80.0
        cart_products = Cart.objects.filter(user=request.user)

        for p in cart_products:
            temp_amount = (p.quantity * p.product.discounted_price) 
            amount += temp_amount
        
        total_amount = amount + shipping_amount
        
        data = {
            "quantity": c.quantity,
            "amount": amount,
            "tamount": total_amount
        }
        return JsonResponse(data)

def buy_now(request):
 return render(request, 'app/buynow.html')


def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})

def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    
    return render(request, 'app/orders.html',{'op':op,})

def change_password(request):
 return render(request, 'app/changepassword.html')

def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data:
        try:
            price_limit = int(data)
            if price_limit <= 10000:
                mobiles = Product.objects.filter(discounted_price__lt=10000,category='M')
            elif price_limit >= 10000:
                mobiles = Product.objects.filter(discounted_price__gt=10000,category='M')
        except ValueError:
            mobiles = Product.objects.filter(brand=data, category='M')

    return render(request, 'app/mobile.html',{'mobiles':mobiles})


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html',{'form':form})
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Registration successful')
            form.save()
        return redirect('login')
    

def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_item = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 80.0
    cart_product = Cart.objects.filter(user=request.user)
    if cart_product:
        for p in cart_product:
            temp_amount = (p.quantity * p.product.discounted_price) 
            amount += temp_amount   
            total_amount = amount + shipping_amount
        return render(request, 'app/checkout.html',{'add':add,'totalamount':total_amount,'cart_item':cart_item})


def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    try:
        customer = Customer.objects.get(id=custid)
    except Customer.DoesNotExist:
        return redirect('some_error_page')  

    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request,'app/profile.html', {'form': form,'active' : 'btn-primary'})
    
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=user,name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            return render(request,'app/profile.html',{'form': form,'active' : 'btn-primary'})
            

