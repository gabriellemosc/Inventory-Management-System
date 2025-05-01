from django.shortcuts import render, redirect       #render give a html page as response, redirect make the user goes to other URL
from .forms import ItemForm, CategoryForm
from django.shortcuts import redirect

# Create your views here.

def homepage(request):  #after the urls.py direct to here, the function decide what to make. If shows or save what the user maked
    return render(request, 'inventory/homepage.html')

def create_product(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)   #send to the function in Forms
        if form.is_valid():
            form.save()
            return redirect('homepage')
    else:
        form = ItemForm()       

    return render(request, 'inventory/Create_Product/create_product.html',{"form":form})   #send the object to the form


def create_category(request):
    next_url = request.GET.get('next', '/')     #take the URL to save to redirect where the user was
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            #redirect to the previous page
            return redirect(next_url)
    else:
            form = CategoryForm()

    return render(request, 'inventory/Create_Product/create_category.html', {"form":form})


def create_subcategory(request):
    return render(request, 'inventory/Create_Product/create_subcategory.html')


