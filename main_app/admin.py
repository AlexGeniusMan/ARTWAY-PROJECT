from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import *


class ArtifactAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    fields = ('name', 'img', 'audio', 'description')


admin.site.register(Artifact, ArtifactAdmin)
