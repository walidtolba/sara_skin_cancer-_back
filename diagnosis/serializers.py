from rest_framework import serializers
from diagnosis.models import DiagnosisPicture

class DiagnosisPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagnosisPicture
        fields = '__all__'