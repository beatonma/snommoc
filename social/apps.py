from django.apps import AppConfig


class SocialConfig(AppConfig):
    name = 'social'

    def ready(self):
        import social.signals.on_user_created  # noqa
