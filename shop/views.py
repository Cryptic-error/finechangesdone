from django.shortcuts import redirect, render
from .models import Product, CartItem
from django.http import HttpResponse
from math import ceil
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CustomUserCreationForm, LoginForm
from django.urls import reverse
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
import json
from .forms import SearchForm





def index(request):
    Products = Product.objects.all()
    n = len(Products)
    print(Products)
    nslides = n // 4 + ceil((n / 4) - (n // 4))
    params = {'no_of_slides': nslides, 'range': range(nslides), 'products': Products}
    return render(request, "shop/index.html", params)\
    

def caraousel():
    all_products = Product.objects.all()
    
    n = len(all_products)
    products_per_slide = 3  # Display 3 products per slide
    
    # Group products into batches for each slide
    prod_batches = [all_products[i:i + products_per_slide] for i in range(0, n, products_per_slide)]
    
    # Calculate the number of slides needed
    nslides = n // products_per_slide + ceil((n / products_per_slide) - (n // products_per_slide))
    
    # Return product batches and slide info
    return {'prod_batches': prod_batches, 'nslides': nslides}
    


def get_all_products():
    allprods = []
    catprods = Product.objects.values('category', 'product_id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nslides = n // 4 + ceil((n / 4) - (n // 4))
        allprods.append([prod, range(1, nslides), nslides])
    return allprods

def get_product_info(product_id):
    try:
        product = Product.objects.get(id=product_id)
        return {'name': product.name, 'price': product.price}  # Assuming 'name' and 'price' are fields in your Product model
    except Product.DoesNotExist:
        return None




def product(request):
    category_filter = request.GET.get('category', 'all')
    allprods = []
    
    # Retrieve all products for the selected category
    if category_filter == 'all':
        catprods = Product.objects.values('category', 'product_id')
        cats = {item['category'] for item in catprods}
    else:
        cats = {category_filter}

    for cat in cats:
        if category_filter == 'all':
            prod = Product.objects.filter(category=cat)
        else:
            prod = Product.objects.filter(category=category_filter)

        n = len(prod)
        nslides = n // 4 + ceil((n / 4) - (n // 4))
        allprods.append([prod, range(1, nslides + 1), nslides])

    categories = Product.objects.values_list('category', flat=True).distinct()

    params = {
        'allprods': allprods,
        'categories': categories,
        'selected_category': category_filter,  # Pass the selected category
    }
    return render(request, "shop/product.html", params)



def about(request):
    return render(request, "shop/about.html")
def index2(request):
    return render(request, "shop/index2.html")
def portfolio(request):
    params =  caraousel()
    return render(request, "shop/portfolio.html",params)
def contact(request):
    return render(request, "shop/contact.html")
def service(request):
    return render(request, "shop/service.html")
def servicedetl(request):
    return render(request, "shop/servicedetail.html")   
# def home(request):
#     return render(request, "shop\template\index.html")

def search(request):
    query = request.GET.get('search', '')
    allprods = []
    catprods = Product.objects.values('category', 'product_id')
    cats = {item['category'] for item in catprods}
    
    for cat in cats:
        if query:
            prod = Product.objects.filter(category=cat, product_name__icontains=query)  # Filter products based on the search query
        else:
            prod = Product.objects.filter(category=cat)
        n = len(prod)
        nslides = n // 4 + ceil((n / 4) - (n // 4))
        allprods.append([prod, range(1, nslides), nslides])

    params = {'allprods': allprods,}
    return render(request, "shop/search.html", params)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'shop/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('shop/home.html')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect(reverse('login'))  # Redirect using named URL 'login'
    return redirect(reverse('home')) 

# @login_required
def home(request):
    # Get all products across categories
    all_products = Product.objects.all()
    
    n = len(all_products)
    products_per_slide = 3  # Display 3 products per slide
    
    # Group products into batches for each slide
    prod_batches = [all_products[i:i + products_per_slide] for i in range(0, n, products_per_slide)]
    
    # Calculate number of slides needed
    nslides = n // products_per_slide + ceil((n / products_per_slide) - (n // products_per_slide))
    
    # Pass product batches and slide info to the template
    params = {'prod_batches': prod_batches, 'nslides': nslides}
    print(params)
    return render(request, "shop/home.html", params)


def basic(request):
    # Get all products across categories
    all_products = Product.objects.all()
    
    n = len(all_products)
    products_per_slide = 3  # Display 3 products per slide
    
    # Group products into batches for each slide
    prod_batches = [all_products[i:i + products_per_slide] for i in range(0, n, products_per_slide)]
    
    # Calculate number of slides needed
    nslides = n // products_per_slide + ceil((n / products_per_slide) - (n // products_per_slide))
    
    # Pass product batches and slide info to the template
    params = {'prod_batches': prod_batches, 'nslides': nslides}
    print(params)
    return render(request, "shop/basic.html", params)

@user_passes_test(lambda u: u.is_superuser)
def admin_only_view(request):
    if request.user.is_superuser:
        return render(request, 'shop/admin.html')
    else:
            # Handle unauthorized access here, e.g., redirect or show an error
            return render(request, 'error.html', {'message': 'You are not authorized to access this page.'})
    


