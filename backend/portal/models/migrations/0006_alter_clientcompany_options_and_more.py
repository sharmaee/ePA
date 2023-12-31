# Generated by Django 4.2.5 on 2023-09-20 10:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("portal", "0005_alter_priorauthdenial_user_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="clientcompany",
            options={
                "verbose_name": "Client Company",
                "verbose_name_plural": "Client Companies",
            },
        ),
        migrations.AlterModelOptions(
            name="priorauthdenial",
            options={
                "ordering": ["-submission_date"],
                "verbose_name": "Denial",
                "verbose_name_plural": "Denials",
            },
        ),
        migrations.AlterModelOptions(
            name="requestnewpriorauthrequirements",
            options={
                "ordering": ["-submission_date"],
                "verbose_name": "Request for More Info",
                "verbose_name_plural": "Requests for More Info",
            },
        ),
        migrations.CreateModel(
            name="RequirementsSearchAction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("insurance_provider", models.TextField(blank=True, null=True)),
                ("insurance_coverage_state", models.TextField(blank=True, null=True)),
                ("medication", models.TextField(blank=True, null=True)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "analytics__requirements_search_action",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="RequirementsSearchActionSummary",
            fields=[],
            options={
                "verbose_name": "Requirements Search Action Summary",
                "verbose_name_plural": "Requirements Search Action Summary",
                "db_table": "analytics__requirements_search_action_summary",
                "ordering": ["-created_on"],
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("portal.requirementssearchaction",),
        ),
    ]
