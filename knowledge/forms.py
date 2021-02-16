from django.forms import ModelForm
from knowledge.models import Book


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = [
            'title',
            'author',
            'year',
            'summary'
        ]
