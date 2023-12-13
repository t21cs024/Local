from django.views.generic import ListView
from .models import User,Item
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls.base import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test


# Create your views here.
class SuperUserHomeView(TemplateView):
    model = User
    template_name = 'superuser_home.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})
    
class UserEditView(TemplateView):
    model = User
    template_name = "Edit/useredit.html"
    success_url=reverse_lazy('superuserhome')
    
class OrderEditView(TemplateView):
    model = Item
    template_name = "Edit/orderedit.html"
    
class NewItemView(TemplateView):
    model = Item
    template_name = "Edit/Item/newitem.html"

class OldItemView(TemplateView):
    model = Item
    template_name = "Edit/Item/olditem.html"
    
    