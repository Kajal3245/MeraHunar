from ai_gemini import llm
from database import get_connection


def calculate_match_score(worker, job):
    score = 0

    # 1. Occupation match — 30 points
    if worker["occupation"] and job["required_occupation"]:
        if worker["occupation"].lower() == job["required_occupation"].strip().lower():
            score += 30

    # 2. Location match — 20 points
    if worker["preferred_location"] and job["location"]:
        if worker["preferred_location"].lower() == job["location"].strip().lower():
            score += 20

    # 3. Experience match — 20 points
    if worker["experience_years"] >= job["min_experience"]:
        score += 20

    # 4. Skills match — 20 points
    worker_skills = worker["skills"].lower()
    required_skills = job["required_skills"].lower()

    required_skill_list = [
        skill.strip()
        for skill in required_skills.split(",")
        if skill.strip()
    ]

    matched_skills = 0

    for skill in required_skill_list:
        if skill in worker_skills:
            matched_skills += 1

    if required_skill_list:
        skill_score = (matched_skills / len(required_skill_list)) * 20
        score += skill_score

    # 5. Availability — 10 points
    if worker["availability"].lower() == "available":
        score += 10

    return round(score, 2)


def ai_match_explanation(worker, job):

    prompt = f"""
You are an AI worker-job matching assistant for Mera Hunar.

Your task is to evaluate whether this worker is suitable for this job.

WORKER:
Name: {worker["name"]}
Occupation: {worker["occupation"]}
Experience: {worker["experience_years"]} years
Skills: {worker["skills"]}
Preferred Location: {worker["preferred_location"]}
Availability: {worker["availability"]}

JOB:
Contractor: {job["contractor_name"]}
Required Occupation: {job["required_occupation"]}
Required Skills: {job["required_skills"]}
Location: {job["location"]}
Minimum Experience: {job["min_experience"]} years
Description: {job["job_description"]}

Give your answer in exactly this format:

AI_MATCH_SCORE: <number from 0 to 100>

REASON:
<2-3 simple sentences explaining why the worker is or is not suitable>

Rules:
- Consider occupation.
- Consider required skills.
- Consider experience.
- Consider location.
- Consider availability.
- Do not invent information.
"""

    response = llm.invoke(prompt)

    return response.content


def match_workers_to_job(job_id):

    connection = get_connection()

    # Get job
    job = connection.execute(
        "SELECT * FROM jobs WHERE job_id = ?",
        (job_id,)
    ).fetchone()

    if not job:
        connection.close()
        return {
            "error": "Job not found"
        }

    # Get all workers
    workers = connection.execute(
        "SELECT * FROM workers"
    ).fetchall()

    connection.close()

    matches = []

    for worker in workers:

        # Only consider available workers
        if worker["availability"].lower() != "available":
            continue

        # Calculate rule-based score
        score = calculate_match_score(worker, job)

        # Get AI analysis
        ai_result = ai_match_explanation(worker, job)

        # Extract AI score
        ai_score = 0

        for line in ai_result.splitlines():

            if line.startswith("AI_MATCH_SCORE:"):

                try:
                    ai_score = float(
                        line.replace("AI_MATCH_SCORE:", "").strip()
                    )

                except ValueError:
                    ai_score = 0

        # Calculate final score
        final_score = round(
            (score * 0.5) + (ai_score * 0.5),
            2
        )

        # Add worker to matches
        matches.append({
            "worker_id": worker["worker_id"],
            "name": worker["name"],
            "occupation": worker["occupation"],
            "experience_years": worker["experience_years"],
            "skills": worker["skills"],
            "preferred_location": worker["preferred_location"],
            "rule_score": score,
            "ai_score": ai_score,
            "final_match_score": final_score,
            "ai_analysis": ai_result
        })

    # Highest final score first
    matches.sort(
        key=lambda x: x["final_match_score"],
        reverse=True
    )

    return {
        "job_id": job["job_id"],
        "contractor_name": job["contractor_name"],
        "required_occupation": job["required_occupation"],
        "location": job["location"],
        "matches": matches
    }