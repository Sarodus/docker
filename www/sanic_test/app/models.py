from sqlalchemy import Column, String, Integer, Sequence
from app.db import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    name = Column(String(50))
    username = Column(String(50))
    email = Column(String(50))
    password = Column(String(12))

    def __repr__(self):
        return '<User%r>' % self.serialize()

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "email": self.email,
            "password": self.password,
        }