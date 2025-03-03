from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  
    path('pages/', views.pages, name='pages'),  
    path('page/<int:pk>/', views.page_detail, name='page_detail'),
    path('page/new/', views.create_page, name='create_page'),
    path('page/<int:pk>/edit/', views.update_page, name='update_page'),
    path('page/<int:pk>/delete/', views.delete_page, name='delete_page'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('about/', views.about, name='about'),
]
