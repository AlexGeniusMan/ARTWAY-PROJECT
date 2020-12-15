from rest_framework import serializers
from .models import *


class AllArtifactsSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 2
        model = Artifact
        exclude = ('description', 'audio', 'qr_code')


class ArtifactSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 2
        model = Artifact
        exclude = ('qr_code',)


class QRCodeSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 2
        model = Artifact
        fields = ('qr_code',)
