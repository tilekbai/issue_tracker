from django import forms

from tracker.models import Issue


class IssueForm(forms.ModelForm):
    """ 
    Форма для создания и редактирваония объектов статьи
    https://docs.djangoproject.com/en/3.1/ref/forms/
    """
    class Meta:
        model = Issue
        fields = ('summary', 'description', 'status', 'issue_type')


class IssueDeleteForm(forms.Form):
    summary = forms.CharField(max_length=120, required=True, label='Введите название задачи, чтобы удалить её')
