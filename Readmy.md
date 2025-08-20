1. # Запустить терминал. Установка Django
bash
pip install django
python -m venv venv
venv\Scripts\activate.bat
2. # Создание проекта
django-admin startproject vector_project

cd vector_project

3. # Создание приложений
python manage.py startapp personnel
python manage.py startapp workplaces

4. # Установка зависимостей
bash
pip install django django-ckeditor==6.3.0
pip install black isort
# Установите зависимости:
bash
pip install -r requirements.txt

# Актевировать расширения
pip freeze > requirements.txt

5. # Настройка settings.py

# vector_project/settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'personnel',
    'workplaces',
    'ckeditor',  # Добавлено
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'vector_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Добавлено
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static",]  # Добавлено

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'  # Добавлено

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CKEditor configuration
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'extraPlugins': 'codesnippet,uploadimage,image2',
    },
}

CKEDITOR_UPLOAD_PATH = "uploads/"  # Директория для загрузки изображений


6. # Модели personnel/models.py

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

# Delete images from disk when the EmployeeImage object is deleted
@receiver(pre_delete, sender=EmployeeImage)
def employeeimage_delete(sender, instance, **kwargs):
    instance.image.delete(False)

7. # Модели workplaces/models.py
from django.db import models
from personnel.models import Employee

class Workplace(models.Model):
    group_number = models.IntegerField()
    post_number = models.IntegerField()
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, blank=True, null=True, related_name='workplaces')

    def __str__(self):
        return f"Group {self.group_number}, Post {self.post_number}"

8. # Миграции и создание базы данных

bash
python manage.py makemigrations personnel workplaces
python manage.py migrate

9. # Регистрация моделей в admin.py

# personnel/admin.py
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

10. # URLs

# vector_project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('personnel/', include('personnel.urls')),
    path('workplaces/', include('workplaces.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# personnel/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/<int:pk>/', views.employee_detail, name='employee_detail'),
]

# workplaces/urls.py

from django.urls import path
from . import views

urlpatterns = [
    #path('', views.some_view, name='workplaces_home'), You would define your views here later.
]

11. # Views

# personnel/views.py

from django.shortcuts import render, get_object_or_404
from .models import Employee
from django.contrib.auth.decorators import login_required

def home(request):
    employees = Employee.objects.all()
    return render(request, 'personnel/home.html', {'employees': employees, 'project_description':"Описание проекта"})

def employee_list(request):
    employees = Employee.objects.all()  # You might want to change this to a paginated version
    return render(request, 'personnel/employee_list.html', {'employees': employees})

@login_required
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'personnel/employee_detail.html', {'employee': employee})

12. # Templates (Создайте папки templates внутри vector_project и personnel)

# {# templates/personnel/home.html #}

{% extends 'base.html' %}
{% block content %}
    <h1>{{ project_description }}</h1>
    <div class="employee-cards">
        {% for employee in employees %}
            <div class="employee-card">
                <a href="{% url 'employee_detail' employee.pk %}">
                    <h2>{{ employee.first_name }} {{ employee.last_name }}</h2>
                    <p>Skills:
                        {% for skill in employee.skills.all %}
                            {{ skill.name }}
                        {% endfor %}
                    </p>
                </a>
            </div>
        {% endfor %}
    </div>
{% endblock %}


# {# templates/personnel/employee_list.html #}

{% extends 'base.html' %}

{% block content %}
  <h1>Employee List</h1>
  {% for employee in employees %}
    <div class="employee-card">
      <a href="{% url 'employee_detail' employee.pk %}">
        <h2>{{ employee.first_name }} {{ employee.last_name }}</h2>
        <p>Skills:
          {% for skill in employee.skills.all %}
            {{ skill.get_name_display }}
          {% endfor %}
        </p>
      </a>
    </div>
  {% endfor %}

{% endblock %}


# {# templates/personnel/employee_detail.html #}

{% extends 'base.html' %}

{% block content %}

{% if user.is_authenticated %}
    <h1>Employee Details</h1>
    <h2>{{ employee.first_name }} {{ employee.last_name }}</h2>
    <p>Gender: {{ employee.get_gender_display }}</p>
    <h3>Skills</h3>
    <ul>
        {% for skill in employee.skills.all %}
            <li>{{ skill.get_name_display }} - Level: {{ skill.level }}</li>
        {% endfor %}
    </ul>
        <h3>Images</h3>
    <div class="image-gallery">
        {% for image in employee.images.all|dictsort:"order" %}
            <img src="{{ image.image.url }}" alt="Employee Image" style="max-width: 200px; margin-right: 10px;">
        {% endfor %}
    </div>
        <a href="{% url 'employee_list' %}">Back to list</a>
{% else %}
<p>Доступно только авторизованным пользователям. Авторизируйтесь или зарегистрируйтесь</p>
    <a href="{% url 'login' %}">Login</a>
    <a href="{% url 'register' %}">Register</a>
    {% endif %}

{% endblock %}


# {# templates/base.html #}

<!DOCTYPE html>
<html>
<head>
    <title>Vector Project</title>
</head>
<body>
<nav>
    <a href="{% url 'home' %}">Home</a>
    <a href="{% url 'employee_list' %}">Employee List</a>

<a href="{% url 'admin:index' %}">Admin Panel</a>
    {% if user.is_authenticated %}

        Hello <strong>{{ user.get_username }}</strong>!
        <a href="{% url 'logout' %}">Logout</a>
        {% else %}
        <a href="{% url 'login' %}">Login</a>
        <a href="{% url 'admin:password_reset' %}">reset</a>
        <a href="{% url 'account_signup' %}">Register</a>
              {% endif %}
</nav>
    <div class="content">

        {% block content %}
        {% endblock %}
    </div>

</body>
</html>

13. # Подключить CKEditor к проекту необходимо следующим образом

# в settings.py необходимо добавить

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static",]  # Добавлено

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'  # Добавлено

# в personnel/model.py


description = RichTextField()


# в vector_project/urls.py добавить зависимости для работы с контентом

python manage.py createsuperuser  # Создайте суперпользователя для доступа к админке
python manage.py runserver
