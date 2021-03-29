from django.db import models
from django.forms import ModelChoiceField
from django.core.validators import MinLengthValidator

# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Issue(BaseModel):
    summary = models.CharField(max_length = 60, null = False, blank = False, verbose_name = "Заголовок", validators=[MinLengthValidator(4)])
    description = models.CharField(max_length = 2000, null = True, blank=True, verbose_name = "Описание", validators=[MinLengthValidator(10)])
    status = models.ForeignKey("tracker.Status", on_delete=models.PROTECT, related_name="status", verbose_name="Статус", null=True, blank=True)
    issue_type = models.ManyToManyField("tracker.Issue_type", related_name="issue_type", blank=True)
    project = models.ForeignKey("tracker.Project", on_delete=models.PROTECT, related_name="project", null=True, blank=True, default=1)

    class Meta:
        db_table = "issues"
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
    
    def __str__(self):
        return f'{self.id}. {self.summary}. Status: {self.status}. Type: {self.issue_type.all()}, Descripton: {self.description}. Project: {self.project}.'


class Status(models.Model):
    status_code = models.CharField(max_length=20, null=False, blank=False)

    class Meta:
        db_table = "statuses"
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"

    def __str__(self):
        return f'{self.status_code}'


class Issue_type(models.Model):
    issue_type_code = models.CharField(max_length=20, null=False, blank=False)

    class Meta:
        db_table = "issue_types"
        verbose_name = "Тип"
        verbose_name_plural = "Типы"

    def __str__(self):
        return f'{self.issue_type_code}'     


class Project(models.Model):
    start_date = models.DateField(auto_now=False)
    end_date = models.DateField(auto_now=False, null=True, blank=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    class Meta:
        db_table = "project"
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

    def __str__(self):
        return f"{self.name}"
