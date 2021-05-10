# Generated by Django 3.1.8 on 2021-05-10 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "course_type",
                    models.CharField(
                        choices=[
                            ("laboratory", "Laboratory"),
                            ("lecture", "Lecture"),
                            ("seminary", "Seminary"),
                        ],
                        max_length=10,
                    ),
                ),
                ("ects_for_course", models.SmallIntegerField(default=1)),
            ],
        ),
    ]
