from django.urls import path, include

from .requirements.urls import requirements_urls
from .user_experience.urls import ux_urls
from .denials.urls import denials_urls
from .auth.urls import auth_urls
from .analytics.urls import analytics_urls

api_url_patterns = [
    path('requirements/', include(requirements_urls)),
    path('ux/', include(ux_urls)),
    path('denials/', include(denials_urls)),
    path('auth/', include(auth_urls)),
    path('analytics/', include(analytics_urls)),
]
