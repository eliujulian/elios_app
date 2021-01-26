from django.template.response import TemplateResponse
from django.http import HttpResponseNotAllowed


def test_view(request):
    context = dict()
    context['data'] = f"You are logged in as {request.user} ({request.user.username})."

    if request.method == "POST":
        return HttpResponseNotAllowed("get")

    return TemplateResponse(request, 'application/base.html', context)
