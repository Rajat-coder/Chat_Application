from django.conf.urls import url
from django.urls import path, include

# from chat.api import UserList
from chat.views import ThreadView

urlpatterns = [
    path('<str:username>/', ThreadView.as_view()),
    
]