from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.api_chat, name='chatbot'),
 
    
]
