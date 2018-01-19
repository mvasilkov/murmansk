from django import forms

from .models import Folder


class PictureForm(forms.Form):
    upload_picture = forms.ImageField()


class FilenameForm(forms.Form):
    filename = forms.CharField(max_length=250, strip=True, widget=forms.TextInput(attrs={'size': 60}))


class FolderNameForm(forms.Form):
    folder_name = forms.CharField(max_length=250, strip=True, widget=forms.TextInput(attrs={'size': 60}))

    def clean_folder_name(self):
        folder_name = self.cleaned_data['folder_name']
        if Folder.objects.filter(name=folder_name).count():
            raise forms.ValidationError('A folder with the same name already exists')
        return folder_name


class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 20, 'cols': 80}), required=False)
