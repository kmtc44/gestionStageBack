from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, ListCreateAPIView
from rest_framework import permissions, viewsets

from .models import Enterprise
from .serializer import EnterpriseSerializers

# Create your views here.


class EnterpriseListView(ListAPIView):
    queryset = Enterprise.objects.all().order_by('-id')
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = EnterpriseSerializers


class EnterpriseDetailView(RetrieveAPIView):
    queryset = Enterprise.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = EnterpriseSerializers


class EnterpriseListCreateView(ListCreateAPIView):
    queryset = Enterprise.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = EnterpriseSerializers
