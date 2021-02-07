from django.template.response import TemplateResponse
from django.http import HttpResponseNotAllowed
from django.contrib.auth.decorators import permission_required


@permission_required('core.landingpage_right')
def test_view(request):
    """
    # Uncomment to create Group on first loading.
    from django.contrib.auth.models import Group, Permission, ContentType
    from core.models import PermissionRegister

    # Create Standard Group if not exisiting in DB and grant landingpage right
    if Group.objects.filter(name="StandardUsers").count() == 0:
        perm = Permission.objects.get(
            content_type=ContentType.objects.get_for_model(PermissionRegister),
            codename="landingpage_right"
        )
        group = Group.objects.create(**{'name': "StandardUsers"})
        group.permissions.add(perm)
        print("Created Group: ", group)


    if Group.objects.filter(name="HealthApp").count() == 0:
        perm = Permission.objects.get(
            content_type=ContentType.objects.get_for_model(PermissionRegister),
            codename="health_app"
        )
        group = Group.objects.create(**{'name': "HealthApp"})
        group.permissions.add(perm)
        print("Created Group: ", group)
    """

    context = dict()
    context['data'] = f"You are logged in as {request.user} ({request.user.username})."

    if request.method != "GET":
        return HttpResponseNotAllowed("get")

    return TemplateResponse(request, 'application/base.html', context)
