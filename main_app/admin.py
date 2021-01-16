from django.contrib import admin
from .models import *


class ArtifactAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    # fields = ('name', 'img', 'audio', 'description')


admin.site.register(Artifact, ArtifactAdmin)
admin.site.register(Museum)
admin.site.register(Location)
admin.site.register(Hall)
admin.site.register(User)
