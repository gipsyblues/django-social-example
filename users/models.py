from django.db import models
from django.conf import settings
from allauth.account.signals import user_signed_up


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True, null=True)

    def __str__(self):
        return f'Profile for {self.user}'


def create_profile(request, user, **kwargs):
    """ Creates empty user profile when a new user signs up """
    Profile.objects.create(user=user)


user_signed_up.connect(create_profile)
