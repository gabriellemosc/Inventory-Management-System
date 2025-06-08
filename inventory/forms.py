#forms that all the request from user
from django import forms
from .models import Item    #impor the struct from our table fro DB
from .models import Category, SubCategory, Item
from .models import User
from .models import StockMovement
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

class StockMovementForm(forms.ModelForm):
    def __init__(self,*args, user=None ,**kwargs):
        super().__init__(*args, **kwargs)
        self.user = user


        #hide field
        self.fields['item'].widget = forms.HiddenInput()
        self.fields['tipo'].widget = forms.HiddenInput()


    class Meta:
        model = StockMovement
        fields = ['item', 'tipo', 'quantidade', 'observacao']
        labels = {
            'observacao': 'Observação',
        }

    def clean(self):
        cleaned_data = super().clean()  
        quantidade = cleaned_data.get('quantidade')
        tipo = cleaned_data.get('tipo')
        item = cleaned_data.get('item')

        if item and self.user and item.user != self.user:
            raise forms.ValidationError("Você não tem permissão para movimentar esse item")
        
        if quantidade > 100000:
            raise forms.ValidationError("Valor não suportado")

        if tipo == 'S' and item and quantidade:
            if item.quantity < quantidade:
                raise forms.ValidationError("Estoque insuficiente para realizar essa saída")
        
        return cleaned_data
    
    
    def save(self, commit=True):
            movimento = super().save(commit=False)
            quantidade = self.cleaned_data.get('quantidade')
            tipo = self.cleaned_data.get('tipo')
            item = self.cleaned_data.get('item')

            if tipo == 'E':
                item.quantity += quantidade
            elif tipo == 'S':
                item.quantity -= quantidade
            
            if commit:
                item.save()
                movimento.save()

            return movimento

#SEPARETE PAGES TO CATEGORY AND SUBCATEGORY
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category']       #the only field to complete


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['category','subcategory']     #fields to complete