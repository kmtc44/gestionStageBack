from rest_framework import permissions, viewsets

from internship.serializers import EnterpriseSerializers
from rest_framework.response import Response

from .models import Enterprise, Convention

from accounts.models import Student


class EnterpriseViewSet(viewsets.ModelViewSet):
    queryset = Enterprise.objects.all().order_by('-id')
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EnterpriseSerializers

    def update(self, request, pk):
        students_id = request.data['students']
        for student_id in students_id:
            student = Student.objects.get(id=student_id)
            enterprise = Enterprise.objects.get(id=pk)
            student.enterprise = enterprise
            student.save()

        return Response(EnterpriseSerializers(enterprise).data)


# class ConventionViewSet(viewsets.ModelViewSet):
#     queryset = Convention.objects
