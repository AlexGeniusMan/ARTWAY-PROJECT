import random
import string
from datetime import timedelta
from django.db.models import Q
from django.utils.datetime_safe import datetime
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from django.views.generic.base import View
from rest_framework.views import APIView
from django.http import HttpResponse
from project.settings import MEDIA_ROOT, DOMAIN_NAME
from .permissions import *
from .serializers import *
import os
from .models import User
from rest_framework.permissions import BasePermission, IsAuthenticated
from django.contrib.auth.models import Group
import segno
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
# import matplotlib.pyplot as plt
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak
from svglib.svglib import svg2rlg
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase import ttfonts
# from PyPDF2 import PdfFileMerger


def is_ticket_valid(museum_pk, token):
    museum = Museum.objects.get(pk=museum_pk)
    d = datetime.now() - timedelta(hours=museum.ticket_lifetime)
    tickets = Ticket.objects.filter(museum=museum).filter(created_at__gte=d)
    try:
        ticket = Ticket.objects.filter(museum=museum).get(token=token)
    except:
        return False

    if ticket in tickets:
        return True
    else:
        return False


class ArtifactsFromThisHallView(APIView):
    """
    Shows artifacts of current artifact's hall
    """

    def post(self, request):
        token = request.data['token']
        artifact_pk = request.data['artifact_pk']
        hall_pk = Artifact.objects.get(pk=artifact_pk).hall.id

        ticket = Ticket.objects.get(token=token)

        if is_ticket_valid(ticket.museum.id, token):
            hall = Hall.objects.get(pk=hall_pk)

            temp_len = len(Artifact.objects.filter(hall=hall_pk))
            if temp_len > 1:
                list_of_artifacts = list()
                artifact = Artifact.objects.filter(hall=hall_pk).get(prev=None)
                list_of_artifacts.append(artifact)

                for i in range(len(Artifact.objects.filter(hall=hall_pk)) - 1):
                    artifact = Artifact.objects.get(prev=artifact.id)
                    list_of_artifacts.append(artifact)

                artifacts_serializer = ArtifactSerializer(list_of_artifacts, context={'request': request}, many=True)

                return Response({
                    'artifacts': artifacts_serializer.data
                })
            elif temp_len == 1:
                artifact = Artifact.objects.get(hall=hall)
                artifact_serializer = ArtifactSerializer(artifact, context={'request': request})
                return Response({
                    'artifacts': [artifact_serializer.data]
                })
            else:
                return Response({
                    'artifacts': []
                })
        else:
            return Response({"error_code": 'YOUR TICKET IS EXPIRED', "status": status.HTTP_403_FORBIDDEN})


class ArtifactsMapView(APIView):
    """
    Shows artifacts map of current hall
    """

    def post(self, request):
        token = request.data['token']
        hall_pk = request.data['hall_pk']

        ticket = Ticket.objects.get(token=token)

        if is_ticket_valid(ticket.museum.id, token):
            hall = Hall.objects.get(pk=hall_pk)

            temp_len = len(Artifact.objects.filter(hall=hall_pk))
            if temp_len > 1:
                list_of_artifacts = list()
                artifact = Artifact.objects.filter(hall=hall_pk).get(prev=None)
                list_of_artifacts.append(artifact)

                for i in range(len(Artifact.objects.filter(hall=hall_pk)) - 1):
                    artifact = Artifact.objects.get(prev=artifact.id)
                    list_of_artifacts.append(artifact)

                artifacts_serializer = ArtifactSerializer(list_of_artifacts, context={'request': request}, many=True)

                return Response({
                    'hall': hall.name,
                    'artifacts': artifacts_serializer.data
                })
            elif temp_len == 1:
                artifact = Artifact.objects.get(hall=hall)
                artifact_serializer = ArtifactSerializer(artifact, context={'request': request})
                return Response({
                    'hall': hall.name,
                    'artifacts': [artifact_serializer.data]
                })
            else:
                return Response({
                    'hall': hall.name,
                    'artifacts': []
                })
        else:
            return Response({"error_code": 'YOUR TICKET IS EXPIRED', "status": status.HTTP_403_FORBIDDEN})


class HallsMapView(APIView):
    """
    Shows halls map of current location
    """

    def post(self, request):
        token = request.data['token']
        location_pk = request.data['location_pk']

        ticket = Ticket.objects.get(token=token)

        if is_ticket_valid(ticket.museum.id, token):
            location = Location.objects.get(pk=location_pk)
            temp_len = len(Hall.objects.filter(location=location_pk))

            if temp_len > 1:
                list_of_halls = list()
                hall = Hall.objects.filter(location=location_pk).get(prev=None)
                list_of_halls.append(hall)

                for i in range(len(Hall.objects.filter(location=location_pk)) - 1):
                    hall = Hall.objects.get(prev=hall.id)
                    list_of_halls.append(hall)

                halls_serializer = HallSerializer(list_of_halls, context={'request': request}, many=True)
                return Response({
                    'location': location.name,
                    'halls': halls_serializer.data
                })
            elif temp_len == 1:
                hall = Hall.objects.get(location=location)
                halls_serializer = HallSerializer(hall, context={'request': request})
                return Response({
                    'location': location.name,
                    'halls': [halls_serializer.data]
                })
            else:
                return Response({
                    'location': location.name,
                    'halls': []
                })
        else:
            return Response({"error_code": 'YOUR TICKET IS EXPIRED', "status": status.HTTP_403_FORBIDDEN})


class LocationsMapView(APIView):
    """
    Shows locations map of current museum
    """

    def post(self, request):
        token = request.data['token']
        ticket = Ticket.objects.get(token=token)

        if is_ticket_valid(ticket.museum.id, token):
            museum = ticket.museum
            museum_data = MuseumSerializer(museum, context={'request': request}).data
            temp_len = len(Location.objects.filter(museum=museum))

            if temp_len > 1:
                list_of_locations = list()
                location = Location.objects.filter(museum=museum).get(prev=None)
                list_of_locations.append(location)

                for i in range(len(Location.objects.filter(museum=museum)) - 1):
                    location = Location.objects.get(prev=location.id)
                    list_of_locations.append(location)

                locations_serializer = LocationSerializer(list_of_locations, context={'request': request}, many=True)

                return Response({
                    'museum': museum_data,
                    'locations': locations_serializer.data
                })
            elif temp_len == 1:
                location = Location.objects.get(museum=museum)
                locations_serializer = LocationSerializer(location, context={'request': request})
                return Response({
                    'museum': museum_data,
                    'locations': [locations_serializer.data]
                })
            else:
                return Response({
                    'museum': museum_data,
                    'locations': []
                })
        else:
            return Response({"error_code": 'YOUR TICKET IS EXPIRED', "status": status.HTTP_403_FORBIDDEN})


class CurrentArtifactView(APIView):
    """
    Shows current artifact
    """

    def post(self, request, artifact_pk):
        token = request.data['token']
        artifact = Artifact.objects.get(pk=artifact_pk)
        if is_ticket_valid(artifact.hall.location.museum.id, token):
            serializer = ArtifactSerializer(artifact, context={'request': request})
            return Response(serializer.data)
        else:
            return Response({"error_code": 'YOUR TICKET IS EXPIRED', "status": status.HTTP_403_FORBIDDEN})
