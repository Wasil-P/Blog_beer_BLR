"""
URL configuration for Blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from Menu import view
from users import views


#
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", view.MenuList.as_view(), name="home"),
    path("blog/", include("beer_BLR.urls_blog"), name="blog"),
    path("folklore/", include("Folklore.urls_folklore"), name="folklore"),
    path("talks/", include("Talks.urls_talks"), name="talks"),
    path("user/", include("users.urls_user", namespace="user")),
    path("register/", views.Register.as_view(), name="register"),
    path(
        "accounts/",
        include(
            ("django.contrib.auth.urls", "django.contrib.auth"), namespace="accounts"
        ),
    ),
    #API_____________________________________________________
    path("api/blog/", include("beer_BLR.api.urls_api")),
    path("api/talks/", include("Talks.api.urls_api")),
    path('api-auth/', include('rest_framework.urls'))
]

    # media___________________________________________________
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


