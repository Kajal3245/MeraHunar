from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ai_gemini import ask_gemini
from worker_profile import create_worker_profile
from database import create_tables, get_connection, get_all_workers
from contractor_search import search_workers
from job_matching import match_workers_to_job


app = FastAPI(title="Mera Hunar")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables when server starts
create_tables()


@app.get("/")
def home():
    return {
        "message": "Mera Hunar AI System is running!"
    }


@app.get("/test-ai")
def test_ai():
    answer = ask_gemini(
        "Explain Mera Hunar in one simple sentence."
    )

    return {
        "ai_response": answer
    }


@app.post("/create-worker-profile")
def create_profile(worker_statement: str):

    profile = create_worker_profile(worker_statement)

    skills_text = ", ".join(profile.skills)

    connection = get_connection()

    worker_count = connection.execute(
        "SELECT COUNT(*) FROM workers"
    ).fetchone()[0]

    worker_id = f"MH{worker_count + 1:03d}"

    connection.execute(
        """
        INSERT INTO workers
        (
            worker_id,
            name,
            occupation,
            experience_years,
            skills,
            preferred_location,
            phone,
            availability,
            verification_status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            worker_id,
            profile.name,
            profile.occupation,
            profile.experience_years,
            skills_text,
            profile.preferred_location,
            "",
            "Available",
            "Worker Reported"
        )
    )

    connection.commit()
    connection.close()

    return {
        "message": "Worker profile created successfully",
        "worker_id": worker_id,
        "profile": profile.model_dump()
    }
@app.get("/search-workers")
def search_worker_profiles(
    occupation: str = None,
    location: str = None,
    min_experience: float = None
):
    workers = search_workers(
        occupation=occupation,
        location=location,
        min_experience=min_experience
    )

    return {
        "total_matches": len(workers),
        "workers": workers
    }
@app.get("/all-workers")
def all_workers():
    return {
        "workers": get_all_workers()
    }
@app.get("/all-jobs")
def all_jobs():
    connection = get_connection()

    jobs = connection.execute(
        "SELECT * FROM jobs WHERE status = 'Open' ORDER BY id DESC"
    ).fetchall()

    connection.close()

    return {
        "total_jobs": len(jobs),
        "jobs": [dict(job) for job in jobs]
    }
@app.post("/create-job")
def create_job(
    contractor_name: str,
    required_occupation: str,
    required_skills: str,
    location: str,
    min_experience: float,
    job_description: str
):
    connection = get_connection()

    # Generate Job ID
    job_count = connection.execute(
        "SELECT COUNT(*) FROM jobs"
    ).fetchone()[0]

    job_id = f"JOB{job_count + 1:03d}"

    # Save job
    connection.execute(
        """
        INSERT INTO jobs
        (
            job_id,
            contractor_name,
            required_occupation,
            required_skills,
            location,
            min_experience,
            job_description,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            job_id,
            contractor_name,
            required_occupation,
            required_skills,
            location,
            min_experience,
            job_description,
            "Open"
        )
    )

    connection.commit()
    connection.close()

    return {
        "message": "Job created successfully",
        "job_id": job_id,
        "status": "Open"
    }
@app.get("/match-job/{job_id}")
def match_job(job_id: str):
    result = match_workers_to_job(job_id)

    if "error" in result:
        return result

    return result
@app.post("/apply-job")
def apply_for_job(job_id: str, worker_id: str):

    connection = get_connection()

    # Check whether the job exists
    job = connection.execute(
        "SELECT * FROM jobs WHERE job_id = ?",
        (job_id,)
    ).fetchone()

    if not job:
        connection.close()
        return {"error": "Job not found"}

    # Check whether the worker exists
    worker = connection.execute(
        "SELECT * FROM workers WHERE worker_id = ?",
        (worker_id,)
    ).fetchone()

    if not worker:
        connection.close()
        return {"error": "Worker not found"}

    # Check if worker already applied
    existing = connection.execute(
        """
        SELECT * FROM job_applications
        WHERE job_id = ? AND worker_id = ?
        """,
        (job_id, worker_id)
    ).fetchone()

    if existing:
        connection.close()
        return {
            "message": "You have already shown interest in this job.",
            "status": "Already Interested"
        }

    # Save the application
    connection.execute(
        """
        INSERT INTO job_applications
        (job_id, worker_id, status)
        VALUES (?, ?, ?)
        """,
        (job_id, worker_id, "Interested")
    )

    connection.commit()
    connection.close()

    return {
        "message": "Your interest has been successfully recorded.",
        "job_id": job_id,
        "worker_id": worker_id,
        "status": "Interested"
    }
@app.get("/job-applications/{job_id}")
def get_job_applications(job_id: str):

    connection = get_connection()

    applications = connection.execute(
        """
        SELECT
            ja.job_id,
            ja.worker_id,
            ja.status,
            ja.created_at,
            w.name,
            w.occupation,
            w.experience_years,
            w.skills,
            w.preferred_location,
            w.availability,
            w.verification_status
        FROM job_applications ja
        JOIN workers w
            ON ja.worker_id = w.worker_id
        WHERE ja.job_id = ?
        ORDER BY ja.created_at DESC
        """,
        (job_id,)
    ).fetchall()

    connection.close()

    return {
        "job_id": job_id,
        "total_applications": len(applications),
        "applications": [dict(application) for application in applications]
    }