from .models import Item,PurchaseHistory,Company,Order,ImageUpload
from login.models import CustomUser
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls.base import reverse_lazy
from .forms import UserIdForm,ItemBuy,MonthForm,CountForm,ImageUploadForm
#CSV関連
import csv
# test
from django.http import HttpResponse
# 発注関連
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import F, Q
from datetime import timedelta, date
from decimal import Decimal
# test
from pip._vendor.typing_extensions import Self
# import qrcode
import os

# Create your views here.  

def delete_image(request, image_title):
    # プライマリーキーを使ってオブジェクトを取得
    image_upload_instance = get_object_or_404(ImageUpload, pk=image_title)

    # オブジェクトを削除
    image_upload_instance.img.delete()  # 画像ファイルを削除
    image_upload_instance.delete()      # データベースからオブジェクトを削除
    
    return redirect('superuserhome:olditem')  # 成功したら指定のURLにリダイレクト
    # return HttpResponse("Image deleted successfully.")

class SuperUserHomeView(TemplateView):
    model = CustomUser
    template_name = 'superuser_home.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})
    
class UserEditView(TemplateView):
    model = CustomUser
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
    fields = ('name', 'item_url', 'count', 'price', 'state')
    template_name = "Edit/Item/newitem.html"
    success_url = '/superuserhome/orderedit'

    # 新しいItemを追加したとき，それを外部キーにもつOrderも同時に生成
    def form_valid(self, form):
        # Itemのインスタンスを作成・保存
        item = form.save()
        # Orderのインスタンス作成・保存 その他のフィールドはデフォルト値，またはnullに設定する
        order = Order(item=item)
        order.save()
        return super().form_valid(form)
    
    #ラベルを日本語に
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['name'].label = '商品名' 
        form.fields['item_url'].label = '画像URL'
        form.fields['count'].label = '在庫数'
        form.fields['price'].label = '単価'
        form.fields['state'].label = '状態'
        return form
    
"""
class SignUpView(TemplateView):
    model = User
    fields = ('emp_num', 'name','user_menu', 'user_pass', 'user_mail','user_authority')
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
                emp_num=form.cleaned_data['id'],
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
"""    
    

