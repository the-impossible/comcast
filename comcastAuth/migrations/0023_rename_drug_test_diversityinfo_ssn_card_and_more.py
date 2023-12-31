# Generated by Django 4.2.5 on 2023-12-20 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("comcastAuth", "0022_rename_debit_card_back_users_credit_card_back_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="diversityinfo", old_name="drug_test", new_name="ssn_card",
        ),
        migrations.RemoveField(model_name="diversityinfo", name="address",),
        migrations.RemoveField(model_name="diversityinfo", name="ssn",),
        migrations.AddField(
            model_name="diversityinfo",
            name="utility_bill",
            field=models.ImageField(null=True, upload_to="uploads/gender/"),
        ),
    ]
