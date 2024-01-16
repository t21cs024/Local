from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, authenticate
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView as BaseLoginView
from django.urls import reverse_lazy
from .forms import SignUpForm, LoginFrom 
# Create your views here.

        
class SignUpView(CreateView):
    """ ユーザー登録用ビュー """
    form_class = SignUpForm # 作成した登録用フォームを設定
    template_name = "Edit/signup.html" 
    success_url = reverse_lazy("superuserhome:home") # ユーザー作成後のリダイレクト先ページ

    def form_valid(self, form):
        # ユーザー作成後にそのままログイン状態にする設定
        response = super().form_valid(form)
        account_id = form.cleaned_data.get("account_id")
        password = form.cleaned_data.get("password1")
        user = authenticate(account_id=account_id, password=password)
        login(self.request, user)
        return response
    
        #ラベルを日本語に
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['account_id'].label = 'ユーザ名' 
        form.fields['emp_num'].label = '社員番号'
        form.fields['name'].label = '名前'
        form.fields['email'].label = 'メールアドレス'
        form.fields['affiliation'].label = '所属'
        return form
    
# ログインビューを作成
class LoginView(BaseLoginView):
    form_class = LoginFrom
    template_name = "login/login.html"
    
    def get_success_url(self):
        user = self.request.user

        #t21cs1 @@@@aaaa superuserhome
        #t21cs0 0000aaaa userhome
        # createsuperuserで作成したユーザはsupseruserhomeに遷移（superuser権限を持つならsuepruserhomeに遷移）
        if user.is_superuser:
            return '/superuserhome/'
        else:
            return '/userhome/'
        
    #ラベル変更
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['username'].label = 'Username' 
        form.fields['password'].label = 'Password' 
        return form
        
class CustomLogoutView(LogoutView):
    next_page=('/login')