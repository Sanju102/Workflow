# Generated by Django 5.1.1 on 2024-09-11 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='exp_end_date',
            field=models.DateTimeField(default=None),
            preserve_default=False,
        ),
    ]
