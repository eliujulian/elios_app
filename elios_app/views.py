from django.template.response import TemplateResponse


def test_view(request):
    context = dict()
    context['data'] = None
    return TemplateResponse(request, 'application/base.html', context)
