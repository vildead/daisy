from django import forms
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm
from core.models import User


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'is_active', 'user_permissions']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)


class PickUserForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['personnel'] = forms.ChoiceField(
            choices=[(d.id, str(d)) for d in User.objects.exclude(username='AnonymousUser').all()])


class UserAuthForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'validate', 'placeholder': settings.LOGIN_USERNAME_PLACEHOLDER}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': settings.LOGIN_PASSWORD_PLACEHOLDER}))

    def clean(self):
        username = self.cleaned_data.get('username')
        suffix = getattr(settings, 'LOGIN_USERNAME_SUFFIX', '')
        if username and suffix:
            if not username.endswith(suffix):
                alternative_suffix = getattr(settings, 'LOGIN_USERNAME_ALTERNATIVE_SUFFIX', '')
                if alternative_suffix and username.endswith(alternative_suffix):
                    self.cleaned_data['username'] = username[0:-len(alternative_suffix)] + suffix
                else:
                    self.cleaned_data['username'] = username + suffix
        return super().clean()



