import logging

from api import status
from django.db.models import Count
from django.http import HttpRequest
from ninja import Router
from social.models import Comment, Vote

from ..models.mixins import GenericTargetMixin
from . import schema

log = logging.getLogger(__name__)
router = Router()


@router.post("votes/", response={201: None})
def create_vote(request: HttpRequest, data: schema.CreateVote):
    vote, _ = Vote.objects.update_or_create(
        **data.resolve_target_kwargs(),
        user=data.resolve_user_token(),
        defaults={
            "vote_type": data.vote_type,
        },
    )
    return status.HTTP_201_CREATED, None


@router.post("comments/", response={201: None})
def create_comment(request: HttpRequest, data: schema.CreateComment):
    comment, _ = Comment.objects.get_or_create(
        **data.resolve_target_kwargs(),
        user=data.resolve_user_token(),
        text=data.text,
        flagged=data.is_flagged(),
    )
    return status.HTTP_201_CREATED, None


@router.delete("votes/", response={204: None})
def delete_vote(request: HttpRequest, data: schema.DeleteVote):
    Vote.objects.get(
        **data.resolve_target_kwargs(),
        user=data.resolve_user_token(),
    ).delete()

    return status.HTTP_204_NO_CONTENT, None


@router.get("", response=schema.SocialContent)
def get_social_content(
    request: HttpRequest,
    target: schema.InteractionTargetKey,
    target_id: int,
    token: str | None = None,  # UserToken.token
):
    target = schema.resolve_target_or_404(target, target_id)
    target_kwargs = GenericTargetMixin.get_target_kwargs(target)

    votes = (
        Vote.objects.filter(**target_kwargs)
        .values("vote_type")
        .order_by("vote_type")
        .annotate(Count("vote_type"))
    )
    votes = {x["vote_type"]: x["vote_type__count"] for x in votes}
    comments = Comment.objects.filter(**target_kwargs)

    user_vote = None
    if user_token := schema.resolve_user_token(token):
        try:
            user_vote = Vote.objects.get(user=user_token, **target_kwargs).vote_type
        except Vote.DoesNotExist:
            pass

    return {
        "title": target.social_title(),
        "votes": votes,
        "comments": comments,
        "user_vote": user_vote,
    }
