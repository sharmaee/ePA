import logging
from django.core.management.base import BaseCommand
from portal.logic.generate_data.generate_auth_requirements import generate_requirements_objects

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Updates or creates prior auth requirements to the database'

    def handle(self, *args, **options):
        generate_requirements_objects()
        logger.info('Requirements successfully updated')
