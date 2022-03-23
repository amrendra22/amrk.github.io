



from urllib.request import Request
from django.shortcuts import render,redirect
from django.views import View

from .models import Customer,Product,Cart,OrdrerPlaced, Slider
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Contact
from datetime import datetime
# from . models import Slider

# def home(request):
#     slider=Slider.objects.all()
#     return render(request, 'app/home.html',{'slider':slider})

class ProductView(View):
    def get(self,request):
        totalitem = 0
        slider= Slider.objects.all().order_by('-id')
        topproducts = Product.objects.filter(category='TP')
        bestproducts = Product.objects.filter(category='BP')
        laptops = Product.objects.filter(category='L')
        mobiles = Product.objects.filter(category='M')
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,'app/home.html',{'slider':slider,'topproducts':topproducts,'bestproducts':bestproducts,'laptops':laptops,'mobiles':mobiles,'totalitem':totalitem,})


# def product_detail(request):
#  return render(request, 'app/productdetail.html')
class ProductDetailView(View):
    def get(self,request,pk):
        totalitem = 0
        product =Product.objects.get(pk=pk)
        item_already_in_cart =False
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            item_already_in_cart =Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request,'app/productdetail.html',{'product':product,'item_already_in_cart':item_already_in_cart,'totalitem':totalitem})

@login_required
def add_to_cart(request):
    
    user =request.user
    product_id =request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')

@login_required
def show_cart(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        user =request.user
        cart = Cart.objects.filter(user=user)
        # print(cart)
        amount = 0.0
        shipping_amount = 60.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        # print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount +=tempamount
                totalamount = amount + shipping_amount
            return render(request,'app/addtocart.html',{'carts':cart,'totalamount':totalamount,'amount':amount,'totalitem':totalitem})
        else:
            return render(request,'app/emptycart.html')

def plus_cart(request):
    if request.method =='GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amount = 60.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount +=tempamount
              
                 
        data ={
            
            
            'quantity':c.quantity,
            'amount' :amount,
            'totalamount':amount + shipping_amount
            }
        return JsonResponse(data)


def minus_cart(request):
    if request.method =='GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping_amount = 60.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount +=tempamount
                
                 
        data ={
            
            
            'quantity':c.quantity,
            'amount' :amount,
            'totalamount':amount + shipping_amount
            }
        return JsonResponse(data)


def remove_cart(request):
    if request.method =='GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        
        c.delete()
        amount = 0.0
        shipping_amount = 60.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                
                 
        data ={
            
            
            
            'amount' :amount,
            'totalamount':amount + shipping_amount
            }
        return JsonResponse(data)






        
def buy_now(request):
 return render(request, 'app/buynow.html')

# def profile(request):
#  return render(request, 'app/profile.html')
@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request,'app/address.html',{'add':add,'active':'btn-primary'})
    
@login_required
def orders(request):
    op =OrdrerPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'order_placed':op})

# mobile view 
def mobile(request,data=None):
    
    totalitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    if data == None:
        mobiles =Product.objects.filter(category='M')
    elif data == 'Redmi' or data == 'Samsung':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'below':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=10000)
        
        
    elif data == 'above':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=10000)    
            
    return render(request, 'app/mobile.html',{'mobiles':mobiles,'totalitem':totalitem})

# laptop view
def laptop(request,data=None):
    totalitem =0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    if data == None:
        laptops =Product.objects.filter(category='L')
    elif data =='Dell' or data == 'Lenavo':
        laptops =Product.objects.filter(category='L').filter(brand=data)
    elif data =='below':
        laptops =Product.objects.filter(category='L').filter(discounted_price__lt=30000)
    elif data == 'above':
        laptops = Product.objects.filter(category='L').filter(discounted_price__gt=30000)            
    
    return render(request,'app/laptop.html',{'laptops':laptops,'totalitem':totalitem})
#top product sections view
def top_product(request,data=None):
    totalitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    if data == None:
        top_products =Product.objects.filter(category='TP')
    
    return render(request,'app/topproduct.html',{'top_products':top_products,'totalitem':totalitem})    
# best product section view
def best_product(request,data=None):
    totalitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    if data == None:
        best_products =Product.objects.filter(category='BP')
    
    return render(request,'app/bestproduct.html',{'best_products':best_products,'totalitem':totalitem})



class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        return render(request,'app/customerregistration.html',{'form':form})
    
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations!! Registered Successfully')
            form.save()
        return render(request,'app/customerregistration.html',{'form':form}) 
       
@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items =Cart.objects.filter(user=user)
    amount = 0.0
    shipping_ammount =60
    totalamount=0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        
        for p in cart_product:
            
            tempamount = (p.quantity * p.product.discounted_price)
            amount +=tempamount
        totalamount = amount + shipping_ammount    
    return render(request,'app/checkout.html',{'add':add,'totalamount':totalamount,'cart_items':cart_items})

@login_required
def payment_done(request):
    user = request.user
    custid =request.GET.get('custid')
    customer =Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrdrerPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect("orders")    


@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    
    
    def get(self,request):
        form = CustomerProfileForm()
        return render(request,'app/profile.html',{'form':form ,'active':'btn-primary'})
    
    def post(self,request):
        form =CustomerProfileForm(request.POST)
        if form.is_valid():
            
            usr =request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,'Congrats profile updated successfully!!')
            return render(request,'app/profile.html',{'form':form ,'active':'btn-primary'}) 




def search(request,):
    
    query = request.GET.get('query')
    # print(query)
    product =Product.objects.filter(title__icontains =query,brand__icontains =query)
    return render(request,'app/search.html',{'product':product})

@login_required
def contact(request):
    if request.method=="POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('desc')
        desc = request.POST.get('desc')
        contact=Contact(name=name,email=email,phone=phone,desc=desc,date=datetime.today())
        contact.save()
        messages.success(request, 'Your message as has been sent')
        
    return render(request,'app/contact.html')


def About_us(request):
    return render(request,'app/aboutus.html')