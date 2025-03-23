from django.urls import path
from . import views
from django.urls import include

urlpatterns = [
    path('', views.home, name='home'),  
    path('pages/', views.PageListView.as_view(), name='pages'),  # Usando CBV
    path('page/<int:pk>/', views.PageDetailView.as_view(), name='page_detail'),  # Usando CBV
    path('page/new/', views.PageCreateView.as_view(), name='create_page'),  # Usando CBV
    path('page/<int:pk>/edit/', views.PageUpdateView.as_view(), name='update_page'),  # Usando CBV
    path('page/<int:pk>/delete/', views.PageDeleteView.as_view(), name='delete_page'),  # Usando CBV
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('about/', views.about, name='about'),
    path('users/', include('users.urls')),  # Incluye las URLs de la app 'users'
]
