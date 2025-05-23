from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('complete/<int:task_id>/', views.complete_task, name='complete_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('edit/<int:task_id>/', views.update_task, name='edit_task'),
    path('change-password/', views.change_password_modal, name='password_change_modal'),  # ✅ смена пароля
]
