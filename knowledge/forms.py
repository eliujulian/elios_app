from django.forms import ModelForm
from django import forms
from knowledge.models import Book, Chapter


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = [
            'title',
            'author',
            'year',
            'summary',
            'source'
        ]
        labels = {
            'title': 'Titel',
            'author': 'Autor',
            'year': 'Jahr',
            'summary': 'Zusammenfassung',
            'source': 'Fundstelle'
        }
        widgets = {
            'summary': forms.Textarea(attrs={'cols': 70, 'rows': 30})
        }



class ChapterForm(ModelForm):
    class Meta:
        model = Chapter
        fields = [
            'title',
            'summary',
            'source'
        ]
        labels = {
            'title': 'Titel',
            'summary': 'Zusammenfassung',
            'source': 'Fundstelle'
        }
        widgets = {
            'summary': forms.Textarea(attrs={'cols': 70, 'rows': 30})
        }
