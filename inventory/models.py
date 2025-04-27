from django.db import models
from django.contrib.auth.models import AbstractUser #management the user
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
import uuid


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

    def __str__(self):
        return self.username    #name on painel ADMIN

#Class for tbe Product
class Category(models.Model):
    category = models.CharField(max_length=30, unique=True)
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
             return f"{self.category.category} - {self.subcategory}"
        

class Item(models.Model):
     code = models.CharField(max_length=7, unique=True, editable=False)   
     category = models.ForeignKey(Category, on_delete=models.CASCADE)
     subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
     name = models.CharField(max_length=40)
     description = models.CharField(max_length=250)
     quantity = models.IntegerField(validators=[MinValueValidator(0)])  #the quantity can be less tha one
     avaible = models.BooleanField(default=True)
 
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