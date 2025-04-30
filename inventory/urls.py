from django.urls import path
from .views import homepage, create_product

#we need to add to the root urls too
urlpatterns = [
    path('', homepage, name='homepage'),  # Receive the request and send to the right function ->
    path('create_product/', create_product, name='create_product')
]