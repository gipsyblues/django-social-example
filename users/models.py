from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings
from allauth.account.signals import user_signed_up


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True, null=True)

    def __str__(self):
        return f'Profile for {self.user}'


def user_created(request, user, **kwargs):
    """ Creates empty user profile when a new user signs up """
    Profile.objects.create(user=user)
    user_created(user, 'has signed up')


user_signed_up.connect(user_created)


class Contact(models.Model):
    user_from = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'


user_model = get_user_model()
user_model.add_to_class(
    'following', models.ManyToManyField('self', through=Contact, related_name='followers', symmetrical=False)
)
