from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, text

load_dotenv()  # loads values from .env

db_url = os.environ.get("DATABASE_URL")
ca_cert_path = os.environ.get("CA_CERT_PATH")


# Create SQLAlchemy engine with SSL
engine = create_engine(
    db_url,
    connect_args={"ssl_ca": ca_cert_path}
)

def load_jobs_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM jobs"))
        jobs = [dict(row._mapping) for row in result]
    return jobs
