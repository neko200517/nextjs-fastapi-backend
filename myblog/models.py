from sqlalchemy import Column, String, DateTime, Integer

from database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(String, primary_key=True, index=True)

    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    publisher = Column(String, nullable=False)
    category = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)


if __name__ == "__main__":
    print("test")
