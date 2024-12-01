from django.db import models
from django.contrib.auth import get_user_model

user = get_user_model()


class CalendarUser(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE, null=True, blank=True)
    userData = models.JSONField(blank=True, null=True)

    def __str__(self):
        # TODO: return this with user model
        # return self.user.username
        return f"user"
