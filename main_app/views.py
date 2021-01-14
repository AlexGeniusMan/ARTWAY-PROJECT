from rest_framework.response import Response
from django.views.generic.base import View
from rest_framework.views import APIView
from django.http import HttpResponse
from .serializers import *
import os


class SwapArtifactsView(APIView):
    """
    Swaps two current artifacts
    """

    def post(self, request):
        artifact_1 = Artifact.objects.get(pk=request.data['artifact_1'])
        artifact_2 = Artifact.objects.get(pk=request.data['artifact_2'])

        print(artifact_1)
        print(artifact_2)

        return Response(True)


class ShowAllArtifactsView(APIView):
    """
    Shows all artifacts
    """

    def get(self, request):

        artifacts = list()
        artifact = Artifact.objects.get(next_artifact=None)
        artifacts.append(artifact)

        for i in range(len(Artifact.objects.all()) - 1):
            artifact = Artifact.objects.get(next_artifact=artifact.id)
            artifacts.append(artifact)

        serializer = AllArtifactsSerializer(artifacts, context={'request': request}, many=True)

        return Response(serializer.data)


class ShowArtifactView(APIView):
    """
    Shows current artifact
    """

    def get(self, request, artifact_pk):
        artifact = Artifact.objects.get(pk=artifact_pk)
        serializer = ArtifactSerializer(artifact, context={'request': request})

        return Response(serializer.data)


class ShowQRCodeOfCurrentArtifactView(APIView):
    """
    Shows QR-code of current artifact
    """

    def get(self, request, artifact_pk):
        artifact = Artifact.objects.get(pk=artifact_pk)
        artifact.save()
        qr_code = QRCodeSerializer(artifact, context={'request': request})

        return Response(qr_code.data)


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
