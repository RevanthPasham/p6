from flask import Flask, render_template, jsonify, request
from database import load_jobs_from_db, load_job_from_db, add_application_to_db

app = Flask(__name__)

@app.route("/")
def hello_jovian():
    jobs = load_jobs_from_db()
    return render_template("home.html",
                           jobs=jobs,
                           company_name="Jovian")

@app.route("/api/jobs")
def list_jobs():
    jobs = load_jobs_from_db()
    return jsonify(jobs)

@app.route("/jobs/<id>")
def show_jobs(id):
    print(f"Route hit with id={id}")
    job = load_job_from_db(id)
    if job is None:
        return "Job not found", 404
    return render_template("job.html", job=job)

@app.route("/job/<id>/apply", methods=["POST"])
def apply_to_job(id):
    data = request.form
    job = load_job_from_db(id)
    if job is None:
        return "Job not found", 404

    add_application_to_db(id, data)

    return render_template("application_submited.html",
                           application=data,
                           job=job)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
