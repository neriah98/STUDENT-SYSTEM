from django.urls import path
from . import views

app_name = "lecturers"

urlpatterns = [
    path('all_lecturers/', views.lecturer_list, name='lecturer_list'),
    path('<int:lecturer_id>/', views.single_lecturer, name='single_lecturer'),
    path('registration/', views.create_lecturer, name='create_lecturer'),
    path('edit/<int:pk>', views.edit_lecturer, name='edit_lecturer'),
    path('delete/<int:lecturer_id>', views.delete_lecturer, name='delete_lecturer'),
    
    path('register/', views.register, name='register'),
    path('session/', views.session, name='session'),
    path('single_session/<int:session_id>/', views.single_session, name='single_session'),
]