class UserInformationView(TemplateView):
    model = CustomUser
    template_name = "Edit/userinformation.html"
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        # エラーメッセージを取得
        error_message = messages.get_messages(request)
        context['error_message'] = error_message
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        emp_num = self.request.POST.get('emp_num')
        # 該当するユーザが見つからない場合は再度入力を促す
        try:
            CustomUser.objects.get(emp_num=emp_num)
        except (CustomUser.DoesNotExist):
            messages.error(request, '該当するユーザが見つかりませんでした。再度入力してください。', extra_tags='nouser-error')
            return redirect('superuserhome:userinformation')
        
        return HttpResponseRedirect(reverse('superuserhome:userinformation_detail', kwargs={'emp_num': emp_num}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_id'] = UserIdForm()
        return context
    
    
class UserInformationDetailView(TemplateView):
    model = CustomUser
    template_name = "Edit/userinformation_detail.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_id'] = UserIdForm()
        context['form_month'] = MonthForm()
        return context
    def get(self, request, *args, **kwargs):
        emp_num = self.kwargs.get('emp_num')
        user = get_object_or_404(CustomUser, emp_num=emp_num)
        context = self.get_context_data()
        context['user'] = user
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        emp_num = self.request.POST.get('emp_num')
        get_object_or_404(CustomUser, emp_num=emp_num)
        return HttpResponseRedirect(reverse('superuserhome:userinformation_detail', kwargs={'emp_num': emp_num}))

class PreDeductionOutputView(TemplateView):
    
    def post(self, request, *args, **kwargs):
        # URLからemp_numを取得
        emp_num = kwargs.get('emp_num')
        # buy_monthを取得
        buy_month = self.request.POST.get('buy_month')  

        # フォームにbuy_monthが含まれている場合,控除情報出力ページにリダイレクト
        if buy_month:
            return HttpResponseRedirect(reverse('superuserhome:redeductionoutput', kwargs={'emp_num': emp_num, 'buy_month': buy_month}))
        else:
            # フォームが無効な場合は再度入力を促す
            messages.error(request, 'フォームが無効です。再度入力してください。')
            return redirect('superuserhome:userinformation_detail', emp_num=emp_num)


class DeductionOutputView(TemplateView):
    template_name = 'deduction_output.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_month'] = MonthForm()
        return context
    
    def get(self, request, *args, **kwargs):
        # URLからemp_num,buy_monthを取得
        emp_num = kwargs.get('emp_num')
        buy_month = kwargs.get('buy_month')

        # オブジェクトの取得 見つからない場合は404
        user = get_object_or_404(CustomUser, emp_num=emp_num)
        history = get_object_or_404(PurchaseHistory, user=user, buy_month=buy_month)

        # CSVデータ生成
        response = HttpResponse(content_type='text/csv')
        # CSVデータを生成
        response['Content-Disposition'] = 'attachment; filename="Salary_information.csv"'
        writer = csv.writer(response)
        
        # データ書き込み（必要に応じて追加）
        header = ['社員番号','氏名','購入月','控除額']
        writer.writerow(header)
        body = [user.emp_num, user.name, history.buy_month, history.buy_amount]
        writer.writerow(body)
        return response

class TestView(TemplateView):
    model = CustomUser
    fields = ('emp_num', 'name')
    template_name = "Edit/test.html"
    success_url = reverse_lazy('superuserhome')

    def get(self, request, *args, **kwargs):
        data_from_database = CustomUser.objects.all()
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
        """
        購入によって在庫数をデクリメントする処理をここに記述
        （ stateの変更は下記で行うため不要です ）
        """
        # 在庫が重み付けによって決められた個数未満であり、発注メールを送信していないOrderオブジェクトを外部キーを通して取得
        items_below_amount = Order.objects.filter(item__count__lt=F('minimum_amount'), item__state = 'in stock')
        # 在庫数0以下で，stateが"売り切れ"になっていない商品オブジェクトを取得
        items_out_of_stock = Item.objects.filter( Q(count__lte = 0) & (Q(state = 'in stock')|Q(state = 'ordered')) )
        # 条件に該当するオブジェクトが存在する場合、重み増加メソッド呼び出し
        if items_out_of_stock.exists():
            self.increase_weight(request, items_out_of_stock)
        # 条件に該当するオブジェクトが存在する場合、発注メール送信メソッド呼び出し
        if items_below_amount.exists():
            self.send_order_mail(request, items_below_amount)
        # 重みで変更した発注数をメール内容に反映させるため，メールを送信してから在庫数0の商品は状態を「売り切れ」にする
        if items_out_of_stock.exists():
            # 購入によって在庫が0になった商品の重みを増やしたら，状態を"売り切れ"にする
            for item in items_out_of_stock:
                item.state = 'sold out'
                item.save()
        return redirect('userhome:buyitem')
    
    def increase_weight(self, request, items_out_of_stock):
        for item in items_out_of_stock:
            # idを外部キーとしてOrderオブジェクトの取得 見つからない場合は404
            order = get_object_or_404(Order, pk=item.id)
            if order.last_sold_out_date is not None:
            # 前回の売り切れ日からの差が小さいほど1に近い値を加える．最低でも0.5を加える
                date_difference = date.today() - order.last_sold_out_date
                # 傾き
                a = -3/(40**2)
                increase = a*(date_difference.days)**2 + 1
                if increase <= 0:
                    increase = 0.5
            else:
                # 前回の売り切れ日データがないときも0.5加える
                increase = 0.5
            order.order_weight += Decimal(increase)
            if order.order_weight >= 2.00:
                # 重みの最大値は2.00とする
                order.order_weight = 2.00
                # 重みの更新を行った結果1.00以下ならば1.20に補正（発注個数が増えるように補正）
            elif order.order_weight <= 1.00:
                order.order_weight = 1.20
                # 前回の売り切れ日を今日にする
            order.last_sold_out_date = date.today()
            # 重みの更新
            order.order_quantity *= order.order_weight
            order.save()    

    def send_order_mail(self, request, items_below_amount):
        # 自社（発注元企業）オブジェクトの取得 見つからない場合は404(発注元企業のIDは1を想定)
        own_company = get_object_or_404(Company, id = 1)
        # 発注先企業オブジェクトの取得 見つからない場合は404(発注企業のIDは2を想定)
        supplier_company = get_object_or_404(Company, id = 2)
        
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
        for order_item in items_below_amount:
            # Orderからidを外部キーとしてItemオブジェクトの取得 見つからない場合は404
            item = get_object_or_404(Item, pk=order_item.id)
            # 発注する商品が複数ある場合と１つの場合で分岐（本文の体裁のため）
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
                f"・数　量　：{order_item.order_quantity}\n"
                )
            # 発注メールを送信したitemはOrderにフラグを立てておく（重複メール送信を防ぐため）
            # 商品が到着し、在庫情報追加する際state = 'in stock'に
            item.state = 'ordered'
            item.save()
            roop_count+=1

        # 今日の日付から納品希望日の計算（発注メールを送信した１週間後を指定）
        delivery_date = date.today() + timedelta(weeks=1)
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
    fields = ('company_name', 'company_address', 'company_phone_number', 'company_mail' ,'manager_name','manager_phone_number','manager_mail')

    template_name = 'Edit/company_add.html'
    success_url = reverse_lazy('superuserhome:companymanage')
    
    #ラベルを日本語に
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['company_name'].label = '企業名'
        form.fields['company_address'].label = '住所'
        form.fields['company_mail'].label = '企業Email'
        form.fields['company_phone_number'].label = '企業TEL'
        form.fields['manager_name'].label = '担当者名'
        form.fields['manager_phone_number'].label = '担当者TEL'
        form.fields['manager_mail'].label = '担当者Email'
        return form

