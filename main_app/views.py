from rest_framework.response import Response
from django.views.generic.base import View
from rest_framework.views import APIView
from django.http import HttpResponse
from .serializers import *
from io import BytesIO
import qrcode
import os
from PIL import Image
import json
import base64


class ShowArtifactView(APIView):
    """
    Shows current artifact
    """

    def get(self, request, artifact_pk):
        categories = Artifact.objects.get(pk=artifact_pk)
        serializer = ArtifactSerializer(categories, context={'request': request})

        return Response(serializer.data)


class ShowQRCodeOfCurrentArtifactView(APIView):
    """
    Shows QR-code of current artifact
    """

    def get(self, request, artifact_pk):
        img = qrcode.make('Some data here')
        image_64_encode = base64.encodestring(img)
        # buffered = BytesIO()
        # image.save(buffered, format="JPEG")
        # img_str = base64.b64encode(buffered.getvalue())
        return Response(image_64_encode)


class ReactAppView(View):

    def get(self, request):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        try:
            with open(os.path.join(BASE_DIR, 'frontend', 'build', 'index.html')) as file:
                return HttpResponse(file.read())

        except:
            return HttpResponse(
                """
                index.html not found ! build your React app !!
                """,
                status=501,
            )
