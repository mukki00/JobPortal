from flask import Blueprint, jsonify, request
from db.connection import connect
from service.getData import (get_all_jobs, get_jobs_count, mark_job_as_applied, get_applied_jobs_from_db,
                             mark_job_as_expired, mark_job_as_rejected, get_expired_and_rejected_jobs,
                             get_available_jobs_count_from_db, get_applied_jobs_count_from_db, get_inactive_jobs_count_from_db)

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
        total = get_available_jobs_count_from_db(job_category if job_category else None)
        return jsonify({
            'jobs': jobs,
            'page': page,
            'per_page': per_page,
            'total': total
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get available jobs count
@job_controller.route('/available/count', methods=['GET'])
def get_available_jobs_count():
    job_category = request.args.get('job_category', None)
    conn = connect()
    try:
        count = get_available_jobs_count_from_db(job_category)
        return jsonify({'count': count})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@job_controller.route('/applied/count', methods=['GET'])
def get_applied_jobs_count():
    job_category = request.args.get('job_category', None)
    conn = connect()
    try:
        count = get_applied_jobs_count_from_db(job_category)
        return jsonify({'count': count})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@job_controller.route('/inactive/count', methods=['GET'])
def get_inactive_jobs_count():
    job_category = request.args.get('job_category', None)
    conn = connect()
    try:
        count = get_inactive_jobs_count_from_db(job_category)
        return jsonify({'count': count})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get jobs count
@job_controller.route('/count', methods=['GET'])
def get_job_count():
    job_category = request.args.get('job_category', None)
    conn = connect()
    try:
        count = get_jobs_count(job_category)
        return jsonify({'count': count})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

# Example endpoint: Update job as applied
@job_controller.route('/jobs/<int:job_id>/apply', methods=['PUT'])
def update_mark_applied(job_id):
    data = request.get_json()
    applied_status = data.get('applied', 'Y')
    affected_row_count = mark_job_as_applied(job_id, applied_status)
    if affected_row_count == 0:
        return jsonify({"message": f"No job found with ID {job_id} or already marked as applied."}), 404
    else:
        return jsonify({"message": "Job added successfully!", "job": data, "job_id": job_id}), 201

# Example endpoint: Update job as expired
@job_controller.route('/jobs/<int:job_id>/expire', methods=['PUT'])
def update_mark_expired(job_id):
    data = request.get_json()
    expired_status = data.get('expired', 'Y')
    affected_row_count = mark_job_as_expired(job_id, expired_status)
    if affected_row_count == 0:
        return jsonify({"message": f"No job found with ID {job_id} or already marked as expired."}), 404
    else:
        return jsonify({"message": "expired status updated successfully!", "job": data, "job_id": job_id}), 201

# Example endpoint: Update job as rejected
@job_controller.route('/jobs/<int:job_id>/reject', methods=['PUT'])
def update_mark_rejected(job_id):
    data = request.get_json()
    rejected_status = data.get('rejected', 'Y')
    affected_row_count = mark_job_as_rejected(job_id, rejected_status)
    if affected_row_count == 0:
        return jsonify({"message": f"No job found with ID {job_id} or already marked as rejected."}), 404
    else:
        return jsonify({"message": "Job rejected successfully!", "job": data, "job_id": job_id}), 201

# Example endpoint: Get applied jobs by ID
@job_controller.route('/jobs/apply', methods=['GET'])
def get_applied_jobs():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 50))
    offset = (page - 1) * per_page
    job_category = request.args.get('job_category', None)
    print(job_category, flush=True)
    try:
        applied_jobs = get_applied_jobs_from_db(offset, per_page, job_category if job_category else None)
        applied_jobs = [applied_job for applied_job in applied_jobs if applied_job.get('APPLIED') == 'Y']
        total = get_applied_jobs_count_from_db(job_category if job_category else None)
        return jsonify({
            'jobs': applied_jobs,
            'page': page,
            'per_page': per_page,
            'total': total
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Example endpoint: Get rejected or expired jobs by ID
@job_controller.route('/jobs/rejected-expired', methods=['GET'])
def get_rejected_or_expired_jobs():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 50))
    offset = (page - 1) * per_page
    job_category = request.args.get('job_category', None)
    print(job_category, flush=True)
    try:
        rejected_and_expired_jobs = get_expired_and_rejected_jobs(offset, per_page, job_category if job_category else None)
        total = get_inactive_jobs_count_from_db(job_category if job_category else None)
        return jsonify({
            'jobs': rejected_and_expired_jobs,
            'page': page,
            'per_page': per_page,
            'total': total
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500