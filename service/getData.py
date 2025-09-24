from db.connection import connect
from db.queries.SQL_QUERIES import sql_get_all_jobs, sql_get_job_count

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
