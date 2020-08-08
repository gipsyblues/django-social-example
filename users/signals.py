from allauth.account.signals import user_signed_up

from actions.utils import create_action

from .models import Profile


def user_created(request, user, **kwargs):
    """ Creates empty user profile when a new user signs up """
    Profile.objects.create(user=user)
    create_action(user, "has signed up")


user_signed_up.connect(user_created)
