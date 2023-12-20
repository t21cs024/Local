from django.db import models
from django.template.defaultfilters import default

# Create your models here.
class User(models.Model):
    '''
    データ例
    User id：1
    Name：a
    User name：a
    User pass：a
    User mail：a@gmail.com
    User authority：False
    '''
    # unique=True 同ユーザーIDの複数回登録を防止
    user_id = models.IntegerField(unique = True)
    name = models.CharField(max_length = 100)
    user_name = models.CharField(max_length = 30, null = True, unique = True)
    user_pass = models.CharField(max_length = 100, null = True)
    user_mail = models.EmailField(blank = False, null = True)
    user_authority = models.BooleanField(default = False) 
    
    def __str__(self):
        return self.name
    
    
class Item(models.Model):
    '''
    データ例
    Name：apple
    Item url：apple.png
    Count：10
    Buy date：2023-12-20
    Price：100
    Buy：False    
    Order quantity：5
    Minimum amount：5
    Send email：False
    '''
    name = models.CharField(max_length=100)
    item_url = models.URLField(blank = True,null = True)
    count = models.PositiveIntegerField(default = 0)
    buy_date = models.DateField(blank = True,null = True)
    #shop = models.ForeignKey(Shop,blank = True,null = True,verbose_name = 'shop',on_delete = models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    buy = models.BooleanField(default = False)
    
    # 以下は発注メール送信機能のため追加したフィールド
    # 発注個数（重み付けで変更されることを想定）
    order_quantity = models.PositiveIntegerField(default = 5)
    # 最低個数：在庫がこれ以下になった商品を発注する（重み付けで変更されることを想定）
    minimum_amount = models.PositiveIntegerField(default = 5)
    # 発注メールを送信したかを管理するフラグ（商品が届き,在庫情報を変更する際Falseに戻されることを想定）
    send_email = models.BooleanField(default = False)
    
    def __str__(self):
        return '{}({})'.format(self.name,self.buy_date)

class PurchaseHistory(models.Model):
    '''
    データ例

    User id：1
    Buy month：1
    Buy amount：1000
    '''
    # 外部キー
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    # 購入月
    buy_month = models.PositiveIntegerField(default = 1)
    # その月の購入額
    buy_amount = models.PositiveIntegerField(default = 0)

    def __str__(self):
        return '{} : {}月'.format(self.user_id,self.buy_month)
    
# 商品を発注する企業（１社と想定）
class OrderingCompany(models.Model):
    '''
    データ例

    Company id：1    (必ず１としてください）
    Company name：abc
    Company address：111
    Company mail：t21cs〇○○@gmail.com    （自分で管理できるメールアドレスにしてください）
    Phone number：111
    '''
    # 企業ID
    company_id = models.PositiveIntegerField(default = 1)
    # 企業名
    company_name = models.CharField(max_length=50)
    # 住所
    company_address = models.CharField(max_length=50)
    # メールアドレス
    company_mail = models.EmailField(blank = False, null = True)
    # 電話番号
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return '{}'.format(self.company_name)

