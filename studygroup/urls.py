from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views

app_name='studygroup'
urlpatterns =[
    path('', views.index, name='index'),
    path('login/', LoginView.as_view(),name='login'),
    path('register/',views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('get-courses/<int:subject_id>/', views.get_courses, name='get_courses'), 
    path('get-courses/<int:subject_id>/<int:course_id>/', views.course_detail, name='course_detail'),
    path('get-courses/<int:subject_id>/<int:course_id>/create_chatroom/', views.create_chatroom, name='create_chatroom'),
    path('join_chatroom/<int:chatroom_id>/', views.join_chatroom, name='join_chatroom'),
    path('chatrooms/<int:chatroom_id>', views.chatroom_view, name='chatroom_view'), 
    path('chatroom/<int:chatroom_id>/resources/', views.chatroom_resources, name='chatroom_resources'),
    path('profile/<int:user_id>', views.profile, name='profile'),
    path('logout/',views.logout_view, name='logout'),
]
