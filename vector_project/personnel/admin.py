from django.contrib import admin
from .models import Employee, Skill, EmployeeImage
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


class EmployeeImageInline(admin.TabularInline):
    model = EmployeeImage
    extra = 1  # Allow adding multiple images at once


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'gender')
    filter_horizontal = ('skills',)  # For ManyToManyField
    inlines = [EmployeeImageInline]


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Skill)
admin.site.register(EmployeeImage)


# Inline Employee information in User admin
class EmployeeInline(admin.StackedInline):
    model = Employee
    can_delete = False
    verbose_name_plural = 'employee'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (EmployeeInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# workplaces/admin.py

from django.contrib import admin
from .models import Workplace

admin.site.register(Workplace)