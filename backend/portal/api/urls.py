from django.urls import path, include

from .requirements.urls import requirements_urls
from .user_experience.urls import ux_urls
from .denials.urls import denials_urls


api_url_patterns = [
    path('requirements/', include(requirements_urls)),
    path('ux/', include(ux_urls)),
    path('denials/', include(denials_urls)),
]
