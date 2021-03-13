from django import forms

from tracker.models import Issue, Status, Issue_type


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ('summary', 'description', 'status', 'issue_type')


class IssueDeleteForm(forms.Form):
    summary = forms.CharField(max_length=120, required=True, label='Введите название задачи, чтобы удалить её')
