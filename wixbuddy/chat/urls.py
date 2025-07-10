from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chatbot_api, name='chatbot'),
    path('history/', views.chat_history, name='chat_history'),
    path('session/<int:session_id>/', views.get_chat_session, name='get_chat_session'),
    path('session/<int:session_id>/delete/', views.delete_chat_session, name='delete_chat_session'),
    path('history/delete-all/', views.delete_all_chat_history, name='delete_all_chat_history'),
] 