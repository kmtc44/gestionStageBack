from rest_framework import serializers
from .models import Enterprise


# THe serializer class allow to fromat the retrieve data in a JSON format 
class EnterpriseSerializers(serializers.ModelSerializer):
    class Meta:
        model = Enterprise
        fields = '__all__'
