from django.contrib.auth import forms, get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django import forms as django_form


User = get_user_model()


class UserChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(forms.UserCreationForm):

    error_message = forms.UserCreationForm.error_messages.update(
        {"duplicate_username": _("This username has already been taken.")}
    )

    class Meta(forms.UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise ValidationError(self.error_messages["duplicate_username"])


class SignUpForm(django_form.ModelForm):
    class Meta:
        model = User
        fields = ['email','name','username','password']

        labels = {
            'email' : '이메일 주소',
            'name' : '이름',
            'username' : '사용자 이름',
            'password' : '비밀번호',
        }

        widgets = {
            'password' : django_form.PasswordInput(),
        }

    # 패스워드가 유효하지 않아 기존의 save함수를 오버라이딩(재정의) 
    def save(self, commit=True):    
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.save()

        return user
