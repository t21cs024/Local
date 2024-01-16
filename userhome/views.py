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
from .forms import ItemIdForm,ItemForm
from django.http import StreamingHttpResponse
from django.views.decorators import gzip
import cv2
import numpy as np

# Create your views here.

class UserHomeView(TemplateView):
    model = User
    template_name = 'user_home.html'
    
class QRCodeDetector:
    def __init__(self):
        self.qrd = cv2.QRCodeDetector()

    def detect_and_decode(self, frame):
        retval, decoded_info, points, straight_qrcode = self.qrd.detectAndDecodeMulti(frame)
        return retval, decoded_info, points, straight_qrcode

# カメラキャプチャ用のクラス
class CameraView(TemplateView):
    model = Item
    template_name = 'Order/buy_item.html'
    
    '''
    def __init__(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.qr_detector = QRCodeDetector()

    def __del__(self):
        self.cap.release()

    def get_frame(self):
        ret, frame = self.cap.read()

        if ret:
            retval, decoded_info, points, straight_qrcode = self.qr_detector.detect_and_decode(frame)

            if retval:
                points = points.astype(np.int32)

                for dec_inf, point in zip(decoded_info, points):
                    if dec_inf != '':
                        # QRコード座標取得
                        x = point[0][0]
                        y = point[0][1]

                        # QRコードデータ
                        frame = cv2.putText(frame, dec_inf, (x, y - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255), 1, cv2.LINE_AA)

                        # バウンディングボックス
                        frame = cv2.polylines(frame, [point], True, (0, 255, 0), 1, cv2.LINE_AA)

            ret, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes()
       ''' 
class BuyHistoryView(TemplateView):
    model = Item
    template_name = 'Order/buy_history.html'

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

