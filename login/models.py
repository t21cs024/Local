from django.db import models
from django.contrib.auth.models import (BaseUserManager,
                                        AbstractBaseUser,
                                        PermissionsMixin)
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def _create_user(self, account_id, password, **extra_fields):
        user = self.model(account_id=account_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, account_id, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(
            account_id=account_id,
            password=password,
            **extra_fields,
        )

    def create_superuser(self, account_id, password, **extra_fields):
        extra_fields['is_active'] = True
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        return self._create_user(
            account_id=account_id,
            password=password,
            **extra_fields,
        )
        
'''
データ例
    
所属が総務人事部またはsuperuser（createsuperuesrで作成したユーザ）ならsuperuserhomeに遷移．
それ以外の所属はuserhome

ユーザ名  ：t21cs1
社員番号  ：100
名前      ：長坂　太郎
メールアドレス  ：100YCC@x.com    
所属　　　      ：総務人事部
パスワード　　　　：@@@@aaaa
パスワード(確認用)：@@@@aaaa
'''

class CustomUser(AbstractBaseUser, PermissionsMixin):
    # 社員番号
    emp_num = models.IntegerField(
        verbose_name=_("emp_num"),
        null=True,
        unique=True,
    )
    
    name = models.CharField(
        verbose_name=_("name"),
        max_length=150,
    )
    
    account_id = models.CharField(
        verbose_name=_("account_id"),
        unique=True,
        max_length=10
    )
    
    email = models.EmailField(
        verbose_name=_("email"),
        unique=True
    )
    
    # 所属
    AFFILIATION_CHOICES = [
        ('HR', '総務人事部'),
        ('Sales', '営業部'),
        ('1st system', '第一システム部'),
        ('2nd system', '第二システム部'),
        ('3rd system', '第三システム部'),
        ('others', 'その他'),
    ]
    affiliation = models.CharField(
        max_length=10, 
        verbose_name=_("affiliation"),
        choices=AFFILIATION_CHOICES,
         default='Sales')
    
    is_superuser = models.BooleanField(
        verbose_name=_("is_superuer"),
        default=False
    )
    is_staff = models.BooleanField(
        verbose_name=_('staff status'),
        default=False,
    )
    is_active = models.BooleanField(
        verbose_name=_('active'),
        default=True,
    )

    objects = UserManager()

    USERNAME_FIELD = 'account_id' # ログイン時、ユーザー名の代わりにusernameを使用

    def __str__(self):
        return '{}(社員番号：{})'.format(self.account_id, self.emp_num)

