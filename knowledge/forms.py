from django.forms import ModelForm
from knowledge.models import Book, Chapter


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = [
            'title',
            'author',
            'year',
            'summary'
        ]


class ChapterForm(ModelForm):
    class Meta:
        model = Chapter
        fields = [
            'title',
            'summary'
        ]
