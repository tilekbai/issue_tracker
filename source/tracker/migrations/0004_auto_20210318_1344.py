# Generated by Django 3.1.7 on 2021-03-18 07:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0003_auto_20210318_1333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='issue_type',
            field=models.ManyToManyField(blank=True, related_name='issue_type', to='tracker.Issue_type'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='status', to='tracker.status', verbose_name='Статус'),
        ),
    ]
