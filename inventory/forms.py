#forms that all the request from user
from django import forms
from .models import Item    #impor the struct from our table fro DB
from .models import Category, SubCategory

#creating a new form
class ItemForm(forms.ModelForm):    #class from django, create a form A DB model
    class Meta: #model to use to buld the form
        model = Item        #we say to use the model item to buidl
        fields = ['images','name', 'category', 'subcategory','quantity', 'price','description', 'avaible']  #field to show on form
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nome do Produto'}),
            'quantity': forms.TextInput(attrs={'placeholder': 'Quantidade em Estoque'}),
            'description': forms.TextInput(attrs={'placeholder': 'Breve Descrição do Produto'})
        }

    def clean_nome(self):
        name = self.cleaned_data.get('name')

        if not name:
            print("Campo Nome Obrigatorio")
            raise forms.ValidationError("Campo nome do produto obrigatório")
        return name


    def clean_price(self):
        price = self.cleaned_data.get('price')  #take the price
        if price is None:
            print("Preco Obrigatorio")
            raise forms.ValidationError("O preço é obrigatório")
        if price <= 0:
            print("Preco deve ser maior que 0")
            raise forms.ValidationError("o preço deve ser maior que ")
        return price

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity < 0:
            print("Quantidade nao pode ser menor que  0")
            forms.ValidationError("Quantidade não pode ser menor que 0")
        if quantity is None:
            print("Quantidade obrigatoria")
            forms.ValidationError("Quantidade Obrigatória")
        return quantity
    
    def clean_images(self):
        images = self.cleaned_data.get('images')

        if images:
            tamanho_maximo = 5 * 1024 * 1024  # 5MB to the image bytes
            if images.size > tamanho_maximo:
                print("Tamanho maximo permitido de 5MB")
                raise forms.ValidationError("Tamanho máximo permitido de 5 MB")
        return images

    def clean_description(self):
        description = self.cleaned_data.get('description')

        if description:
            if len(description) >= 250: 
                raise forms.ValidationError("Descrição deve ter menos de 250 caracteres")
        
        return description



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category']       #the only field to complete


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['category','subcategory']     #fields to complete