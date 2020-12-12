import datetime
import os

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.views.generic.base import View
from rest_framework.generics import UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Q, CharField
from django.db.models.functions import Lower

from .models import *
from .serializers import *

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect


# from .forms import ContactForm
# from project.settings import DEFAULT_FROM_EMAIL, DEFAULT_ADMIN_EMAIL

class ShowArtifactView(APIView):
    """
    Shows current artifact
    """

    def get(self, request, artifact_pk):
        categories = Artifact.objects.get(pk=artifact_pk)
        serializer = ArtifactSerializer(categories, context={'request': request})

        return Response(serializer.data)

# class ShowProductsView(APIView):
#     """
#     Shows all products of current category (searching by letters available)
#     """
#
#     def post(self, request, category_pk):
#         find_by_letters = request.POST['find_by_letters']
#
#         data = []
#         next_page = 1
#         previous_page = 1
#         products = Product.objects.filter(
#             Q(category=category_pk),
#             Q(name__icontains=find_by_letters) |
#             Q(name__icontains=find_by_letters.capitalize()) |
#             Q(name__icontains=find_by_letters.lower()) |
#             Q(name__icontains=find_by_letters.upper())
#         )
#
#         page = request.GET.get('page', 1)
#         paginator = Paginator(products, 1)
#         try:
#             data = paginator.page(page)
#         except PageNotAnInteger:
#             data = paginator.page(1)
#         except EmptyPage:
#             data = paginator.page(paginator.num_pages)
#
#         serializer = ProductSerializer(data, context={'request': request}, many=True)
#
#         if data.has_next():
#             next_page = data.next_page_number()
#         if data.has_previous():
#             previous_page = data.previous_page_number()
#
#         return Response({'products': serializer.data, 'count': paginator.count, 'numpages': paginator.num_pages,
#                          'nextlink': '/api/categories/' + str(category_pk) + '?page=' + str(next_page),
#                          'prevlink': '/api/categories/' + str(category_pk) + '?page=' + str(previous_page)})
#
#
# class ShowCategoriesView(APIView):
#     """
#     Shows all categories
#     """
#
#     def get(self, request):
#         categories = Category.objects.all()
#         serializer = CategorySerializer(categories, context={'request': request}, many=True)
#
#         return Response(serializer.data)
#
#
# class ShowCurrentProductView(APIView):
#     """
#     Shows current product
#     """
#
#     def get(self, request, product_pk):
#         product = Product.objects.get(pk=product_pk)
#         serializer = ProductSerializer(product, context={'request': request})
#
#         return Response(serializer.data)
#
#
# class ReactAppView(View):
#
#     def get(self, request):
#         BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#
#         try:
#             with open(os.path.join(BASE_DIR, 'frontend', 'build', 'index.html')) as file:
#                 return HttpResponse(file.read())
#
#         except:
#             return HttpResponse(
#                 """
#                 index.html not found ! build your React app !!
#                 """,
#                 status=501,
#             )