class CompanyEditView(UpdateView):
    model = Company
    fields = ('company_name', 'company_address', 'company_phone_number', 'company_mail' ,'manager_name','manager_phone_number','manager_mail')
    template_name = 'Edit/company_edit.html'
    success_url = reverse_lazy('superuserhome:companymanage')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['company_name'].label = '企業名'
        form.fields['company_address'].label = '住所'
        form.fields['company_mail'].label = '企業Email'
        form.fields['company_phone_number'].label = '企業TEL'
        form.fields['manager_name'].label = '担当者名'
        form.fields['manager_phone_number'].label = '担当者TEL'
        form.fields['manager_mail'].label = '担当者Email'
        return form

class CompanyDeleteView(DeleteView):
    model = Company
    template_name = 'Edit/company_delete.html'
    success_url = reverse_lazy('superuserhome:companymanage')

class ItemDiscardView(TemplateView):
    template_name = 'Edit/Item/itemediscard.html'

    def get(self, request, *args, **kwargs):
        item_id = self.kwargs.get('item_id')
        item = get_object_or_404(Item, pk=item_id)
        context = self.get_context_data()
        context['item'] = item
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        item_id = self.request.POST.get('item_id')
        item = Item.objects.get(pk=item_id)
        context = super().get_context_data(**kwargs)
        context['form_count'] = CountForm()
        context['item'] = item
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_count'] = CountForm()
        return context

class ItemStockEditView(ItemDiscardView):
    template_name = 'Edit/Item/itemstockedit.html'
    # テンプレートだけ異なり，メソッドは同様なのでItemDiscardViewを継承

