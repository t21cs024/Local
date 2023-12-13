from django.contrib.auth.views import LoginView

# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        user = self.request.user

        # スーパーユーザーかどうかを確認
        #t21cs1 @@@@aaaa superuserhome
        #t21cs0 0000aaaa userhome
        if user.groups.filter(name='superuserhome').exists():
        #(lambda u: u.groups.filter(name='superuserhome')):
            return '/superuserhome/'
        else:
            return '/userhome/'