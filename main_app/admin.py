from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _

from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter

from .models import *


# class ProductAdmin(admin.ModelAdmin):
#     search_fields = ('name',)
#     list_filter = ('category',)
#     list_display = ('name', 'category',)
#     pass
#
#
# admin.site.register(Category)
# admin.site.register(Product, ProductAdmin)

# class SchoolAdmin(admin.ModelAdmin):
#     # list_filter = ('city',)
#     # list_display = ('name', 'city', 'years_and_months')
#
#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         if request.user.is_superuser:
#             return qs
#         return qs.filter(admin=request.user)
#
#
# class ArenaRentEventAdmin(admin.ModelAdmin):
#
#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         if request.user.is_superuser:
#             self.list_filter = ('arena', ('date', DateRangeFilter))
#             self.list_display = ('arena', 'arena_field', 'date', 'start_time', 'duration', 'is_booked', 'price')
#             return qs
#         self.list_filter = ('arena', ('date', DateRangeFilter))
#         self.list_display = ('date', 'arena_field', 'start_time', 'duration', 'price', 'is_booked')
#         arenas = Arena.objects.filter(arena_admins=request.user)
#         return qs.filter(arena__in=arenas)
#
#
# class ArenaFieldAdmin(admin.ModelAdmin):
#
#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         print(request.user.is_superuser)
#         if request.user.is_superuser:
#             self.fields = ['name', 'arena']
#             self.list_filter = ('arena',)
#             self.list_display = ('name', 'arena')
#             return qs
#         self.list_filter = ()
#         self.list_display = ('name', 'arena')
#         self.fields = ['name']
#         arenas = Arena.objects.filter(arena_admins=request.user)
#         return qs.filter(arena__in=arenas)
#
#
# class BenchAdAdmin(admin.ModelAdmin):
#     list_display = ('adult_club', 'status')
#
#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         print(request.user.is_superuser)
#         if request.user.is_superuser:
#             self.list_filter = ('status',)
#             return qs
#         self.list_filter = ()
#         adult_clubs = AdultClub.objects.filter(users=request.user)
#         return qs.filter(adult_club__in=adult_clubs)
#
#
# class KidClubAdmin(admin.ModelAdmin):
#
#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         if request.user.is_superuser:
#             self.list_filter = ('club_type',)
#             self.list_display = ('name', 'club_type', 'arena')
#             self.exclude = ()
#             return qs
#         self.list_filter = ()
#         self.list_display = ('name', 'club_type', 'arena')
#         self.exclude = ('arena',)
#         return qs.filter(admin=request.user)
#
#
# class KidsTournamentAdmin(admin.ModelAdmin):
#     list_filter = ('city',)
#     list_display = ('name', 'city', 'years_and_months')
#
#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         if request.user.is_superuser:
#             return qs
#         return qs.filter(admin=request.user)
#
#
# class LeagueAdmin(admin.ModelAdmin):
#     list_filter = ('age_group',)
#     list_display = ('name', 'city', 'age_group')
#
#
# class ArenaAdmin(admin.ModelAdmin):
#     search_fields = ('name', 'location')
#
#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         if request.user.is_superuser:
#             self.list_filter = ('metro',)
#             self.list_display = ('name', 'metro', 'location')
#             return qs
#         self.list_filter = ()
#         self.list_display = ('name',)
#         return qs.filter(arena_admins=request.user)
#
#
# class TimetableEventAdmin(admin.ModelAdmin):
#
#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         if request.user.is_superuser:
#             self.list_filter = ('arena', 'day')
#             self.list_display = ('start_time', 'duration', 'club', 'event_type', 'day', 'arena_field', 'arena')
#             self.fields = [('arena', 'arena_field'), 'club', ('day', 'start_time', 'duration'), 'event_type']
#             return qs
#         self.list_filter = ('arena', 'day')
#         self.list_display = ('start_time', 'duration', 'club', 'event_type', 'day', 'arena_field')
#         self.fields = ['arena', 'arena_field', 'club', ('day', 'start_time', 'duration'), 'event_type']
#         arenas = Arena.objects.filter(arena_admins=request.user)
#         return qs.filter(arena__in=arenas)
#
#
# class AdultClubAdmin(admin.ModelAdmin):
#     filter_horizontal = [
#         'users',
#     ]
#
#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         if request.user.is_superuser:
#             self.exclude = ()
#             return qs
#         self.exclude = ('arena',)
#         return qs.filter(users=request.user)
#
#     def __str__(self):
#         return "%s.%s" % (self.model._meta.app_label, self.__class__.__name__)
#         # return 'Teachers'
#
#
# class CustomUserAdmin(UserAdmin):
#     filter_horizontal = [
#         'arenas',
#     ]
#     list_display = ('email', 'last_name', 'first_name', 'status', 'in_search', 'is_staff', 'is_superuser', 'is_active')
#     fieldsets = (
#         (None, {'fields': ('username', 'password')}),
#         (_('Personal info'), {'fields': ('img', 'email', 'first_name', 'last_name',
#                                          'middle_name', 'date_of_birth', 'grip', 'height', 'weight', 'phone_number',
#                                          'vk_account',
#                                          'inst_account', 'fb_account', 'status', 'game_number', 'in_search',
#                                          'arenas', 'kid_club_admin', 'kids_tournament_admin', 'school_admin')}),
#         (_('Permissions'), {
#             'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
#         }),
#         (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('img', 'username', 'email', 'password1', 'password2', 'first_name', 'last_name',
#                        'middle_name', 'groups', 'date_of_birth', 'grip', 'height', 'weight', 'phone_number', 'status',
#                        'game_number',
#                        'vk_account', 'inst_account',
#                        'fb_account', 'in_search', 'arenas', 'kid_club_admin', 'kids_tournament_admin', 'school_admin'),
#         }),
#     )
#
#
# admin.site.register(User, CustomUserAdmin)
# admin.site.register(Arena, ArenaAdmin)
# admin.site.register(ArenaField, ArenaFieldAdmin)
# admin.site.register(AdultClub, AdultClubAdmin)
# admin.site.register(KidClub, KidClubAdmin)
# admin.site.register(TimetableEvent, TimetableEventAdmin)
# admin.site.register(ArenaRentEvent, ArenaRentEventAdmin)
# admin.site.register(BenchAd, BenchAdAdmin)
# admin.site.register(League, LeagueAdmin)
# admin.site.register(KidsTournament, KidsTournamentAdmin)
# admin.site.register(School, SchoolAdmin)
# admin.site.register(Question)
