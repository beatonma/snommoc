"""

"""
import logging

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
    LordsDivision,
    Person,
)
from social.models import Comment
from social.models.votes import (
    Vote,
    VoteType,
)
from social.serializers.comments import (
    CommentSerializer,
    PostCommentSerializer,
)
from social.serializers.votes import PostVoteSerializer
from social.views.decorators.auth_token_required import user_token_required

log = logging.getLogger(__name__)


def _get_comment_serializer(method):
    if method == 'POST':
        return PostCommentSerializer
    else:
        return CommentSerializer


def _get_vote_serializer(method):
    log.info(method)
    if method == 'POST':
        return PostVoteSerializer
    else:
        log.warning(f'UNSUPPORTED METHOD {method}')


class AbstractSocialViewSet(KeyRequiredViewSet, ModelViewSet):
    model_class = None

    class Meta:
        abstract = True

    def get_serializer_class(self):
        raise NotImplemented(
            'Use one of the content-specific methods instead '
            'e.g. _get_comment_serializer')

    def get_queryset_for_target(self, Model):
        return Model.objects.filter(
            target_type=ContentType.objects.get_for_model(self.model_class),
            target_id=self.kwargs.get('pk')
        )

    def get_vote_queryset(self):
        return self.get_queryset_for_target(Vote)

    def get_comment_queryset(self):
        return self.get_queryset_for_target(Comment)

    @action(methods=['get', 'post'], detail=False)
    def comments(self, request, *args, **kwargs):
        if request.method == 'GET':
            return self.get_comments()

        elif request.method == 'POST':
            return self.create_comment(request)

    @action(methods=['get', 'post'], detail=False)
    def votes(self, request, *args, **kwargs):
        if request.method == 'GET':
            return self.get_votes()

        elif request.method == 'POST':
            return self.create_vote(request)

    def get_comments(self):
        data = _get_comment_serializer('GET')(self.get_comment_queryset(), many=True)
        return Response(data=data.data)

    @user_token_required
    def create_comment(self, request, token):
        return self._create(request, _get_comment_serializer('POST'))

    def get_votes(self):
        """Return count of each vote type"""
        qs = self.get_vote_queryset()
        vote_types = VoteType.objects.all()
        vote_counts = {}

        for vt in vote_types:
            vote_counts[vt.name] = qs.filter(
                vote_type=vt,
                user__enabled=True
            ).count()

        return JsonResponse(vote_counts)

    @user_token_required
    def create_vote(self, request, token):
        return self._create(request, _get_vote_serializer('POST'))

    def _create(self, request, serializer):
        target = self.get_target_or_404()
        data = serializer(target=target, data=request.data)
        if data.is_valid():
            data.save()
            return HttpResponse('OK', status=status.HTTP_201_CREATED)
        else:
            log.warning(f'Invalid data [{request.path}]: {data}')
            return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_target_or_404(self):
        return get_object_or_404(self.model_class, pk=self.kwargs.get('pk'))


class MemberSocialViewSet(AbstractSocialViewSet):
    model_class = Person


class CommonsDivisionSocialViewSet(AbstractSocialViewSet):
    model_class = CommonsDivision


class LordsDivisionSocialViewSet(AbstractSocialViewSet):
    model_class = LordsDivision


class BillSocialViewSet(AbstractSocialViewSet):
    model_class = Bill
