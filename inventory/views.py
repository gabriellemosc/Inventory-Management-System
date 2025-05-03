from django.shortcuts import render, redirect       #render give a html page as response, redirect make the user goes to other URL
from .forms import ItemForm, CategoryForm, SubCategoryForm
from django.shortcuts import redirect

# Create your views here.

def homepage(request):  #after the urls.py direct to here, the function decide what to make. If shows or save what the user maked
    return render(request, 'inventory/homepage.html')

def create_product(request):
    if request.method == 'POST':        #check if was a POST
        form = ItemForm(request.POST)   #IF yes, takes the parameter by the USER CREATE A FORM AND SAVE ON DB 
        if form.is_valid():
            form.save()
            return redirect('homepage')
    else:                               #if was A GET e not a post
        form = ItemForm()               #create the form

    return render(request, 'inventory/Create_Product/create_product.html',{"form":form})   #send the object to the form


def create_category(request):
    next_url = request.GET.get('next', '/')     #take the URL, beside next to save to redirect where the user was
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
    next_url = request.GET.get('next', '/')
    category_id  = request.GET.get('category_id')

    if request.method == 'POST':
        form = SubCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            #redirect previous page
            return redirect(next_url)
    else:
        inital_data = {}
        if category_id:
            inital_data['category'] = category_id
        form = SubCategoryForm(initial=inital_data)     #pass the DATAS already to the form as context

    return render(request, 'inventory/Create_Product/create_subcategory.html', {"form":form})


