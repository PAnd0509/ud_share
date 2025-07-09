from sqlalchemy import Column, Integer, String, Date, ForeignKey, CheckConstraint, UniqueConstraint, PrimaryKeyConstraint, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

#  CATÁLOGOS (tablas de dominio)

class CatTypeUser(Base):
    __tablename__ = "cat_type_user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(6), unique=True, nullable=False)
    label = Column(String(10), nullable=False)
    description = Column(String(30))


class CatVisibilityType(Base):
    __tablename__ = "cat_visibility_type"

    id = Column(Integer, primary_key=True, autoincrement=True)
    visibility = Column(String(6), unique=True, nullable=False)
    label = Column(String(10))
    description = Column(String(10))


class CatReaction(Base):
    __tablename__ = "cat_reaction"

    id = Column(Integer, primary_key=True, autoincrement=True)
    reaction = Column(String(6), unique=True, nullable=False)
    label = Column(String(10))
    description = Column(String(10))
    date_reaction = Column(Date)  # fecha de catalogación


#  MÓDULO DE USUARIO


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    date_create = Column(
        Date, nullable=False, server_default=text("CURRENT_DATE")
    )
    nickname = Column(String(10), unique=True, nullable=False)
    name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    birth_date = Column(Date,CheckConstraint(
        "birth_date <= (CURRENT_DATE - INTERVAL '15 years')",
        name="chk_user_min_age_15"),
    nullable=False
    )
    email = Column(String(30), unique=True, nullable=False)
    password = Column(String(60), nullable=False)  # hash
    profile_image = Column(String(255))
    fk_type_user = Column(
        Integer, ForeignKey("cat_type_user.id"), nullable=False
    )

    __table_args__ = (
        CheckConstraint(
            "status IN ('active','inactive','banned')", name="chk_user_status"
        ),
        CheckConstraint(
            "birth_date IS NULL OR birth_date <= CURRENT_DATE",
            name="chk_birth_not_future",
        ),
    )


class UserAddData(Base):
    __tablename__ = "user_add_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    profile_description = Column(String(100))
    phone = Column(String(10))
    social_media = Column(String(100))
    fk_user_id = Column(Integer, ForeignKey("user.id"), nullable=False, unique=True)

    __table_args__ = (
        CheckConstraint(
            "phone IS NULL OR phone ~ '^[0-9]{7,10}$'", name="chk_phone_regex"
        ),
    )


class UserAccountConected(Base):
    __tablename__ = "user_account_conected"

    facebook_key = Column(String(100), unique=True)
    google_key = Column(String(100), unique=True)
    fk_user_id = Column(
        Integer, ForeignKey("user.id"), primary_key=True, nullable=False
    )


class UserAud(Base):
    __tablename__ = "user_aud"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date_create = Column(Date, server_default=text("CURRENT_DATE"))
    date_modificate = Column(Date)
    date_delete = Column(Date)
    status = Column(String(6))

    __table_args__ = (
        CheckConstraint(
            "status IN ('create','update','delete')",
            name="chk_user_aud_status",
        ),
    )


class ReportUser(Base):
    __tablename__ = "report_user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date_report = Column(Date, nullable=False, server_default=text("CURRENT_DATE"))
    reason = Column(String(50), nullable=False)
    add_comment = Column(String(300))
    fk_report_to_user = Column(Integer, ForeignKey("user.id"), nullable=False)
    fk_report_by_user = Column(Integer, ForeignKey("user.id"), nullable=False)
    status_report = Column(String(5), nullable=False)
    resolution_comment = Column(String(300))

    __table_args__ = (
        CheckConstraint(
            "status_report IN ('OPEN','PROC','CLOSE')",
            name="chk_report_status",
        ),
    )

#  MÓDULO DE POSTS

class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date_post = Column(Date, nullable=False, server_default=text("CURRENT_DATE"))
    text_post = Column(String(800), nullable=False)
    fk_visibility_type = Column(Integer, ForeignKey("cat_visibility_type.id"))
    fk_user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

class AttachedMultimedia(Base):
    __tablename__ = "attached_multimedia"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False)
    format = Column(String(4), nullable=False)
    size = Column(String(10))
    characteristics = Column(String(100))
    fk_post_id = Column(Integer, ForeignKey("post.id"))
    fk_comment_id = Column(Integer, ForeignKey("comment.id"))

    __table_args__ = (
        CheckConstraint(
            "format IN ('jpg','png','gif','mp4')", name="chk_media_format"
        ),
        CheckConstraint(
            "(fk_post_id IS NULL) <> (fk_comment_id IS NULL)",
            name="chk_media_target",
        ),
    )