# Generated by Django 3.1.8 on 2021-05-13 09:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_lecturer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lecturer',
            name='courses',
        ),
    ]
