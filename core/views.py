from django.shortcuts import render, get_object_or_404, redirect
from . forms import NewUser
from django.contrib import messages,auth
from . models import Product, Category, CartItem
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
# Create your views here.
#
def navbar(request):
    category = Category.get_all_category()
    return render(request, "core/navbar.html",{'category':category})

# def checkout(request):
#     return render(request, "core/checkout.html")

def homepage(request):
    category = Category.objects.all()
    return render(request, "core/homepage.html",{'category':category})

def signup(request):
    if request.method == "POST":
        form = NewUser(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registered Successfully!!!")
        else:
            messages.error(request, "Something went wrong!")
    else:
        form = NewUser()
    return render(request, "core/register.html",{'form':form})

def login(request):
    if request.user.is_authenticated:
        return redirect('core:homepage')
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect("homepage")
        return render(request, 'core/login.html')

def logout(request):
    auth.logout(request)
    return redirect("homepage")

def productlist(request):
    category = Category.objects.all()
    product = Product.objects.all()
    return render(request, "core/productlist.html",{'product':product,'category':category})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    category = Category.objects.all()
    context = {
        'product':product,
        'category':category
    }
    return render(request, 'core/product_detail.html', context)

def catprod(request,slug):
    cat = get_object_or_404(Category, slug=slug)
    product = Product.objects.filter(category=cat)
    category = Category.objects.filter(active=True)
    context = {'category':category, 'product':product}
    return render(request, "core/catprod.html", context)

def search(request):
    q = request.GET["q"]
    product = Product.objects.filter(name__icontains=q)
    category = Category.objects.filter(active=True)
    context = {'category':category, 'product':product}
    return render(request, "core/productlist.html", context)

@login_required(login_url='login')
def cart(request):
    cart = CartItem.objects.filter(cart_id=request.user)
    context = {'cart':cart}
    return render(request, "core/cart.html",context)

@login_required(login_url='login')
def addtocart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    cart, created = CartItem.objects.get_or_create(product=product, cart_id=request.user)
    # order = Order.objects.filter(user=request.user, ordered=False)

    if CartItem.objects.filter(product=product.id).exists():
        cart.quantity += 1
        cart.save()
        return redirect('core:cart')

def decrease_quantity(request, slug):
    product = get_object_or_404(Product, slug=slug)
    cart = CartItem.objects.get(product=product, cart_id=request.user)
    if CartItem.objects.filter(product=product.id).exists():
        cart.quantity -= 1
        cart.save()
        if cart.quantity < 1:
            cart.delete()
            return redirect('core:cart')
        return redirect('core:cart')

def clear(request):
    cart = CartItem.objects.filter(cart_id=request.user)
    cart.delete()
    return redirect('core:cart')

def remove_item(request, slug):
    product = get_object_or_404(Product, slug=slug)
    ci = get_object_or_404(CartItem, product=product)
    ci.delete()
    return redirect('core:cart')
