from django.db import models
from django.contrib.auth.models import User


class CronofyUser(models.Model):
    # TODO: link this with our user model
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    accessToken = models.CharField(max_length=200, null=True, blank=True)
    refreshToken = models.CharField(max_length=200, null=True, blank=True)
    sub = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        # TODO: return this with user model
        # return self.user.username
        return f"user with this refresh token: {self.refreshToken}"
