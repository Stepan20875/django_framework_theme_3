from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.db.models.signals import pre_delete
from django.dispatch import receiver

SKILL_CHOICES = [
    ('frontend', 'Frontend'),
    ('backend', 'Backend'),
    ('testing', 'Testing'),
    ('project_management', 'Project Management'),
]

GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
]


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    skills = models.ManyToManyField('Skill', related_name='employees')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Skill(models.Model):
    name = models.CharField(max_length=50, choices=SKILL_CHOICES)
    level = models.IntegerField(choices=[(i, i) for i in range(1, 11)])
    description = RichTextField()

    def __str__(self):
        return f"{self.get_name_display()} ({self.level})"

class EmployeeImage(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='employee_images/')
    order = models.IntegerField(default=0)  # Порядковый номер

    def __str__(self):
        return f"Image for {self.employee.first_name} {self.employee.last_name} - Order: {self.order}"

class Workplace(models.Model):
    # Ваши поля для модели Workplace
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return self.name

            # Возможно, у вас тут есть и другие модели
# class OtherModel(models.Model):
#     pass


# Delete images from disk when the EmployeeImage object is deleted
@receiver(pre_delete, sender=EmployeeImage)
def employeeimage_delete(sender, instance, **kwargs):
    instance.image.delete(False)