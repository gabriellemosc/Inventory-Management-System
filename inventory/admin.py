from django.contrib import admin
from inventory.models import User, Category, SubCategory, Item     #import everthing from models
# Register your models here.

#ALWAYS GIVE ACESS TO THE ADMIN WHEN CREATE A NEW MODEL
admin.site.register(User)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Item)