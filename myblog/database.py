from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://root:root@localhost:5432/myblog"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def test():
    with engine.connect() as conn:
        conn.execute(text("CREATE TABLE test (x int, y int)"))
        conn.execute(
            text("INSERT INTO test (x, y) VALUES (:x, :y)"),
            [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
        )
        conn.close()


if __name__ == "__main__":
    test()
