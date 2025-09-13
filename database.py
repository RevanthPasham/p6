from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, text

load_dotenv()  # loads values from .env

db_url = os.environ.get("DATABASE_URL")
ca_cert_path = os.environ.get("CA_CERT_PATH")

if not db_url:
    import warnings
    warnings.warn("DATABASE_URL environment variable is not set. Using default SQLite database for deployment/testing.")
    db_url = "sqlite:///./test.db"
    ca_cert_path = None

# Create SQLAlchemy engine
engine = create_engine(db_url)

print("Connecting to database at:", db_url)

def load_jobs_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM jobs"))
        jobs = [dict(row._mapping) for row in result]
    return jobs

def load_job_from_db(id):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM jobs WHERE id=:val"), {"val": id})
        rows = result.all()
        if len(rows) == 0:
            return None
        return dict(rows[0]._mapping)

def add_application_to_db(job_id, data):
    with engine.begin() as conn:  # begin() ensures commit/rollback
        query = text("""
            INSERT INTO job_applications (job_id, full_name, email, linkedin_url, education, experience)
            VALUES (:job_id, :full_name, :email, :linkedin_url, :education, :experience)
        """)
        conn.execute(query, {
            "job_id": job_id,
            "full_name": data["full_name"],
            "email": data["email"],
            "linkedin_url": data["linkedin_url"],
            "education": data["education"],
            "experience": data["experience"]
        })
