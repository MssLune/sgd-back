import typing

from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.core import validators
from django.utils.functional import cached_property
from django.db import models

from sgd.constants import DELETED_USER, ROLE
from utils.text import get_random_name


def get_deleted_user():
    try:
        return User.objects.get(pk=DELETED_USER)
    except User.DoesNotExist:
        return User.objects.get_or_create(username='DELETED')[0]


def get_image_path(instance, filename):
    return 'user_profile/{0}'.format(get_random_name(filename))


class User(AbstractUser):
    class Gender(models.TextChoices):
        MALE = 'M'
        FEMALE = 'F'

    services = models.ManyToManyField(
        'Service',
        through='TechnicalService',
        related_name='users',
        help_text='Servicios asignados al técnico.')
    dni = models.CharField(
        verbose_name='DNI', max_length=8, null=True, blank=True, unique=True,
        validators=[validators.MinLengthValidator(8)])
    gender = models.CharField(max_length=1, choices=Gender.choices)
    photo = models.ImageField(
        verbose_name='foto',
        upload_to=get_image_path,
        default='user_profile/user_default.png')
    phone = models.CharField(verbose_name='teléfono', max_length=9)

    class Meta:
        db_table = 'public\".\"user'
        ordering = ['date_joined']
        get_latest_by = 'date_joined'

    def in_group(
        self,
        group_list: typing.List[str],
        group_lockup='id'
    ) -> bool:
        return self.groups.all().filter(
            **{'{}__in'.format(group_lockup): group_list}).exists()


class TechnicianManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(groups__id=ROLE.TECHNICIAN)


class Technician(User):
    """
    Proxy class for register technician users in admin.
    """
    objects = TechnicianManager()

    class Meta:
        proxy = True
        verbose_name = 'Técnico'


def get_service_path(instance, filename):
    return 'services/{}'.format(get_random_name(filename))


class Service(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET(get_deleted_user))
    name = models.CharField(
        verbose_name='nombre', max_length=50)
    description = models.TextField(
        verbose_name='descripción', max_length=512, default='')
    image = models.ImageField(
        verbose_name='imagen', upload_to=get_service_path)
    icon = models.CharField(
        max_length=50, default='bolt',
        help_text='Nombre de un ícono de Material')
    register_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'public\".\"service'
        ordering = ['register_date']
        get_latest_by = 'register_date'
        verbose_name = 'Servicio'

    def __str__(self):
        return self.name


class TechnicalService(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    register_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'public\".\"technical_service'
        ordering = ['register_date']
        get_latest_by = 'register_date'


class ScheduledService(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PE', 'Pendiente'
        COMPLETED = 'CO', 'Completado'
        CANCELED = 'CA', 'Cancelado'

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_deleted_user),
        verbose_name='cliente',
        related_name='scheduled_services')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    status = models.CharField(
        verbose_name='estado',
        max_length=2,
        choices=Status.choices,
        default=Status.PENDING)
    technician = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='técnico',
        on_delete=models.SET(get_deleted_user),
        related_name='services_provided')
    date = models.DateField(verbose_name='fecha')
    time = models.TimeField(verbose_name='hora')
    # TODO: check address, latitude, longitude required constraint
    address = models.CharField(
        verbose_name='direccion', max_length=124, null=True, blank=True)
    latitude = models.CharField(
        verbose_name='latitud', max_length=20, null=True, blank=True)
    longitude = models.CharField(
        verbose_name='longitud', max_length=20, null=True, blank=True)
    reference = models.CharField(
        verbose_name='referencia', max_length=1000, default='')
    register_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'public\".\"scheduled_service'
        ordering = ['register_date']
        get_latest_by = 'register_date'
        verbose_name = 'Servicio Agendado'
        verbose_name_plural = 'Servicios Agendados'

    def __str__(self):
        return f'{self.service} - {self.client}: {self.status}'

    @cached_property
    def gradable(self) -> bool:
        if (self.status == ScheduledService.Status.COMPLETED
                and not hasattr(self, 'calification')):
            return True
        return False


class Calification(models.Model):
    # client = models.ForeignKey(
    #     settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # technician = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.CASCADE,
    #     related_name='califications')
    # service = models.ForeignKey(Service, on_delete=models.CASCADE)
    scheduled_service = models.OneToOneField(
        ScheduledService, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField(
        validators=[validators.MaxValueValidator(limit_value=5)])
    comment = models.CharField(max_length=255, default='')
    register_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'public\".\"calification'
        ordering = ['register_date']
        get_latest_by = 'register_date'
        verbose_name = 'Calificación'
        verbose_name_plural = 'Calificaciones'
