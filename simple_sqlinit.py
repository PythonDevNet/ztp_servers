from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, User,Device
import hashlib, binascii

SQLDB = 'sqlite:///database.db'
engine = create_engine(SQLDB)
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

session.query(User).all()


def encrypt_psw(plain_psw):
    SALT = "s|\xaa\xe8qw0\x9eaI\x05>l\xe8\x13\x1c\xf2\xcb\xa1J\x12\x18\xe4a\xfa\xef"
    dk = hashlib.pbkdf2_hmac('sha256', plain_psw, SALT , 100000)
    return  binascii.hexlify(dk)

# Create dummy user
psw = encrypt_psw("admin")
user = User(id="admin",psw=psw)
session.add(user)
session.commit()


# Create dummy devicez
newdevice = Device( id='14:02:ec:2d:f0:00'.upper(), image='onie-installer-arm-HPE_AL_6900-picos-2.9.2.5-30f7332.bin', user_name='admin')
session.add(newdevice)
session.commit()

newdevice = Device( id='14:02:ec:2d:e0:80'.upper(), image='onie-installer-arm-HPE_AL_6900-picos-2.9.2.5-30f7332.bin', user_name='admin')
session.add(newdevice)
session.commit()

newdevice = Device( id='8c:ea:1b:20:cb:c0'.upper(), image='onie-installer-arm-accton_as4610-picos-2.9.2.5-30f7332.bin', user_name='admin')
session.add(newdevice)
session.commit()

newdevice = Device( id='8c:ea:1b:20:c9:c0'.upper(), image='onie-installer-arm-accton_as4610-picos-2.9.2.5-30f7332.bin', user_name='admin')
session.add(newdevice)
session.commit()

newdevice = Device( id='dell_s4000_c2338'.upper(), image='onie-installer-x86-DELL_S4048-ON-picos-2.9.2.5-30f7332.bin', user_name='admin')
session.add(newdevice)
session.commit()
session.close()
