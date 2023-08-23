from django import forms
from .models import Question, Answer, Category


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'category', 'text']
        labels = {
            'text': 'Text',
            'category': 'Category',
            'title': 'Title',
        }
        category = forms.ModelChoiceField(queryset=Category.objects.all()),
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'})
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']
        labels = {'text': ''}
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'})
        }