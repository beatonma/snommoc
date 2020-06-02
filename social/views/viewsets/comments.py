"""

"""

import logging

from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.views.viewsets import KeyRequiredViewSet
from repository.models import Person
from social.models import Comment
from social.serializers.comments import (
    CommentSerializer,
    PostCommentSerializer,
)
from social.views.decorators.auth_token_required import user_token_required

log = logging.getLogger(__name__)


class MemberSocialViewSet(KeyRequiredViewSet, ModelViewSet):

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostCommentSerializer
        else:
            return CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(
            target_type=ContentType.objects.get_for_model(Person),
            target_id=self.kwargs.get('pk')
        )

    @action(methods=['get', 'post'], detail=False)
    def comments(self, request, *args, **kwargs):
        if request.method == 'GET':
            data = self.get_serializer_class()(self.get_queryset(), many=True)
            return Response(data=data.data)

        elif request.method == 'POST':
            return self.create_comment(request)

    @user_token_required
    def create_comment(self, request, token):
        target = get_object_or_404(Person, pk=self.kwargs.get('pk'))
        data = self.get_serializer_class()(target=target, data=request.data)
        if data.is_valid():
            data.save()
            return HttpResponse('OK', status=status.HTTP_201_CREATED)
        else:
            log.warning(f'[Post comment] Invalid data: {data}')
            return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
