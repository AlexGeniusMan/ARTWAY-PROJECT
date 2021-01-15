from rest_framework.response import Response
from django.views.generic.base import View
from rest_framework.views import APIView
from django.http import HttpResponse
from .serializers import *
import os


def serialize_museum_and_locations(request):
    list_of_locations = list()
    location = Location.objects.get(prev=None)
    list_of_locations.append(location)
    for i in range(len(Location.objects.filter(museum=request.user.museum)) - 1):
        location = Location.objects.get(prev=location.id)
        list_of_locations.append(location)
    if len(list_of_locations) == 1:
        locations_serializer = LocationSerializer(list_of_locations, context={'request': request})
    else:
        locations_serializer = LocationSerializer(list_of_locations, context={'request': request}, many=True)

    museum = Museum.objects.get(admins=request.user)
    museum_serializer = MuseumSerializer(museum, context={'request': request})

    return {
        'museum': museum_serializer.data,
        'locations': locations_serializer.data
    }


def swap_and_save_location(swap_type, request):
    if swap_type == 'up':
        cur = Location.objects.get(pk=request.data['obj_id'])
    elif swap_type == 'down':
        cur = Location.objects.get(prev=request.data['obj_id'])
    up = Location.objects.get(pk=cur.prev)
    try:
        down = Location.objects.get(prev=cur.id)
        cur.prev = None  # deleting obj from list
        down.prev = up.id
        cur.prev = up.prev  # adding obj to list
        up.prev = cur.id
        cur.save()
        up.save()
        down.save()
    except:  # exception only if 'cur' is the last el in the list (then obj 'down' doesn't exists)
        if swap_type == 'down':
            cur = Location.objects.get(prev=request.data['obj_id'])
            up = Location.objects.get(pk=request.data['obj_id'])
        cur.prev = up.prev
        up.prev = cur.id
        cur.save()
        up.save()
    return True


def delete_location(request, location_pk):
    cur = Location.objects.get(pk=location_pk)
    down = Location.objects.get(prev=cur.id)

    down.prev = cur.prev
    down.save()
    cur.delete()
    return True


class SwapLocationsView(APIView):
    """
    Swaps current location with upper or lower location
    """

    def post(self, request):
        swap_type = request.data['swap_type']
        swap_and_save_location(swap_type, request)
        return Response(serialize_museum_and_locations(request))


class AllLocationsView(APIView):
    """
    Shows or changes or deletes current location
    """

    def get(self, request):
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, context={'request': request}, many=True)
        return Response(serializer.data)


class CurrentLocationView(APIView):
    """
    Shows or changes or deletes current location
    """

    def get(self, request, location_pk):
        location = Location.objects.get(pk=location_pk)
        serializer = LocationSerializer(location, context={'request': request})
        return Response(serializer.data)

    def put(self, request, location_pk):
        location = Location.objects.get(pk=location_pk)

        location.name = request.data['name']
        location.description = request.data['description']
        try:
            location.img = request.FILES['img']
        except:
            pass
        location.save()

        location = Location.objects.get(pk=location_pk)
        serializer = LocationSerializer(location, context={'request': request})
        return Response(serializer.data)

    def delete(self, request, location_pk):
        delete_location(request, location_pk)
        return Response(serialize_museum_and_locations(request))


class CurrentMuseumView(APIView):
    """
    Shows or changes current museum
    """

    def get(self, request):
        return Response(serialize_museum_and_locations(request))

    def post(self, request):
        name = request.data['name']
        img = request.FILES['img']
        description = request.data['description']

        new_location = Location.objects.create(name=name, img=img, description=description,
                                               museum=request.user.museum.id)
        new_location.save()

        return Response(serialize_museum_and_locations(request))

    def put(self, request):
        museum = Museum.objects.get(pk=request.user.museum.id)

        # img = request.FILES['img']
        # img_extension = img.name.split(".")[-1].lower()

        museum.name = request.data['name']
        museum.description = request.data['description']
        try:
            museum.img = request.FILES['img']
        except:
            pass
        museum.save()

        return Response(serialize_museum_and_locations(request))


