def sql_get_job_count(job_category=None):
    if job_category:
        return "SELECT count(*) FROM JOB_POST WHERE JOB_CATEGORY = :job_category"
    else:
        return "SELECT count(*) FROM JOB_POST"

def sql_get_available_job_count(job_category=None):
    if job_category:
        return "SELECT count(*) FROM JOB_POST WHERE JOB_CATEGORY = :job_category and APPLIED = 'N' and (EXPIRED = 'N' and REJECTED = 'N')"
    else:
        return "SELECT count(*) FROM JOB_POST WHERE APPLIED = 'N' and (EXPIRED = 'N' and REJECTED = 'N')"

def sql_get_all_jobs(job_category=None):
    if job_category:
        return  """
                SELECT
                JOB_ID, JOB_TITLE, COMPANY, COMPANY_LOCATION, JOB_LINK, JOB_TYPE, LINKEDIN_VERIFIED, JOB_CATEGORY, APPLIED, JOB_SOURCE,
                EXPIRED, REJECTED
                FROM JOB_POST
                WHERE JOB_CATEGORY = :job_category
                AND APPLIED = 'N'
                ORDER BY JOB_ID OFFSET :offset ROWS FETCH NEXT :per_page ROWS ONLY
                """
    else:
        return  """
                SELECT
                JOB_ID, JOB_TITLE, COMPANY, COMPANY_LOCATION, JOB_LINK, JOB_TYPE, LINKEDIN_VERIFIED, JOB_CATEGORY, APPLIED, JOB_SOURCE,
                EXPIRED, REJECTED
                FROM JOB_POST
                WHERE APPLIED = 'N'
                ORDER BY JOB_ID OFFSET :offset ROWS FETCH NEXT :per_page ROWS ONLY
                """

def sql_get_all_applied_jobs(job_category=None):
    if job_category:
        return  """
                SELECT
                JOB_ID, JOB_TITLE, COMPANY, COMPANY_LOCATION, JOB_LINK, JOB_TYPE, LINKEDIN_VERIFIED, JOB_CATEGORY, APPLIED, JOB_SOURCE,
                EXPIRED, REJECTED
                FROM JOB_POST
                WHERE JOB_CATEGORY = :job_category
                AND APPLIED = 'Y'
                ORDER BY JOB_ID OFFSET :offset ROWS FETCH NEXT :per_page ROWS ONLY
                """
    else:
        return  """
                SELECT
                JOB_ID, JOB_TITLE, COMPANY, COMPANY_LOCATION, JOB_LINK, JOB_TYPE, LINKEDIN_VERIFIED, JOB_CATEGORY, APPLIED, JOB_SOURCE,
                EXPIRED, REJECTED
                FROM JOB_POST
                WHERE APPLIED = 'Y'
                ORDER BY JOB_ID OFFSET :offset ROWS FETCH NEXT :per_page ROWS ONLY
                """

def sql_get_all_rejected_and_expired_jobs(job_category=None):
    if job_category:
        return  """
                SELECT
                JOB_ID, JOB_TITLE, COMPANY, COMPANY_LOCATION, JOB_LINK, JOB_TYPE, LINKEDIN_VERIFIED, JOB_CATEGORY, APPLIED, JOB_SOURCE,
                EXPIRED, REJECTED
                FROM JOB_POST
                WHERE JOB_CATEGORY = :job_category
                AND (EXPIRED = 'Y' OR REJECTED = 'Y')
                ORDER BY JOB_ID OFFSET :offset ROWS FETCH NEXT :per_page ROWS ONLY
                """
    else:
        return  """
                SELECT
                JOB_ID, JOB_TITLE, COMPANY, COMPANY_LOCATION, JOB_LINK, JOB_TYPE, LINKEDIN_VERIFIED, JOB_CATEGORY, APPLIED, JOB_SOURCE,
                EXPIRED, REJECTED
                FROM JOB_POST
                WHERE EXPIRED = 'Y' AND REJECTED = 'Y'
                ORDER BY JOB_ID OFFSET :offset ROWS FETCH NEXT :per_page ROWS ONLY
                """

def sql_mark_job_as_applied():
    return """
           UPDATE JOB_POST
           SET APPLIED = :applied_status
           WHERE JOB_ID = :job_id
           """

def sql_mark_job_as_expired():
    return """
           UPDATE JOB_POST
           SET EXPIRED = :expired_status
           WHERE JOB_ID = :job_id
           """
def sql_mark_job_as_retired():
    return """
           UPDATE JOB_POST
           SET REJECTED = :rejected_status
           WHERE JOB_ID = :job_id
           """