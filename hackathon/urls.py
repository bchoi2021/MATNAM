from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.views.generic import RedirectView


urlpatterns = [
    path("admin/", admin.site.urls),
    path('home/', include('home.urls')),
    path('', RedirectView.as_view(url='/home/', permanent=True)),
    path('user/', include('user.urls')),
    path('board/', include('board.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('mateboard/', include('mateboard.urls')),
    path('shareboard/', include('shareboard.urls')),
    path('photo/',include('photo.urls')),
]

