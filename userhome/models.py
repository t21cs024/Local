from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    user_menu = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=100)
    item_url = models.URLField(blank = True,null = True)
    count = models.PositiveIntegerField(default = 0)
    buy_date = models.DateField(blank = True,null = True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) 
    buy = models.BooleanField(default = False)
    
    def __str__(self):
        return '{}({})'.format(self.name,self.buy_date)
    
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, through='CartItem')

    def __str__(self):
        return f"{self.user.name} さんのカート"

    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.item.name} in {self.cart}"
    
#class BuyHistory(models.Model):
    