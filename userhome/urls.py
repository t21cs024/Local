'''
Created on 2023/12/08

@author: t21cs011
'''
from django.urls import path
from .views import UserHomeView ,BuyItemView ,BuyHistoryView ,change_password, CartContentsView,AddToCartView
from superuserhome.views import OrderConfirmedView
from userhome.views import AddToCartView
'''
from .views import ItemList, ItemAddView, ItemShowView, ItemEditView, ItemDeleteView
'''
app_name = 'userhome'
urlpatterns = [
    path('',UserHomeView.as_view()),
    path('buyitem/',BuyItemView.as_view(), name='buyitem'),
    path('buyitem/<int:item_id>',AddToCartView.as_view(),name='addtocart'),
    path('buyhistory/',BuyHistoryView.as_view(),name='buyhistory'),
    path('changepass/',change_password, name='changepass'),
    path('buyitem/cartcontents/',CartContentsView.as_view(), name='cartcontents'),
    path('sendordermail/',OrderConfirmedView.as_view(), name='sendordermail'),
       ]

