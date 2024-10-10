from django.contrib import admin
from django.urls import path
from app.views import WeatherRequestListView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("logs/", WeatherRequestListView.as_view(), name="weather-logs"),
    path("logs/<int:user_id>/", WeatherRequestListView.as_view(), name="user-weather-logs"),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
