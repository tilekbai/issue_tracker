from django import forms

from tracker.models import Issue, Status, Issue_type


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ('summary', 'description', 'status', 'issue_type')
        issue_type = forms.ModelMultipleChoiceField(required=False, label="Типы", queryset=Issue_type.objects.all())

    def clean_summary(self):
        summary = self.cleaned_data["summary"]
        if len(summary) < 4:
            raise ValidationError("Название задачи слишком короткое!")
        return summary

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data["summary"] == cleaned_data["description"]:
            raise ValidationError("Название и описание задачи не должны быть одинаковыми!")
        return cleaned_data


class IssueDeleteForm(forms.Form):
    summary = forms.CharField(max_length=120, required=True, label='Введите название задачи, чтобы удалить её')
