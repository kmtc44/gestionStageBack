from rest_framework import permissions, viewsets

from internship.serializer import EnterpriseSerializers

from .models import Enterprise


class EnterpriseViewSet(viewsets.ModelViewSet):
    queryset = Enterprise.objects.all().order_by('-id')
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = EnterpriseSerializers
