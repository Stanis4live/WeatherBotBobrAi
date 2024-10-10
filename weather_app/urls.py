from django.contrib import admin
from django.urls import path
from app.views import WeatherRequestListView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("logs/", WeatherRequestListView.as_view(), name="weather-logs"),
    path("logs/<int:user_id>/", WeatherRequestListView.as_view(), name="user-weather-logs"),
]
