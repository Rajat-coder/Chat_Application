from django.urls import path
from django.conf.urls.static import static
from ChatBackend import settings
from authentication.views import LoginView,HomeView,IndexView,SignUpView


urlpatterns=[
    path('',IndexView, name = "index"),
    path("home/",HomeView,name="homepage"),
    path("login/", LoginView, name = "login"),
    path("signup/",SignUpView,name="signup")

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)