from django.http import Http404
from django.shortcuts import get_object_or_404, render

from diskarray.models import File
from finder.models import Folder

MODELS = {
    'File': File,
    'Folder': Folder,
}


def index(request, *, model_name: str = None, model_id: int = None):
    if model_name is not None:
        try:
            model_class = MODELS[model_name]
        except KeyError:
            raise Http404()

        selected_model = get_object_or_404(model_class, id=model_id)
    else:
        selected_model = None

    return render(request, 'finder/index.html', {
        'files': File.objects.all(),
        'folders': Folder.objects.all(),
        'selected_file': selected_model if model_name == 'File' else None,
        'selected_folder': selected_model if model_name == 'Folder' else None,
    })
