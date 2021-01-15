"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.conf import settings
from django.urls import path, include
from .yasg import urlpatterns as doc_url
from django.conf.urls.static import static

import main_app.views as views

urlpatterns = [

    # Админ-панель
    path('admin/', admin.site.urls),

    # Получить выбранный экспонат
    path('api/artifacts/<int:artifact_pk>', views.ShowArtifactView.as_view()),

    # Получить все экспонаты
    path('api/artifacts', views.ShowAllArtifactsView.as_view()),

    # Поменять два выбранных экспоната местами
    path('api/swap', views.SwapArtifactsView.as_view()),

    # Получить QR-код выбранного экспоната
    path('api/artifacts/<int:artifact_pk>/qr-code', views.ShowQRCodeOfCurrentArtifactView.as_view()),

    # Получить музей, к которому привязан данный администратор
    path('api/m-admin', views.ShowCurrentMuseum.as_view()),

    # Авторизация
    url(r'^auth/', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.jwt')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += doc_url
urlpatterns.append(url(r'^', views.ReactAppView.as_view()))
