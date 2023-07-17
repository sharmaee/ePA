from django.db import migrations
from django.contrib.postgres.operations import TrigramExtension


class Migration(migrations.Migration):
    dependencies = [
        ("portal", "0002_alter_priorauthrequirement_insurance_coverage_state_and_more"),
    ]

    operations = [
        TrigramExtension(),
    ]
