from rest_framework import serializers
from .models import *


class ArtifactSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 2
        model = Artifact
        fields = '__all__'
