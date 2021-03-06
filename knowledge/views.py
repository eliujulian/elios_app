import random
from django.shortcuts import reverse, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.mixins import PermissionRequiredMixin
from core.views import CustomCreateView, CustomListView, CustomDetailView, CustomUpdateView, CustomDeleteView, View
from knowledge.forms import *


perm = 'core.knowledge_app'


class BookCreateView(PermissionRequiredMixin, CustomCreateView):
    model = Book
    permission_required = perm
    form_class = BookForm


class BookListView(PermissionRequiredMixin, CustomListView):
    model = Book
    permission_required = perm
    template_name = "knowledge/book_list.html"

    def get_queryset(self):
        return Book.objects.filter(created_by=self.request.user)


class BookDetailView(PermissionRequiredMixin, CustomDetailView):
    model = Book
    permission_required = perm
    slug_field = 'id_slug'
    http_method_names = ['get']
    template_name = 'knowledge/book_detail.html'

    def get_object(self, queryset=None):
        if self.slug_field == 'id_slug':
            return get_object_or_404(self.model, created_by=self.request.user, id_slug=self.kwargs['slug'])
        else:
            raise Exception("Please reconfigure")


class BookUpdateView(PermissionRequiredMixin, CustomUpdateView):
    model = Book
    permission_required = perm
    slug_field = 'id_slug'
    form_class = BookForm

    def get_object(self, queryset=None):
        if self.slug_field == 'id_slug':
            return get_object_or_404(self.model, created_by=self.request.user, id_slug=self.kwargs['slug'])
        else:
            raise Exception("Please reconfigure")


class BookDeleteView(PermissionRequiredMixin, CustomDeleteView):
    model = Book
    permission_required = perm
    slug_field = 'id_slug'

    def get_success_url(self):
        return reverse("books")

    def get_object(self, queryset=None):
        if self.slug_field == 'id_slug':
            return get_object_or_404(self.model, created_by=self.request.user, id_slug=self.kwargs['slug'])
        else:
            raise Exception("Please reconfigure")


class ChapterCreateView(PermissionRequiredMixin, CustomCreateView):
    model = Chapter
    permission_required = perm
    slug_field = 'id_slug'
    form_class = ChapterForm

    def get(self, request, *args, **kwargs):
        book = Book.objects.get(id_slug=self.kwargs['book'])
        if book.created_by != self.request.user:
            raise Http404()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        book = Book.objects.get(id_slug=self.kwargs['book'])
        if book.created_by != self.request.user:
            raise Http404()
        return super(ChapterCreateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        book = Book.objects.get(id_slug=self.kwargs['book'])
        form.instance.book = book
        form.instance.order_num = Chapter.objects.filter(book=book).count()
        return super().form_valid(form)


class ChapterDetailView(PermissionRequiredMixin, CustomDetailView):
    model = Chapter
    permission_required = perm
    http_method_names = ['get']
    template_name = 'knowledge/chapter_detail.html'

    def get_object(self, queryset=None):
        try:
            book = Book.objects.get(id_slug=self.kwargs['book'])
        except:
            raise Http404(f"Book with the id_slug: {self.kwargs['book']} could not be found.")
        return get_object_or_404(Chapter, book=book, order_num=self.kwargs['order_num'], created_by=self.request.user)


class ChapterUpdateView(PermissionRequiredMixin, CustomUpdateView):
    model = Chapter
    permission_required = perm
    form_class = ChapterForm

    def get_object(self, queryset=None):
        try:
            book = Book.objects.get(id_slug=self.kwargs['book'])
        except:
            raise Http404(f"Book with the id_slug: {self.kwargs['book']} could not be found.")
        return get_object_or_404(Chapter, book=book, order_num=self.kwargs['order_num'], created_by=self.request.user)


class ChapterDeleteView(PermissionRequiredMixin, CustomDeleteView):
    model = Chapter
    permission_required = perm

    def get_object(self, queryset=None):
        try:
            book = Book.objects.get(id_slug=self.kwargs['book'])
        except:
            raise Http404(f"Book with the id_slug: {self.kwargs['book']} could not be found.")
        return get_object_or_404(Chapter, book=book, order_num=self.kwargs['order_num'], created_by=self.request.user)

    def post(self, request, *args, **kwargs):
        book = Book.objects.get(id_slug=self.kwargs['book'])

        if book.created_by != request.user:
            raise Http404()

        instance = get_object_or_404(self.model,
                                     book=book,
                                     order_num=self.kwargs['order_num'],
                                     created_by=self.request.user)

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

    def get_random_book(self):
        books_qs = Book.objects.filter(created_by=self.request.user)
        instances_count = books_qs.count()
        if instances_count == 0:
            return None
        random_index = random.randrange(0, instances_count, 1)
        instance = books_qs[random_index]
        return instance

    def get(self, *args, **kwargs):
        instance = self.get_random_book()
        if not instance:
            return HttpResponseRedirect(reverse('message') + "?message=Bitte leg zuerst ein Buch an.")
        else:
            return HttpResponseRedirect(instance.get_absolute_url())


class RandomChapterRedirect(PermissionRequiredMixin, View):
    http_method_names = ['get']
    permission_required = perm

    def get_random_chapter(self):
        chapter_qs = Chapter.objects.filter(created_by=self.request.user).exclude(summary__isnull=True)
        instances_count = chapter_qs.count()
        if instances_count == 0:
            return None
        random_index = random.randrange(0, instances_count, 1)
        instance = chapter_qs[random_index]
        return instance

    def get(self, *args, **kwargs):
        instance = self.get_random_chapter()
        if not instance:
            return HttpResponseRedirect(reverse('message') + "?message=Bitte leg zuerst ein Buch mit Kapiteln an.")
        else:
            return HttpResponseRedirect(instance.get_absolute_url())


class ChapterOrderUpRedirect(ChapterDetailView):
    def get(self, *args, **kwargs):
        instance = self.get_object()
        instance.order_one_up()
        return HttpResponseRedirect(instance.get_absolute_url())


class ChapterOderDownRedirect(ChapterDetailView):
    def get(self, *args, **kwargs):
        instance = self.get_object()
        instance.order_num_one_down()
        return HttpResponseRedirect(instance.get_absolute_url())
