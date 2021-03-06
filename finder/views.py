from django.db.models import Q
from django.http.response import HttpResponseNotAllowed, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render

from diskarray.models import File
from .forms import CommentForm, FilenameForm, FolderNameForm
from .models import Folder

MODELS = {
    'File': File,
    'Folder': Folder,
}


def index(request, *, model_name: str = None, model_id: int = None):
    if model_name is not None:
        if model_name not in MODELS:
            return HttpResponseNotFound()

        selected_model = get_object_or_404(MODELS[model_name], id=model_id)
    else:
        selected_model = None

    return render(request, 'finder/index.html', {
        'files': File.objects.filter(folders=None),
        'folders': Folder.objects.filter(Q(parent__isnull=True) | Q(parent__is_collapsed=False)),
        'selected_file': selected_model if model_name == 'File' else None,
        'selected_folder': selected_model if model_name == 'Folder' else None,
    })


def change_comment(request, *, model_name: str, model_id: int):
    if model_name not in MODELS:
        return HttpResponseNotFound()

    selected_model = get_object_or_404(MODELS[model_name], id=model_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            selected_model.comment = form.cleaned_data['comment']
            selected_model.save()
            return redirect('select_any', model_name=model_name, model_id=model_id)
    else:
        form = CommentForm({'comment': selected_model.comment})

    return render(request, 'finder/change_comment.html', {'form': form})


def remove_comment(request, *, model_name: str, model_id: int):
    if model_name not in MODELS:
        return HttpResponseNotFound()

    if request.method == 'POST':
        selected_model = get_object_or_404(MODELS[model_name], id=model_id)
        selected_model.comment = ''
        selected_model.save()
        return redirect('select_any', model_name=model_name, model_id=model_id)

    return HttpResponseNotAllowed(permitted_methods=['POST'])


def rename_file(request, *, file_id: int):
    file = get_object_or_404(File, id=file_id)

    if request.method == 'POST':
        form = FilenameForm(request.POST)
        if form.is_valid():
            file.name = form.cleaned_data['filename']
            file.save()
            return redirect('select_any', model_name='File', model_id=file_id)
    else:
        form = FilenameForm({'filename': file.name})

    return render(request, 'finder/rename_file.html', {'form': form})


def rename_folder(request, *, folder_id: int):
    folder = get_object_or_404(Folder, id=folder_id)

    if request.method == 'POST':
        form = FolderNameForm(request.POST)
        if form.is_valid():
            folder.name = form.cleaned_data['folder_name']
            folder.save()
            return redirect('select_any', model_name='Folder', model_id=folder_id)
    else:
        form = FolderNameForm({'folder_name': folder.name})

    return render(request, 'finder/rename_folder.html', {'form': form})


def collapse_folder(request, *, folder_id: int, collapse: bool):
    folder = get_object_or_404(Folder, id=folder_id)

    if collapse:
        folder.collapse_subdirectories()

    folder.is_collapsed = collapse
    folder.save()
    return redirect('select_any', model_name='Folder', model_id=folder_id)
