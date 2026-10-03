from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.services.apploadconfig import config


database = config["database"]

DATABASE_URL = (
    f"mysql+pymysql://"
    f"{database['user']}:{database['password']}@"
    f"{database['host']}:{database['port']}/"
    f"{database['database']}"
)


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass