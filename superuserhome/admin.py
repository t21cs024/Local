from django.contrib import admin
from .models import User,Item,PurchaseHistory,Company,Order

# Register your models here.

admin.site.register(User)
admin.site.register(Item)
admin.site.register(PurchaseHistory)
admin.site.register(Company)
admin.site.register(Order)
