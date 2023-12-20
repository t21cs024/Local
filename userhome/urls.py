'''
Created on 2023/12/08

@author: t21cs011
'''
from django.urls import path
from .views import UserHomeView ,BuyItemView ,BuyHistoryView ,change_password, CartContentsView
'''
from .views import ItemList, ItemAddView, ItemShowView, ItemEditView, ItemDeleteView
'''
app_name = 'userhome'
urlpatterns = [
    path('',UserHomeView.as_view()),
    path('buyitem/',BuyItemView.as_view(), name='buyitem'),
    path('buyhistory/',BuyHistoryView.as_view(),name='buyhistory'),
    path('changepass/',change_password, name='changepass'),
    path('cartcontents/',CartContentsView.as_view(), name='cartcontents'),
       ]

