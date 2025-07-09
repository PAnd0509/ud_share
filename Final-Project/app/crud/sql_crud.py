from sqlalchemy.orm import Session
from app.models.sql_models import CatTypeUser, User, UserAddData
from app.schemas.cat_type_user import CatTypeUserCreate, CatTypeUserUpdate, UserCreate, UserUpdate, UserAddDataCreate, UserAddDataUpdate

# -- Cat Type User --

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

# -- User --

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

# -- User Add Data --

# Crear
def create_user_add_data(db: Session, data: UserAddDataCreate):
    # Verificar si ya existe para ese usuario
    existing = db.query(UserAddData).filter(UserAddData.fk_user_id == data.fk_user_id).first()
    if existing:
        return None  # O lanzar excepción si prefieres
    new_data = UserAddData(**data.dict())
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return new_data

# Obtener por ID
def get_user_add_data_by_id(db: Session, record_id: int):
    return db.query(UserAddData).filter(UserAddData.id == record_id).first()

# Obtener por usuario
def get_user_add_data_by_user_id(db: Session, user_id: int):
    return db.query(UserAddData).filter(UserAddData.fk_user_id == user_id).first()

# Actualizar
def update_user_add_data(db: Session, record_id: int, update_data: UserAddDataUpdate):
    record = db.query(UserAddData).filter(UserAddData.id == record_id).first()
    if not record:
        return None
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(record, key, value)
    db.commit()
    db.refresh(record)
    return record

# Eliminar
def delete_user_add_data(db: Session, record_id: int):
    record = db.query(UserAddData).filter(UserAddData.id == record_id).first()
    if not record:
        return None
    db.delete(record)
    db.commit()
    return record