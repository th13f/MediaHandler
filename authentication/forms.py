from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class ProfileForm(forms.Form):
    email = forms.EmailField(required=False)
    preferences = forms.CharField(widget=forms.Textarea, required=False)
    profile_image = forms.FileField(required=False)