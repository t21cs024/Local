from .models import User,Item,PurchaseHistory,Company
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls.base import reverse_lazy
from .forms import SignUpForm,UserIdForm,ItemBuy,MonthForm
#CSV関連
import csv
# test
from django.http import HttpResponse
# 発注メール送信関連
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import F
from datetime import datetime, timedelta
# test
from pip._vendor.typing_extensions import Self
import qrcode
import os

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
    fields = ('name', 'item_url', 'count', 'price', 'buy_date')
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
        context = self.get_context_data()
        context['user'] = user
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        user_id = self.request.POST.get('user_id')
        get_object_or_404(User, user_id=user_id)
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

        # オブジェクトの取得 見つからない場合は404
        user = get_object_or_404(User, pk=user_id)
        history = get_object_or_404(PurchaseHistory, user_id=user, buy_month=buy_month)

        # CSVデータ生成
        response = HttpResponse(content_type='text/csv')
        # CSVデータを生成
        response['Content-Disposition'] = 'attachment; filename="Salary_information.csv"'
        writer = csv.writer(response)
        
        # データ書き込み（必要に応じて追加）
        header = ['社員番号','氏名','購入月','控除額']
        writer.writerow(header)
        body = [user.user_id, user.name, history.buy_month, history.buy_amount]
        writer.writerow(body)
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
    
class OrderConfirmedView(TemplateView):
    template_name = "Order/buy_item.html"

    def get(self, request):
        # 在庫が重み付けによって決められた個数未満であり、発注メールを送信していないItemオブジェクトを取得
        items_below_amount = Item.objects.filter(count__lt=F('minimum_amount'), send_email = False)
        # 条件に該当するオブジェクトが存在する場合、発注メール送信メソッド呼び出し
        if items_below_amount.exists():
            self.send_order_mail(request, items_below_amount)
        return redirect('userhome:buyitem')

    def send_order_mail(self, request, items_below_amount):
        # 自社（発注元企業）オブジェクトの取得 見つからない場合は404(発注元企業のIDは1を想定)
        own_company = get_object_or_404(Company, company_id = 1)
        # 発注先企業オブジェクトの取得 見つからない場合は404(発注企業のIDは2を想定)
        supplier_company = get_object_or_404(Company, company_id = 2)

        """題名"""
        subject = f"商品注文のお願い（{own_company.company_name})"
        """本文"""
        message = (
            f"{supplier_company.company_name}\n"
            f"ご担当　{supplier_company.manager_name}様\n"
            "\n"
            "いつもお世話になっております。\n"
            f"{own_company.company_name}の{own_company.manager_name}でございます。\n"
            "\n"
            "このたびは貴社の商品を発注したく連絡いたしました。\n"
            "なお、具体的には以下の内容にて発注を考えており、ご了承いただいたのち注文書を発行いたします。ご確認いただければ幸いです。\n"
            )
        roop_count = 0
        for item in items_below_amount:
            # 発注する商品が複数ある場合
            if items_below_amount.count() >= 2:
                message += (
                    "\n"
                    f"商品{roop_count+1}：\n"
                    )
            else:
                message += ("\n")
            message += (
                f"・商品名　：{item.name}\n"
                f"・商品ID　：{item.id}\n"
                f"・数　量　：{item.order_quantity}\n"
                )
            # 発注メールを送信したitemはフラグを立てておく（重複メール送信を防ぐため）
            # 商品が到着し、在庫情報追加する際Falseに戻してください
            item.send_email = True
            item.save()
            roop_count+=1

        # 現在の日付から納品希望日の計算（発注メールを送信した１週間後を指定）
        delivery_date = datetime.now() + timedelta(weeks=1)
        # フォーマットを整える
        desired_delivery_date = delivery_date.strftime("%Y年%m月%d日")
        if items_below_amount.count() >= 2:
            message += "\n"
        message += (
            f"・納入場所：弊社  {own_company.company_name}（住所：{own_company.company_address}）\n"
            f"・納品希望日：{desired_delivery_date}\n"
            "\n"
            "ご不明な点がございましたら、"
            f"担当の{own_company.manager_name}（連絡先：{own_company.manager_phone_number} / {own_company.manager_mail}）までご連絡くださいませ。\n"
            "何卒、よろしくお願い申し上げます。\n"
            "\n"
            "────────────────────────\n"
            f"{own_company.company_name}\n"
            f"{own_company.manager_name}\n"
            f"{own_company.company_address}\n"
            f"TEL：{own_company.manager_phone_number}\n"
            f"Email：{own_company.manager_mail}\n"
            "URL：https://www.ycc.co.jp/\n"
            "────────────────────────\n"
            )

        """送信元メールアドレス（企業DBから取得）"""
        from_email = own_company.company_mail

        """宛先メールアドレス（企業DBから取得）"""
        recipient_list = [
            supplier_company.company_mail
            ]
        send_mail(subject, message, from_email, recipient_list)    
    
class CompanyManagementView(ListView):
    model = Company
    template_name = 'Edit/company_management.html'
    success_url = 'superuserhome/'

class CompanyAddView(CreateView):
    model = Company
    fields = ('company_id', 'company_name', 'company_address', 'company_mail', 'company_phone_number', 'manager_name','manager_phone_number','manager_mail')
    template_name = 'Edit/company_add.html'
    success_url = reverse_lazy('superuserhome:companymanage')

class CompanyEditView(UpdateView):
    model = Company
    fields = ('company_id', 'company_name', 'company_address', 'company_mail', 'company_phone_number', 'manager_name','manager_phone_number','manager_mail')
    template_name = 'Edit/company_edit.html'
    success_url = reverse_lazy('superuserhome:companymanage')

class CompanyDeleteView(DeleteView):
    model = Company
    template_name = 'Edit/company_delete.html'
    success_url = reverse_lazy('superuserhome:companymanage')    


class QrCodeView(TemplateView):
    model = Item
    template_name = "Edit/Item/qrcode/qrcode.html"
    
    def get(self, request, *args, **kwargs):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(str('item_id'))
        qr.make(fit=True)

        # 生成したQRコードをHttpResponseに設定
        img = qr.make_image(fill_color="black", back_color="white")
        response = HttpResponse(content_type="image/png")
        img.save(response, format="PNG")
            
        return response
    
        
    
    
    