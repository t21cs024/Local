from django.views.generic import ListView
from .models import User,Item
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
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

# Create your views here.

class UserHomeView(TemplateView):
    model = User
    template_name = 'user_home.html'
    
class BuyItemView(TemplateView):
    model = Item
    template_name = 'Order/buy_item.html'
    
class BuyHistoryView(TemplateView):
    model = Item
    template_name = 'Order/buy_history.html'
    

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # セッションの再認証
            messages.success(request, 'パスワードが変更されました。')
            return redirect('userhome')
        else:
            messages.error(request, 'パスワードの変更にエラーがあります。')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'Order/change_pass.html', {'form': form})

'''
from flask import Flask, render_template, Response
import cv2
from pyzbar import pyzbar

app = Flask(__name__)

def gen_frames():
    camera = cv2.VideoCapture(0)  # カメラを開く
    while True:
        success, frame = camera.read()  # カメラからフレームを読み込む
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # フレームをストリームする

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
'''
    
    