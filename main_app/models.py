from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField
from django.conf import settings
import datetime


# STATUSES = (('none', 'Статус отсутствует'),
#             ('Нападающий', 'Нападающий'),
#             ('Защитник', 'Защитник'),
#             ('Вратарь', 'Вратарь'),
#             ('Главный тренер', 'Главный тренер'),
#             ('Помощник тренера', 'Помощник тренера'),
#             ('Тренер вратарей', 'Тренер вратарей'),)

class Artifact(models.Model):
    name = models.CharField(_("Название"), max_length=100)
    img = models.ImageField(_("Фотография"), null=True, upload_to='Artifact photos', blank=True)
    audio = models.FileField(_("Аудио"), upload_to='Artifact audios', blank=True)
    description = models.TextField(_("Описание"), max_length=10000, blank=True)

    class Meta:
        verbose_name = 'Экспонат'
        verbose_name_plural = 'Экспонаты'

    def __str__(self):
        return self.name

# class School(models.Model):
#     img = models.ImageField(_("Прикреплённое фото"), null=True, upload_to='schools')
#     name = models.CharField(_("Название школы"), max_length=64)
#     city = models.CharField(_("Город"), max_length=64)
#     directions = MultiSelectField(_("Направления развития"), choices=DIRECTIONS_OF_DEVELOPMENT, max_length=2000,
#                                   default='Базовые и сложные элементы катания')
#     text = models.TextField(_("Описание школы"))
#     admin_phone = models.CharField(_("Телефон администратора"), max_length=64, blank=True)
#     admin_email = models.CharField(_("Email администратора"), max_length=64, blank=True)
#     details_link = models.CharField(_("Ссылка на подробности"), max_length=200)
#
#     class Meta:
#         verbose_name = 'Школа'
#         verbose_name_plural = 'Школы'
#
#     def __str__(self):
#         return self.name
#
#
# class KidsTournament(models.Model):
#     img = models.ImageField(_("Прикреплённое фото"), null=True, upload_to='tournaments/images')
#     file = models.FileField(_("Прикреплённый файл"), upload_to='tournaments/files')
#     name = models.CharField(_("Название турнира"), max_length=64)
#     city = models.CharField(_("Город проведения"), max_length=64)
#     # age_group = models.CharField(_("Возрастная группа"), choices=AGE_GROUPS, max_length=64)
#     years_and_months = MultiSelectField(_("Время проведения"), choices=YEARS_AND_MONTHS)
#     text = models.TextField(_("Описание турнира"))
#     organiser_phone = models.CharField(_("Телефон организатора"), max_length=64)
#     organiser_email = models.CharField(_("Email организатора"), max_length=64)
#     details_link = models.CharField(_("Ссылка на подробности"), max_length=200)
#
#     class Meta:
#         verbose_name = 'Детский турнир'
#         verbose_name_plural = 'Детские турниры'
#
#     def __str__(self):
#         return self.name
#
#
# class League(models.Model):
#     img = models.ImageField(_("Прикреплённое фото"), null=True, upload_to='leagues')
#     name = models.CharField(_("Название лиги"), max_length=64)
#     city = models.CharField(_("Город проведения"), max_length=64)
#     age_group = models.CharField(_("Возрастная группа"), choices=AGE_GROUPS, max_length=64)
#     # years = models.CharField(_("Год проведения"), choices=YEARS, max_length=64)
#     # months = MultiSelectField(_("Месяц проведения"), choices=MONTHS)
#     text = models.TextField(_("Описание лиги"))
#     organiser_phone = models.CharField(_("Телефон организатора"), max_length=64)
#     organiser_email = models.CharField(_("Email организатора"), max_length=64)
#     details_link = models.CharField(_("Ссылка на подробности"), max_length=200)
#
#     class Meta:
#         verbose_name = 'Лига'
#         verbose_name_plural = 'Взрослые и детские лиги'
#
#     def __str__(self):
#         return self.name
#
#
# class BenchAd(models.Model):
#     img = models.ImageField(_("Прикреплённое фото"), null=True, upload_to='ads')
#     adult_club = models.ForeignKey('AdultClub', on_delete=models.PROTECT, verbose_name='Клуб', related_name='bench_ads',
#                                    null=True)
#     status = models.CharField(_("Кого ищет"), choices=STATUSES, max_length=64, default='none')
#
#     text = models.TextField(_("Текст объявления"))
#
#     class Meta:
#         verbose_name = 'Объявление клуба'
#         verbose_name_plural = 'Объявления клубов'
#
#     def __str__(self):
#         return str(self.adult_club) + ': ' + str(self.status)
#
#
# EVENT_TYPES = (('Открытая тренировка', 'Открытая тренировка'),
#                ('Закрытая тренировка', 'Закрытая тренировка'),
#                ('Просмотровая тренировка', 'Просмотровая тренировка'),
#                ('Матч', 'Матч'),
#                ('Двусторонка', 'Двусторонка'))
#
# WEEK_DAYS = (('Понедельник', 'Понедельник'),
#              ('Вторник', 'Вторник'),
#              ('Среда', 'Среда'),
#              ('Четверг', 'Четверг'),
#              ('Пятница', 'Пятница'),
#              ('Суббота', 'Суббота'),
#              ('Воскресенье', 'Воскресенье'))
#
# START_TIMES = (
#     ('00:00', '00:00'),
#     ('00:30', '00:30'),
#     ('01:00', '01:00'),
#     ('01:30', '01:30'),
#     ('02:00', '02:00'),
#     ('02:30', '02:30'),
#     ('03:00', '03:00'),
#     ('03:30', '03:30'),
#     ('04:00', '04:00'),
#     ('04:30', '04:30'),
#     ('05:00', '05:00'),
#     ('05:30', '05:30'),
#     ('06:00', '06:00'),
#     ('06:30', '06:30'),
#     ('07:00', '07:00'),
#     ('07:30', '07:30'),
#     ('08:00', '08:00'),
#     ('08:30', '08:30'),
#     ('09:00', '09:00'),
#     ('09:30', '09:30'),
#     ('10:00', '10:00'),
#     ('10:30', '10:30'),
#     ('11:00', '11:00'),
#     ('11:30', '11:30'),
#     ('12:00', '12:00'),
#     ('12:30', '12:30'),
#     ('13:00', '13:00'),
#     ('13:30', '13:30'),
#     ('14:00', '14:00'),
#     ('14:30', '14:30'),
#     ('15:00', '15:00'),
#     ('15:30', '15:30'),
#     ('16:00', '16:00'),
#     ('16:30', '16:30'),
#     ('17:00', '17:00'),
#     ('17:30', '17:30'),
#     ('18:00', '18:00'),
#     ('18:30', '18:30'),
#     ('19:00', '19:00'),
#     ('19:30', '19:30'),
#     ('20:00', '20:00'),
#     ('20:30', '20:30'),
#     ('21:00', '21:00'),
#     ('21:30', '21:30'),
#     ('22:00', '22:00'),
#     ('22:30', '22:30'),
#     ('23:00', '23:00'),
#     ('23:30', '23:30'),
#     ('24:00', '24:00'),
# )
#
# DURATION_TIMES = (
#     ('1 ч. 00 мин.', '1 ч. 00 мин.'),
#     ('1 ч. 30 мин.', '1 ч. 30 мин.'),
#     ('2 ч. 00 мин.', '2 ч. 00 мин.'),
# )
#
#
# class ArenaRentEvent(models.Model):
#     arena = models.ForeignKey('Arena', on_delete=models.SET_NULL, verbose_name='Арена', related_name='rent_events',
#                               null=True)
#     arena_field = models.ForeignKey('ArenaField', on_delete=models.SET_NULL, verbose_name='Поле арены',
#                                     related_name='rent_events', null=True, blank=True)
#     date = models.DateField(_("День"), default=datetime.date.today())
#     start_time = models.CharField(_("Начало события"), choices=START_TIMES, max_length=64, default='13:15')
#     duration = models.CharField(_("Длительность"), choices=DURATION_TIMES, max_length=64, default='1:15')
#     is_booked = models.BooleanField(_("Забронировано"), default=False)
#     price = models.IntegerField(_("Стоимость"), null=True)
#
#     class Meta:
#         verbose_name = 'Аренда поля'
#         verbose_name_plural = 'Аренда полей'
#
#     def __str__(self):
#         return 'Arena: ' + str(self.arena) + ' | Field: ' + str(self.arena_field) + ' | Date: ' + str(self.date)
#
#
# class TimetableEvent(models.Model):
#     arena = models.ForeignKey('Arena', on_delete=models.PROTECT, verbose_name='Арена', related_name='events',
#                               null=True)
#     club = models.ForeignKey('AdultClub', on_delete=models.PROTECT, verbose_name='Взрослый клуб', related_name='events',
#                              null=True)
#     arena_field = models.ForeignKey('ArenaField', on_delete=models.PROTECT, verbose_name='Поле арены',
#                                     related_name='events', null=True, blank=True)
#
#     day = models.CharField(_("День недели"), choices=WEEK_DAYS, max_length=64, default='monday')
#     event_type = models.CharField(_("Тип события"), choices=EVENT_TYPES, max_length=64, default='closed_training')
#     start_time = models.CharField(_("Время начала"), choices=START_TIMES, max_length=64, default='13:15')
#     duration = models.CharField(_("Длительность"), choices=DURATION_TIMES, max_length=64, default='1:15')
#
#     class Meta:
#         verbose_name = 'Расписание арены'
#         verbose_name_plural = 'Расписания арен'
#
#     def __str__(self):
#         return 'Arena: ' + str(self.arena) + ' | Club: ' + str(self.club) + ' | Day: ' + str(self.day)
#
#
# class ArenaField(models.Model):
#     name = models.CharField(_("Название поля"), max_length=64, default='')
#
#     arena = models.ForeignKey('Arena', on_delete=models.PROTECT, verbose_name='Arena', related_name='arena_fields',
#                               null=True)
#
#     class Meta:
#         verbose_name = 'Поле'
#         verbose_name_plural = 'Поля арен'
#
#     def __str__(self):
#         return 'Арена: ' + str(self.arena) + ' | ' + str(self.name)
#
#
# class Arena(models.Model):
#     img = models.ImageField(_("Фотография арены"), null=True, upload_to='arenas')
#     name = models.CharField(_("Название арены"), max_length=64, default='')
#     metro = models.CharField(_("Ближайшее метро"), max_length=64, default='', blank=True)
#     location = models.CharField(_("Адрес арены"), max_length=64, default='')
#     how_to_get_there = models.TextField(_("Как добраться"), max_length=264, default='', blank=True)
#     operating_mode = models.TextField(_("Режим работы"), max_length=264, default='', blank=True)
#     site_address = models.CharField(_("Ссылка на сайт арены"), max_length=64, blank=True, default='')
#     vk_account = models.CharField(_("Ссылка на аккаунт во Вконтакте"), max_length=100, blank=True, default='')
#     inst_account = models.CharField(_("Ссылка на аккаунт в Instagram"), max_length=100, blank=True, default='')
#     fb_account = models.CharField(_("Ссылка на аккаунт в Facebook"), max_length=100, blank=True, default='')
#     yt_account = models.CharField(_("Ссылка на аккаунт в YouTube"), max_length=100, blank=True, default='')
#     throw_zone = models.BooleanField(_("Наличие бросковой зоны"), default=False)
#     ofp_class_hall = models.BooleanField(_("Наличие зала для занятий ОФП"), default=False)
#     gym = models.BooleanField(_("Наличие тренажерного зала"), default=False)
#     dressing_room_counter = models.IntegerField(_("Количество раздевалок для хоккеистов"), default=1)
#
#     class Meta:
#         verbose_name = 'Арена'
#         verbose_name_plural = 'Арены'
#
#     def __str__(self):
#         return self.name
#
#
# KID_CLUB_TYPES = (('Статус отсутствует', 'Статус отсутствует'),
#                   ('СШОР', 'СШОР'),
#                   ('СДЮШОР', 'СДЮШОР'),
#                   ('Детская коммерческая', 'Детская коммерческая'))
#
#
# class KidClub(models.Model):
#     logo = models.ImageField(_("Логотип"), null=True, upload_to='adult_clubs/logos')
#     img = models.ImageField(_("Фото клуба"), null=True, upload_to='adult_clubs/images')
#     name = models.CharField(_("Название клуба"), max_length=64, default='')
#     year_of_foundation = models.DateField(_("Дата основания"), default="2000-01-01")
#     club_type = models.CharField(_("Тип команды"), choices=KID_CLUB_TYPES, max_length=64, default='none')
#     coaches = models.TextField(_("Информация о тренерах"), max_length=1000, default='', blank=True)
#     site_address = models.CharField(_("Ссылка на сайт клуба"), max_length=100, blank=True, default='')
#     vk_account = models.CharField(_("Ссылка на аккаунт во Вконтакте"), max_length=100, blank=True, default='')
#     inst_account = models.CharField(_("Ссылка на аккаунт в Instagram"), max_length=100, blank=True, default='')
#     fb_account = models.CharField(_("Ссылка на аккаунт в Facebook"), max_length=100, blank=True, default='')
#     yt_account = models.CharField(_("Ссылка на аккаунт в YouTube"), max_length=100, blank=True, default='')
#
#     arena = models.ForeignKey('Arena', on_delete=models.PROTECT, verbose_name='Арена', related_name='kid_clubs',
#                               null=True)
#
#     class Meta:
#         verbose_name = 'Детский клуб'
#         verbose_name_plural = 'Детские клубы'
#
#     def __str__(self):
#         return self.name
#
#
# class AdultClub(models.Model):
#     logo = models.ImageField(_("Логотип"), null=True, upload_to='adult_clubs/logos')
#     img = models.ImageField(_("Фото клуба"), null=True, upload_to='adult_clubs/images')
#     name = models.CharField(_("Название клуба"), max_length=64, default='')
#     year_of_foundation = models.DateField(_("Дата основания"), default="2000-01-01")
#     phone_number = models.CharField(_("Номер телефона"), max_length=20, blank=True)
#     email = models.EmailField(_("Email"), blank=True)
#     site_address = models.CharField(_("Ссылка на сайт клуба"), max_length=100, blank=True)
#     vk_account = models.CharField(_("Ссылка на аккаунт во Вконтакте"), max_length=100, blank=True, default='')
#     inst_account = models.CharField(_("Ссылка на аккаунт в Instagram"), max_length=100, blank=True, default='')
#     fb_account = models.CharField(_("Ссылка на аккаунт в Facebook"), max_length=100, blank=True, default='')
#     yt_account = models.CharField(_("Ссылка на аккаунт в YouTube"), max_length=100, blank=True, default='')
#     women_can_train = models.BooleanField(_("Женщины могут тренироваться"), default=False)
#
#     arena = models.ForeignKey('Arena', on_delete=models.SET_NULL, verbose_name='Арена', related_name='adult_clubs',
#                               null=True)
#     users = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='Игроки', related_name='adult_clubs',
#                                    blank=True)
#
#     class Meta:
#         verbose_name = 'Взрослый клуб'
#         verbose_name_plural = 'Взрослые клубы'
#
#     def __str__(self):
#         return self.name
#
#
# GRIPS = (('Левша', 'Левша'),
#          ('Правша', 'Правша'))
#
#
# class User(AbstractUser):
#     img = models.ImageField(_("Фото пользователя"), null=True, upload_to='users')
#     middle_name = models.CharField(_("Отчество"), max_length=64, blank=True)
#     date_of_birth = models.DateField('Дата рождения', default="2000-01-01")
#     grip = models.CharField(_("Хват"), choices=GRIPS, max_length=64, default='right-handed', blank=True)
#     coach_info = models.TextField(_("Карьера тренера"), max_length=300, blank=True)
#     coaching_experience = models.IntegerField(_("Тренерский стаж"), null=True, blank=True)
#     game_number = models.IntegerField(_("игровой номер"), null=True, blank=True)
#     r_hokey = models.CharField(_("Ссылка на r-hokey.ru"), max_length=200, blank=True)
#     height = models.IntegerField(_("Рост"), null=True, blank=True)
#     weight = models.IntegerField(_("Вес"), null=True, blank=True)
#     status = models.CharField(_("Статус"), choices=STATUSES, max_length=64, default='none', blank=True)
#     phone_number = models.CharField(_("Номер телефона"), max_length=20, blank=True)
#     vk_account = models.CharField(_("Ссылка на аккаунт во Вконтакте"), max_length=100, blank=True)
#     inst_account = models.CharField(_("Ссылка на аккаунт в Instagram"), max_length=100, blank=True)
#     fb_account = models.CharField(_("Ссылка на аккаунт в Facebook"), max_length=100, blank=True)
#     yt_account = models.CharField(_("Ссылка на аккаунт в YouTube"), max_length=100, blank=True)
#     in_search = models.BooleanField(_("В поиске команды"), default=False)
#
#     arenas = models.ManyToManyField('Arena', verbose_name='Админ. арены', related_name='arena_admins', null=True,
#                                     blank=True)
#
#     kid_club_admin = models.OneToOneField('KidClub', on_delete=models.SET_NULL, verbose_name='Админ. детского клуба',
#                                           related_name='admin', null=True, blank=True)
#
#     kids_tournament_admin = models.OneToOneField('KidsTournament', on_delete=models.SET_NULL,
#                                                  verbose_name='Админ. детского турнира',
#                                                  related_name='admin', null=True, blank=True)
#
#     school_admin = models.OneToOneField('School', on_delete=models.SET_NULL, verbose_name='Админ. школы',
#                                         related_name='admin', null=True, blank=True)
#
#     class Meta:
#         verbose_name = 'Пользователь'
#         verbose_name_plural = 'Пользователи'
#
#     def __str__(self):
#         return self.status + ' | ' + self.first_name + ' ' + self.last_name + ' | ' + self.email
