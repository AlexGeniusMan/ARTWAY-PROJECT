from django.db.models import Q
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from django.views.generic.base import View
from rest_framework.views import APIView
from django.http import HttpResponse

from .permissions import *
from .serializers import *
import os
from .models import User
from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Group


# class CreateNewCashierView(APIView):
#     permission_classes = (IsMuseumAdmin,)
#
#     # permission_classes = [HasGroupPermission]
#     # required_groups = {
#     #     'GET': ['Кассир'],
#     #     # 'POST': ['moderators', 'someMadeUpGroup'],
#     #     # 'PUT': ['__all__'],
#     # }
#
#     def get(self, request):
#         groups = Group.objects.all()
#         print(groups)
#         user = User.objects.get(pk=1)
#         # print(user.groups.all())
#         return Response(True)
#
#     def post(self, request):
#         user = User.objects.create_user(username='awffe', password='123', last_name='Chentsov', first_name='Alex')
#         print(user.groups)
#         return Response(True)


class SwapArtifactsView(APIView):
    """
    Swaps current hall with upper or lower hall
    """
    permission_classes = (IsMuseumAdmin,)

    # queryset = Museum.objects.all()

    def swap_and_save_artifact(self, swap_type, request):
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

    def post(self, request):
        print('oooooooooooooo')
        swap_type = request.data['swap_type']
        self.swap_and_save_artifact(swap_type, request)
        hall_pk = Artifact.objects.get(pk=request.data['obj_id']).hall.id
        location_pk = Hall.objects.get(pk=hall_pk).location.id
        return Response(serialize_hall_and_artifacts(request, location_pk, hall_pk))


class CurrentArtifactView(APIView):
    """
    Shows current artifact
    """

    def get_artifact(self, request, location_pk, hall_pk, artifact_pk):
        artifact = Artifact.objects.get(pk=artifact_pk)
        serializer = ArtifactSerializer(artifact, context={'request': request})
        return serializer.data

    def delete_artifact(self, request, location_pk, hall_pk, artifact_pk):
        cur = Artifact.objects.get(pk=artifact_pk)
        try:
            down = Artifact.objects.get(prev=cur.id)
            down.prev = cur.prev
            down.save()
        except:
            pass
        cur.delete()
        return True

    def get(self, request, location_pk, hall_pk, artifact_pk):
        return Response(self.get_artifact(request, location_pk, hall_pk, artifact_pk))

    def put(self, request, location_pk, hall_pk, artifact_pk):
        artifact = Artifact.objects.get(pk=artifact_pk)

        artifact.name = request.data['name']
        artifact.description = request.data['description']
        try:
            artifact.img = request.FILES['img']
        except:
            pass
        try:
            artifact.audio = request.FILES['audio']
        except:
            pass
        artifact.save()

        return Response(self.get_artifact(request, location_pk, hall_pk, artifact_pk))

    def delete(self, request, location_pk, hall_pk, artifact_pk):
        self.delete_artifact(request, location_pk, hall_pk, artifact_pk)
        return Response(serialize_hall_and_artifacts(request, location_pk, hall_pk))


class SwapHallsView(APIView):
    """
    Swaps current hall with upper or lower hall
    """

    def swap_and_save_hall(self, swap_type, request):
        if swap_type == 'up':
            cur = Hall.objects.get(pk=request.data['obj_id'])
        elif swap_type == 'down':
            cur = Hall.objects.get(prev=request.data['obj_id'])
        up = Hall.objects.get(pk=cur.prev)
        try:
            down = Hall.objects.get(prev=cur.id)
            cur.prev = None  # deleting obj from list
            down.prev = up.id
            cur.prev = up.prev  # adding obj to list
            up.prev = cur.id
            cur.save()
            up.save()
            down.save()
        except:  # exception only if 'cur' is the last el in the list (then obj 'down' doesn't exists)
            if swap_type == 'down':
                cur = Hall.objects.get(prev=request.data['obj_id'])
                up = Hall.objects.get(pk=request.data['obj_id'])
            cur.prev = up.prev
            up.prev = cur.id
            cur.save()
            up.save()
        return True

    def post(self, request):
        swap_type = request.data['swap_type']
        self.swap_and_save_hall(swap_type, request)
        location_pk = Hall.objects.get(pk=request.data['obj_id']).location.id
        return Response(serialize_location_and_halls(request, location_pk))


