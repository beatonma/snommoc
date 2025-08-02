from django.apps import AppConfig


class SocialConfig(AppConfig):
    name = "social"

    def ready(self):
        import social.signals.on_comment_deleted  # noqa
        import social.signals.on_user_created  # noqa
        import social.signals.on_username_changed  # noqa
