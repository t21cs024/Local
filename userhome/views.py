from django.views.generic import ListView
from .models import User,Item,Cart,CartItem
from superuserhome.models import Item as SuperuserItem
from django.views.generic.base import TemplateView
from django.shortcuts import render,redirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls.base import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from superuserhome.models import BuyHistory
from .forms import ItemIdForm,ItemForm
from django.http import StreamingHttpResponse
from django.views.decorators import gzip
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import cv2
import numpy as np
import threading
import time
import websocket

# Create your views here.

class UserHomeView(TemplateView):
    model = User
    template_name = 'user_home.html'
    
# カメラキャプチャ用のクラス
class CameraView(TemplateView):
    model = Item
    template_name = 'Order/buy_item.html'
    
class CartContentsView(ListView):
    model = Item
    template_name = 'Order/cart/cart_contents.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # カートの内容を取得
        
        cart = self.request.user.cart
        cart_items = cart.cartitem_set.all()
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        
        if not cart_items:
            context['cart_is_empty'] = True
        else:
            total_price = sum(item.product.price * item.quantity for item in cart_items)
            context['cart_items'] = cart_items
            context['total_price'] = total_price

        return context


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # セッションの再認証
            messages.success(request, 'パスワードが変更されました。')
            return redirect('/userhome')
            messages.error(request, 'パスワードの変更にエラーがあります。')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'Order/change_pass.html', {'form': form})
    
class AddToCartView(TemplateView):
    template_name = 'Order/cart/add_to_cart.html'
    
    def post(self, request, *args, **kwargs):
        item_id = self.request.POST.get('item_id')
        item = Item.objects.get(pk=item_id)
        context = super().get_context_data(**kwargs)
        context['form_id'] = ItemIdForm()
        context['item'] = item
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_id'] = ItemIdForm()
        return context

    return redirect('cart_view')  # カートの表示ページにリダイレクト

class BuyHistoryView(TemplateView):
    template_name = 'Order/buy_history.html'

    def get(self, request, *args, **kwargs):
        # ログインしているユーザを参照
        user = request.user
        object_list = BuyHistory.objects.filter(user = user)
        return render(request, self.template_name, {'object_list':object_list})
