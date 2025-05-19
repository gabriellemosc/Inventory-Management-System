from django.urls import path
from .views import homepage, create_product, create_category,create_subcategory, login_view, logout_view

#we need to add to the root urls too
urlpatterns = [
    path('', homepage, name='homepage'),  # Receive the request and send to the right function ->
    path('create-product/', create_product, name='create_product'),
    path('create-category/', create_category, name='create_category'),
    path('create-subcategory/', create_subcategory, name='create_subcategory'),
    path('login/', login_view, name='login_view'),
    path('logout/', logout_view, name='logout_view')

]

