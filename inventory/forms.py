#forms that all the request from user
from django import forms
from .models import Item    #impor the struct from our table fro DB
from .models import Category, SubCategory
from .models import User
from django.contrib.auth.forms import AuthenticationForm

#LOGIN FORM
class LoginForm(AuthenticationForm):    
        username = forms.CharField(label="Username", max_length=100)  
        password = forms.CharField( label="Password", widget=forms.PasswordInput)

        class Meta:
            model = User
            fields = ['username', 'password']


class ItemForm(forms.ModelForm):    #class from django, create a form A DB model
    class Meta: #model to use to buld the form
        model = Item        #we say to use the model item to buidl
        fields = ['images','name', 'category', 'subcategory','quantity', 'price','description', 'avaible']  #field to show on form
        exclude = ['user'] #remove user from the form
        widgets = {
            'name': forms.TextInput(attrs={
                                            'placeholder': 'Nome do Produto',
                                            'required': False
                                            }),
            'quantity': forms.TextInput(attrs={'placeholder': 'Quantidade em Estoque'}),
            'description': forms.TextInput(attrs={'placeholder': 'Breve Descrição do Produto'})
        }

#VALIDATIONS
    def clean_name(self):
        name = self.cleaned_data.get('name')

        if not name:
            raise forms.ValidationError("Campo nome do produto obrigatório")
        return name

    def clean_category(self):
        category = self.cleaned_data.get('category')

        if not category:
            raise forms.ValidationError("CATEGORIA NÃO PODE SER VAZIA")
        return category

    def clean_price(self):
        price = self.cleaned_data.get('price')  #take the price
        if price is None:
            raise forms.ValidationError("O preço é obrigatório")
        if price <= 0:
            raise forms.ValidationError("O PREÇO DEVE SER MAIOR QUE 0")
        return price

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity < 0:
            raise forms.ValidationError("QUANTIDADE NÃO PODE SER MENOR QUE 0")
        if quantity is None:
            raise forms.ValidationError("Quantidade Obrigatória")
        return quantity
    
    def clean_images(self):
        image = self.cleaned_data.get('images')

        if image and hasattr(image, 'size'):                #check if its a image
            max_size = 10 * 1024 * 1024  # 5MB to the image bytes
            if image.size > max_size:
                raise forms.ValidationError("TAMANHO MÁXIMO PERMITIDO DE 5 MB")
        return image

    def clean_description(self):
        description = self.cleaned_data.get('description')

        if description:
            if len(description) >= 250: 
                raise forms.ValidationError("DESCRIÇÃO DEVE TER MENOS DE 250 CARACTERES")
        
        return description



#SEPARETE PAGES TO CATEGORY AND SUBCATEGORY
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category']       #the only field to complete


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['category','subcategory']     #fields to complete