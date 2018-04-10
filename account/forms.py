from django.contrib.auth.models import User
from django import forms

from django.contrib.auth import (
    authenticate,
    get_user_model,
)

User = get_user_model()

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(label='Confirmer le mot de passe',widget=forms.PasswordInput)
    pass2 = forms.CharField(label='Mot de passe',widget=forms.PasswordInput)
    first_name = forms.CharField(label='Prénom',widget=forms.TextInput, required=True)
    last_name = forms.CharField(label='Nom',widget=forms.TextInput, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'pass2', 'password']


    def clean_password(self):
        # check password
        pwd1 = self.cleaned_data.get("password")
        pwd2 = self.cleaned_data.get("pass2")

        if pwd1 != pwd2:
            raise forms.ValidationError("les mots de passe ne sont pas identique!")
        return pwd1

    def clean_email(self):
        # check email
        email = self.cleaned_data.get("email")
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("Cette email est déjà existant!")
        return email


class UserLoginForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        label="Nom",
        widget=forms.TextInput,
        required=True
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput,
        required=True
    )

    # Validation password
    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Cette utilisateur n'existe pas !")
        if not user.check_password(password):
            raise forms.ValidationError("Mot de passe invalid!")
        if not user.is_active:
            raise forms.ValidationError("Le compte utilisateur n'est pas activé.")
        return super(UserLoginForm, self).clean(*args, **kwargs)