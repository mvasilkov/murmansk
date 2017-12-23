import hashlib

from django.shortcuts import get_object_or_404, redirect, render

from .forms import PictureForm, FolderNameForm
from .models import Picture, Folder


def _compute_size_sha256(pic_file):
    size = 0
    sha256 = hashlib.sha256()
    for chunk in pic_file.chunks():
        assert type(chunk) is bytes
        size += len(chunk)
        sha256.update(chunk)

    return size, sha256.hexdigest()


def picture(request, pic_id: int):
    pic = get_object_or_404(Picture, id=pic_id)
    return render(request, 'dir/picture.html', {'picture': pic})


def upload_picture(request):
    if request.method == 'POST':
        form = PictureForm(request.POST, request.FILES)
        if form.is_valid():
            pic_file = request.FILES['upload_picture']
            size, sha256 = _compute_size_sha256(pic_file)
            pic = Picture(file=pic_file, size=size, sha256=sha256)
            pic.save()
            return redirect(pic)
    else:
        form = PictureForm()

    return render(request, 'dir/upload_picture.html', {'form': form})


def list_folders(request):
    if request.method == 'POST':
        form = FolderNameForm(request.POST)
        if form.is_valid():
            new_folder = Folder(name=form.cleaned_data['folder_name'])
            new_folder.save()
            return redirect(new_folder)
    else:
        form = FolderNameForm()

    return render(request, 'dir/list_folders.html', {
        'folders': Folder.objects.all(),
        'selected': None,
        'form': form,
    })


def select_folder(request, folder_id: int):
    if request.method == 'POST':
        form = FolderNameForm(request.POST)
        if form.is_valid():
            new_folder = Folder(name=form.cleaned_data['folder_name'], parent_id=folder_id)
            new_folder.save()
            return redirect(new_folder)
    else:
        form = FolderNameForm()

    return render(request, 'dir/select_folder.html', {
        'folders': Folder.objects.all(),
        'selected': folder_id,
        'form': form,
    })
