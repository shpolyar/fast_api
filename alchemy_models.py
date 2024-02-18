from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

DATABASE_URL = "sqlite:///./fs.db"

# init session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Integer)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, index=True)
    password = Column(String)


Base.metadata.create_all(bind=engine)


def get_db():
    """
    Get the database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
