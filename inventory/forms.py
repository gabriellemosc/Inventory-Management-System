#forms that all the request from user
from django import forms
from .models import Item    #impor the struct from our table fro DB
from .models import Category

#creating a new form
class ItemForm(forms.ModelForm):    #class from django, create a form A DB model
    class Meta: #model to use to buld the form
        model = Item        #we say to use the model item to buidl
        fields = ['images','name', 'category', 'subcategory','quantity', 'price','description', 'avaible']  #field to show on form


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category']       #the only field to complete