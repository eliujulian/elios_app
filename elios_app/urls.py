"""elios_app URL Configuration

urls are build only within this file.

Group them together in variables to allow the IDE to build a structure.

"""
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from elios_app.views import *
from core.views import *
from health.views import *
from personality.views import *
from knowledge.views import *
from habit.views import *


basic_urls = [
    path("", login_required(test_view, login_url="login-url"), name="landingpage"),
    path("success/", MessageView.as_view(), name="message-success-public"),
    path("message/", login_required(MessageView.as_view()), name="message"),
    path("failure/", MessageView.as_view(), name="message-failure-public"),
    path("login/", LoginView.as_view(template_name="application/login.html"), name="login-url"),
    path("logout/", LogoutView.as_view(template_name="application/login.html"), name="logout-url"),
    path("user/<slug>/", login_required(UserDetailView.as_view()), name="user-detail"),
]

account_management_urls = [
    path("register/", AccountRegisterView.as_view(), name="account-register"),
    path("account/confirm/", AccountConfirmEMailView.as_view(), name="account-confirm"),
    path("account/", login_required(AccountDetailView.as_view()), name="account-detail"),
    path("account/update/", login_required(AccountUpdateView.as_view()), name="account-update"),
    path("account/delete/", login_required(AccountDeleteView.as_view()), name="account-delete")
]

admin_urls = [
    path("admin/", admin.site.urls)
]

health_urls = [
    path("health/weight/", login_required(WeightView.as_view()), name="weight"),
    path("health/weight/create/", login_required(WeightCreateView.as_view()), name="weight-create"),
]

personality_urls = [
    path("personality/", login_required(PersonalityView.as_view()), name="personality"),
    path("personality/update/", login_required(PersonalityUpdateView.as_view()), name="personality-update"),
    path("personality/create/", login_required(PersonalityNoteCreateView.as_view()), name="personality-note-create"),
    path("personality/<slug>/", login_required(PersonalityNoteUpdateView.as_view()), name="personality-note-update"),
    path("personality/<slug>/delete/", login_required(PersonalityNoteDeleteView.as_view()),
         name="personality-note-delete"),
]

habit_urls = [
    path("habitprofile/", login_required(HabitProfileView.as_view()), name="habitprofile"),
    path("habitprofile/update/", login_required(HabitProfileUpdateView.as_view()), name="habitprofile-update"),
    path("sphere/<int:sphere>/", login_required(SphereView.as_view()), name="sphere"),
    path("goals/", login_required(GoalListView.as_view()), name="goals"),
    path("goal/create/", login_required(GoalCreateView.as_view()), name="goal-create"),
    path("goal/<slug>/", login_required(GoalDetailView.as_view()), name="goal-detail"),
    path("goal/<slug>/update/", login_required(GoalUpdateView.as_view()), name="goal-update"),
    path("goal/<slug>/delete/", login_required(GoalDeleteView.as_view()), name="goal-delete"),
    path("habits/", login_required(HabitListView.as_view()), name="habits"),
    path("habit/create/", login_required(HabitCreateView.as_view()), name="habit-create"),
    path("habit/<slug>/", login_required(HabitDetailView.as_view()), name="habit-detail"),
    path("habit/<slug>/update/", login_required(HabitUpdateView.as_view()), name="habit-update"),
    path("habit/<slug>/delete/", login_required(HabitDeleteView.as_view()), name="habit-delete"),
]

habit_api_urls = [
    path("api/habit/<slug>/event/", login_required(habit_event_view), name="habit-event"),
]

knowledge_urls = [
    path("knowledge/book/", login_required(BookListView.as_view()), name="books"),
    path("knowledge/book/create/", login_required(BookCreateView.as_view()), name="book-create"),
    path("knowledge/book/<slug>/", login_required(BookDetailView.as_view()), name="book-detail"),
    path("knowledge/book/<slug>/update/", login_required(BookUpdateView.as_view()), name="book-update"),
    path("knowledge/book/<slug>/delete/", login_required(BookDeleteView.as_view()), name="book-delete"),
    path("knowledge/book_<str:book>/chapter/create/", login_required(ChapterCreateView.as_view()),
         name="chapter-create"),
    path("knowledge/book_<str:book>/chapter/<int:order_num>/", login_required(ChapterDetailView.as_view()),
         name="chapter-detail"),
    path("knowledge/book_<str:book>/chapter/<int:order_num>/up/", login_required(ChapterOrderUpRedirect.as_view()),
         name="chapter-up"),
    path("knowledge/book_<str:book>/chapter/<int:order_num>/down/", login_required(ChapterOderDownRedirect.as_view()),
         name="chapter-down"),
    path("knowledge/book_<str:book>/chapter/<int:order_num>/update/", login_required(ChapterUpdateView.as_view()),
         name="chapter-update"),
    path("knowledge/book_<str:book>/chapter/<int:order_num>/delete/", login_required(ChapterDeleteView.as_view()),
         name="chapter-delete"),
    path("knowledge/random-book/", login_required(RandomBookRedirect.as_view()), name="book-random"),
    path("knowledge/random-chapter/", login_required(RandomChapterRedirect.as_view()), name="chapter-random"),
]

urlpatterns = basic_urls
urlpatterns.extend(account_management_urls)
urlpatterns.extend(admin_urls)
urlpatterns.extend(health_urls)
urlpatterns.extend(personality_urls)
urlpatterns.extend(habit_urls)
urlpatterns.extend(habit_api_urls)
urlpatterns.extend(knowledge_urls)
