# Generated by Django 3.1.8 on 2021-05-11 12:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_lecturer"),
        ("courses", "0005_auto_20210511_1114"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="lecturer",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="users.lecturer",
            ),
            preserve_default=False,
        ),
    ]
