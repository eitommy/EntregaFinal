
from django.contrib import admin
from django.urls import path, include   
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from blog import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('blog.urls')), 
    path('', views.home, name='home'),  
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'), 
    path('users/', include('users.urls')), 
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)