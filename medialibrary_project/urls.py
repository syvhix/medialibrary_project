from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('medialibrary.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
]