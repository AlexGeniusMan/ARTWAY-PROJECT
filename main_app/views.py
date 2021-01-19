from django.db.models import Q
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from django.views.generic.base import View
from rest_framework.views import APIView
from django.http import HttpResponse

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

import matplotlib.pyplot as plt
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
from svglib.svglib import svg2rlg
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase import ttfonts

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
#         user = User.objects.get(pk=1)
#         return Response(True)
#
#     def post(self, request):
#         user = User.objects.create_user(username='awffe', password='123', last_name='Chentsov', first_name='Alex')
#         return Response(True)

# def plot_data(data):
#     # Plot the data using matplotlib.
#     plt.plot(data)
#
#     # Save the figure to SVG format in memory.
#     # svg_file = BytesIO()
#     svg_file = segno.make('Henry Lee', micro=False)
#     # plt.savefig(svg_file, format='SVG')
#
#     # Rewind the file for reading, and convert to a Drawing.
#     # svg_file.seek(0)
#     drawing = svg2rlg(svg_file)
#
#     # Scale the Drawing.
#     scale = 0.75
#     drawing.scale(scale, scale)
#     drawing.width *= scale
#     drawing.height *= scale
#
#     return drawing


class TestingQRCode(APIView):

    def scale(self, drawing, scaling_factor):
        """
        Scale a reportlab.graphics.shapes.Drawing()
        object while maintaining the aspect ratio
        """
        scaling_x = scaling_factor
        scaling_y = scaling_factor

        drawing.width = drawing.minWidth() * scaling_x
        drawing.height = drawing.height * scaling_y
        drawing.scale(scaling_x, scaling_y)
        return drawing

    def get(self, request):
        # try:
        #     path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'svg_on_canvas.pdf')
        #     os.remove(path)
        #     print('ok')
        # except:
        #     raise
        #     pass

        qr = segno.make('https://devgang.ru', micro=False)
        qr.save('qr.svg')

        MyFontObject = ttfonts.TTFont('Arial', 'arial.ttf')
        pdfmetrics.registerFont(MyFontObject)
        my_canvas = canvas.Canvas('svg_scaled_on_canvas.pdf')
        my_canvas.setFont('Arial', 14)
        drawing = svg2rlg('qr.svg')
        scaling_factor = 10
        scaled_drawing = self.scale(drawing, scaling_factor=scaling_factor)
        # renderPDF.draw(scaled_drawing, my_canvas, 0, 40)
        # my_canvas.drawString(50, 30, 'My SVG Image')
        # my_canvas.save()

        # MyFontObject = ttfonts.TTFont('Arial', 'arial.ttf')
        # pdfmetrics.registerFont(MyFontObject)
        # my_canvas = canvas.Canvas('svg_on_canvas.pdf')
        # my_canvas.setFont('Arial', 14)
        # drawing = svg2rlg('qr.svg')
        # renderPDF.draw(drawing, my_canvas, 50, 640)
        strings = (
            'Музей "Третьяковская галерея"',
            '',
            'Кантакты: +7 (495) 957-07-27, tretyakov@tretyakov.ru',
            'Часы работы колл-центра:',
            'Пн — 10:00–16:00, Вт, Ср, Вс — 10:00–18:00, Чт, Пт, Сб — 10:00–21:00',
            'Часы работы службы поддержки:',
            'Пн, Вт, Ср, Чт — 10:00–18:00, Пт — 10:00–15:30',
            '',
            'Инструкция:',
            '• Перейдите к сканированию QR-кода выбранного экспоната или введите его ID',
            '• На странице экспоната Вы сможете просмотреть информацию о нём,',
            '  а также прослушать аудиогид',
            '• Любите искусство вместе с ArtWay',
            '',
            '',
            'Ваш персональный QR-код для перехода на страницу сервиса:',
        )
        i = 800
        for string in strings:
            my_canvas.drawString(50, i, string)
            i -= 20
        renderPDF.draw(scaled_drawing, my_canvas, 130, 190)
        my_canvas.save()

        # styles = getSampleStyleSheet()
        # pdf_path = 'sketch.pdf'
        # doc = SimpleDocTemplate(pdf_path)
        # data = [1, 3, 2]
        # story = [Paragraph('Lorem ipsum!', styles['Normal']), plot_data(data),
        #          Paragraph('Dolores sit amet.', styles['Normal'])]
        # doc.build(story)

        qr = segno.make('https://devgang.ru', micro=False)
        qr.save('qr.svg')
        # drawing = svg2rlg("qr.svg")
        # renderPDF.drawToFile(drawing, "ticket.pdf")
        return Response(True)


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

    if temp_len > 1:
        list_of_artifacts = list()
        artifact = Artifact.objects.filter(hall=hall_pk).get(prev=None)
        list_of_artifacts.append(artifact)

        for i in range(len(Artifact.objects.filter(hall=hall_pk)) - 1):
            artifact = Artifact.objects.get(prev=artifact.id)
            list_of_artifacts.append(artifact)

        artifacts_serializer = ArtifactSerializer(list_of_artifacts, context={'request': request}, many=True)

        return {
            'hall': hall_serializer.data,
            'artifacts': artifacts_serializer.data
        }
    elif temp_len == 1:
        # location = Location.objects.get(pk=location_pk)
        artifact = Artifact.objects.get(hall=hall_pk)
        artifact_serializer = ArtifactSerializer(artifact, context={'request': request})
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

    # permission_classes = (IsAuthenticated,)

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

    if temp_len > 1:
        list_of_halls = list()
        hall = Hall.objects.filter(location=location_pk).get(prev=None)
        list_of_halls.append(hall)

        for i in range(len(Hall.objects.filter(location=location_pk)) - 1):
            hall = Hall.objects.get(prev=hall.id)
            list_of_halls.append(hall)

        halls_serializer = HallSerializer(list_of_halls, context={'request': request}, many=True)
        return {
            'location': location_serializer.data,
            'halls': halls_serializer.data
        }
    elif temp_len == 1:
        # location = Location.objects.get(pk=location_pk)
        hall = Hall.objects.get(location=location)
        halls_serializer = HallSerializer(hall, context={'request': request})
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
    is_museum_super_admin = request.user.groups.filter(name='museum_super_admins').exists()

    if len(Location.objects.filter(museum=request.user.museum)) > 0:
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

        return {
            'museum': museum_serializer.data,
            'is_museum_super_admin': is_museum_super_admin,
            'locations': locations_serializer.data
        }
    else:
        return {
            'museum': museum_serializer.data,
            'is_museum_super_admin': is_museum_super_admin,
            'locations': []
        }


