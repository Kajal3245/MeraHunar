
import os
import re
from typing import List

from pydantic import BaseModel, Field


class WorkerProfile(BaseModel):
    name: str = Field(default="Not provided")
    occupation: str = Field(default="Not specified")
    experience_years: float = Field(default=0)
    skills: List[str] = Field(default_factory=list)
    preferred_location: str = Field(default="Not specified")


def create_local_profile(statement: str):
    text = statement.strip()
    lower_text = text.lower()

    # Extract name if the worker mentions it.
    name = "Not provided"
    name_match = re.search(
        r"(?:my name is|mera naam)\s+([A-Za-z]+(?:\s+[A-Za-z]+)?)",
        text,
        re.IGNORECASE
    )
    if name_match:
        name = name_match.group(1).title()

    # Identify occupation.
    occupations = {
        "Mason": ["mason", "rajmistri", "raj mistri", "mistri"],
        "Electrician": ["electrician", "electrical"],
        "Plumber": ["plumber", "plumbing"],
        "Painter": ["painter", "painting"],
        "Carpenter": ["carpenter", "carpentry"],
        "Welder": ["welder", "welding"],
        "Driver": ["driver", "driving"],
        "Mechanic": ["mechanic"],
        "Tailor": ["tailor", "darzi"],
        "Cook": ["cook", "cooking"],
        "Cleaner": ["cleaner", "cleaning"],
        "Helper": ["helper", "mazdoor"]
    }

    occupation = "Not specified"

    for role, keywords in occupations.items():
        if any(word in lower_text for word in keywords):
            occupation = role
            break

    # Extract experience.
    experience = 0.0
    experience_match = re.search(
        r"(\d+(?:\.\d+)?)\s*(?:years?|yrs?|saal)",
        lower_text
    )

    if experience_match:
        experience = float(experience_match.group(1))

    # Extract skills.
    skill_keywords = {
        "Brick work": ["brick work", "brickwork"],
        "Plastering": ["plastering"],
        "Tile fitting": ["tile fitting"],
        "Wiring": ["wiring"],
        "Fan fitting": ["fan fitting"],
        "Pipe fitting": ["pipe fitting"],
        "Wall painting": ["wall painting"],
        "Putty application": ["putty"],
        "Carpentry": ["carpentry"],
        "Welding": ["welding"],
        "Driving": ["driving"]
    }

    skills = []

    for skill, keywords in skill_keywords.items():
        if any(word in lower_text for word in keywords):
            skills.append(skill)

    # Extract preferred location.
    location = "Not specified"

    hindi_location = re.search(
        r"\b([A-Z][A-Za-z-]+)\s+(?:mein|me)\b",
        text
    )

    english_location = re.search(
        r"\b(?:in|at|near)\s+([A-Za-z][A-Za-z-]*(?:\s+[A-Za-z][A-Za-z-]*)?)",
        text,
        re.IGNORECASE
    )

    if hindi_location:
        location = hindi_location.group(1).title()
    elif english_location:
        location = english_location.group(1).title()

    return WorkerProfile(
        name=name,
        occupation=occupation,
        experience_years=experience,
        skills=skills,
        preferred_location=location
    )


def create_worker_profile(worker_statement: str):

    # Keep Gemini disabled during development.
    # This avoids API quota and model availability problems.
    use_gemini = (
        os.getenv("MERAHUNAR_USE_GEMINI_PROFILE", "false").lower()
        == "true"
    )

    if use_gemini:
        try:
            from ai_gemini import llm

            structured_llm = llm.with_structured_output(WorkerProfile)

            prompt = f"""
            Extract a worker profile from this statement.

            Statement: {worker_statement}

            Extract only information actually provided.
            Do not invent a name, experience, skills or location.
            Convert Hindi and Hinglish into English.
            """

            return structured_llm.invoke(prompt)

        except Exception as error:
            print("Gemini unavailable. Using local profile extraction.")
            print("Gemini error:", str(error))

    return create_local_profile(worker_statement)
