from django.urls import path
from .views import homepage, create_product, create_category,create_subcategory, login_view, logout_view, item_details, move_stock,minimun_stock, stock_movement_report

#we need to add to the root urls too
urlpatterns = [
    path('', homepage, name='homepage'),  # Receive the request and send to the right function ->
    path('create-product/', create_product, name='create_product'),
    path('create-category/', create_category, name='create_category'),
    path('create-subcategory/', create_subcategory, name='create_subcategory'),
    path('login/', login_view, name='login_view'),
    path('logout/', logout_view, name='logout_view'),
    path('item/<int:pk>/', item_details, name='item_details'),
    path('move_stock/<int:pk>/', move_stock, name='move_stock'),
    path('minimun_stock', minimun_stock, name='minimun_stock'),
    path('stock_movement_report', stock_movement_report, name='stock_movement_report'),

]

