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

    # # Получить выбранный экспонат
    # path('api/artifacts/<int:artifact_pk>', views.ShowCurrentArtifactView.as_view()),
    # # Получить все экспонаты
    # path('api/artifacts', views.ShowAllArtifactsView.as_view()),
    # # Поменять два выбранных экспоната местами
    # path('api/swap_artifacts', views.SwapArtifactsView.as_view()),
    # # Получить QR-код выбранного экспоната
    # path('api/artifacts/<int:artifact_pk>/qr-code', views.ShowQRCodeOfCurrentArtifactView.as_view()),

    # Получить все музеи или добавить новый
    path('api/s-admin', views.MuseumsView.as_view()),
    # Удалить выбранный музей
    path('api/s-admin/<int:museum_pk>', views.ServiceCurrentMuseumView.as_view()),

    # Получить музей со всеми его локациями, или изменить музей, или добавить новую локацию
    path('api/m-admin', views.CurrentMuseumView.as_view()),
    # Получить профиль супер-админа музея, а также списки админов и кассиров музея, к которому привязан супер-админ
    path('api/m-admin/hr-management', views.MuseumProfilesView.as_view()),
    # Изменить/удалить выбранного администратора/кассира музея
    path('api/m-admin/hr-management/<int:user_pk>', views.MuseumProfilesView.as_view()),

    # Получить локацию со всеми её залами, или изменить/удалить выбранную локацию, или добавить новый зал
    path('api/m-admin/<int:location_pk>', views.CurrentLocationView.as_view()),
    # Поменять две выбранных локации местами
    path('api/swap_locations', views.SwapLocationsView.as_view()),
    # Получить все локации
    path('api/all_locations', views.AllLocationsView.as_view()),

    # Получить выбранный зал со всеми его экспонатами, или изменить/удалить выбранный зал, или добавить новый экспонат
    path('api/m-admin/<int:location_pk>/<int:hall_pk>', views.CurrentHallView.as_view()),
    # Поменять две выбранных зала местами
    path('api/swap_halls', views.SwapHallsView.as_view()),
    # Получить все залы
    path('api/all_halls', views.AllHallsView.as_view()),

    # Получить выбранный экспонат или изменить/удалить выбранный экспонат
    path('api/m-admin/<int:location_pk>/<int:hall_pk>/<int:artifact_pk>', views.CurrentArtifactView.as_view()),
    # Поменять две выбранных зала местами
    path('api/swap_artifacts', views.SwapArtifactsView.as_view()),
    # Получить все залы
    path('api/all_artifacts', views.AllArtifactsView.as_view()),

    # Создать нового пользователя
    # path('api/create_new_cashier', views.CreateNewCashierView.as_view()),

    # Вызвать метод save() у всех экспонатов (используется для переноса сервиса с IP/домена на IP/домен)
    # path('api/update_all_qrs', views.UpdateAllQRsView.as_view()),

    # Авторизация
    url(r'^auth/', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.jwt')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += doc_url
urlpatterns.append(url(r'^', views.ReactAppView.as_view()))
