from rest_framework.response import Response
from django.views.generic.base import View
from rest_framework.views import APIView
from django.http import HttpResponse
from .serializers import *
import os


class CurrentLocationView(APIView):
    """
    Shows or changes or deletes current location
    """

    def get(self, request):
        locations = Location.objects.filter(museum=request.user.museum)
        serializer = SpecialLocationSerializer(locations, context={'request': request}, many=True)
        return Response(serializer.data)

    def post(self, request):
        name = request.data['name']
        img = request.FILES['img']
        description = request.data['description']

        new_location = Location.objects.create(name=name, img=img, description=description, museum=request.user.museum)
        new_location.save()

        locations = Location.objects.filter(museum=request.user.museum)
        serializer = SpecialLocationSerializer(locations, context={'request': request}, many=True)
        return Response(serializer.data)

    def put(self, request):
        location = Location.objects.get(pk=request.data['location_id'])

        location.name = request.data['name']
        location.description = request.data['description']
        location.img = request.FILES['img']
        location.save()

        locations = Location.objects.filter(museum=request.user.museum)
        serializer = SpecialLocationSerializer(locations, context={'request': request}, many=True)
        return Response(serializer.data)

    # def delete(self, request):


class CurrentMuseumView(APIView):
    """
    Shows or changes current museum
    """

    def get(self, request):
        museum = Museum.objects.get(admins=request.user)
        serializer = MuseumSerializer(museum, context={'request': request})

        return Response(serializer.data)

    def put(self, request):
        museum = Museum.objects.get(pk=request.data['museum_id'])

        # img = request.FILES['img']
        # img_extension = img.name.split(".")[-1].lower()

        museum.name = request.data['name']
        museum.description = request.data['description']
        museum.img = request.FILES['img']
        museum.save()

        museum = Museum.objects.get(admins=request.user)
        serializer = MuseumSerializer(museum, context={'request': request})

        return Response(serializer.data)


class SwapArtifactsView(APIView):
    """
    Swaps two current artifacts
    """

    def post(self, request):
        swap_type = request.data['swap_type']

        if swap_type == 'up':

            cur = Artifact.objects.get(pk=request.data['artifact_id'])
            up = Artifact.objects.get(pk=cur.prev_artifact)
            try:
                down = Artifact.objects.get(prev_artifact=cur.id)
                # deleting obj from list
                cur.prev_artifact = None
                down.prev_artifact = up.id
                # adding obj to list
                cur.prev_artifact = up.prev_artifact
                up.prev_artifact = cur.id

                cur.save()
                up.save()
                down.save()

            except:  # exception only if 'cur' is the last el in the list (then obj 'down' doesn't exists)
                cur.prev_artifact = up.prev_artifact
                up.prev_artifact = cur.id

                cur.save()
                up.save()

        elif swap_type == 'down':

            cur = Artifact.objects.get(prev_artifact=request.data['artifact_id'])
            up = Artifact.objects.get(pk=cur.prev_artifact)
            try:
                down = Artifact.objects.get(prev_artifact=cur.id)

                # deleting obj from list
                cur.prev_artifact = None
                down.prev_artifact = up.id
                # adding obj to list
                cur.prev_artifact = up.prev_artifact
                up.prev_artifact = cur.id

                cur.save()
                up.save()
                down.save()

            except:
                cur = Artifact.objects.get(prev_artifact=request.data['artifact_id'])
                up = Artifact.objects.get(pk=request.data['artifact_id'])

                cur.prev_artifact = up.prev_artifact
                up.prev_artifact = cur.id

                cur.save()
                up.save()
        else:
            return Response(False)

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

        # objs = Artifact.objects.all()
        # serializer = AllArtifactsSerializer(objs, context={'request': request}, many=True)

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
