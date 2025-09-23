from flask import Blueprint, jsonify, request
from db.connection import connect
from service.getData import get_all_jobs, get_jobs_count

job_controller = Blueprint('job_controller', __name__)

# Example endpoint: Home
@job_controller.route('/')
def home():
    return jsonify({"message": "Welcome to the Job Portal!"})

# Example endpoint: Get all jobs with pagination
@job_controller.route('/jobs', methods=['GET'])
def get_jobs():
    # Get pagination params from query string, with defaults
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 50))
    offset = (page - 1) * per_page
    job_category = request.args.get('job_category', None)
    print(job_category, flush=True)
    try:
        # Only pass job_category if it has a value, else pass None
        jobs = get_all_jobs(offset, per_page, job_category if job_category else None)
        total = get_jobs_count(job_category if job_category else None)
        return jsonify({
            'jobs': jobs,
            'page': page,
            'per_page': per_page,
            'total': total
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get jobs count
@job_controller.route('/count', methods=['GET'])
def get_job_count():
    conn = connect()
    try:
        count = get_jobs_count()
        return jsonify({'count': count})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

# Example endpoint: Add a new job
@job_controller.route('/jobs', methods=['POST'])
def add_job():
    data = request.get_json()
    return jsonify({"message": "Job added successfully!", "job": data}), 201

# Example endpoint: Get job by ID
@job_controller.route('/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    job = {"id": job_id, "title": "Software Engineer", "company": "TechCorp"}
    return jsonify(job)

# Example endpoint: Delete a job
@job_controller.route('/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    return jsonify({"message": f"Job with ID {job_id} deleted successfully!"})