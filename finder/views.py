from django.shortcuts import get_object_or_404, render

from diskarray.models import File


def index(request, selected_id=None):
    files = File.objects.all()
    selected = None if selected_id is None else get_object_or_404(File, id=selected_id)

    return render(request, 'finder/index.html', {
        'files': files,
        'selected': selected,
    })
