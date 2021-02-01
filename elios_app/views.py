from django.template.response import TemplateResponse
from django.http import HttpResponseNotAllowed
from django.contrib.auth.decorators import permission_required


@permission_required('core.landingpage_right')
def test_view(request):
    context = dict()
    context['data'] = f"You are logged in as {request.user} ({request.user.username})."

    if request.method != "GET":
        return HttpResponseNotAllowed("get")

    return TemplateResponse(request, 'application/base.html', context)
