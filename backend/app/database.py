from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# DATABASE_URLを環境変数から取得
DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemyエンジンを作成
engine = create_engine(DATABASE_URL)

# セッションを作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# データベースモデルのベースクラス
Base = declarative_base()

# 依存性注入のための関数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
