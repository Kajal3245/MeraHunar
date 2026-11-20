import sqlite3

DATABASE_NAME = "merahunar.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def create_tables():
    connection = get_connection()

    # Workers table
    connection.execute("""
        CREATE TABLE IF NOT EXISTS workers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            worker_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            occupation TEXT,
            experience_years REAL,
            skills TEXT,
            preferred_location TEXT,
            phone TEXT,
            availability TEXT,
            verification_status TEXT
        )
    """)

    # Jobs table
    connection.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id TEXT UNIQUE NOT NULL,
            contractor_name TEXT,
            required_occupation TEXT,
            required_skills TEXT,
            location TEXT,
            min_experience REAL,
            job_description TEXT,
            status TEXT
        )
    """)
        # Job applications / worker interest table
    connection.execute("""
        CREATE TABLE IF NOT EXISTS job_applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id TEXT NOT NULL,
            worker_id TEXT NOT NULL,
            status TEXT DEFAULT 'Interested',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def get_all_workers():
    connection = get_connection()

    workers = connection.execute(
        "SELECT * FROM workers"
    ).fetchall()

    connection.close()

    return [dict(worker) for worker in workers]