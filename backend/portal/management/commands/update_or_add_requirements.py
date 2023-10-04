import logging
from django.core.management.base import BaseCommand
from portal.logic.load_csv_data.load_requirements import generate_insurance_coverage_criteria_objects

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Updates or creates prior auth requirements to the database'

    def handle(self, *args, **options):
        generate_insurance_coverage_criteria_objects()
        logger.info('Requirements successfully updated')
