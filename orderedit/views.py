from django.views.generic import ListView
from .models import User,Item
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls.base import reverse_lazy

# Create your views here.
class OrderEditView(ListView):
    model = Item
    template_name = "orderedit.html"
    
class NewItemView(ListView):
    model = Item
    template_name = "Item/newitem.html"

class OldItemView(ListView):
    model = Item
    template_name = "Item/olditem.html"