def swap_and_save_artifact(swap_type, request):
    if swap_type == 'up':
        cur = Artifact.objects.get(pk=request.data['obj_id'])
    elif swap_type == 'down':
        cur = Artifact.objects.get(prev=request.data['obj_id'])
    up = Artifact.objects.get(pk=cur.prev)
    try:
        down = Artifact.objects.get(prev=cur.id)
        cur.prev = None  # deleting obj from list
        down.prev = up.id
        cur.prev = up.prev  # adding obj to list
        up.prev = cur.id
        cur.save()
        up.save()
        down.save()
    except:  # exception only if 'cur' is the last el in the list (then obj 'down' doesn't exists)
        if swap_type == 'down':
            cur = Artifact.objects.get(prev=request.data['obj_id'])
            up = Artifact.objects.get(pk=request.data['obj_id'])
        cur.prev = up.prev
        up.prev = cur.id
        cur.save()
        up.save()
    return True


class SwapArtifactsView(APIView):
    """
    Swaps current artifact with upper or lower artifact
    """

    def post(self, request):
        swap_type = request.data['swap_type']
        swap_and_save_artifact(swap_type, request)
        return Response(True)


class ShowAllArtifactsView(APIView):
    """
    Shows all artifacts
    """

    def get(self, request):

        list_of_artifacts = list()
        artifact = Artifact.objects.get(prev=None)
        list_of_artifacts.append(artifact)

        for i in range(len(Artifact.objects.all()) - 1):
            artifact = Artifact.objects.get(prev=artifact.id)
            list_of_artifacts.append(artifact)

        if len(list_of_artifacts) == 1:
            serializer = AllArtifactsSerializer(list_of_artifacts, context={'request': request})
        else:
            serializer = AllArtifactsSerializer(list_of_artifacts, context={'request': request}, many=True)

        # objs = Artifact.objects.all()
        # serializer = AllArtifactsSerializer(objs, context={'request': request}, many=True)

        return Response(serializer.data)


class ShowCurrentArtifactView(APIView):
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

# class SwapArtifactsView(APIView):
#     """
#     Swaps two current artifacts
#     """
#
#     def post(self, request):
#         swap_type = request.data['swap_type']
#
#         if swap_type == 'up':
#
#             cur = Artifact.objects.get(pk=request.data['artifact_id'])
#             up = Artifact.objects.get(pk=cur.prev_artifact)
#             print(1)
#
#             try:
#                 down = Artifact.objects.get(prev_artifact=cur.id)
#                 # deleting obj from list
#                 cur.prev_artifact = None
#                 down.prev_artifact = up.id
#                 # adding obj to list
#                 cur.prev_artifact = up.prev_artifact
#                 up.prev_artifact = cur.id
#
#                 cur.save()
#                 up.save()
#                 down.save()
#
#             except:  # exception only if 'cur' is the last el in the list (then obj 'down' doesn't exists)
#                 cur.prev_artifact = up.prev_artifact
#                 up.prev_artifact = cur.id
#
#                 cur.save()
#                 up.save()
#
#         elif swap_type == 'down':
#
#             cur = Artifact.objects.get(prev_artifact=request.data['artifact_id'])
#             up = Artifact.objects.get(pk=cur.prev_artifact)
#             try:
#                 down = Artifact.objects.get(prev_artifact=cur.id)
#
#                 # deleting obj from list
#                 cur.prev_artifact = None
#                 down.prev_artifact = up.id
#                 # adding obj to list
#                 cur.prev_artifact = up.prev_artifact
#                 up.prev_artifact = cur.id
#
#                 cur.save()
#                 up.save()
#                 down.save()
#
#             except:
#                 cur = Artifact.objects.get(prev_artifact=request.data['artifact_id'])
#                 up = Artifact.objects.get(pk=request.data['artifact_id'])
#
#                 cur.prev_artifact = up.prev_artifact
#                 up.prev_artifact = cur.id
#
#                 cur.save()
#                 up.save()
#         else:
#             return Response(False)
#
#         return Response(True)
