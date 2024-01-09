from django.db import models
from django.template.defaultfilters import default
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

def savePath(instance, filename):
    ext = filename.split('.')[-1]
    new_name = instance.title
    return f'img/{new_name}.{ext}'

class User(models.Model):
    '''
    データ例
    
    User id   ：1
    Name      ：a
    User name ：a
    User pass ：a
    User mail ：a@gmail.com
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
    
    Name     ：apple
    Item url ：apple.png
    Count    ：10
    Buy date ：2023-12-20
    Price    ：100
    State ：在庫あり
    '''
    name = models.CharField(max_length=100)
    item_url = models.URLField(blank = True,null = True)
    count = models.PositiveIntegerField(default = 0)
    price = models.PositiveIntegerField(default = 100)
    # 商品の状態を管理する（商品が届き,在庫情報を変更する際"在庫あり"にされることを想定）
    STATE_CHOICES = [
        ('in stock', '在庫あり'),
        ('sold out', '売り切れ'),
        ('ordered', '発注済み'),
    ]
    state = models.CharField(max_length=10, choices=STATE_CHOICES, default='in stock')

    def __str__(self):
        return '{}({})'.format(self.name, self.get_state_display())

# 発注DB   
class Order(models.Model):
    '''
    データ例
    Item           ：apple(登録されているItem)
    Order weight   ：1.00
    Order quantity ：50
    Minimum amount ：10
    '''
    # 外部キー(一意)
    item = models.OneToOneField(Item, on_delete=models.CASCADE, null = True)
    # 発注重み(三桁未満の小数 重みの最小値は0.01であり，0未満にならない)
    order_weight = models.DecimalField(max_digits = 3, decimal_places = 2, validators = [MinValueValidator(0.01) ,MaxValueValidator(2.00)], default = 1)
    # 発注個数（重み付けで変更されることを想定）
    order_quantity = models.PositiveIntegerField(default = 50)
    # 最低個数：在庫がこれ以下になった商品を発注する
    minimum_amount = models.PositiveIntegerField(default = 10)
    # 前回の売り切れ日（商品登録する際はnullを想定）
    last_sold_out_date = models.DateField(blank = True, null = True)

    def __str__(self):
        return '{} [発注重み:{}] '.format(self.item, self.order_weight)

class PurchaseHistory(models.Model):
    '''
    データ例
    User id ：a(登録されているUser)
    Buy month ：1
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
    
class ImageUpload(models.Model):
    title = models.CharField(max_length=100, primary_key=True)
    img = models.ImageField(upload_to=savePath)#こちらの通り

    def __str__(self):
        return self.title

# 企業
class Company(models.Model):
    '''
    データ例
    Company id      ：1  (１は自社、２は発注企業）
    Company name    ：株式会社ワイ・シー・シー
    Company address ：111
    Company mail    ：t21cs○○○@gmail.com （!!必ず自分で管理できるメールアドレスにしてください。id=1送信元メールアドレス、id=2送信先メールアドレス）
    （id=1で登録する送信元メールアドレスは、user.txtで記述したメールアドレスと同一のものとしてください）
    （id=2で登録する送信先メールアドレスは，gmail以外でも大丈夫です）
    Company phone number    ：111
    Manager name    ：田中太郎
    Manager phone number：1111        （署名に使用）
    Manager mail    ：tanaka@gmail.com    （署名に使用。こちらのメールアドレスは適当でいいです）
    '''
    # 企業ID(unique=True 同ユーザーIDの複数回登録を防止)
    company_id = models.PositiveIntegerField(default=1,unique = True)
    # 企業名
    company_name = models.CharField(blank = True, max_length=50)
    # 企業住所
    company_address = models.CharField(blank = True, max_length=100)
    # 企業メールアドレス
    company_mail = models.EmailField()
    # 企業電話番号
    company_phone_number = models.CharField(max_length=15)
    # 担当者名
    manager_name = models.CharField(blank = True, max_length=50)
    # 担当者電話番号
    manager_phone_number = models.CharField(max_length=15)
    # 担当者メールアドレス
    manager_mail = models.EmailField()

    def __str__(self):
        return '{}'.format(self.company_name)

