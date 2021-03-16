# Generated by Django 3.1.7 on 2021-03-16 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issue',
            name='issue_type',
        ),
        migrations.AddField(
            model_name='issue',
            name='issue_type',
            field=models.ManyToManyField(blank=True, related_name='issue_type', to='tracker.Issue_type'),
        ),
    ]
