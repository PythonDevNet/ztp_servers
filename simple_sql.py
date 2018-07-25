from sqlalchemy import create_engine, desc,  Column, ForeignKey, Integer, String,DateTime,Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
import datetime, os 

APP_HOME = os.getcwd()
SQLDB = 'sqlite:///'+os.path.join(APP_HOME,'../database/database.db')
engine = create_engine(SQLDB)
DBSession = sessionmaker(bind = engine)
session = DBSession()

Base = declarative_base()

class Device(Base):
    __tablename__ = 'device'

    id = Column(String(250),primary_key=True, nullable=False)
    image = Column(String(250), nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

def get_all():
    return session.query(Device).all()

def get_deviceID(id):
    id = str(id).strip()
    try:
        print('searching db for %s ...' % id)
        device = session.query(Device).filter_by(id=id).one()
        return device
    except:
        return None
