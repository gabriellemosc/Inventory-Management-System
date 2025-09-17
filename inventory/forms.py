#forms that all the request from user
from django import forms
from .models import Item    #impor the struct from our table fro DB
from .models import Category, SubCategory, Item
from .models import User
from .models import StockMovement
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm


#LOGIN FORM
class LoginForm(forms.Form):    
        login = forms.CharField(
            label="Usuário ou Email",
                                    max_length=254,
                                    widget=forms.TextInput(attrs={
                                        "class":"form-control",
                                        "placeholder": "Digite seu usuário",
                                        "autofocus": True
                                    })
                                    )  
        password = forms.CharField(
                                    label="Senha",
                                    strip=False,
                                    widget=forms.PasswordInput(attrs={
                                        "class": "form-control",
                                        "placeholder": "Digite sua senha",
                                    })
                                    )
        
        def __init__(self, *args, **kwargs):
            self.user = None
            super().__init__(*args, **kwargs)

       
        def clean(self):
            cleaned_data = super().clean()
            login_input = cleaned_data.get("login")
            password = cleaned_data.get("password")

            if login_input and password:
                # Busca usuário por username ou email
                from django.contrib.auth import get_user_model
                User = get_user_model()

                user_obj = User.objects.filter(username=login_input).first() or User.objects.filter(email=login_input).first()

                if not user_obj:
                    raise forms.ValidationError("Usuário ou senha inválidos")

                # Aqui passa o email ou username de acordo com USERNAME_FIELD
                user = authenticate(
                    username=user_obj.email if User.USERNAME_FIELD == 'email' else user_obj.username, 
                    password=password
                )

                if not user:
                    raise forms.ValidationError("Usuário ou senha inválidos")

                self.user = user

            return cleaned_data

        def get_user(self):
            return self.user
    


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
            label="Email",
            required=True,
            widget=forms.EmailInput(attrs={
                            'class': 'form-control',
                            'placeholder': "Digite seu email"
            })
    )
    password1 = forms.CharField(
            label="Senha",
            widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': "Digite sua senha"})
    ) 
    password2 = forms.CharField(
        label="Confirme sua Senha",
        widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Repita sua Senha'})
    )

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

class ItemForm(forms.ModelForm):    #class from django, create a form A DB model
    class Meta: #model to use to buld the form
        model = Item        #we say to use the model item to buidl
        fields = ['images','name', 'category', 'subcategory','quantity', 'minimum_stock', 'price','description', 'avaible']  #field to show on form
        exclude = ['user'] #remove user from the form
        widgets = {
            'name': forms.TextInput(attrs={
                                            'placeholder': 'Nome do Produto',
                                            'required': False
                                            }),
            'quantity': forms.TextInput(attrs={'placeholder': 'Quantidade em Estoque'}),
            'description': forms.TextInput(attrs={'placeholder': 'Breve Descrição do Produto'}),
            'minimum_stock': forms.NumberInput(attrs={
                'min': 0,
                'placeholder': 'Quantidade Mínima para Alerta'
            }),
            'price': forms.TextInput(attrs={
                'placeholder': 'Preço',
                'id': 'id_price'
            }),
        }

    def __init__(self, *args, **kwargs):
            user = kwargs.pop('user', None)
            super().__init__(*args, **kwargs)

            if user:
                self.fields['category'].queryset = Category.objects.filter(user=user)
                self.fields['subcategory'].queryset = SubCategory.objects.filter(category__user=user)


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

    def clean_minimum_stock(self):
        minimo = self.cleaned_data.get('minimum_stock')
        if minimo is None or minimo <= 0:
            raise forms.ValidationError("A Quatidade Mínima de Estoque Deve ser Maior que 0")
        return minimo



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
            movimento.user = self.user
            quantidade = self.cleaned_data.get('quantidade')
            tipo = self.cleaned_data.get('tipo')
            item = self.cleaned_data.get('item')



            if not movimento.pk:        #novo movimento em estoque
                movimento.quantidade_antes = item.quantity  #save quantity before movimentation

                if tipo == 'E':
                    item.quantity += quantidade
                elif tipo == 'S':
                    item.quantity -= quantidade
                
                if commit:
                    item.save()

            if commit:
                    movimento.save()

            return movimento
    
#allow user edit the products

class ItemEditForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['category', 'subcategory', 'name', 'price', 'description', 'minimum_stock', 'images']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['images'].required = False 


    def clean_name(self):
        novo_nome = self.cleaned_data.get('name')

        if not novo_nome:
            return self.instance.name
        
        novo_nome = novo_nome.strip().title()

        if len(novo_nome) > 200:
            raise ValueError("O nome do produto deve ter menos que 200 caracteres")
        
        return novo_nome
    
    def clean_minimum_stock(self):
        novo_minimo_estoque = self.cleaned_data.get('minimum_stock')

        if  novo_minimo_estoque is None:
            return self.instance.minimum_stock
        
        if novo_minimo_estoque <= 0:
            raise forms.ValidationError("O Estoque Mínimo não pode ser menor ou igual à 0")
        
        return novo_minimo_estoque
    

        
#SEPARETE PAGES TO CATEGORY AND SUBCATEGORY
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category']       #the only field to complete


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['category','subcategory']     #fields to complete