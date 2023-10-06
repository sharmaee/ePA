from typing import Union
from django.conf import settings
from rest_framework.exceptions import (
    APIException,
    ValidationError,
    AuthenticationFailed,
)
from rest_framework import status

error_props = settings.ERROR_RESPONSE_PROPS


class PortalException(APIException):
    """
    Providing the common client response format to REST API exceptions.
    Common API error format
        * descriptive message is stored in `eror_props.DETAILED_MSG` property
        * all validation errors are listed in `eror_props.VALIDATION_ERRORS` property
        * any extra information useful for debug is stored in `eror_props.SRC_ERROR` poperty
    """

    def __init__(
        self,
        detailed_message: str,
        extra_data: Union[Exception, dict] = None,
        code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    ):
        client_response_data = {error_props.DETAILED_MSG: detailed_message}
        self.status_code = code

        if extra_data is not None:
            # including extra data directly(if dict) or to the 'details' otherwise
            if isinstance(extra_data, dict):
                client_response_data = {**extra_data, **client_response_data}
            else:
                client_response_data[error_props.SRC_ERROR] = extra_data

        super().__init__(client_response_data)

    @staticmethod
    def adapt_to_common_format(exc: Exception):
        """
        Adapts some known errors to the common API error format.
        """
        print(exc)
        # skip entirely if the error is already in the right format
        if isinstance(exc, PortalException):
            return exc

        code = status.HTTP_500_INTERNAL_SERVER_ERROR

        if isinstance(exc, APIException):
            code = exc.status_code

        if isinstance(exc, AuthenticationFailed):
            return PortalException(exc.detail, exc, code)

        if isinstance(exc, ValidationError):
            return PortalException("Validation failed", {error_props.VALIDATION_ERRORS: exc.detail}, code)

        # unknown error. providing original info for debug purposes
        return PortalException(
            "Something went wrong. Please contact us at founders@lamarhealth.com",
            {error_props.DETAILED_MSG: exc.__class__.__name__},
            code,
        )
