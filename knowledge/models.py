from django.db import models
from core.models import AbstractBaseModel


class Book(AbstractBaseModel):
    class Meta:
        abstract = True

    title = models.CharField(max_length=160)
    author = models.CharField(max_length=160)
    year = models.IntegerField()
    is_favorite = models.BooleanField(default=False)
    summary = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.author} - {self.title} ({str(self.year)})'


class Chapter(AbstractBaseModel):
    class Meta:
        abstract = True

    book = models.ForeignKey(to=Book, on_delete=models.CASCADE)
    title = models.CharField(max_length=160)
    summary = models.TextField(null=True, blank=True)
    order_num = models.IntegerField(default=0)

    def __str__(self):
        return self.title
