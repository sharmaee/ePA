# Generated by Django 4.2.3 on 2023-08-08 10:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("portal", "0006_priorauthrequirement_requirements_flow_file_location"),
    ]

    operations = [
        migrations.AddField(
            model_name="priorauthrequirement",
            name="insurance_plan_type",
            field=models.TextField(blank=True, db_index=True, null=True),
        ),
    ]