from rest_framework import serializers
from .models import Enterprise
from accounts.serializers import StudentSerializer


# THe serializer class allow to fromat the retrieve data in a JSON format
class EnterpriseSerializers(serializers.ModelSerializer):
    students = StudentSerializer(many=True, read_only=True)

    class Meta:
        model = Enterprise
        fields = '__all__'
