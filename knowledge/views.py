from django.shortcuts import reverse
from django.http import HttpResponse
from django.contrib.auth.mixins import PermissionRequiredMixin
from core.views import CustomCreateView, CustomListView, CustomDetailView, CustomUpdateView, CustomDeleteView, \
    OnlyCreatorAccessMixin
from knowledge.forms import *


perm = 'core.knowledge_app'


class BookCreateView(PermissionRequiredMixin, CustomCreateView):
    model = Book
    permission_required = perm
    form_class = BookForm

    def form_valid(self, form):
        form.instance.id_slug = self.model.get_id_slug(10)
        return super().form_valid(form)


class BookListView(PermissionRequiredMixin, CustomListView):
    model = Book
    permission_required = perm

    def get_queryset(self):
        return Book.objects.filter(created_by=self.request.user)


class BookDetailView(PermissionRequiredMixin, OnlyCreatorAccessMixin, CustomDetailView):
    model = Book
    permission_required = perm
    slug_field = 'id_slug'
    http_method_names = ['get']


class BookUpdateView(PermissionRequiredMixin, OnlyCreatorAccessMixin, CustomUpdateView):
    model = Book
    permission_required = perm
    slug_field = 'id_slug'
    form_class = BookForm


class BookDeleteView(PermissionRequiredMixin, OnlyCreatorAccessMixin, CustomDeleteView):
    model = Book
    permission_required = perm
    slug_field = 'id_slug'

    def get_success_url(self):
        return reverse("books")


class ChapterCreateView(PermissionRequiredMixin, CustomCreateView):
    model = Book
    permission_required = perm
    slug_field = 'id_slug'

    def form_valid(self, form):
        form.instance.id_slug = self.model.get_id_slug(10)

        book = Book.objects.get(id_slug=self.kwargs['book'])
        if book.created_by != self.request.user:
            return HttpResponse("Unauthorized", status=401)
        else:
            form.instance.book = book

        return super().form_valid(form)


class ChapterDetailView(PermissionRequiredMixin, OnlyCreatorAccessMixin, CustomDetailView):
    model = Book
    permission_required = perm
    slug_field = 'id_slug'
    http_method_names = ['get']


class ChapterUpdateView(PermissionRequiredMixin, OnlyCreatorAccessMixin, CustomUpdateView):
    model = Book
    permission_required = perm
    slug_field = 'id_slug'
    form_class = ChapterForm


class ChapterDeleteView(PermissionRequiredMixin, OnlyCreatorAccessMixin, CustomDeleteView):
    model = Book
    permission_required = perm
    slug_field = 'id_slug'

    def get_success_url(self):
        return reverse("book-detail", args=self.kwargs['book'])
