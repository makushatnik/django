from django import forms
from .models import Product


# class ProductForm(forms.Form):
#     name = forms.CharField(max_length=100)
#     description = forms.CharField(
#         widget=forms.Textarea(attrs={"rows": 5, "cols": 30})
#     )
#     price = forms.DecimalField(min_value=1, max_value=10000000)
#     seller = forms.CharField(widget=forms.HiddenInput)

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "name", "description", "price", "discount", "preview"

    images = MultipleFileField(
        widget=MultipleFileInput(),
        required=False
    )

