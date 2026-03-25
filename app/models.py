from app import db
from datetime import datetime


class User(db.Model):
    __tablename__= 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True , nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime , default=datetime.utcnow)
    
    # One user has may jobs applications
    jobs = db.relationship('Job',backref='user',lazy=True)
    
    def __repr__(self):
        return f'<User {self.email}>'
    
class Job(db.Model):
    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key= True)
    company = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100) , nullable=False)
    status = db.Column(db.String(50), default='applied')
    date_applied = db.Column(db.DateTime , default = datetime.utcnow)
    user_id= db.Column(db.Integer,db.ForeignKey('users.id'), nullable=False)
    
    # one Job has many notes
    notes =db.relationship('Note',backref='job', lazy=True)
    
    def __repr__(self):
        return f'<Job {self.company} - {self.role}>'
    
    def to_dict(self):
        return{
            'id':self.id,
            'company':self.company,
            'role':self.role,
            'status':self.status,
            'date_applied':self.date_applied.isoformat(),
        }
        
class Note(db.Model):
    __tablename__='notes'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text , nullable=False)
    created_at = db.Column(db.DateTime ,default = datetime.utcnow)
    job_id = db.Column(db.Integer , db.ForeignKey('jobs.id'), nullable=False)
    
    def __repr__(self):
        return f'<Note {self.id}>'
    
    def to_dict(self):
        return{
            'id': self.id,
            'content':self.content,
            'created_at':self.created_at.isoformat(),
            'job_id':self.job_id
        }