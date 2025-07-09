from sqlalchemy import Column, Integer, String, Date, ForeignKey, CheckConstraint, UniqueConstraint, PrimaryKeyConstraint, text, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

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
    
#  MÓDULO DE POST

def create_post(db: Session, post_data: PostCreate):
    new_post = Post(**post_data.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

def get_post_by_id(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()

def get_all_posts(db: Session):
    return db.query(Post).all()

def update_post(db: Session, post_id: int, update_data: PostUpdate):
    post = get_post_by_id(db, post_id)
    if not post:
        return None
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(post, key, value)
    db.commit()
    db.refresh(post)
    return post

def delete_post(db: Session, post_id: int):
    post = get_post_by_id(db, post_id)
    if not post:
        return None
    db.delete(post)
    db.commit()
    return post

# -------- ATTACHED MULTIMEDIA --------

def create_attachment(db: Session, data: AttachedMultimediaCreate):
    # ⚠️ Validación XOR ya está en el modelo SQL con CheckConstraint
    new_media = AttachedMultimedia(**data.dict())
    db.add(new_media)
    db.commit()
    db.refresh(new_media)
    return new_media

def get_attachment_by_id(db: Session, media_id: int):
    return db.query(AttachedMultimedia).filter(AttachedMultimedia.id == media_id).first()

def get_all_attachments(db: Session):
    return db.query(AttachedMultimedia).all()

def update_attachment(db: Session, media_id: int, update_data: AttachedMultimediaUpdate):
    media = get_attachment_by_id(db, media_id)
    if not media:
        return None
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(media, key, value)
    db.commit()
    db.refresh(media)
    return media

def delete_attachment(db: Session, media_id: int):
    media = get_attachment_by_id(db, media_id)
    if not media:
        return None
    db.delete(media)
    db.commit()
    return media