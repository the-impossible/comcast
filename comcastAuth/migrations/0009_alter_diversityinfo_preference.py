# Generated by Django 4.2.5 on 2023-09-20 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("comcastAuth", "0008_diversityinfo_email"),
    ]

    operations = [
        migrations.AlterField(
            model_name="diversityinfo",
            name="preference",
            field=models.CharField(max_length=50),
        ),
    ]