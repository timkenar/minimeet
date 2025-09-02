from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_meeting, name='create_meeting'),
    path('list/', views.MeetingListView.as_view(), name='meeting_list'),
    path('<int:pk>/', views.MeetingUpdateView.as_view(), name='meeting_update'),
    path('<int:pk>/ics/', views.download_ics, name='download_ics'),
    path('admin/login/', views.admin_login, name='admin_login'),
    path('admin/logout/', views.admin_logout, name='admin_logout'),
    path('admin/create/', views.admin_create_meeting, name='admin_create_meeting'),
]