"""

"""

import logging

from social.serializers.comments import CommentSerializer
from social.views import contract

log = logging.getLogger(__name__)


class SocialSerializer:
    def __init__(self, comments, votes):
        print(comments)
        print(votes)
        serialized_comments = CommentSerializer(comments, many=True)
        comment_data = serialized_comments.data

        self.data = {
            contract.COMMENTS: comment_data,
            contract.VOTES: votes,
        }
