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
        artifact_id = Artifact.objects.get(pk=request.data['artifact_id'])
        swap_type = request.data['swap_type']

        current = Artifact.objects.get(pk=artifact_id)
        prev = Artifact.objects.get(pk=current.prev_artifact)
        next = Artifact.objects.get(prev_artifact=artifact_id)

        temp_prev_cur = current.prev_artifact
        temp_prev_prev = prev.prev_artifact
        current.prev_artifact = temp_prev_prev
        prev.prev_artifact = temp_prev_cur
        next.prev_artifact = prev.id

        # if swap_type == 'up':
        #     temp_next_artifact = artifact.next_artifact
        #     artifact

        return Response(True)


class ShowAllArtifactsView(APIView):
    """
    Shows all artifacts
    """

    def get(self, request):

        list_of_artifacts = list()
        artifact = Artifact.objects.get(prev_artifact=None)
        list_of_artifacts.append(artifact)

        for i in range(len(Artifact.objects.all()) - 1):
            artifact = Artifact.objects.get(prev_artifact=artifact.id)
            list_of_artifacts.append(artifact)

        if len(list_of_artifacts) == 1:
            serializer = AllArtifactsSerializer(list_of_artifacts, context={'request': request})
        else:
            serializer = AllArtifactsSerializer(list_of_artifacts, context={'request': request}, many=True)

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
