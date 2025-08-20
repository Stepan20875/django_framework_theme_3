"""
URL configuration for vector_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from personnel import views
from django.contrib.auth import views as auth_views # <-- ИМПОРТИРУЙТЕ ЭТО

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('personnel/', include('personnel.urls')),
    path('workplaces/', include('workplaces.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='personnel/login.html'), name='login'), # (опционально, если у вас уже есть свой view для логина)
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'), # <-- ДОБАВЬТЕ ЭТУ СТРОКУ
    # next_page='название_вашей_домашней_страницы' или '/'
    # Если у вас есть 'home' URL, можете использовать next_page='home'

    # path('register/', your_app_views.register, name='register'), # Если у вас есть регистрация
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
