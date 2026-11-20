from database import get_connection


def search_workers(
    occupation=None,
    location=None,
    min_experience=None
):
    connection = get_connection()

    query = """
        SELECT
            worker_id,
            name,
            occupation,
            experience_years,
            skills,
            preferred_location,
            availability,
            verification_status
        FROM workers
        WHERE 1=1
    """

    parameters = []

    if occupation:
        query += " AND LOWER(occupation) LIKE LOWER(?)"
        parameters.append(f"%{occupation}%")

    if location:
        query += " AND LOWER(preferred_location) LIKE LOWER(?)"
        parameters.append(f"%{location}%")

    if min_experience is not None:
        query += " AND experience_years >= ?"
        parameters.append(min_experience)

    query += " ORDER BY experience_years DESC"

    workers = connection.execute(
        query,
        parameters
    ).fetchall()

    connection.close()

    return [dict(worker) for worker in workers]