class CurrentMuseumView(APIView):
    """
    Shows or changes current museum
    """
    permission_classes = (IsAuthenticated,)

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


class MuseumSuperAdminView(APIView):
    """
    # Shows all museums, creates new one or deletes current
    """
    permission_classes = (IsServiceSuperAdmin,)

    def get_museum_super_admin(self, request, museum_pk):
        museum = Museum.objects.get(pk=museum_pk)
        museum_serializer = MuseumSerializer(museum, context={'request': request})

        users = User.objects.filter(museum=museum_pk).exclude(pk=request.user.id)
        for user in users:
            if user.groups.filter(name='museum_super_admins').exists():
                museum_super_admin = user
                break
        try:
            museum_super_admin_serializer = UserSerializer(museum_super_admin, context={'request': request})
            return {
                'status': True,
                'museum_super_admin': museum_super_admin_serializer.data,
                # 'museum': museum_serializer.data
            }
        except:
            return {
                'status': False,
                'museum_super_admin': {},
                # 'museum': museum_serializer.data
            }

    def get(self, request, museum_pk):
        return Response(self.get_museum_super_admin(request, museum_pk))

    def post(self, request, museum_pk):
        username = request.data['email']
        email = request.data['email']
        password = request.data['password']
        last_name = request.data['last_name']
        first_name = request.data['first_name']
        middle_name = request.data['middle_name']

        # username = 'm_super_1'
        # email = 'email'
        # password = 'password'
        # last_name = 'Chentsov'
        # first_name = 'Alex'
        # middle_name = ''

        users = User.objects.filter(museum=museum_pk).exclude(pk=request.user.id)
        for user in users:
            if user.groups.filter(name='museum_super_admins').exists():
                return Response(
                    {"error_code": 'MUSEUM SUPER ADMIN IS ALREADY EXISTS', "status": status.HTTP_403_FORBIDDEN})

        user = User.objects.create_user(username=username, password=password, last_name=last_name,
                                        first_name=first_name, middle_name=middle_name,
                                        email=email, museum=request.user.museum)

        group = Group.objects.get(name='museum_super_admins')
        user.groups.add(group.id)
        group = Group.objects.get(name='museum_admins')
        user.groups.add(group.id)
        user.save()
        return Response(self.get_museum_super_admin(request, museum_pk))

    def delete(self, request, museum_pk):

        # users = User.objects.filter(museum=museum_pk).exclude(pk=request.user.id)
        users = User.objects.filter(museum=museum_pk).exclude(pk=request.user.id)
        print(users)
        for user in users:
            print(user)
            if user.groups.filter(name='museum_super_admins').exists():
                user.delete()
                return Response(self.get_museum_super_admin(request, museum_pk))
        return Response(
            {"error_code": 'MUSEUM SUPER ADMIN DOES NOT EXISTS', "status": status.HTTP_404_NOT_FOUND})


