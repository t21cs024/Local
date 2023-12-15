'''
Created on 2023/12/15

@author: t21cs011
'''
from django import forms
from .models import User,Item

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
        fields = ['name', 'item_url', 'count', 'buy_date']

class SignUpForm(forms.Form):
    id = forms.CharField(label='ID', required=True)
    full_name = forms.CharField(label='氏名', required=True)
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput, required=True)
    email = forms.EmailField(label='メールアドレス', required=True)
    authority = forms.BooleanField(label='権限', required=False)

    # 他のフィールドも適切に追加

class UserIdForm(forms.Form):
    user_id = forms.IntegerField(label='ID')