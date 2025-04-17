from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from store.models import Product

class HomeView(ListView):
    model = Product
    template_name = 'core/home.html'
    context_object_name = 'products'
    
# Create your views here.
