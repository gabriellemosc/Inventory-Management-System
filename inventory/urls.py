from django.urls import path
from .views import homepage, create_product, create_category,create_subcategory, login_view, logout_view, item_details, move_stock,minimun_stock, stock_movement_report, edit_product, dowloand_report_pdf, report_stock_movement,category_list,category_detail,delete_product, register_view, change_mode



#we need to add to the root urls too
urlpatterns = [
    path('', homepage, name='homepage'),  # Receive the request and send to the right function ->
    path('create-product/', create_product, name='create_product'),
    path('create-category/', create_category, name='create_category'),
    path('create-subcategory/', create_subcategory, name='create_subcategory'),
    path('login/', login_view, name='login_view'),
    path('logout/', logout_view, name='logout_view'),
    path('register_view/', register_view, name='register_view'),
    path('item/<int:pk>/', item_details, name='item_details'),
    path('move_stock/<int:pk>/', move_stock, name='move_stock'),
    path('minimun_stock', minimun_stock, name='minimun_stock'),
    path('stock_movement_report', stock_movement_report, name='stock_movement_report'),
    path('edit_product/<int:pk>/', edit_product, name='edit_product'),
    path('report_stock_movement/', report_stock_movement, name="report_stock_movement"),
    path('dowloand_report_pdf/', dowloand_report_pdf, name="dowloand_report_pdf"),
    path('category_list/', category_list, name="category_list"),
    path('category_detail/<int:pk>/', category_detail, name="category_detail"),
    path('product/<int:pk>/delete/', delete_product, name="delete_product"),
    path('change-mode/', change_mode, name='change_mode'),




]

