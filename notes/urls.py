from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.user_signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('notes/create/', views.create_note, name='create_note'),
    path('notes/<int:id>/', views.get_note, name='get_note'),
    path('notes/share/', views.share_note, name='share_note'),
    path('notes/<int:id>/update/', views.update_note, name='update_note'),
    path('notes/version-history/<int:id>/', views.note_version_history, name='note_version_history'),
]
