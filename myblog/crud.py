import traceback
from sqlalchemy import extract, and_
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

# from . import models, schemas

import models
import schemas
import error_code


# カスタム例外モデル
class CustomException(Exception):
    def __init__(
        self,
        error_code: int = error_code.NETWORK_ERROR,
        message: str = "Network Error",
        log: str = "",
    ):
        self.error_code = error_code
        self.message = message
        self.log = log


# 記事一覧を取得する
def get_posts(db: Session, skip: int = 0, limit: int = 0):
    results = []
    try:
        results = db.query(models.Post).offset(skip).limit(limit).all()
    except:
        raise
    finally:
        db.close()

    return results


# 記事を取得する
def get_post(db: Session, id: str):
    return db.query(models.Post).filter(models.Post.id == id).first()


# 記事登録
def create_post(db: Session, post: schemas.PostCreate):
    db_post = None
    try:
        db_post = models.Post(
            id=post.id,
            title=post.title,
            content=post.content,
            publisher=post.publisher,
            category=post.category,
            image_url=post.image_url,
            created_at=post.created_at
            )
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
    except SQLAlchemyError as e:
        db.rollback()
        # TODO: 重複チェック
        # logの中にdupulicateという文字列が存在したら重複エラーそれ以外はネットワークエラー
        raise CustomException(
            error_code=error_code.ERROR_DUPULICATE_POST,
            message=error_code.ERROR_MESSAGES[error_code.ERROR_DUPULICATE_POST],
            log=traceback.format_exception_only(type(e), e)[0],
        )
    finally:
        db.close()

    return db_post


# 記事の削除
def delete_post(db: Session, id: str):
    try:
        db.query(models.Post).filter(models.Post.id == id).delete()
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()

    return []