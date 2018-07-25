from sqlalchemy import Column, ForeignKey, Integer, String,DateTime,Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine 
from flask_login import UserMixin
import datetime

SQLDB = 'sqlite:///database.db'

Base = declarative_base()

class User(Base,UserMixin):
    __tablename__ = 'user'
    id  =  Column(String(250), primary_key=True,  nullable=False)
    psw =  Column(String, nullable=False)


class Device(Base):
    __tablename__ = 'device'

    id = Column(String(250),primary_key=True, nullable=False)
    image = Column(String(250), nullable=False)
    template = Column(String(250), nullable=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    user_name = Column(Integer,ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):

        return {
            'id': self.id,
            'image': self.image,
            'creator': self.user_name,
            'created_date': self.created_date,
            'template': self.template,
            'image': self.images,
        }


engine = create_engine(SQLDB)
Base.metadata.create_all(engine)
