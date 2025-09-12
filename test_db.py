from database import load_jobs_from_db

def test_load_jobs():
    try:
        jobs = load_jobs_from_db()
        print("Jobs loaded successfully:")
        for job in jobs:
            print(job)
    except Exception as e:
        print(f"Error loading jobs: {e}")

if __name__ == "__main__":
    test_load_jobs()
