# Generated by Django 3.1.7 on 2021-04-20 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0008_auto_20210418_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='project',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project', to='tracker.project'),
        ),
    ]
