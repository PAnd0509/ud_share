from sqlalchemy.orm import Session
from app.models.sql_models import CatTypeUser, User
from app.schemas.cat_type_user import CatTypeUserCreate, CatTypeUserUpdate, UserCreate, UserUpdate

# Create
def create_cat_type_user(db: Session, cat_data: CatTypeUserCreate):
    new_cat = CatTypeUser(**cat_data.dict())
    db.add(new_cat)
    db.commit()
    db.refresh(new_cat)
    return new_cat

# Get (todos)
def get_all_cat_type_users(db: Session):
    return db.query(CatTypeUser).all()

# Get (por ID)
def get_cat_type_user_by_id(db: Session, cat_id: int):
    return db.query(CatTypeUser).filter(CatTypeUser.id == cat_id).first()

# Upddate
def update_cat_type_user(db: Session, cat_id: int, update_data: CatTypeUserUpdate):
    cat = db.query(CatTypeUser).filter(CatTypeUser.id == cat_id).first()
    if not cat:
        return None
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(cat, key, value)
    db.commit()
    db.refresh(cat)
    return cat

# Delete
def delete_cat_type_user(db: Session, cat_id: int):
    cat = db.query(CatTypeUser).filter(CatTypeUser.id == cat_id).first()
    if not cat:
        return None
    db.delete(cat)
    db.commit()
    return cat

# Crear usuario
def create_user(db: Session, user_data: UserCreate):
    new_user = User(**user_data.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Obtener todos los usuarios
def get_all_users(db: Session):
    return db.query(User).all()

# Obtener usuario por ID
def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

# Actualizar usuario
def update_user(db: Session, user_id: int, update_data: UserUpdate):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

# Eliminar usuario
def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    db.delete(user)
    db.commit()
    return user