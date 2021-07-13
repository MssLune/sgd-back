from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils.html import mark_safe

from .models import User, Technician, Service, ScheduledService
from sgd.constants import ROLE
from utils.validators import number_validator


class TechnicianForm(forms.ModelForm):
    services = forms.ModelMultipleChoiceField(
        label='Servicios',
        queryset=Service.objects.all())
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    dni = forms.CharField(max_length=8, validators=[number_validator])
    phone = forms.CharField(max_length=9, validators=[number_validator])

    class Meta:
        model = Technician
        fields = [
            'first_name', 'last_name', 'dni', 'photo', 'phone', 'groups',
            'services'
        ]


class TechnicianAdmin(admin.ModelAdmin):
    form = TechnicianForm
    list_display = [
        'full_name', 'dni', 'photo', 'phone', 'list_services'
    ]
    search_fields = [
        'username', 'email', 'dni', 'first_name', 'last_name',
        # 'services_provided__service__name'
    ]
    readonly_fields = ['groups']
    list_per_page = 20

    def get_queryset(self, request):
        return Technician.objects.prefetch_related('groups', 'services')

    def get_fields(self, request, obj=None):
        fields = list(super().get_fields(request, obj=obj))
        if obj is None:  # add view
            fields.remove('groups')
        return fields

    def save_model(self, request, obj, form, change):
        if not change:
            obj.username = form.cleaned_data.get('dni')
        super().save_model(request, obj, form, change)
        if not change:
            obj.set_password(obj.dni)
            obj.groups.set([ROLE.TECHNICIAN])
            obj.save()

    @admin.display(description='Nombre')
    def full_name(self, obj):
        return f'{obj.last_name}, {obj.first_name}'

    @admin.display(description='Servicios')
    def list_services(self, obj):
        return ', '.join([
            service.name for service in obj.services.all()
        ])


class UserAdmin(admin.ModelAdmin):
    # date_hierarchy = 'date_joined'
    list_display = ['username', 'email', 'dni', 'is_active']
    fields = [('username', 'email'), 'dni', 'groups']
    filter_horizontal = ['groups']
    list_filter = [
        ('groups', admin.RelatedFieldListFilter)
    ]
    list_per_page = 20
    search_fields = ['username', 'email', 'dni']
    readonly_fields = ['groups']
    sortable_by = []
    view_on_site = False

    def _get_queryset(self, request):
        return User.objects.filter(groups__id=ROLE.ADMIN)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    fields = ['user', 'name', 'description', 'icon', 'image', 'image_file']
    readonly_fields = ['user', 'image_file']
    per_page = 20

    def _get_fields(self, request, obj=None):
        fields = list(super().get_fields(request, obj=obj))
        if obj is not None:  # change view
            fields.append('user')
        return fields

    @admin.display(description='Imagen(archivo)')
    def image_file(self, obj):
        return mark_safe(
            '<img src="{url}" width="{width}" height="{height}" >'.format(
                url=obj.image.url,
                width=100,
                height=100
            )
        )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        return super().save_model(request, obj, form, change)


class ScheduledServiceAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'technician_name', 'client_name', 'service', 'date', 'time',
        'technician_dni', 'address', 'client_phone', 'status'
    ]
    list_display_links = ['id', 'technician_name']
    readonly_fields = [
        'client', 'service', 'technician', 'date', 'time', 'address',
        'latitude', 'longitude', 'reference'
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('technician', 'client', 'service')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.display(description='Técnico')
    def technician_name(self, obj):
        return obj.technician.first_name

    @admin.display(description='Cliente')
    def client_name(self, obj):
        return obj.client.first_name

    @admin.display(description='DNI Técnico')
    def technician_dni(self, obj):
        return obj.technician.dni

    @admin.display(description='Teléfono del cliente')
    def client_phone(self, obj):
        return obj.client.phone


admin.site.empty_value_display = '-----'
admin.site.site_header = 'Administración - SGD'
admin.site.site_title = 'SGD'

admin.site.register(User, UserAdmin)
admin.site.register(Technician, TechnicianAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(ScheduledService, ScheduledServiceAdmin)
