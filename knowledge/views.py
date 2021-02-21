import random
from django.shortcuts import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from core.views import CustomCreateView, CustomListView, CustomDetailView, CustomUpdateView, CustomDeleteView, \
    OnlyCreatorAccessMixin, View
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
    template_name = 'knowledge/book_detail.html'


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
    model = Chapter
    permission_required = perm
    slug_field = 'id_slug'
    form_class = ChapterForm

    def get(self, request, *args, **kwargs):
        book = Book.objects.get(id_slug=self.kwargs['book'])
        if book.created_by != self.request.user:
            return HttpResponse("Unauthorized", status=401)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        book = Book.objects.get(id_slug=self.kwargs['book'])
        if book.created_by != self.request.user:
            return HttpResponse("Unauthorized", status=401)
        return super(ChapterCreateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.id_slug = self.model.get_id_slug(10)
        book = Book.objects.get(id_slug=self.kwargs['book'])
        form.instance.book = Book.objects.get(id_slug=self.kwargs['book'])
        form.instance.order_num = Chapter.objects.filter(book=book).count()
        return super().form_valid(form)


class ChapterDetailView(PermissionRequiredMixin, OnlyCreatorAccessMixin, CustomDetailView):
    model = Chapter
    permission_required = perm
    http_method_names = ['get']
    template_name = 'knowledge/chapter_detail.html'

    def get_object(self, queryset=None):
        book = Book.objects.get(id_slug=self.kwargs['book'])
        return Chapter.objects.get(
            book_id=book.id,
            order_num=self.kwargs['order_num']
        )


class ChapterUpdateView(PermissionRequiredMixin, OnlyCreatorAccessMixin, CustomUpdateView):
    model = Chapter
    permission_required = perm
    form_class = ChapterForm

    def get_object(self, queryset=None):
        book = Book.objects.get(id_slug=self.kwargs['book'])
        return Chapter.objects.get(
            book_id=book.id,
            order_num=self.kwargs['order_num']
        )


class ChapterDeleteView(PermissionRequiredMixin, OnlyCreatorAccessMixin, CustomDeleteView):
    model = Chapter
    permission_required = perm

    def get_object(self, queryset=None):
        book = Book.objects.get(id_slug=self.kwargs['book'])
        return Chapter.objects.get(
            book_id=book.id,
            order_num=self.kwargs['order_num']
        )

    def post(self, request, *args, **kwargs):
        book = Book.objects.get(id_slug=self.kwargs['book'])

        if book.created_by != request.user:
            return HttpResponse("Unauthorized", 401)

        instance = Chapter.objects.get(
            book_id=book.id,
            order_num=self.kwargs['order_num']
        )

        self.object = instance  # noqa
        success_url = self.get_success_url()
        self.object.delete()
        chapters = book.chapter_set.all()
        for i, c in enumerate(chapters):
            c.order_num = i
            c.save()
        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        return reverse("book-detail", args=[self.kwargs['book'], ])


class RandomBookRedirect(PermissionRequiredMixin, View):
    http_method_names = ['get']
    permission_required = perm

    def get(self, *args, **kwargs):
        books_qs = Book.objects.filter(created_by=self.request.user)
        instances_count = books_qs.count()
        random_index = random.randrange(0, instances_count, 1)
        instance = books_qs[random_index]
        return HttpResponseRedirect(instance.get_absolute_url())


class RandomChapterRedirect(PermissionRequiredMixin, View):
    http_method_names = ['get']
    permission_required = perm

    def get(self):
        chapter_qs = Chapter.objects.filter(created_by=self.request.user).exclude(summary__exact="")
        instances_count = chapter_qs.count()
        random_index = random.randrange(0, instances_count, 1)
        instance = chapter_qs[random_index]
        return HttpResponseRedirect(instance.get_absolute())
