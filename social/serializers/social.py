from social.serializers.comments import CommentSerializer
from social.views import contract


class SocialSerializer:
    def __init__(self, title, comments, votes, user_vote_type):
        serialized_comments = CommentSerializer(comments, many=True)
        comment_data = serialized_comments.data

        self.data = {
            contract.TITLE: title,
            contract.COMMENTS: comment_data,
            contract.VOTES: votes,
            contract.VOTE_TYPE: user_vote_type,
        }
