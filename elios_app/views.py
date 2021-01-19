from django import db
from django.template.response import TemplateResponse
from elios_app import settings


def test_view(request):
    context = {}
    context['data'] = None
    return TemplateResponse(request, 'application/home_test.html', context)
