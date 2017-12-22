import hashlib

from django.shortcuts import get_object_or_404, redirect, render

from directory.forms import PictureForm
from directory.models import Picture


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
            pic_file = request.FILES['picture']
            size, sha256 = _compute_size_sha256(pic_file)
            pic = Picture(picture=pic_file, size=size, sha256=sha256)
            pic.save()
            return redirect(pic)
    else:
        form = PictureForm()

    return render(request, 'dir/upload_picture.html', {'form': form})
