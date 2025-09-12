from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, text

load_dotenv()  # loads values from .env

db_url = os.environ.get("DATABASE_URL")
ca_cert_path = os.environ.get("CA_CERT_PATH")

if not db_url:
    raise ValueError("DATABASE_URL environment variable is not set. Please set it in your environment or .env file.")

# Create SQLAlchemy engine with SSL if ca_cert_path is set
if ca_cert_path:
    engine = create_engine(
        db_url,
        connect_args={"sslrootcert": ca_cert_path}
    )
else:
    engine = create_engine(db_url)

def load_jobs_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM jobs"))
        jobs = [dict(row._mapping) for row in result]
    return jobs
