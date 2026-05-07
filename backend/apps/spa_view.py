import os
from django.conf import settings
from django.http import FileResponse, Http404

def spa_index(request):
    path = os.path.join(settings.STATIC_ROOT, 'index.html')
    if not os.path.exists(path):
        raise Http404('SPA not built. Run frontend build first.')
    response = FileResponse(open(path, 'rb'), content_type='text/html')
    return response
