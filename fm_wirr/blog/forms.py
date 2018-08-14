from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from api_1.models import Album, Artist, ScrobbleCard, Song


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=True, help_text="Обязательно.", label="Имя"
    )
    last_name = forms.CharField(
        max_length=30, required=False, help_text="Необязательно.", label="Фамилия"
    )
    email = forms.EmailField(
        max_length=254, required=True, help_text="Введите ваш email"
    )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )


class UniteWrondAlbum(forms.Form):
    pass
