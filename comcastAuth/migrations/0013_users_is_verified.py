# Generated by Django 4.2.5 on 2023-09-25 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "comcastAuth",
            "0012_salaryaccount_remove_users_name_remove_users_phone_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="users",
            name="is_verified",
            field=models.BooleanField(default=False),
        ),
    ]
