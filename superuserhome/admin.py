from django.contrib import admin
from .models import Item,PurchaseHistory,Company,Order,ImageUpload, BuyHistory

# Register your models here.

admin.site.register(Item)
admin.site.register(PurchaseHistory)
admin.site.register(Company)
admin.site.register(Order)
admin.site.register(ImageUpload)
admin.site.register(BuyHistory)