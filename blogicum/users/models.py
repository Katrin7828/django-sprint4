from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class User(AbstractUser):
    def str(self):
        return self.username
