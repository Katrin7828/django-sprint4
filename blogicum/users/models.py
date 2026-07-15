from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    def str(self):
        return self.username
