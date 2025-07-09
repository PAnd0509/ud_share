from datetime import datetime
from typing import Optional, Literal, List

from bson import ObjectId
from pydantic import BaseModel, Field, root_validator, validator, model_validator


# Small helper so Pydantic handles ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):  # noqa: D401  (simple validator)
        if isinstance(v, ObjectId):
            return v
        try:
            return ObjectId(str(v))
        except Exception as exc:  # pragma: no cover
            raise ValueError("Not a valid ObjectId") from exc

#  FOLLOWER  (collection: follower)

class FollowerDoc(BaseModel):

    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")

    follower_user_id: int = Field(..., gt=0, description="SQL user.id that follows")
    followed_user_id: int = Field(..., gt=0, description="SQL user.id being followed")

    date_begin_follow: datetime = Field(default_factory=datetime.today)
    status: Literal["ON", "OFF"] = "ON"

    # ----- validation rules -----
    @validator("followed_user_id")
    def users_must_be_distinct(cls, v, values):
        if "follower_user_id" in values and v == values["follower_user_id"]:
            raise ValueError("A user cannot follow themselves.")
        return v

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
        schema_extra = {"collection": "follower"}

# COMMENT  (collection: comment)

class CommentDoc(BaseModel):

    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")

    text_comment: str = Field(..., min_length=1, max_length=800)
    post_id: int = Field(..., gt=0, description="SQL post.id")
    user_id: int = Field(..., gt=0, description="SQL user.id who writes")

    # 👉  NUEVO: lista de enteros que apuntan a attached_multimedia.id
    multimedia_ids: List[int] = Field(
        default_factory=list,
        description="IDs de archivos en attached_multimedia vinculados a este comentario",
    )

    date_comment: datetime = Field(default_factory=datetime.today)

    # ----- validación opcional -----
    @validator("multimedia_ids", each_item=True)
    def ids_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Cada multimedia_id debe ser un entero positivo.")
        return v

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
        schema_extra = {"collection": "comment"}

#  REACTION  (collection: reaction)

class ReactionDoc(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")

    user_id: int = Field(..., gt=0, description="SQL user.id who reacts")
    post_id: Optional[int] = Field(None, gt=0, description="SQL post.id")
    comment_id: Optional[int] = Field(None, gt=0, description="SQL comment.id")
    cat_reaction_id: int = Field(
        ..., gt=0, description="SQL cat_reaction.id – type of emoji/reaction"
    )
    date_reaction: datetime = Field(default_factory=datetime.today)

    # ----- XOR rule: post xor comment -----
    @model_validator(mode="after")
    def check_target_exclusive(cls, values):
        post_id, comment_id = values.get("post_id"), values.get("comment_id")
        if (post_id is None) == (comment_id is None):
            raise ValueError("Reaction must reference either a post or a comment, not both.")
        return values

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
        schema_extra = {"collection": "reaction"}


#   HISTORICAL POST / COMMENT VERSION

class HistoricalPostDoc(BaseModel):

    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")

    post_id: int = Field(..., gt=0, description="SQL post.id")
    date_modificate: datetime = Field(..., description="When the change occurred")
    text_version: str = Field(..., max_length=800)
    status: Literal["EDIT", "DEL"]
    date_create: Optional[datetime] = Field(None, description="Original creation date")

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
        schema_extra = {"collection": "historical_post"}


class HistoricalCommentDoc(BaseModel):

    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")

    comment_id: int = Field(..., gt=0, description="SQL comment.id")
    date_modificate: datetime = Field(..., description="When the change occurred")
    text_version: str = Field(..., max_length=800)
    status: Literal["EDIT", "DEL"]
    date_create: Optional[datetime] = Field(None, description="Original creation date")

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
        schema_extra = {"collection": "historical_comment"}

#  OPTIONAL helper – Referential check

def sql_reference_exists(session, model_cls, pk: int) -> bool:
    return session.query(model_cls).filter_by(id=pk).first() is not None
