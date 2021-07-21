import json
import logging
from abc import abstractmethod
from typing import Dict

from django.contrib.contenttypes.models import ContentType
from django.http import (
    HttpResponse,
    JsonResponse,
)
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.views.viewsets import KeyRequiredViewSet
from repository.models import (
    Bill,
    CommonsDivision,
    Constituency,
    ConstituencyResult,
    LordsDivision,
    Person,
)
from social.models import Comment
from social.models.mixins import get_target_kwargs
from social.models.token import UserToken
from social.models.votes import (
    Vote,
    VoteType,
)
from social.serializers.comments import (
    CommentSerializer,
    PostCommentSerializer,
)
from social.serializers.social import SocialSerializer
from social.serializers.votes import PostVoteSerializer
from social.views import contract
from social.views.decorators.auth_token_required import user_token_required

log = logging.getLogger(__name__)


def _get_comment_serializer(method):
    if method == "POST":
        return PostCommentSerializer
    else:
        return CommentSerializer


def _get_vote_serializer(method):
    if method == "POST":
        return PostVoteSerializer
    else:
        log.warning(f"UNSUPPORTED METHOD {method}")


class _AbstractSocialViewSet(KeyRequiredViewSet, ModelViewSet):
    model_class = None

    class Meta:
        abstract = True

    @abstractmethod
    def get_target_title(self, target) -> str:
        pass

    def get_queryset(self):
        return None

    def get_serializer_class(self):
        # TODO This should not be called but GET /comments/ does call it.
        return CommentSerializer

    def get_queryset_for_target(self, Model):
        return Model.objects.filter(
            target_type=ContentType.objects.get_for_model(self.model_class),
            target_id=self.kwargs.get("pk"),
        )

    def get_vote_queryset(self):
        return self.get_queryset_for_target(Vote)

    def get_comment_queryset(self):
        return self.get_queryset_for_target(Comment)

    @action(methods=["get", "post"], detail=False)
    def comments(self, request, *args, **kwargs):
        if request.method == "GET":
            return self.get_comments()

        elif request.method == "POST":
            return self.create_comment(request)

    @action(methods=["get", "post", "delete"], detail=False)
    def votes(self, request, *args, **kwargs):
        if request.method == "GET":
            return self.get_votes()

        elif request.method == "POST":
            return self.create_vote(request)

        elif request.method == "DELETE":
            return self.delete_vote(request)

    @action(methods=["get"], detail=False)
    def all(self, request, *args, **kwargs):
        target = self.get_target_or_404()
        user_vote = self.get_user_vote_type(request, target)

        data = SocialSerializer(
            self.get_target_title(target),
            self._get_comments_data(),
            self._get_votes_data(),
            user_vote,
        ).data
        return Response(data)

    def _get_comments_data(self):
        return self.get_comment_queryset()

    def get_comments(self):
        data = _get_comment_serializer("GET")(self._get_comments_data(), many=True)
        return Response(data=data.data)

    @user_token_required
    def create_comment(self, request, token):
        return self._create(request, _get_comment_serializer("POST"))

    def _get_votes_data(self) -> Dict[str, int]:
        qs = self.get_vote_queryset()
        vote_types = VoteType.objects.all()
        vote_counts = {}

        for vt in vote_types:
            vote_counts[vt.name] = qs.filter(vote_type=vt, user__enabled=True).count()
        return vote_counts

    def get_votes(self):
        """Return count of each vote type"""
        data = self._get_votes_data()

        return JsonResponse(data)

    def get_user_token(self, request):
        # token = request.GET.get(contract.USER_TOKEN)
        token = request.query_params.get(contract.USER_TOKEN)
        if token is None:
            return None

        try:
            return UserToken.objects.get(token=token)
        except Exception as e:
            log.warning(f"Unable to retrieve UserToken for received token: {e}")
            return None

    def get_user_vote_type(self, request, target):
        user_token = self.get_user_token(request)
        if user_token is None:
            return

        try:
            return Vote.objects.get(
                user=user_token,
                **get_target_kwargs(target),
            ).vote_type.name
        except Exception as e:
            return None

    @user_token_required
    def create_vote(self, request, token):
        return self._create(request, _get_vote_serializer("POST"))

    def _create(self, request, serializer):
        target = self.get_target_or_404()
        data = serializer(target=target, data=request.data)

        if data.is_valid():
            data.save()
            return HttpResponse(status=status.HTTP_201_CREATED)
        else:
            log.warning(f"Invalid data [{request.path}]: {data}")
            return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete_vote(self, request):
        target = self.get_target_or_404()

        try:
            token = json.loads(request.body).get(contract.USER_TOKEN)
            user_token = UserToken.objects.get(token=token)

            Vote.objects.get(
                user=user_token,
                **get_target_kwargs(target),
            ).delete()
        except Exception as e:
            log.warning(f"Failed to delete vote: {e} {target}")

        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

    def get_target_or_404(self):
        return get_object_or_404(self.model_class, pk=self.kwargs.get("pk"))


class MemberSocialViewSet(_AbstractSocialViewSet):
    def get_target_title(self, target: Person) -> str:
        return target.name

    model_class = Person


class CommonsDivisionSocialViewSet(_AbstractSocialViewSet):
    def get_target_title(self, target: CommonsDivision) -> str:
        return target.title

    model_class = CommonsDivision


class LordsDivisionSocialViewSet(_AbstractSocialViewSet):
    def get_target_title(self, target: LordsDivision) -> str:
        return target.title

    model_class = LordsDivision


class BillSocialViewSet(_AbstractSocialViewSet):
    def get_target_title(self, target: Bill) -> str:
        return target.title

    model_class = Bill


class ConstituencySocialViewSet(_AbstractSocialViewSet):
    def get_target_title(self, target) -> str:
        return target.name

    model_class = Constituency


class ConstituencyResultSocialViewSet(_AbstractSocialViewSet):
    def get_target_title(self, target) -> str:
        return target.election.name

    model_class = ConstituencyResult
