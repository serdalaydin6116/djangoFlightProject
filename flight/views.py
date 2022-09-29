from django.shortcuts import render
from .serializers import FlightSerializer, ReservationSerializer,StaffFlightSerializer
from rest_framework import viewsets
from .models import Flight, Passenger, Reservation
from .permissions import IsStafforReadOnly
from datetime import datetime, date


class FlightView(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes= (IsStafforReadOnly,)

    def get_serializer_class(self):
        serializer=super().get_serializer_class()
        if self.request.user.is_staff:
            return StaffFlightSerializer
        return FlightSerializer

    #user sadece müteakip uçuşları, admin hepsini
    def get_queryset(self):  #karşılaştırma önce şu anki tarih saati almalıyım
        now=datetime.now()
        current_time=now.strftime('%H:%M:%S')
        today=date.today()
        #staff hepsini görecek
        if self.request.user.is_staff:
            return super().get_queryset
        else:
            queryset=Flight.objects.filter(date_of_departure__gt=today) ##filter lookupları (contains, exists, startswith..) kullanırken iki altçizgi ile
            if Flight.objects.filter(date_of_departure=today): #bugun olanları saat olarak filterla
                today_qs=Flight.objects.filter(date_of_departure=today).filter(etd__gt=current_time) #önce bugune göre filterla, sonra bu saatten sonrakileri al
                ##şimdi elimde 2 tane queryset var, birleştirmeliyim.
                queryset=queryset.union(today_qs)
                return queryset



class ReservationView(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def get_queryset(self):
        queryset=super().get_queryset()
        if self.request.user.is_staff:  # admin ise tum flight ve reservationları göster
            return queryset
        return queryset.filter(user=self.request.user) #staff değilse sadece flights ları göster




