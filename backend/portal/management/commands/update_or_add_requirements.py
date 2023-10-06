import logging
from django.core.management.base import BaseCommand
from portal.logic.load_csv_data.load_requirements import (
    generate_insurance_coverage_criteria_objects,
    generate_requirement_template_objects,
    generate_requirement_option_template_objects,
    generate_smart_engine_item_objects,
    generate_requirement_option_objects,
)

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Updates or creates prior auth requirements to the database'

    def handle(self, *args, **options):
        logger.info('Adding or updating Insurance Coverage Criteria')
        generate_insurance_coverage_criteria_objects()
        logger.info('Adding or updating Requirement Templates')
        generate_requirement_template_objects()
        logger.info('Adding or updating Requirement Option Templates')
        generate_requirement_option_template_objects()
        logger.info('Adding or updating Smart Engine Items')
        generate_smart_engine_item_objects()
        logger.info('Adding or updating Requirement Options')
        generate_requirement_option_objects()
