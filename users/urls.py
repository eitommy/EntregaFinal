from django.urls import path
from . import views

app_name = 'users'  # Definir el espacio de nombres

urlpatterns = [
    path('profile/', views.profile, name='profile'),  # Vista del perfil
    path('profile/edit/', views.edit_profile, name='edit_profile'),  # Vista de editar perfil
    path('password_change/', views.CustomPasswordChangeView.as_view(), name='password_change'),  # Vista de cambio de contraseña
    path('password_change_done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),  # Vista de éxito
]
