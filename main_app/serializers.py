from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 2
        model = User
        # fields = ('last_name', 'first_name', 'middle_name')
        fields = ('id', 'username', 'last_name', 'first_name', 'middle_name')


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 2
        model = Ticket
        # exclude = ('token', 'museum')
        exclude = ('museum',)


class SpecialHallSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 2
        model = Hall
        fields = ('id',)


class ArtifactSerializer(serializers.ModelSerializer):
    hall = SpecialHallSerializer(read_only=True)

    class Meta:
        depth = 2
        model = Artifact
        exclude = ('qr_code',)


class HallSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 2
        model = Hall
        exclude = ('location',)


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 2
        model = Location
        exclude = ('museum',)


class MuseumSerializer(serializers.ModelSerializer):
    # locations = LocationSerializer(read_only=True, many=True)

    class Meta:
        depth = 2
        model = Museum
        fields = '__all__'

# class AllArtifactsSerializer(serializers.ModelSerializer):
#     class Meta:
#         depth = 2
#         model = Artifact
#         exclude = ('description', 'audio', 'qr_code')
#
#
# class ArtifactSerializer(serializers.ModelSerializer):
#     class Meta:
#         depth = 2
#         model = Artifact
#         exclude = ('qr_code',)
#
#
# class QRCodeSerializer(serializers.ModelSerializer):
#     class Meta:
#         depth = 2
#         model = Artifact
#         fields = ('qr_code',)
