from django.db import models
from django.forms import ModelChoiceField
# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Issue(BaseModel):
    summary = models.CharField(max_length = 60, null = False, blank = False, verbose_name = "Заголовок")
    description = models.CharField(max_length = 2000, null = True, blank=True, verbose_name = "Описание")
    status = models.ForeignKey("tracker.Status", on_delete=models.PROTECT, related_name="status", verbose_name="Статус")
    issue_type = models.ForeignKey("models.Issue_type", on_delete=models.PROTECT, related_name="issue_type", verbose_name="Тип_задачи")

    class Meta:
        db_table = "issues"
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
    
    def __str__(self):
        return f'{self.id}. {self.summary}: {self.status}, {self.issue_type}, {self.description}'


class Status(models.Model):
    status_code = models.CharField(max_length=20, null=False, blank=False)

    class Meta:
        db_table = "statuses"
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"

    def __str__(self):
        return f'{self.id}: {self.status_code}'


class Issue_type(models.Model):
    issue_type_code = models.CharField(max_length=20, null=False, blank=False)

    class Meta:
        db_table = "issue_types"
        verbose_name = "Тип"
        verbose_name_plural = "Типы"

    def __str__(self):
        return f'{self.id}: {self.issue_type_code}'     


