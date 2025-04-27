from django.db import models
from django.contrib.auth.models import AbstractUser

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
    category_name = models.CharField(max_length=30, unique=True)
    #plural of the words on django
    class Meta:
         verbose_name = "Category"
         verbose_name_plural = "Categories"

    def __str__(self):
         return str(self.category_name)



class SubCategory(models.Model):
        category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")
        subcategory_name = models.CharField(max_length=50)

        class Meta:
         verbose_name = "Sub Category"
         verbose_name_plural = "Sub Categories"
             
        def __str__(self):
             return f"{self.category.category_name} - {self.subcategory_name}"
     
