# Generated by Django 4.2.4 on 2023-08-18 11:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("portal", "0012_remove_priorauthdenial_cover_my_meds_key_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="priorauthdenial",
            name="notes",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="requestnewpriorauthrequirements",
            name="notes",
            field=models.TextField(blank=True, null=True),
        ),
    ]