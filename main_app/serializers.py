from rest_framework import serializers
from .models import *


class ArtifactSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 2
        model = Artifact
        fields = '__all__'

# class AccountSerializer(serializers.ModelSerializer):
#     class Meta:
#         depth = 2
#         model = User
#         fields = ('id', 'first_name', 'middle_name', 'last_name', 'img', 'date_of_birth', 'phone_number', 'email',
#                   'vk_account', 'inst_account', 'fb_account', 'yt_account', 'status', 'height', 'weight', 'grip',
#                   'game_number', 'r_hokey', 'coach_info', 'coaching_experience', 'in_search')
#         # fields = '__all__'
#
#
# class CurrentKidsTournamentSerializer(serializers.ModelSerializer):
#     class Meta:
#         depth = 2
#         model = KidsTournament
#         fields = '__all__'
#
#
# class CurrentLeagueSerializer(serializers.ModelSerializer):
#     class Meta:
#         depth = 2
#         model = League
#         exclude = ('age_group',)
#
#
# class KidsTournamentSerializer(serializers.ModelSerializer):
#     class Meta:
#         depth = 2
#         model = KidsTournament
#         fields = ('id', 'img', 'name', 'city', 'years_and_months')
#
#
# class CurrentSchoolSerializer(serializers.ModelSerializer):
#     class Meta:
#         depth = 2
#         model = School
#         fields = '__all__'
#
#
# class SchoolSerializer(serializers.ModelSerializer):
#     class Meta:
#         depth = 2
#         model = School
#         fields = ('id', 'img', 'name', 'city')
#
#
# class LeagueSerializer(serializers.ModelSerializer):
#     class Meta:
#         depth = 2
#         model = League
#         fields = ('id', 'img', 'name', 'city')
#
#
# class AdultClubsSpecialForUserBenchAdsSerializer(serializers.ModelSerializer):
#     class Meta:
#         depth = 2
#         model = AdultClub
#         fields = ('id', 'logo', 'name')
#
#
# class UserBenchAdsSerializer(serializers.ModelSerializer):
#     adult_clubs = AdultClubsSpecialForUserBenchAdsSerializer(read_only=True, many=True)
#
#     class Meta:
#         depth = 2
#         model = User
#         fields = (
#             'id', 'img', 'first_name', 'last_name', 'middle_name', 'date_of_birth', 'grip', 'weight', 'height',
#             'vk_account', 'inst_account', 'fb_account', 'yt_account', 'game_number', 'r_hokey', 'adult_clubs')
#
#
# class BenchAdsSerializer(serializers.ModelSerializer):
#     adult_club = AdultClubsSpecialForUserBenchAdsSerializer(read_only=True)
#
#     class Meta:
#         depth = 2
#         model = BenchAd
#         fields = ('id', 'img', 'status', 'text', 'adult_club')
#
#
# class QuestionSerializer(serializers.ModelSerializer):
#     class Meta:
#         depth = 2
#         model = Question
#         fields = '__all__'
#
#
# class AdultClubsSpecialForAllPlayerSerializerSerializer(serializers.ModelSerializer):
#     class Meta:
#         depth = 2
#         model = AdultClub
#         fields = ('id', 'logo', 'name')
#
#
# class AllPlayersSerializer(serializers.ModelSerializer):
#     adult_clubs = AdultClubsSpecialForAllPlayerSerializerSerializer(read_only=True, many=True)
#
#     class Meta:
#         depth = 2
#         model = User
#         fields = ('id', 'first_name', 'middle_name', 'last_name', 'img', 'adult_clubs', 'game_number', 'status')
#
#
# class AllAdultClubsSerializer(serializers.ModelSerializer):
#     class Meta:
#         depth = 2
#         model = AdultClub
#         fields = ('id', 'name', 'logo', 'img')
#
#
# class ArenaFieldForArenaRentSerializer(serializers.ModelSerializer):
#     class Meta:
#         depth = 2
#         model = ArenaField
#         fields = ('id', 'name')
#
#
# class ArenaRentSerializer(serializers.ModelSerializer):
#     arena_field = ArenaFieldForArenaRentSerializer(read_only=True)
#
#     class Meta:
#         depth = 2
#         model = ArenaRentEvent
#         fields = ('id', 'start_time', 'duration', 'arena_field', 'is_booked', 'price')
#
#
# class ArenaFieldForTimetableEventsSerializer(serializers.ModelSerializer):
#     class Meta:
#         depth = 2
#         model = ArenaField
#         fields = ('id', 'name')
#
#
# class AdultClubsSpecialForTimetableEventsSerializer(serializers.ModelSerializer):
#     class Meta:
#         depth = 2
#         model = AdultClub
#         fields = ('id', 'logo', 'name')
#
#
# class TimetableEventsSerializer(serializers.ModelSerializer):
#     arena_field = ArenaFieldForTimetableEventsSerializer(read_only=True)
#     club = AdultClubsSpecialForTimetableEventsSerializer(read_only=True)
#
#     class Meta:
#         depth = 2
#         model = TimetableEvent
#         fields = ('id', 'event_type', 'start_time', 'duration', 'arena_field', 'club')
#
#
# class CurrentKidClubSerializer(serializers.ModelSerializer):
#     class Meta:
#         depth = 2
#         model = KidClub
#         fields = '__all__'
#
#
# class AdultClubsSpecialForUsersSerializer(serializers.ModelSerializer):
#     class Meta:
#         depth = 2
#         model = AdultClub
#         fields = ('id', 'logo', 'name')
#
#
# class CurrentUserSerializer(serializers.ModelSerializer):
#     adult_clubs = AdultClubsSpecialForUsersSerializer(read_only=True, many=True)
#
#     class Meta:
#         depth = 2
#         model = User
#         fields = (
#             'id', 'img', 'first_name', 'last_name', 'middle_name', 'date_of_birth', 'grip', 'weight', 'height',
#             'vk_account', 'inst_account', 'fb_account', 'yt_account', 'game_number', 'r_hokey', 'adult_clubs',
#             'coaching_experience', 'coach_info', 'email', 'phone_number', 'in_search')
#
#
# class PlayerFromCurrentAdultClubSerializer(serializers.ModelSerializer):
#     class Meta:
#         depth = 2
#         model = User
#         fields = ('id', 'first_name', 'last_name', 'img', 'status')
#
#
# class CoachFromCurrentAdultClubSerializer(serializers.ModelSerializer):
#     class Meta:
#         depth = 2
#         model = User
#         fields = ('id', 'first_name', 'last_name', 'img', 'status')
#
#
# class CurrentAdultClubSerializer(serializers.ModelSerializer):
#     class Meta:
#         depth = 2
#         model = AdultClub
#         exclude = ('users',)
#
#
# class AdultClubsSerializer(serializers.ModelSerializer):
#     class Meta:
#         depth = 2
#         model = AdultClub
#         fields = ('id', 'name', 'logo', 'img')
#
#
# class CurrentArenaSerializer(serializers.ModelSerializer):
#     class Meta:
#         depth = 2
#         model = Arena
#         fields = '__all__'
#
#
# class ArenaSerializer(serializers.ModelSerializer):
#     class Meta:
#         depth = 2
#         model = Arena
#         fields = ('id', 'name', 'metro', 'location', 'operating_mode', 'img')
