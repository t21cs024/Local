#from django.views.generic import ListView
from .models import User,Item,PurchaseHistory
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
from .forms import SignUpForm,UserIdForm,ItemBuy,MonthForm
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
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        # エラーメッセージを取得
        error_message = messages.get_messages(request)
        context['error_message'] = error_message
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        user_id = self.request.POST.get('user_id')
        #user = get_object_or_404(User, user_id=user_id)
        # user_idが存在しない場合はHTTP 404 Not Found
                # 購入履歴が見つからない場合は再度入力を促す
        try:
            User.objects.get(pk=user_id)
        except (User.DoesNotExist):
            messages.error(request, '該当するユーザが見つかりませんでした。再度入力してください。')
            return redirect('superuserhome:userinformation')
        
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
        context['form_month'] = MonthForm()
        return context

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        user = get_object_or_404(User, pk=user_id)
        history = get_object_or_404(PurchaseHistory, pk=user_id)
        context = self.get_context_data()
        context['user'] = user
        context['history'] = history
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        user_id = self.request.POST.get('user_id')
        user = get_object_or_404(User, pk=user_id)
        return HttpResponseRedirect(reverse('superuserhome:userinformation_detail', kwargs={'user_id': user_id}))

from django.contrib import messages

class PreDeductionOutputView(TemplateView):
    
    def post(self, request, *args, **kwargs):
        # URLからuser_idを取得
        user_id = kwargs.get('user_id')
        # buy_monthを取得
        buy_month = self.request.POST.get('buy_month')  

        # フォームにbuy_monthが含まれている場合,控除情報出力ページにリダイレクト
        if buy_month:
            return HttpResponseRedirect(reverse('superuserhome:redeductionoutput', kwargs={'user_id': user_id, 'buy_month': buy_month}))
        else:
            # フォームが無効な場合は再度入力を促す
            messages.error(request, 'フォームが無効です。再度入力してください。')
            return redirect('superuserhome:userinformation_detail', user_id=user_id)


class DeductionOutputView(TemplateView):
    template_name = 'deduction_output.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_month'] = MonthForm()
        return context
    
    def get(self, request, *args, **kwargs):
        
        # URLからuser_id,buy_monthを取得
        user_id = kwargs.get('user_id')
        buy_month = kwargs.get('buy_month')

        # 購入履歴が見つからない場合は再度入力を促す
        user = get_object_or_404(User, pk=user_id)
        history = get_object_or_404(PurchaseHistory, user_id=user, buy_month=buy_month)
        '''
        try:
            user = User.objects.get(pk=user_id)
            history = PurchaseHistory.objects.get(user_id=user, buy_month=buy_month)
        except (PurchaseHistory.DoesNotExist):
            return redirect('superuserhome:userinformation_detail', user_id=user_id)
        '''
        # CSVデータを生成
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="users.csv"'
        writer = csv.writer(response)
        
        # ヘッダー
        writer.writerow(['Deduction Information'])
        # csvに書き込むデータ群（必要に応じて追加）
        user_data = [user.user_id, user.name, history.buy_month, history.buy_amount]
        writer.writerow(user_data)
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
    
    