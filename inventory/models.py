from django.db import models
from django.contrib.auth.models import AbstractUser #management the user
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
import uuid
from django.utils import timezone
from django.utils.timezone import localtime


# Create your models here.

from django.db import models

#username, password<data_joined, last_login came from Abstract user
class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=15, 
                            choices=[
                                ('admin','Admin'),
                                ('user','User')],
                            default='user')
    
    USERNAME_FIELD = 'email'    #login will made by EMAIL
    REQUIRED_FIELDS = ['username']  #obrigation fields

    def __str__(self):
        return self.username    #name on painel ADMIN

#Class for tbe Product
class Category(models.Model):
    category = models.CharField(max_length=30, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # adiciona quem criou

    #plural of the words on django
    class Meta:
         verbose_name = "Category"
         verbose_name_plural = "Categories"

    def __str__(self):
         return str(self.category)



class SubCategory(models.Model):
        category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")
        subcategory = models.CharField(max_length=50)

        class Meta:
         verbose_name = "Sub Category"
         verbose_name_plural = "Sub Categories"
             
        def __str__(self):
             return f"{self.subcategory}"
        

class Item(models.Model):
     code = models.CharField(max_length=7, unique=True, editable=False)   
     category = models.ForeignKey(Category, on_delete=models.CASCADE)
     subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     name = models.CharField(max_length=40, null=False, blank=False)
     price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, default=0.00)
     description = models.TextField(max_length=250)
     minimum_stock = models.IntegerField(default=10)
     quantity = models.IntegerField(validators=[MinValueValidator(0)])  #the quantity can be less tha one
     avaible = models.BooleanField(default=True)
     images = models.ImageField(upload_to='product_images/', null=True, blank=True, default='default_images.png')
 
     def save(self, *args, **kwargs):
         if not self.code:
            self.code = self.make_unique_code()
         super().save(*args, **kwargs)
      
     def make_unique_code(self):    
        #make a unique UUID and taje the 7 first caracters
        code = uuid.uuid4().hex.upper()   #hex to get a compact string
        return code[:7] #return 7 caracters to add to the product code
     
     def __str__(self):
         return str(self.name)
     

class StockMovement(models.Model):
    ENTRADA = 'E'
    SAIDA = 'S'
    TIPO_MOVIMENTO  = [
        (ENTRADA, 'Entrada'),
        (SAIDA, 'Saída'),
    ]

    @staticmethod
    def now_no_microseconds():
         return timezone.now().replace(microsecond=0)

    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=1, choices=TIPO_MOVIMENTO)
    quantidade = models.IntegerField()
    data = models.DateTimeField(default=timezone.now)  #not have the microsegunds
    observacao = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantidade_antes = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        data_local = localtime(self.data)
        data_formatada = data_local.strftime('%d/%m/%Y %H:%M')
        tipo_str = dict(self.TIPO_MOVIMENTO).get(self.tipo, "DESCONHECIDO")

        return str(f"{self.item} - {tipo_str.upper()} - {self.quantidade} - EM {data_formatada} FROM {self.user}")

  
