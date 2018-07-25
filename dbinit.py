from flask_sqlalchemy import SQLAlchemy
import hashlib, binascii
from flask import Flask
from sql import load_db

app = Flask(__name__)
app.config.from_object('default_settings')

(db,User,Device,Role,GitlabKey,GitlabRepo) = load_db(app)

db.drop_all()
db.create_all()
    
def hash_password(plain_psw, salt):
    dk = hashlib.pbkdf2_hmac('sha256', plain_psw, salt , 100000)
    return  binascii.hexlify(dk)

if not Role.query.filter_by(name='Admin').first():
    admin_role = Role(name='Admin')
    db.session.add(admin_role)
    db.session.commit()

if not Role.query.filter_by(name='User').first():
    user_role = Role(name='User')
    db.session.add(user_role)
    db.session.commit()
    
if not Role.query.filter_by(name='Guest').first():
    user_role = Role(name='Guest')
    db.session.add(user_role)
    db.session.commit()


if not User.query.filter(User.username.ilike('admin')).first():
    role = Role.query.filter_by(name='Admin').first()
    admin = User(username='admin',password=hash_password('admin',app.config['SALT']),role=role)
    db.session.add(admin)
    db.session.commit()

if not User.query.filter(User.username.ilike('guest')).first():
    role = Role.query.filter_by(name = 'Guest').first()
    guest = User(username='guest',password=hash_password('admin',app.config['SALT']),role=role)
    db.session.add(guest)
    db.session.commit()



