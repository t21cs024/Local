#from django.views.generic import ListView
from .models import User,Item
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
#from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views.generic.edit import CreateView
from django.urls.base import reverse_lazy
#from django.utils.decorators import method_decorator
#from django.contrib.auth.decorators import login_required, user_passes_test
#from .forms import SignUpForm,UserIdForm,ItemBuy,ItemIdForm, ItemForm
from .forms import SignUpForm,UserIdForm,ItemBuy
#CSV関連のライブラリ
import csv
# test
from django.http import HttpResponse
from pip._vendor.typing_extensions import Self

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
    success_url=reverse_lazy('superuserhome')

    def post(self, request, *args, **kwargs):
        item_id = self.request.POST.get('item_id')
        item = get_object_or_404(Item, pk=item_id)
        item_status = self.request.POST.get('item_status')
        item.buy = item_status
        item.save()
        return HttpResponseRedirect(reverse('shoppinglist:list'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ItemBuy()
        return context
    
class NewItemView(CreateView):
    model = Item
    fields = ('name', 'item_url', 'count', 'buy_date')
    template_name = "Edit/Item/newitem.html"
    success_url = '/superuserhome/orderedit'
    
class SignUpView(TemplateView):
    model = User
    fields = ('user_id', 'name','user_menu', 'user_pass', 'user_mail','user_authority')
    template_name = "Edit/signup.html"
    success_url=reverse_lazy('superuserhome')

    def get(self, request, *args, **kwargs):
        form = SignUpForm()  # YourFormは適切なフォームのクラスに置き換えてください
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)  # YourFormは適切なフォームのクラスに置き換えてください
        if form.is_valid():
            # フォームのデータを使って新しいUserオブジェクトを作成
            new_user = User(
                user_id=form.cleaned_data['id'],
                name=form.cleaned_data['full_name'],
                user_pass=form.cleaned_data['password'],
                user_mail=form.cleaned_data['email'],
                user_authority=form.cleaned_data['authority'],
                # 他のフィールドも適切に追加
            )
            new_user.save()  # データベースに保存
            return redirect('superuserhome:useredit')  # 成功したら指定のURLにリダイレクト

        # フォームが無効な場合は再度入力を促す
        return render(request, self.template_name, {'form': form})
    
    

class UserInformationView(TemplateView):
    model = User
    template_name = "Edit/userinformation.html"

    def post(self, request, *args, **kwargs):
        user_id = self.request.POST.get('user_id')
        user = get_object_or_404(User, user_id=user_id)
        # user_idが存在しない場合はHTTP 404 Not Found
        return HttpResponseRedirect(reverse('superuserhome:userinformation_detail', kwargs={'user_id': user_id}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_id'] = UserIdForm()
        return context
    
    
class UserInformationDetailView(TemplateView):
    model = User
    template_name = "Edit/userinformation_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_id'] = UserIdForm()
        return context

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        user = get_object_or_404(User, pk=user_id)
        context = self.get_context_data()
        context['user'] = user
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        user_id = self.request.POST.get('user_id')
        user = get_object_or_404(User, pk=user_id)
        return HttpResponseRedirect(reverse('superuserhome:userinformation_detail', kwargs={'user_id': user_id}))


class DeductionOutputView(TemplateView):
    # ! for test to use User Model 
    
    def post(self, request, *args, **kwargs):
        # CSVデータを生成
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="users.csv"'

        # CSVライターを初期化
        writer = csv.writer(response)
        
        # ヘッダー行を書き込む
        writer.writerow(['Deduction Information'])

        # データを書き込む
        # URLからuser_idを取得
        user_id = kwargs.get('user_id')
        user = get_object_or_404(User, pk=user_id)
        writer.writerow([user.name])

        return response

class TestView(TemplateView):
    model = User
    fields = ('user_id', 'name')
    template_name = "Edit/test.html"
    success_url = reverse_lazy('superuserhome')

    def get(self, request, *args, **kwargs):
        data_from_database = User.objects.all()
        return render(request, self.template_name, {'data_from_database': data_from_database})
    

class OldItemView(TemplateView):
    model = Item
    template_name = "Edit/Item/olditem.html"
    fields =('name')



    def get(self, request, *args, **kwargs):
        object_list = Item.objects.all()
        return render(request, self.template_name, {'object_list':object_list})
    
    