from django.shortcuts import render, redirect       #render give a html page as response, redirect make the user goes to other URL
from .forms import ItemForm

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

    return render(request, 'inventory/create_product.html',{"form":form})