def serialize_hall_and_artifacts(request, location_pk, hall_pk):
    hall = Hall.objects.get(pk=hall_pk)
    hall_serializer = HallSerializer(hall, context={'request': request})

    temp_len = len(Artifact.objects.filter(hall=hall_pk))
    print(temp_len)

    if temp_len > 1:
        list_of_artifacts = list()
        artifact = Artifact.objects.filter(hall=hall_pk).get(prev=None)
        list_of_artifacts.append(artifact)

        for i in range(len(Artifact.objects.filter(hall=hall_pk)) - 1):
            print('ok')
            artifact = Artifact.objects.get(prev=artifact.id)
            list_of_artifacts.append(artifact)

        artifacts_serializer = ArtifactSerializer(list_of_artifacts, context={'request': request}, many=True)

        return {
            'hall': hall_serializer.data,
            'artifacts': artifacts_serializer.data
        }
    elif temp_len == 1:
        # location = Location.objects.get(pk=location_pk)
        print('ok')
        artifact = Artifact.objects.get(hall=hall_pk)
        print('ok')
        artifact_serializer = ArtifactSerializer(artifact, context={'request': request})
        print('ok')
        return {
            'hall': hall_serializer.data,
            'artifacts': [artifact_serializer.data]
        }
        return True
    else:
        return {
            'hall': hall_serializer.data,
            'artifacts': []
        }


class CurrentHallView(APIView):
    """
    Shows or changes or deletes current hall
    """

    def get_hall(self, request, location_pk, hall_pk):
        return serialize_hall_and_artifacts(request, location_pk, hall_pk)

    def delete_hall(self, request, location_pk, hall_pk):
        cur = Hall.objects.get(pk=hall_pk)
        try:
            down = Hall.objects.get(prev=cur.id)
            down.prev = cur.prev
            down.save()
        except:
            pass
        cur.delete()
        return True

    def get(self, request, location_pk, hall_pk):
        return Response(self.get_hall(request, location_pk, hall_pk))

    def post(self, request, location_pk, hall_pk):
        name = request.data['name']
        img = request.FILES['img']
        audio = request.FILES['audio']
        description = request.data['description']

        try:
            artifact = Artifact.objects.filter(hall=hall_pk).get(prev=None)
            for i in range(len(Artifact.objects.filter(hall=hall_pk)) - 1):
                artifact = Artifact.objects.get(prev=artifact.id)

            hall = Hall.objects.get(pk=hall_pk)
            Artifact.objects.create(name=name, img=img, audio=audio, description=description, hall=hall,
                                    prev=artifact.id)
        except:
            hall = Hall.objects.get(pk=hall_pk)
            Artifact.objects.create(name=name, img=img, audio=audio, description=description, hall=hall, prev=None)

        return Response(serialize_hall_and_artifacts(request, location_pk, hall_pk))

    def put(self, request, location_pk, hall_pk):
        hall = Hall.objects.get(pk=hall_pk)

        hall.name = request.data['name']
        hall.description = request.data['description']
        try:
            hall.img = request.FILES['img']
        except:
            pass
        hall.save()

        return Response(self.get_hall(request, location_pk, hall_pk))

    def delete(self, request, location_pk, hall_pk):
        self.delete_hall(request, location_pk, hall_pk)
        return Response(serialize_location_and_halls(request, location_pk))


class AllArtifactsView(APIView):
    """
    Shows all artifacts
    """

    def get(self, request):
        artifacts = Artifact.objects.all()
        serializer = ArtifactSerializer(artifacts, context={'request': request}, many=True)
        return Response(serializer.data)


