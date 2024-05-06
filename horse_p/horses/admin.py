from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from adminsortable2.admin import SortableInlineAdminMixin

from .models import Equine, Employee, Antigen, Manipulation
from .models import Calendar, Lab_group, Restriction, Cure


class EquineInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Equine
    fields = ['image', 'headshot_image']
    readonly_fields = ['headshot_image']

    def headshot_image(self, obj):
        return format_html('<img src="{}" style="max-height: {height}px";>',
                           mark_safe(obj.image.url), height=200)

    headshot_image.short_description = 'Preview'


@admin.register(Equine)
class EquineAdmin(SortableInlineAdminMixin, admin.ModelAdmin):
    list_display = ['title', 'lab_group', 'image']
    readonly_fields = ["preview"]

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.image.url}">')


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['title', 'laboratory', 'job_title']
    readonly_fields = ["preview"]

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.image.url}">')


@admin.register(Antigen)
class AntigenAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(Manipulation)
class ManipulationAdmin(admin.ModelAdmin):
    list_display = ['title', 'volume', 'volume_measure']


@admin.register(Calendar)
class CalendarAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple}, }
    list_display = ['date_manipulation', 'manipulations', 'get_category']


@admin.register(Lab_group)
class Lab_groupAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple}, }
    list_display = ['title', 'antigen', 'employee_names']
    inlines = [
        EquineInline, ]


@admin.register(Restriction)
class RestrictionAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple}, }
    list_display = ['begin_restriction', 'end_restriction', 'title']


@admin.register(Cure)
class CureAdmin(admin.ModelAdmin):
    list_display = ['title']
