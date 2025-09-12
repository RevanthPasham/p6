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

# Create SQLAlchemy engine without SSL connect_args to avoid errors
engine = create_engine(db_url)

def load_jobs_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM jobs"))
        jobs = [dict(row._mapping) for row in result]
    return jobs
