# Generated by Django 5.1.1 on 2024-09-14 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_task_exp_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='completed_on',
            field=models.DateTimeField(blank=True),
        ),
    ]
