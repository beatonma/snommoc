import uuid

from common.models import BaseModel, BaseQuerySet
from django.core.validators import RegexValidator
from django.db import models
from social.models.mixins import DeletionPendingMixin


def _create_default_username() -> str:
    return uuid.uuid4().hex[:10]


class OAuthQuerySet(BaseQuerySet):
    def create_default(self, username: str):
        try:
            return self.create(provider="snommoc", user_id=username)
        except InterruptedError:
            return self.create(
                provider="snommoc",
                user_id=f"{username}-{uuid.uuid4().hex[:6]}",
            )


class OAuthToken(BaseModel):
    objects = OAuthQuerySet.as_manager()
    provider = models.CharField(max_length=50)
    user_id = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.provider}:{self.user_id[:6]}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["provider", "user_id"],
                name="unique_provider_user_id_per_provider",
            )
        ]


class UserToken(DeletionPendingMixin, BaseModel):
    @staticmethod
    def username_validator():
        return RegexValidator(
            regex=r"^[0-9a-zA-Z][0-9a-zA-Z-_.]{2,}[0-9a-zA-Z]$",
            message="Must start and end with alphanumerics. "
            "Otherwise also allow dash, underscore, dot. "
            "Minimum 4 characters.",
        )

    oauth_session = models.OneToOneField("social.OAuthToken", on_delete=models.CASCADE)

    token = models.UUIDField(default=uuid.uuid4)
    username = models.CharField(
        max_length=16,
        default=_create_default_username,
        unique=True,
        validators=[
            username_validator(),
        ],
    )
    enabled = models.BooleanField(default=True)

    def mark_pending_deletion(self):
        super().mark_pending_deletion()
        self.enabled = False

    def __str__(self):
        return self.username


class UsernameChanged(BaseModel):
    """Created when a UserToken username is changed"""

    token = models.ForeignKey(
        "UserToken",
        on_delete=models.CASCADE,
    )
    new_name = models.CharField(max_length=16)
    previous_name = models.CharField(max_length=16)

    def __str__(self):
        return f"{self.created_at}: {self.previous_name} -> {self.new_name}"
