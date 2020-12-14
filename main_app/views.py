from rest_framework.response import Response
from django.views.generic.base import View
from rest_framework.views import APIView
from django.http import HttpResponse
from .serializers import *
import os


class ShowArtifactView(APIView):
    """
    Shows current artifact
    """

    def get(self, request, artifact_pk):
        categories = Artifact.objects.get(pk=artifact_pk)
        serializer = ArtifactSerializer(categories, context={'request': request})

        return Response(serializer.data)


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
