from django.shortcuts import render
from .serializers import FlightSerializer
from rest_framework import viewsets
from .models import Flight


class FlightView(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer


