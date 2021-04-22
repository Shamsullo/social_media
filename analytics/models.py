from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# removing content type cause in this case I don't have to show who did what
# if it will work then maybe i will think about how can fix user thing


class RequestTracking(models.Model):
    """Table to save tracking the requests of users."""
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self, ):
        return f'{self.user} made a request at: {self.timestamp}'

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'Requests Tracking'

