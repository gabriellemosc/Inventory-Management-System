from django.shortcuts import render, redirect       #render give a html page as response, redirect make the user goes to other URL
from .forms import ItemForm, CategoryForm, SubCategoryForm, LoginForm, Item, StockMovementForm
from django.shortcuts import redirect
from .models import Category, SubCategory
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

# Create your views here.

@login_required
def homepage(request):  #after the urls.py direct to here, the function decide what to make. If shows or save what the user maked

    #filter products by user
    itens = Item.objects.filter(user=request.user)

    print(f"Usuario {request.user}")
    for item in itens:
         print(item.name)
    return render(request, 'inventory/homepage.html', {'itens':itens})

@login_required
def item_details(request, pk):
     item = get_object_or_404(Item, pk=pk, user=request.user)
     return render(request, 'inventory/item_details.html', {'item': item})

def login_view(request):
     if request.method == 'POST':
          form = LoginForm(data=request.POST)
          if form.is_valid():
               #auth and make login
               user = form.get_user()
               login(request, user)
               return redirect('homepage')
     else:
            form = LoginForm()
     return render(request, 'inventory/User/login.html',{"form":form})

def logout_view(request):
     logout(request)
     return redirect('login')

@login_required
def create_product(request):
    #when the user register a new subcategory we get to the form
    category_id = request.GET.get('category_id')
    subcategory_id = request.GET.get('subcategory_id')
    
    inital_data = {}
#if the user already register, we try to get 
    if category_id:
            try:
                inital_data['category']  = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                pass
    
    if subcategory_id:
            try:
                inital_data['subcategory'] = SubCategory.objects.get(id=subcategory_id)  
            except SubCategory.DoesNotExist:
                pass          

    if request.method == 'POST':        #check if was a POST
        form = ItemForm(request.POST, request.FILES)   #IF yes, takes the parameter by the USER CREATE A FORM AND SAVE ON DB 
        if form.is_valid():
            #link product with user
            product  = form.save(commit=False)
            product.user = request.user 
            product.save()
            return redirect('homepage')
    else:     
        #when the user register subcategory, we already take 
        form = ItemForm(initial=inital_data)               #create the form and if we have the other context give to the forms

    return render(request, 'inventory/Create_Product/create_product.html',{"form":form})   #send the object to the form

@login_required
def create_category(request):
    next_url = request.GET.get('next', '/')     #take the URL, beside next to save to redirect where the user was

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category =  form.save() 
            #redirect to the previous page
            redirect_url = f"{next_url}?category_id={category.id}"  #send the ID of the category
            return redirect(redirect_url)
    else:
            form = CategoryForm()

    return render(request, 'inventory/Create_Product/create_category.html', {"form":form})

@login_required
def create_subcategory(request):
    next_url = request.GET.get('next', '/')         #take the previous path
    category_id  = request.GET.get('category_id')

    if request.method == 'POST':
        form = SubCategoryForm(request.POST)
        if form.is_valid():
            subcategory = form.save()
            #redirect previous page with the context of the category and subcategory
            redirect_url = f"{next_url}?category_id={subcategory.category.id}&subcategory_id={subcategory.id}" #send to the context
            return redirect(redirect_url)
    else:
        inital_data = {}
        if category_id:
            inital_data['category'] = category_id
        form = SubCategoryForm(initial=inital_data)     #pass the DATAS already to the form as context

    return render(request, 'inventory/Create_Product/create_subcategory.html', {"form":form})



@login_required
def move_stock(request, pk):
    item = get_object_or_404(Item, pk=pk, user=request.user)  if pk else None
    tipo_predefinido = request.GET.get('tipo')


    if request.method == 'POST':
          form = StockMovementForm(request.POST)
          if form.is_valid():
               form.save()
               return redirect('item_details', pk=pk)
    else:
        form = StockMovementForm(initial={'item': item, 'tipo_predefinido': tipo_predefinido})
        print(tipo_predefinido)

    return render(request,'inventory/move_stock.html', {'form': form, 'item': item})
