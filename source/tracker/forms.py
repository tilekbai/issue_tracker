from django import forms
from django.core.exceptions import ValidationError

from tracker.models import Issue, Status, Issue_type


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ('summary', 'description', 'status', 'issue_type')
        issue_type = forms.ModelMultipleChoiceField(required=False, label="Типы", queryset=Issue_type.objects.all())

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data["summary"] == cleaned_data["description"]:
            raise ValidationError("Название и описание задачи не должны быть одинаковыми!", code="message_error", params={"id": "id"})
        return cleaned_data

    def clean_stat_type(self):
        cleaned_data = super().clean()
        if cleaned_data["status"] == cleaned_data["status_type"]:
            raise ValidationError("Статус и тип задачи не должны быть одинаковыми!", code="message_error", params={"id": "id"})
        return cleaned_data


class IssueDeleteForm(forms.Form):
    summary = forms.CharField(max_length=120, required=True, label='Введите название задачи, чтобы удалить её')


class SearchForm(forms.Form):
    search_value = forms.CharField(max_length=100, required=False, label="Поиск")
