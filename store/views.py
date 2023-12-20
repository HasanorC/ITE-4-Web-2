from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from .forms import ProductForm, SignUpForm, CategoryForm
from .models import Product, Category
from django.utils import timezone


def user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect('admin_products')  # Redirect to product_list for admin
            else:
                login(request, user)
                return redirect('product_list')
        else:
            # Handle invalid login credentials
            return render(request, 'store/loginUser.html', {'error_message': 'Invalid username or password'})

    return render(request, 'store/loginUser.html')

def signupUser(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')  # Redirect to product_list after successful signup
    else:
        form = SignUpForm()

    return render(request, 'store/signupUser.html', {'form': form})

def logoutUser(request):
    logout(request)
    return redirect('product_list')

def food_list(request, category_id=None):
    categories = Category.objects.all()
    
    if category_id:
        selected_category = Category.objects.get(pk=category_id)
        products = selected_category.products.all()
    else:
        selected_category = None
        products = Product.objects.all()

    return render(request, 'store/food_list.html', {'products': products, 'categories': categories, 'selected_category': selected_category})

def food_description(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/food_des.html', {'product': product})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'store/category_list.html', {'categories': categories})

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()

    return render(request, 'store/add_foodcategory.html', {'form': form})
def is_admin(user):
    return user.is_staff

@user_passes_test(is_admin)
def admin_food_list(request):
    products = Product.objects.all()
    return render(request, 'store/admin_foods.html', {'products': products})


@user_passes_test(is_admin)
def add_food(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'store/add_food.html', {'form': form})

@user_passes_test(is_admin)
def edit_food(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('admin_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'store/edit_food.html', {'form': form, 'product': product})

@user_passes_test(is_admin)
def delete_food(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('admin_products')


@user_passes_test(is_admin)
def admin_food_categories(request):
    categories = Category.objects.all()
    return render(request, 'store/admin_foodcategories.html', {'categories': categories})

@user_passes_test(is_admin)
def add_food_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.created_at = timezone.now()
            category.save()
            return redirect('admin_products')  
    else:
        form = CategoryForm()
    return render(request, 'store/add_foodcategory.html', {'form': form})

@user_passes_test(is_admin)
def edit_food_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('admin_categories')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'store/edit_foodcategory.html', {'form': form, 'category': category})

@user_passes_test(is_admin)
def delete_food_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('admin_categories')
    
def aboutStore(request):
    return render(request, 'store/storeAbout.html')