from flask import Blueprint ,request , jsonify
from app import db
from app.models import Job , Note


jobs_bp = Blueprint('jobs',__name__,url_prefix='/jobs')

# Get All Jobs for a user
@jobs_bp.route('/',methods=['GET'])
def get_jobs():
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({'Error':'user_id is required'}),400
    
    jobs = Job.query.filter_by(user_id=user_id).all()
    return jsonify([job.to_dict() for job in jobs]),200

#Post Create a new Job
@jobs_bp.route('/',methods=['POST'])
def create_job():
    data = request.get_json()
    
    if not data or not data.get('company') or not data.get('role') or not data.get('user_id'):
        return jsonify({'error':'company, role and user_id are required'}),400
    new_job = Job(
        company = data['company'],
        role = data['role'],
        status=data.get('status','applied'),
        user_id = data.get('user_id')
    )
    db.session.add(new_job)
    db.session.commit()
    
    return jsonify(new_job.to_dict()),201

# Put Update Job
@jobs_bp.route('/<int:job_id>',methods=['PUT'])
def update_job(job_id):
    job= Job.query.get_or_404(job_id)
    data = request.get_json()
    
    job.company = data.get('company', job.company)
    job.role =data.get('role',job.role)
    job.status = data.get('status',job.status)
    
    db.session.commit()
    
    return jsonify(job.to_dict()),200

# DELETE a Job
@jobs_bp.route('/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    return jsonify({'message':'job deleted successfully'}),200

#GET stats for user
@jobs_bp.route('/stats',methods=['GET'])
def get_stats():
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({'error':'user_id is required'})
    
    total = Job.query.filter_by(user_id= user_id).count()
    applied = Job.query.filter_by(user_id=user_id, status='applied').count()
    interview = Job.query.filter_by(user_id=user_id, status ='interview').count()
    offer = Job.query.filter_by(user_id=user_id , status ='offer').count()
    rejected = Job.query.filter_by(user_id=user_id , status="rejected").count()
    
    return jsonify({
        'total': total,
        'applied': applied,
        "interview": interview,
        'offer' : offer,
        'rejected':rejected
    }),200
    
    
    