class AllHallsView(APIView):
    """
    Shows all halls
    """

    def get(self, request):
        halls = Hall.objects.all()
        serializer = LocationSerializer(halls, context={'request': request}, many=True)
        return Response(serializer.data)


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


class SwapLocationsView(APIView):
    """
    Swaps current location with upper or lower location
    """

    def post(self, request):
        swap_type = request.data['swap_type']
        swap_and_save_location(swap_type, request)
        return Response(serialize_museum_and_locations(request))


def delete_location(request, location_pk):
    cur = Location.objects.get(pk=location_pk)
    try:
        down = Location.objects.get(prev=cur.id)
        down.prev = cur.prev
        down.save()
    except:
        pass
    cur.delete()
    return True


def serialize_location_and_halls(request, location_pk):
    location = Location.objects.get(pk=location_pk)
    location_serializer = LocationSerializer(location, context={'request': request})

    temp_len = len(Hall.objects.filter(location=location_pk))
    print(temp_len)

    if temp_len > 1:
        list_of_halls = list()
        hall = Hall.objects.filter(location=location_pk).get(prev=None)
        list_of_halls.append(hall)

        for i in range(len(Hall.objects.filter(location=location_pk)) - 1):
            print('ok')
            hall = Hall.objects.get(prev=hall.id)
            list_of_halls.append(hall)

        halls_serializer = HallSerializer(list_of_halls, context={'request': request}, many=True)
        return {
            'location': location_serializer.data,
            'halls': halls_serializer.data
        }
    elif temp_len == 1:
        # location = Location.objects.get(pk=location_pk)
        print('ok')
        hall = Hall.objects.get(location=location)
        print('ok')
        halls_serializer = HallSerializer(hall, context={'request': request})
        print('ok')
        return {
            'location': location_serializer.data,
            'halls': [halls_serializer.data]
        }
        return True
    else:
        return {
            'location': location_serializer.data,
            'halls': []
        }


class CurrentLocationView(APIView):
    """
    Shows or changes or deletes current location
    """

    def get(self, request, location_pk):
        return Response(serialize_location_and_halls(request, location_pk))

    def post(self, request, location_pk):
        name = request.data['name']
        img = request.FILES['img']
        description = request.data['description']

        try:
            hall = Hall.objects.filter(location=location_pk).get(prev=None)
            for i in range(len(Hall.objects.filter(location=location_pk)) - 1):
                hall = Hall.objects.get(prev=hall.id)

            location = Location.objects.get(pk=location_pk)
            Hall.objects.create(name=name, img=img, description=description, location=location, prev=hall.id)
        except:
            location = Location.objects.get(pk=location_pk)
            Hall.objects.create(name=name, img=img, description=description, location=location, prev=None)

        return Response(serialize_location_and_halls(request, location_pk))

    def put(self, request, location_pk):
        location = Location.objects.get(pk=location_pk)

        location.name = request.data['name']
        location.description = request.data['description']
        try:
            location.img = request.FILES['img']
        except:
            pass
        location.save()
        return Response(serialize_location_and_halls(request, location_pk))

        # location = Location.objects.get(pk=location_pk)
        # serializer = LocationSerializer(location, context={'request': request})
        # return Response(serializer.data)

    def delete(self, request, location_pk):
        delete_location(request, location_pk)
        return Response(serialize_museum_and_locations(request))


class AllLocationsView(APIView):
    """
    Shows all locations
    """

    def get(self, request):
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, context={'request': request}, many=True)
        return Response(serializer.data)


