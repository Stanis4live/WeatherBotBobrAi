from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from app.models import WeatherRequest
from app.serializers import WeatherRequestSerializer


class WeatherRequestListView(generics.ListAPIView):
    serializer_class = WeatherRequestSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['timestamp']

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        if user_id:
            return WeatherRequest.objects.filter(user_id=user_id)
        return WeatherRequest.objects.all()