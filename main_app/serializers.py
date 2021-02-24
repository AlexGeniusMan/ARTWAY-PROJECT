from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 2
        model = User
        fields = ('id', 'username', 'last_name', 'first_name', 'middle_name')


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 2
        model = Ticket
        exclude = ('museum',)


class SpecialHallSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 2
        model = Hall
        fields = ('id',)


# class ArtifactLinkSerializer(serializers.ModelSerializer):
#     class Meta:
#         depth = 2
#         model = ArtifactLink
#         exclude = ('id', 'artifact')


class ArtifactSerializer(serializers.ModelSerializer):
    hall = SpecialHallSerializer(read_only=True)
    # links = ArtifactLinkSerializer(read_only=True, many=True)

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
    class Meta:
        depth = 2
        model = Museum
        fields = '__all__'
