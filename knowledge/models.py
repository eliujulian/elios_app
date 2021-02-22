from django.db import models
from django.shortcuts import reverse
from core.models import AbstractBaseModel


class Book(AbstractBaseModel):
    class Meta:
        ordering = ['author']

    id_slug = models.CharField(max_length=18, unique=True, editable=False)
    title = models.CharField(max_length=160)
    author = models.CharField(max_length=160)
    year = models.IntegerField()
    is_favorite = models.BooleanField(default=False)
    summary = models.TextField(null=True, blank=True)
    source = models.CharField(max_length=160, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('book-detail', args=[self.id_slug, ])

    def get_create_url(self):
        return reverse('book-create')

    def __str__(self):
        return f'{self.author} - {self.title} ({str(self.year)})'


class Chapter(AbstractBaseModel):
    class Meta:
        ordering = ['order_num']

    id_slug = models.CharField(max_length=18, unique=True, editable=False)
    book = models.ForeignKey(to=Book, on_delete=models.CASCADE, editable=False)
    title = models.CharField(max_length=160)
    summary = models.TextField(null=True, blank=True)
    source = models.CharField(max_length=160, null=True, blank=True)
    order_num = models.IntegerField(default=0, editable=False)

    def order_num_plus_one(self):
        return self.order_num + 1

    def order_num_minus_one(self):
        return self.order_num - 1

    def next_chapter(self):
        if self.order_num + 1 == self.book.chapter_set.all().count():
            return None
        else:
            return self.book.chapter_set.filter(order_num=self.order_num + 1).first()

    def previous_chapter(self):
        if self.order_num == 0:
            return None
        else:
            return self.book.chapter_set.filter(order_num=self.order_num - 1).first()

    def get_absolute_url(self):
        return reverse("chapter-detail", args=[self.book.id_slug, self.order_num])

    def get_create_url(self):
        return reverse("chapter-create", args=[self.book.id_slug, ])

    def __str__(self):
        return self.title
