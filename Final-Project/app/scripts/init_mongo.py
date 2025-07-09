from pymongo import MongoClient, ASCENDING, errors
from pymongo.errors import CollectionInvalid, OperationFailure
from typing import Dict, Any


#   DEFINICIONES DE JSON SCHEMA

def _json_schema_for_follower() -> Dict[str, Any]:
    return {
        "bsonType": "object",
        "required": [
            "follower_user_id",
            "followed_user_id",
            "status",
            "date_begin_follow",
        ],
        "properties": {
            "follower_user_id": {"bsonType": "int", "minimum": 1},
            "followed_user_id": {"bsonType": "int", "minimum": 1},
            "status": {"enum": ["ON", "OFF"]},
            "date_begin_follow": {"bsonType": "date"},
        },
        "additionalProperties": False,
    }

def _json_schema_for_comment() -> Dict[str, Any]:
    return {
        "bsonType": "object",
        "required": ["text_comment", "post_id", "user_id", "date_comment"],
        "properties": {
            "text_comment": {"bsonType": "string", "minLength": 1, "maxLength": 800},
            "post_id": {"bsonType": "int", "minimum": 1},
            "user_id": {"bsonType": "int", "minimum": 1},
            "multimedia_ids": {
                "bsonType": ["array"],
                "items": {"bsonType": "int", "minimum": 1},
            },
            "date_comment": {"bsonType": "date"},
        },
        "additionalProperties": False,
    }


def _json_schema_for_reaction() -> Dict[str, Any]:

    return {
        "bsonType": "object",
        "required": ["user_id", "cat_reaction_id", "date_reaction"],
        "properties": {
            "user_id": {"bsonType": "int", "minimum": 1},
            "post_id": {"bsonType": ["int", "null"], "minimum": 1},
            "comment_id": {"bsonType": ["int", "null"], "minimum": 1},
            "cat_reaction_id": {"bsonType": "int", "minimum": 1},
            "date_reaction": {"bsonType": "date"},
        },
        "additionalProperties": False,
    }


def _json_schema_for_hist_post() -> Dict[str, Any]:
    return {
        "bsonType": "object",
        "required": ["post_id", "date_modificate", "text_version", "status"],
        "properties": {
            "post_id": {"bsonType": "int", "minimum": 1},
            "date_modificate": {"bsonType": "date"},
            "text_version": {"bsonType": "string", "maxLength": 800},
            "status": {"enum": ["EDIT", "DEL"]},
            "date_create": {"bsonType": ["date", "null"]},
        },
        "additionalProperties": False,
    }


def _json_schema_for_hist_comment() -> Dict[str, Any]:
    schema = _json_schema_for_hist_post().copy()
    # cambiar post_id → comment_id
    schema["required"][0] = "comment_id"
    schema["properties"]["comment_id"] = schema["properties"].pop("post_id")
    return schema


# Diccionario de <colección>: <jsonSchema>
_VALIDATORS: Dict[str, Dict[str, Any]] = {
    "follower": _json_schema_for_follower(),
    "comment": _json_schema_for_comment(),
    "reaction": _json_schema_for_reaction(),
    "historical_post": _json_schema_for_hist_post(),
    "historical_comment": _json_schema_for_hist_comment(),
}

#   FUNCIÓN PÚBLICA

def init_collections(db):
    # Colecciones + validadores
    for coll_name, schema in _VALIDATORS.items():
        try:
            db.create_collection(
                coll_name,
                validator={"$jsonSchema": schema},
                validationLevel="strict",
            )
            print(f"✓ Colección creada: {coll_name}")
        except CollectionInvalid:
            print(f"ℹ La colección '{coll_name}' ya existe.")
            try:
                db.command(
                    "collMod",
                    coll_name,
                    validator={"$jsonSchema": schema},
                    validationLevel="strict",
                )
                print(f"✓ Validador actualizado para: {coll_name}")
            except OperationFailure as e:
                print(f"⚠ No se pudo aplicar el validador a '{coll_name}': {e.details.get('errmsg', str(e))}")

    # Índices
    db["follower"].create_index(
        [("follower_user_id", ASCENDING), ("followed_user_id", ASCENDING)],
        unique=True,
        name="uq_follower_pair",
    )

    db["comment"].create_index([("post_id", ASCENDING)], name="ix_comment_post")
    db["comment"].create_index([("user_id", ASCENDING)], name="ix_comment_user")

    db["reaction"].create_index(
        [("user_id", ASCENDING), ("post_id", ASCENDING), ("comment_id", ASCENDING)],
        unique=True,
        name="uq_reaction_once",
    )

    db["historical_post"].create_index(
        [("post_id", ASCENDING), ("date_modificate", ASCENDING)],
        name="ix_hist_post",
    )

    db["historical_comment"].create_index(
        [("comment_id", ASCENDING), ("date_modificate", ASCENDING)],
        name="ix_hist_comment",
    )

    print("✓ MongoDB listo")