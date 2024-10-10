from django.db import models


class WeatherRequest(models.Model):
    user_id = models.BigIntegerField()
    command = models.CharField(max_length=100)
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_id} {self.command}"


class UserSettings(models.Model):
    user_id = models.BigIntegerField(unique=True)
    preferred_city = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Настройки пользователя {self.user_id}"


