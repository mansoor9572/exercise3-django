from django.db import models

class User(models.Model):
    user_id = models.UUIDField(primary_key=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email

    class Meta:
        app_label = 'music'
