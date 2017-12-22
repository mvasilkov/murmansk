from django import forms


class PictureForm(forms.Form):
    picture = forms.ImageField()
