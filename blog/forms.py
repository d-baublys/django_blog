from django import forms


class SearchForm(forms.Form):
    q = forms.CharField(label="", max_length=200, required=False)
