# Generated by Django 3.1.8 on 2021-05-13 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_course_lecturer'),
        ('students', '0003_auto_20210510_1001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='courses',
            field=models.ManyToManyField(blank=True, to='courses.Course'),
        ),
    ]
