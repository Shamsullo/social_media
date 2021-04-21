from django.contrib import admin
from django.urls import path, include
from .yasg import urlpatterns as doc_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('djoser.urls')),
    path('api-auth/', include('djoser.urls.jwt')),
    path('api-post/', include('post.api.urls')),
]

urlpatterns += doc_urls
