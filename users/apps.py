from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = "users"

    def ready(self):
        # noinspection PyUnresolvedReferences
        from . import signals
