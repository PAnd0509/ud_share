import datetime as _dt
from typing import Optional

from mongoengine import Document, EmbeddedDocument, StringField, DateTimeField, ReferenceField, ObjectIdField, connect, ValidationError,



def init_db(uri: str, **kwargs) -> None:
    connect(host=uri, **kwargs)


class User(Document):
    meta = {"collection": "user"}
    nickname = StringField(max_length=10, unique=True, required=True)


class Post(Document):
    meta = {"collection": "post"}
    text_post = StringField(max_length=800, required=True)


class CatReaction(Document):
    meta = {"collection": "cat_reaction"}
    reaction = StringField(max_length=6, unique=True, required=True)


#  MAIN MODULE DOCUMENTS
class Follower(Document):
    """
    A follows B (unique pair) – status ON/OFF
    """

    meta = {
        "collection": "follower",
        "indexes": [
            {"fields": ("follower", "followed"), "unique": True},
        ],
    }

    date_begin_follow = DateTimeField(default=_dt.datetime.utcnow)
    follower = ReferenceField(User, required=True, reverse_delete_rule=2)  # CASCADE
    followed = ReferenceField(User, required=True, reverse_delete_rule=2)
    status = StringField(
        choices=("ON", "OFF"),
        required=True,
    )

    def clean(self) -> None:
        if self.follower == self.followed:
            raise ValidationError("A user cannot follow themselves.")


class Comment(Document):
    """
    Comment belongs to a Post & an Author (User)
    """

    meta = {"collection": "comment"}

    text_comment = StringField(max_length=800, required=True)
    user = ReferenceField(User, required=True, reverse_delete_rule=2)
    post = ReferenceField(Post, required=True, reverse_delete_rule=2)
    date_create = DateTimeField(default=_dt.datetime.utcnow)


class Reaction(Document):
    """
    Reaction to either a Post XOR a Comment
    """

    meta = {
        "collection": "reaction",
        "indexes": [
            # Ensure a user can react only once to the same target
            {"fields": ("user", "post", "comment"), "unique": True},
        ],
    }

    date_reaction = DateTimeField(default=_dt.datetime.utcnow)
    user = ReferenceField(User, required=True, reverse_delete_rule=2)
    post = ReferenceField(Post, null=True, reverse_delete_rule=2)
    comment = ReferenceField(Comment, null=True, reverse_delete_rule=2)
    cat_reaction = ReferenceField(CatReaction, required=True, reverse_delete_rule=2)

    def clean(self) -> None:
        """
        Enforces XOR rule: target must be *either* post or comment, not both, not none.
        """
        has_post = self.post is not None
        has_comment = self.comment is not None
        if has_post == has_comment:  # both True or both False
            raise ValidationError(
                "Reaction must reference exactly one of `post` or `comment`."
            )


class HistoricalPost(Document):
    """
    Immutable versions of a Post (EDIT / DEL states)
    """

    meta = {
        "collection": "historical_post",
        "indexes": [
            {"fields": ("post", "date_modificate"), "unique": True},
        ],
    }

    post = ReferenceField(Post, required=True, reverse_delete_rule=2)
    date_modificate = DateTimeField(required=True)
    text_version = StringField(max_length=800, required=True)
    status = StringField(choices=("EDIT", "DEL"), required=True)
    date_create = DateTimeField(default=_dt.datetime.utcnow)


class HistoricalComment(Document):
    """
    Immutable versions of a Comment
    """

    meta = {
        "collection": "historical_comment",
        "indexes": [
            {"fields": ("comment", "date_modificate"), "unique": True},
        ],
    }

    comment = ReferenceField(Comment, required=True, reverse_delete_rule=2)
    date_modificate = DateTimeField(required=True)
    text_version = StringField(max_length=800, required=True)
    status = StringField(choices=("EDIT", "DEL"), required=True)
    date_create = DateTimeField(default=_dt.datetime.utcnow)
