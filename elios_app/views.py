from django.template.response import TemplateResponse
from django.http import HttpResponseNotAllowed


def test_view(request):
    context = dict()
    context['data'] = None

    if request.method == "POST":
        return HttpResponseNotAllowed("get")

    return TemplateResponse(request, 'application/base.html', context)
