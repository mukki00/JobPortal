from db.connection import connect
from db.queries.SQL_QUERIES import (sql_get_all_jobs, sql_get_job_count, sql_mark_job_as_applied, sql_get_all_applied_jobs,
                                    sql_mark_job_as_expired, sql_mark_job_as_retired, sql_get_all_rejected_and_expired_jobs,
                                    sql_get_available_job_count)

def get_all_jobs(offset=0, per_page=50, job_category=None):
    conn = connect()
    try:
        cursor = conn.cursor()
        if job_category:
            cursor.execute(sql_get_all_jobs(job_category), {"offset": offset, "per_page": per_page, "job_category": job_category})
        else:
            cursor.execute(sql_get_all_jobs(None), {"offset": offset, "per_page": per_page})
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        jobs = []
        for row in rows:
            job = {}
            for col, val in zip(columns, row):
                if hasattr(val, 'read'):
                    job[col] = val.read()
                elif str(type(val)).endswith("LOB'>"):
                    job[col] = str(val)
                else:
                    job[col] = val
            jobs.append(job)
    except Exception as e:
        print("Error fetching jobs:", e)
        jobs = []
    finally:
        conn.close()
    return jobs

def get_jobs_count(job_category):
    conn = connect()
    cursor = conn.cursor()
    if job_category:
        cursor.execute(sql_get_job_count(job_category), {"job_category": job_category})
    else:
        cursor.execute(sql_get_job_count(job_category))
    rows = cursor.fetchall()
    conn.close()
    return rows[0][0]

def get_available_jobs_count_from_db(job_category):
    conn = connect()
    cursor = conn.cursor()
    if job_category:
        cursor.execute(sql_get_available_job_count(job_category), {"job_category": job_category})
    else:
        cursor.execute(sql_get_available_job_count(job_category))
    rows = cursor.fetchall()
    conn.close()
    return rows[0][0]

def mark_job_as_applied(job_id, applied_status):
    conn = connect()
    cursor = conn.cursor()
    try:
        cursor.execute(sql_mark_job_as_applied(), {"job_id": job_id, "applied_status": applied_status})
        conn.commit()
        return cursor.rowcount  # Number of rows updated
    except Exception as e:
        print("Error marking job as applied:", e)
        return 0
    finally:
        conn.close()

def mark_job_as_expired(job_id, expired_status):
    conn = connect()
    cursor = conn.cursor()
    try:
        cursor.execute(sql_mark_job_as_expired(), {"job_id": job_id, "expired_status": expired_status})
        conn.commit()
        return cursor.rowcount  # Number of rows updated
    except Exception as e:
        print("Error marking job as expired:", e)
        return 0
    finally:
        conn.close()

def mark_job_as_rejected(job_id, rejected_status):
    conn = connect()
    cursor = conn.cursor()
    try:
        cursor.execute(sql_mark_job_as_retired(), {"job_id": job_id, "rejected_status": rejected_status})
        conn.commit()
        return cursor.rowcount  # Number of rows updated
    except Exception as e:
        print("Error marking job as rejected:", e)
        return 0
    finally:
        conn.close()

def get_applied_jobs_from_db(offset, per_page, job_category):
    conn = connect()
    try:
        cursor = conn.cursor()
        if job_category:
            cursor.execute(sql_get_all_applied_jobs(job_category),
                           {"offset": offset, "per_page": per_page, "job_category": job_category})
        else:
            cursor.execute(sql_get_all_applied_jobs(None), {"offset": offset, "per_page": per_page})
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        jobs = []
        for row in rows:
            job = {}
            for col, val in zip(columns, row):
                if hasattr(val, 'read'):
                    job[col] = val.read()
                elif str(type(val)).endswith("LOB'>"):
                    job[col] = str(val)
                else:
                    job[col] = val
            jobs.append(job)
    except Exception as e:
        print("Error fetching jobs:", e)
        jobs = []
    finally:
        conn.close()
    return jobs

def get_expired_and_rejected_jobs(offset, per_page, job_category):
    conn = connect()
    try:
        cursor = conn.cursor()
        cursor.execute(sql_get_all_rejected_and_expired_jobs(job_category),
                       {"offset": offset, "per_page": per_page, "job_category": job_category})
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        jobs = []
        for row in rows:
            job = {}
            for col, val in zip(columns, row):
                if hasattr(val, 'read'):
                    job[col] = val.read()
                elif str(type(val)).endswith("LOB'>"):
                    job[col] = str(val)
                else:
                    job[col] = val
            jobs.append(job)
    except Exception as e:
        print("Error fetching expired and rejected jobs:", e)
        jobs = []
    finally:
        conn.close()
    return jobs
