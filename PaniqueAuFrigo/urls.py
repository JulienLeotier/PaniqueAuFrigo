"""PaniqueAuFrigo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from PaniqueAuFrigo import settings
from front import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.base, name="base"),
    path("login/", views.login_request, name="login"),
    path("register/", views.register_request, name="register"),
    path("account/", views.account, name="account"),
    path("guilty/", views.guilty, name="guilty"),
    path("askTalkPerso/<int:pk>", views.askTalkPerso, name="askTalkPerso"),
    path("joinAskTalkPerso/<int:pk>", views.joinAskTalkPerso, name="joinAskTalkPerso"),
    path("send_message/", views.send_message, name="send_message"),
    path("clash/", views.clash, name="clash"),
    path("accept_clash/<int:pk>", views.accept_clash, name="accept_clash"),
    path("cancel_clash/<int:pk>", views.cancel_clash, name="cancel_clash"),
    path("refuse_clash/<int:pk>", views.refuse_clash, name="refuse_clash"),
    path("logout/", views.logout_request, name="logout"),
    path("history/", views.history, name="history"),
    path("all/", views.all, name="all"),
    path("select_perso/<int:pk>", views.select_perso, name="select_perso"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
