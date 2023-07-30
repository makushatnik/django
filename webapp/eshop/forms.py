from django import forms


class ProductForm(forms.Form):
    name = forms.CharField(max_length=100)
    description = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 5, "cols": 30})
    )
    price = forms.DecimalField(min_value=1, max_value=10000000)
    seller = forms.CharField(widget=forms.HiddenInput)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput)


class SignupForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput)
    password_confirm = forms.CharField(max_length=30, widget=forms.PasswordInput)
    user_type = forms.ChoiceField(choices=('customer', 'seller'))
