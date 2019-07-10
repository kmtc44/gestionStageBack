from rest_framework import permissions, viewsets, generics
from rest_framework.parsers import FileUploadParser

from internship.serializers import EnterpriseSerializers, ConventionSerializer
from rest_framework.response import Response

from .models import Enterprise, Convention

from accounts.models import Student


class EnterpriseViewSet(viewsets.ModelViewSet):
    queryset = Enterprise.objects.all().order_by('-id')
    parser_class = (FileUploadParser,)
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


class EnterprisePartnerView(generics.ListAPIView):
    queryset = Enterprise.objects.filter(is_partner=True).order_by('-id')
    serializer_class = EnterpriseSerializers


class EnterprisePotentialView(generics.ListAPIView):
    queryset = Enterprise.objects.filter(is_partner=False).order_by('-id')
    serializer_class = EnterpriseSerializers


class ConventionViewSet(viewsets.ModelViewSet):
    queryset = Convention.objects.all().order_by('-id')
    serializer_class = ConventionSerializer

    def create(self, request, *args, **kwargs):
        print(request.data)
        title = request.data['title']
        life_time = request.data['life_time']
        state = request.data['state']
        enterpriseId = request.data['enterprise']
        enterprise = Enterprise.objects.get(id=enterpriseId)
        convention = Convention(
            title=title, enterprise=enterprise, life_time=life_time, state=state)
        convention.save()
        return Response(ConventionSerializer(convention).data)
