'''
Created on 2024/01/10

@author: t21cs011
'''
from django import forms
from .models import Item

class ItemBuy(forms.Form):
    status = (
            (0, '未購入'),
            (1, '購入済')
            )
    item_id = forms.IntegerField(label='ID')
    item_status = forms.ChoiceField(label='STATUS',widget=forms.Select, choices=status)


class ItemIdForm(forms.Form):
    item_id = forms.IntegerField(label='ID')

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'price', 'count']