class MuseumsView(APIView):
    """
    Shows all museums, creates new one or deletes current
    """
    permission_classes = (IsServiceSuperAdmin,)

    def get_all_museums(self, request):
        museums = Museum.objects.all()
        serializer = MuseumSerializer(museums, context={'request': request}, many=True)
        return serializer.data

    def get(self, request):
        return Response(self.get_all_museums(request))

    def post(self, request):
        name = request.data['name']
        img = request.data['img']
        description = request.data['description']

        Museum.objects.create(name=name, img=img, description=description)

        return Response(self.get_all_museums(request))

    def delete(self, request):
        museum_pk = request.data['museum_pk']
        try:
            museum = Museum.objects.get(pk=museum_pk)
            museum.delete()
            return Response(self.get_all_museums(request))
        except:
            return Response({"error_code": 'MUSEUM DOES NOT EXISTS', "status": status.HTTP_404_NOT_FOUND})


class MuseumProfilesView(APIView):
    """
    Shows/creates/deletes employees of current museum
    """
    permission_classes = (IsMuseumAdmin,)

    def get_users(self, request):
        museum_super_admin = User.objects.get(pk=request.user.id)
        users = User.objects.filter(museum=request.user.museum).exclude(pk=request.user.id)

        museum_admins = list()
        museum_cashiers = list()
        for user in users:
            if user.groups.filter(name='museum_admins').exists():
                museum_admins.append(user)
            elif user.groups.filter(name='museum_cashiers').exists():
                museum_cashiers.append(user)

        museum_super_admin_serializer = UserSerializer(museum_super_admin, context={'request': request})
        museum_admins_serializer = UserSerializer(museum_admins, context={'request': request}, many=True)
        museum_cashiers_serializer = UserSerializer(museum_cashiers, context={'request': request}, many=True)
        return {'museum_super_admin': museum_super_admin_serializer.data,
                'museum_admins': museum_admins_serializer.data,
                'museum_cashiers': museum_cashiers_serializer.data
                }

    def get(self, request):
        return Response(self.get_users(request))

    def post(self, request):
        username = request.data['email']
        email = request.data['email']
        password = request.data['password']
        last_name = request.data['last_name']
        first_name = request.data['first_name']
        middle_name = request.data['middle_name']
        role = request.data['role']

        # username = 'm_cashier_2'
        # email = 'email'
        # password = 'password'
        # last_name = 'Chentsov'
        # first_name = 'Alex'
        # middle_name = ''
        # role = 'museum_cashiers'

        user = User.objects.create_user(username=username, password=password, last_name=last_name,
                                        first_name=first_name, middle_name=middle_name,
                                        email=email, museum=request.user.museum)
        if role == 'museum_admins':
            group = Group.objects.get(name='museum_admins')
        elif role == 'museum_cashiers':
            group = Group.objects.get(name='museum_cashiers')
        user.groups.add(group.id)
        user.save()
        return Response(self.get_users(request))

    def put(self, request, user_pk):
        museum_super_admin = request.user
        user = User.objects.get(pk=user_pk)

        if museum_super_admin.museum == user.museum:
            user.last_name = request.data['last_name']
            user.first_name = request.data['first_name']
            user.middle_name = request.data['middle_name']
            user.email = request.data['email']
            user.username = request.data['email']

            # user.last_name = 'last'
            # user.first_name = 'first'
            # user.middle_name = 'middle'
            # user.email = 'email'
            # user.username = 'username'
            user.save()

            return Response(self.get_users(request))
        else:
            return Response({"error_code": 'ERROR', "status": status.HTTP_403_FORBIDDEN})

    def delete(self, request, user_pk):
        museum_super_admin = request.user
        user = User.objects.get(pk=user_pk)

        if user.id != museum_super_admin.id:
            if museum_super_admin.museum == user.museum:
                user.delete()
                return Response(self.get_users(request))
            else:
                return Response({"error_code": 'ERROR', "status": status.HTTP_403_FORBIDDEN})
        else:
            return Response({"error_code": 'ERROR', "status": status.HTTP_403_FORBIDDEN})


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
