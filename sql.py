from flask_sqlalchemy import SQLAlchemy 
from flask_user import  UserMixin
import datetime

def load_db(app, key=""):
    db = SQLAlchemy(app)
    
        # Define the Role data-model
    class Role(db.Model):
        __tablename__ = 'roles'
        id = db.Column(db.Integer(), primary_key=True)
        name = db.Column(db.String(50), unique=True)

        def __repr__(self):
            return '<Role %r>' % self.name   
               
    class User(db.Model,UserMixin):
        __tablename__ = 'users'
        id = db.Column(db.Integer, primary_key=True)
        username  = db.Column(db.String(80), unique=True)
        password =  db.Column(db.String(200), nullable=False)
        role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
        role = db.relationship(Role)
        
        def __repr__(self):
            return '<User %r>' % self.username  
        
        def has_roles(self, value):
            return self.role.name == value 
        
    class GitlabKey(db.Model):
        __tablename__ = 'gitlabkey'
        id = db.Column(db.Integer, primary_key=True)
        private_key = db.Column(db.String, nullable=False)
        title = db.Column(db.String, nullable=False, unique=True)
        created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
        update_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id',ondelete='CASCADE'))
                
    class GitlabRepo(db.Model):
        __tablename__ = 'gitlabrepo'
        
        id = db.Column(db.Integer, primary_key=True)
        active = db.Column(db.Boolean, unique=False, default=False) 
        url = db.Column(db.String, nullable=False, unique=True)
        title = db.Column(db.String, nullable=False, unique=True)
        created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
        update_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id',ondelete='CASCADE'))
        key_id = db.Column(db.Integer, db.ForeignKey('gitlabkey.id'))
        key = db.relationship(GitlabKey)
           
        
    class Device(db.Model):
        __tablename__ = 'devices'
        
        id = db.Column(db.Integer, primary_key=True)
        onie_id = db.Column(db.String(80),  unique=True)
        image_name = db.Column(db.String(200), nullable=False)
        created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
        last_update = db.Column(db.DateTime, default=datetime.datetime.utcnow)
        template= db.Column(db.String(80), nullable=True)
        hostvars= db.Column(db.String(80), nullable=True)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id',ondelete='CASCADE'))
        user = db.relationship(User)
    
        @property
        def serialize(self):
    
            return {
                'db_id': self.id,
                'onie_id': self.onie_id,
                'image_name': self.image_name,
                'creator': self.user.username,
                'created_date': self.created_date,
                'template': self.template,
            }
    
        def __repr__(self):
            return '<Device %r>' % self.onie_id
    
    if key == "device_table":
        return(db,Device)
    
    return(db,User,Device,Role,GitlabKey,GitlabRepo)
