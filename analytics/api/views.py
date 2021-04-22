from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from .serializers import RequestTrackingViewSerializer
from analytics.models import RequestTracking


class UserLastActionView(generics.RetrieveAPIView):
    """
    View to generate user last action by his/her id. Only Admin can has
    permission.
    """
    permission_classes = (IsAdminUser,)
    serializer_class = RequestTrackingViewSerializer

    def get_object(self):
        user_id = self.kwargs['user_pk']
        last_request = RequestTracking.objects.filter(user__id=user_id).first()
        return last_request
