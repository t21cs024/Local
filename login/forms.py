from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            "account_id",
            "emp_num",
            "name",
            "email",
            "affiliation",
        )

# ログインフォームを追加
class LoginFrom(AuthenticationForm):
    class Meta:
        model = CustomUser