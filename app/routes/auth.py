from flask import Blueprint , request , jsonify
from app import db
from app.models import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
auth_bp= Blueprint('auth',__name__,url_prefix='/auth')

@auth_bp.route('/register',methods=['POST'])
def register():
    data = request.get_json()
    
    # validate incoming data
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error':'email and password are required'}),400
    
    # check if email already exists
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'error':'email already registered'}),409
    
    # Hash the password
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    
    #Create new user
    new_user= User(
        email=data['email'],
        password = hashed_password
    )
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message':'user created successfully'}),201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Validate incoming data
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error':'email and password are required'}),400
    
    # find user by email
    user = User.query.filter_by(email=data['email']).first()
    
    # Check user exists and password matches
    if not user or not bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({'error':'invalid email or password'}),401
    
    return jsonify({'message':'logged in successfully', 'user_id':user.id}),200

@auth_bp.route('/logout',methods=['POST'])
def logout():
    return jsonify({'message':'logged out successfully'}),200
    


