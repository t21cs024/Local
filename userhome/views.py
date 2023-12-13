from django.views.generic import ListView
from .models import User,Item
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls.base import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.
'''
def Superuserhome(request):
    return render(request, 'Order/superuserhome_menu.html', {})

def EmployeeManage(request):
    return render(request, 'Order/superuserhome_employee.html', {})

def FoodManage(request):
    return render(request, 'Order/superuserhome_food.html', {})
'''
class UserHomeView(TemplateView):
    model = User
    template_name = 'user_home.html'
    
class BuyItemView(TemplateView):
    model = Item
    template_name = 'Order/buy_item.html'
    
class BuyHistoryView(TemplateView):
    model = Item
    template_name = 'Order/buy_history.html'
    
class ChangePassView(TemplateView):
    model = User
    template_name = 'Order/change_pass.html'
    success_url=reverse_lazy('userhome')


class OrderEditView(ListView):
    model = Item
    template_name = "Order/orderedit.html"
    
class UserEditView(ListView):
    model = User
    template_name = "Order/useredit.html"

    
class NewItemView(ListView):
    model = Item
    template_name = "Order/NewItem.html"


class OldItemView(ListView):
    model = Item
    template_name = "Order/OldItem.html"

    
    