from django.urls import path, include

from .requirements.urls import requirements_urls


api_url_patterns = [
    path('requirements/', include(requirements_urls)),
]
