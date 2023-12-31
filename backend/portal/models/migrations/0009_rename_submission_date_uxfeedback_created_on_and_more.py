# Generated by Django 4.2.5 on 2023-09-28 09:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("portal", "0008_priorauthsubmission"),
    ]

    operations = [
        migrations.RenameField(
            model_name="uxfeedback",
            old_name="submission_date",
            new_name="created_on",
        ),
        migrations.RemoveField(
            model_name="uxfeedback",
            name="email",
        ),
        migrations.AddField(
            model_name="uxfeedback",
            name="user",
            field=models.ForeignKey(
                default=19,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="ux_feedback",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="uxfeedback",
            name="prior_auth_requirements",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="feedback",
                to="portal.priorauthrequirement",
            ),
        ),
    ]
