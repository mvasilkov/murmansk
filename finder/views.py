from django.shortcuts import get_object_or_404, render

from diskarray.models import File
from finder.models import Folder


def index(request, folder_id=None, file_id=None):
    folders = Folder.objects.all()
    files = File.objects.all()

    selected_folder = selected_file = None
    if folder_id is not None:
        assert file_id is None
        selected_folder = get_object_or_404(Folder, id=folder_id)
    elif file_id is not None:
        selected_file = get_object_or_404(File, id=file_id)

    return render(request, 'finder/index.html', {
        'folders': folders,
        'files': files,
        'selected_folder': selected_folder,
        'selected_file': selected_file,
    })