def serialize_museum_and_locations(request):
    museum = Museum.objects.get(admins=request.user)
    museum_serializer = MuseumSerializer(museum, context={'request': request})

    if len(Location.objects.filter(museum=request.user.museum)) > 0:
        list_of_locations = list()
        location = Location.objects.get(prev=None)
        list_of_locations.append(location)
        print(list_of_locations)

        for i in range(len(Location.objects.filter(museum=request.user.museum)) - 1):
            location = Location.objects.get(prev=location.id)
            list_of_locations.append(location)
            print(list_of_locations)

        if len(list_of_locations) == 1:
            locations_serializer = LocationSerializer(list_of_locations, context={'request': request})
        else:
            locations_serializer = LocationSerializer(list_of_locations, context={'request': request}, many=True)

        return {
            'museum': museum_serializer.data,
            'locations': locations_serializer.data
        }
    else:
        return {
            'museum': museum_serializer.data,
            'locations': []
        }


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

        location = Location.objects.get(prev=None)
        for i in range(len(Location.objects.filter(museum=request.user.museum)) - 1):
            location = Location.objects.get(prev=location.id)

        Location.objects.create(name=name, img=img, description=description, museum=request.user.museum,
                                prev=location.id)

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


# def swap_and_save_artifact(swap_type, request):
#     if swap_type == 'up':
#         cur = Artifact.objects.get(pk=request.data['obj_id'])
#     elif swap_type == 'down':
#         cur = Artifact.objects.get(prev=request.data['obj_id'])
#     up = Artifact.objects.get(pk=cur.prev)
#     try:
#         down = Artifact.objects.get(prev=cur.id)
#         cur.prev = None  # deleting obj from list
#         down.prev = up.id
#         cur.prev = up.prev  # adding obj to list
#         up.prev = cur.id
#         cur.save()
#         up.save()
#         down.save()
#     except:  # exception only if 'cur' is the last el in the list (then obj 'down' doesn't exists)
#         if swap_type == 'down':
#             cur = Artifact.objects.get(prev=request.data['obj_id'])
#             up = Artifact.objects.get(pk=request.data['obj_id'])
#         cur.prev = up.prev
#         up.prev = cur.id
#         cur.save()
#         up.save()
#     return True
#
#
# class SwapArtifactsView(APIView):
#     """
#     Swaps current artifact with upper or lower artifact
#     """
#
#     def post(self, request):
#         swap_type = request.data['swap_type']
#         swap_and_save_artifact(swap_type, request)
#         return Response(True)
#
#
# class ShowAllArtifactsView(APIView):
#     """
#     Shows all artifacts
#     """
#
#     def get(self, request):
#
#         list_of_artifacts = list()
#         artifact = Artifact.objects.get(prev=None)
#         list_of_artifacts.append(artifact)
#
#         for i in range(len(Artifact.objects.all()) - 1):
#             artifact = Artifact.objects.get(prev=artifact.id)
#             list_of_artifacts.append(artifact)
#
#         if len(list_of_artifacts) == 1:
#             serializer = AllArtifactsSerializer(list_of_artifacts, context={'request': request})
#         else:
#             serializer = AllArtifactsSerializer(list_of_artifacts, context={'request': request}, many=True)
#
#         # objs = Artifact.objects.all()
#         # serializer = AllArtifactsSerializer(objs, context={'request': request}, many=True)
#
#         return Response(serializer.data)
#
#
# class ShowCurrentArtifactView(APIView):
#     """
#     Shows current artifact
#     """
#
#     def get(self, request, artifact_pk):
#         artifact = Artifact.objects.get(pk=artifact_pk)
#         serializer = ArtifactSerializer(artifact, context={'request': request})
#
#         return Response(serializer.data)
#
#
# class ShowQRCodeOfCurrentArtifactView(APIView):
#     """
#     Shows QR-code of current artifact
#     """
#
#     def get(self, request, artifact_pk):
#         artifact = Artifact.objects.get(pk=artifact_pk)
#         artifact.save()
#         qr_code = QRCodeSerializer(artifact, context={'request': request})
#
#         return Response(qr_code.data)


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

# give status to front
# return Response({"data": data, "status": status.HTTP_200_OK})

# validate data
# def post(self, request):
#     user = request.data
#     serializer = UserSerializer(data=user)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return Response({"user": serializer.data, "status": status.HTTP_200_OK})
