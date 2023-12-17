from django.db import models

# Create your models here.
class User(models.Model):
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
    name = models.CharField(max_length=100)
    item_url = models.URLField(blank = True,null = True)
    count = models.PositiveIntegerField(default = 0)
    buy_date = models.DateField(blank = True,null = True)
    #shop = models.ForeignKey(Shop,blank = True,null = True,verbose_name = 'shop',on_delete = models.PROTECT)
    buy = models.BooleanField(default = False)
    
    def __str__(self):
        return '{}({})'.format(self.name,self.buy_date)
    
class PurchaseHistory(models.Model):
    # 外部キー
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    # 購入月
    buy_month = models.PositiveIntegerField(default = 1)
    # その月の購入額
    buy_amount = models.PositiveIntegerField(default = 0)


    def __str__(self):
        return '{} : {}月'.format(self.user_id,self.buy_month)
    
    