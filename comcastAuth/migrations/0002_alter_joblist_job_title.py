# Generated by Django 4.2.5 on 2023-09-18 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("comcastAuth", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="joblist",
            name="job_title",
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
