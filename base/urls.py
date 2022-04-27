from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView 

urlpatterns = [
    
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/',newUser, name='register'),
    path('productdetails/<int:pk>/', buyproduct, name='productdetails'),
    path('deleteproduct/<int:pk>/', DeleteProduct.as_view(), name='deleteproduct'),
    path('updateproduct/<int:pk>/', ProductUpdate.as_view(), name='deleteproduct'),
    path('myproducts/', myProducts, name='myproducts'),
    path('enlist/', enlistProduct, name='enlist' ),
    path('', homePage, name='home'),
]