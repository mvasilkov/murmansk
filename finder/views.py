from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from diskarray.models import File
from .forms import CommentForm
from .models import Folder

MODELS = {
    'File': File,
    'Folder': Folder,
}


def index(request, *, model_name: str = None, model_id: int = None):
    if model_name is not None:
        if model_name not in MODELS:
            raise Http404

        selected_model = get_object_or_404(MODELS[model_name], id=model_id)
    else:
        selected_model = None

    return render(request, 'finder/index.html', {
        'files': File.objects.all(),
        'folders': Folder.objects.all(),
        'selected_file': selected_model if model_name == 'File' else None,
        'selected_folder': selected_model if model_name == 'Folder' else None,
    })


def change_comment(request, *, model_name: str, model_id: int):
    if model_name not in MODELS:
        raise Http404

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
