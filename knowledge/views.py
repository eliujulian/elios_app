from django.contrib.auth.mixins import PermissionRequiredMixin
from core.views import CustomCreateView, CustomListView, CustomDetailView, CustomUpdateView, CustomDeleteView, \
    OnlyCreatorAccessMixin
from knowledge.forms import *


class BookCreateView(PermissionRequiredMixin, CustomCreateView):
    model = Book
    permission_required = 'core.knowledge_app'
    form_class = BookForm

    def form_valid(self, form):
        form.instance.id_slug = self.model.get_id_slug(10)
        return super().form_valid(form)


class BookListView(PermissionRequiredMixin, CustomListView):
    model = Book
    permission_required = 'core.knowledge_app'

    def get_queryset(self):
        return Book.objects.filter(created_by=self.request.user)


class BookDetailView(PermissionRequiredMixin, OnlyCreatorAccessMixin, CustomDetailView):
    model = Book
    permission_required = 'core.knowledge_app'
    slug_field = 'id_slug'


class BookUpdateView(PermissionRequiredMixin, OnlyCreatorAccessMixin, CustomUpdateView):
    model = Book
    permission_required = 'core.knowledge_app'
    slug_field = 'id_slug'
    form_class = BookForm


class BookDeleteView(PermissionRequiredMixin, OnlyCreatorAccessMixin, CustomDeleteView):
    model = Book
    permission_required = 'core.knowledge_app'
