from django.contrib import admin
from  app.models import WeatherRequest, UserSettings

admin.site.register(WeatherRequest)
admin.site.register(UserSettings)
