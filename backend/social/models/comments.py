from common.models import BaseModel
from django.db import models
from social.models.mixins import DeletionPendingMixin, GenericTargetMixin, UserMixin


class Comment(DeletionPendingMixin, UserMixin, GenericTargetMixin, BaseModel):
    text = models.CharField(max_length=240)
    flagged = models.BooleanField(
        default=False,
        help_text="Somebody has flagged this comment for review",
    )
    visible = models.BooleanField(
        default=True,
        help_text="This comment may be displayed publicly",
    )

    def mark_pending_deletion(self):
        super().mark_pending_deletion()
        self.visible = False

    def create_placeholder(self):
        """If this comment is deleted, replace it with an empty placeholder."""
        if self.user is None and self.text == "":
            # Comment is already a placeholder, don't create a replacement.
            return

        Comment.objects.create(
            user=None,
            text="",
            visible=True,
            target_type=self.target_type,
            target_id=self.target_id,
            created_at=self.created_at,
        )

    class Meta:
        verbose_name_plural = "Comments"
        verbose_name = "Comment"

        constraints = [
            models.UniqueConstraint(
                fields=["target_type", "target_id", "text", "user"],
                name="unique_comment_per_user_per_object",
            )
        ]

    def __str__(self):
        return f"[{self.target}] '{self.text}'"
