from django.urls import path
from .views import homepage

#we need to add to the root urls too
urlpatterns = [
    path('', homepage, name='homepage'),  # '' = root do site
]