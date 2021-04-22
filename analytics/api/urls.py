from django.urls import path

from .views import UserLastActionView

urlpatterns = [
    path('last-action/<int:user_pk>', UserLastActionView.as_view(),
         name='user-last-action'),
]
