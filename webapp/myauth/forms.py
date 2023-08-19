from django import forms


class SignupForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput)
    password_confirm = forms.CharField(max_length=30, widget=forms.PasswordInput)
    user_type = forms.ChoiceField(choices=('customer', 'seller'))
