from rest_framework import serializers

from analytics.models import RequestTracking


class RequestTrackingViewSerializer(serializers.ModelSerializer):
    """For last action endpoint"""
    username = serializers.SerializerMethodField(read_only=True)
    last_login = serializers.SerializerMethodField(read_only=True)
    last_request = serializers.DateTimeField(source='timestamp', read_only=True)

    class Meta:
        model = RequestTracking
        fields = ('username', 'last_login', 'last_request')

    def get_last_login(self, req_obj):
        return req_obj.user.last_login

    def get_username(self, req_obj):
        return req_obj.user.username
