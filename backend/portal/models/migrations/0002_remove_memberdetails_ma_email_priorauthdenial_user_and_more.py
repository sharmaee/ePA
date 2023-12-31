# Generated by Django 4.2.4 on 2023-09-05 14:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("portal", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="memberdetails",
            name="ma_email",
        ),
        migrations.AddField(
            model_name="priorauthdenial",
            name="user",
            field=models.ForeignKey(
                default=5,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="denials",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="requestnewpriorauthrequirements",
            name="user",
            field=models.ForeignKey(
                default=5,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="requests_new_pa",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="priorauthdenial",
            name="member_details",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="denials",
                to="portal.memberdetails",
            ),
        ),
        migrations.AlterField(
            model_name="requestnewpriorauthrequirements",
            name="member_details",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="requests_new_pa",
                to="portal.memberdetails",
            ),
        ),
    ]
