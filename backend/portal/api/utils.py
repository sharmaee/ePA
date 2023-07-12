from typing import Any

from rest_framework import views
from portal.exceptions import PortalException


def api_exception_handler(exc: Exception, context: dict[str, Any]) -> views.Response:
    """Custom API exception handler."""

    adapted_esc = PortalException.adapt_to_common_format(exc)

    # get the standard error response
    return views.exception_handler(adapted_esc, context)
