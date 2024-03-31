from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.core.mail import send_mail


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)

        common_users = Group.objects.get(name="common users")
        user.groups.add(common_users)

        send_mail(
            subject='Добро пожаловать на наш новостной портал!!!',
            message=f'{user.username}, вы успешно зарегистрировались!',
            from_email=None,
            recipient_list=[user.email],
        )

        return user

class SignUpForm:
    pass