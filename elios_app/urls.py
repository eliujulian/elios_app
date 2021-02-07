"""elios_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path  # , include
from elios_app.views import *
from core.views import *
from health.views import *


basic_urls = [
    path("", login_required(test_view, login_url="login-url"), name="landingpage"),
    path("success/", MessageView.as_view(), name="message-success-public"),
    path("failure/", MessageView.as_view(), name="message-failure-public"),
    path("login/", LoginView.as_view(template_name="application/login.html"), name="login-url"),
    path("logout/", LogoutView.as_view(template_name="application/login.html"), name="logout-url"),
    path("user/<slug>/", login_required(UserDetailView.as_view()), name="user-detail"),
]

account_management_urls = [
    path("register/", AccountRegisterView.as_view(), name="account-register"),
    path("account/confirm/", AccountConfirmEMailView.as_view(), name="account-confirm"),
    path("account/<slug>/", login_required(AccountDetailView.as_view()), name="account-detail"),
    path("account/<slug>/update/", login_required(AccountUpdateView.as_view()), name="account-update"),
    path("account/<slug>/delete/", login_required(AccountDeleteView.as_view()), name="account-delete")
]

admin_urls = [
    path("admin/", admin.site.urls)
]

health_urls = [
    path("health/weight/", login_required(WeightListView.as_view()), name="health-weight"),
    path("health/weight/create/", login_required(WeightCreateView.as_view()), name="health-weight-create"),
    path("health/weight/<int:pk>/", login_required(WeightDetailView.as_view()), name="health-weight-detail"),
    path("health/weight/<int:pk>/update/", login_required(WeightDetailView.as_view()), name="health-weight-update"),
    path("health/weight/<int:pk>/delete/", login_required(WeightDeleteView.as_view()), name="health-weight-delete"),
]

urlpatterns = list()
urlpatterns.extend(basic_urls)
urlpatterns.extend(account_management_urls)
urlpatterns.extend(admin_urls)
urlpatterns.extend(health_urls)
