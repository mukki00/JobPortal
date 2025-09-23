def sql_get_job_count(job_category=None):
    if job_category:
        return "SELECT count(*) FROM JOB_POST WHERE JOB_CATEGORY = :job_category"
    else:
        return "SELECT count(*) FROM JOB_POST"

def sql_get_all_jobs(job_category=None):
    if job_category:
        return  """
                SELECT
                JOB_ID, JOB_TITLE, COMPANY, COMPANY_LOCATION, JOB_LINK, JOB_TYPE, LINKEDIN_VERIFIED, JOB_CATEGORY, APPLIED, JOB_SOURCE
                FROM JOB_POST
                WHERE JOB_CATEGORY = :job_category
                ORDER BY JOB_ID OFFSET :offset ROWS FETCH NEXT :per_page ROWS ONLY
                """
    else:
        return  """
                SELECT
                JOB_ID, JOB_TITLE, COMPANY, COMPANY_LOCATION, JOB_LINK, JOB_TYPE, LINKEDIN_VERIFIED, JOB_CATEGORY, APPLIED, JOB_SOURCE
                FROM JOB_POST
                ORDER BY JOB_ID OFFSET :offset ROWS FETCH NEXT :per_page ROWS ONLY
                """