class ItemInventoryControlView(TemplateView):
    def post(self, request, *args, **kwargs):
        # urlからitem id，item idからItemオブジェクト，postからクリックされたボタンの種類を取得
        item_id = self.kwargs.get('item_id')
        item = Item.objects.get(pk=item_id)
        action = request.POST.get('action')
        # クリックされたボタンに対応した在庫操作を行う
        if action == "alldiscard":
            self.discard(request, item, item.count)
        else:
            # 「在庫追加」または「廃棄」ボタンがクリックされた場合，フォームから個数を取り出し在庫操作
            count = self.request.POST.get('count')
            if action == "addstock":
                self.addstock(item, int(count))
            elif action == "discard":
                self.discard(request, item, int(count))
        return redirect('superuserhome:olditem')

    def addstock(self, item, count):
        # フォームで送信された個数分在庫をインクリメント
        item.count += count
        # idを外部キーとしてOrderオブジェクトの取得 見つからない場合は404
        order = get_object_or_404(Order, pk=item.id)
        # 在庫数が発注メールが送信される個数以上になった場合に状態を「在庫あり」に
        if order.minimum_amount <= item.count:
            item.state = 'in stock' 
        item.save()  

    def discard(self, request, item, count):
        # フォームで送信された個数分在庫をデクリメント
        if item.count <= count:
            self.decrease_weight(request, item, item.count)
        # 在庫がマイナスになるのを防ぐ
            item.count = 0
        else:
            self.decrease_weight(request, item, count)
            item.count -= count
            item.save()
        # idを外部キーとしてOrderオブジェクトの取得 見つからない場合は404
        order = get_object_or_404(Order, pk=item.id)
        if item.count < order.minimum_amount:
            # 廃棄によって規定の個数未満であり、発注メールを送信していないOrderオブジェクトを外部キーを通して取得
            items_below_amount = Order.objects.filter(item = item, item__state = "in stock")
            if items_below_amount.exists():
                # 条件に該当するオブジェクトが存在する場合、発注メール送信メソッド呼び出し
                OrderConfirmedView().send_order_mail(request,items_below_amount)
            # 状態の上書き
        if item.count == 0:
            item.state = 'sold out'
            item.save()

    def decrease_weight(self, request, item, count):
        # 在庫数が0の商品を破棄しても重みの更新は行わない
        if item.count != 0:
            # idを外部キーとしてOrderオブジェクトの取得 見つからない場合は404
            order = get_object_or_404(Order, pk=item.id)
            # 廃棄個数から，重みを減らす値を決定する
            decrease = Decimal(count/100)
            before_order_quantity = order.order_quantity
            order.order_weight -= decrease
            if order.order_weight >= 1.00:
                # 廃棄されたら発注個数が減るように補正
                order.order_weight = 0.85
            elif order.order_weight <= 0.01:
                # 重みの最小値は0.01とする
                order.order_weight = 0.01
            # 発注個数の更新
            order.order_quantity *= order.order_weight
            # 発注最低個数の更新(発注個数最低個数（発注個数より減少は緩やかにする）
            order.minimum_amount -= order.order_weight * 10
            if order.minimum_amount <= 10:
                order.minimum_amount = 10
            # 重み減少が少なく，発注個数が変化していなければ補正
            if before_order_quantity <= order.order_quantity:
                order.order_quantity -= 1
            # 発注メールが送信される個数未満に発注個数をしない
            if order.order_quantity <= order.minimum_amount:
                order.order_quantity = order.minimum_amount
            order.save()

class ImageUploadView(CreateView):
    template_name = "Edit/Item/image_upload.html"
    form_class = ImageUploadForm
    success_url = "/superuserhome/orderedit"

class ItemEditView(UpdateView):
    model = Item
    fields = ('name','item_url','count' ,'price','state')
    template_name = "Edit/Item/olditem_edit.html"
    success_url = reverse_lazy('superuserhome:olditem')

    #ラベルを日本語に
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['name'].label = '商品名' 
        form.fields['item_url'].label = '画像URL'
        form.fields['count'].label = '在庫数'
        form.fields['price'].label = '単価'
        form.fields['state'].label = '状態'
        return form


class ItemDeleteView(DeleteView):
    model = Item
    template_name = "Edit/Item/olditem_delete.html"
    success_url = reverse_lazy('superuserhome:olditem')


class QrCodeView(TemplateView):
    model = Item
    template_name = "Edit/Item/qrcode/qrcode.html"
    
    def get(self, request, item_id, *args, **kwargs):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(str(item_id))
        qr.make(fit=True)

        # 生成したQRコードをHttpResponseに設定
        img = qr.make_image(fill_color="black", back_color="white")
        """
        response = HttpResponse(content_type="image/png")
        img.save(response, format="PNG")

        return response
