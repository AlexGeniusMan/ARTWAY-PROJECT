from rest_framework import serializers
from .models import *


class SpecialLocationSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 2
        model = Location
        exclude = ('museum',)


class MuseumSerializer(serializers.ModelSerializer):
    locations = SpecialLocationSerializer(read_only=True, many=True)

    class Meta:
        depth = 2
        model = Museum
        fields = ('id', 'name', 'img', 'description', 'locations')


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
