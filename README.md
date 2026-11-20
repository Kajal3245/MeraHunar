# 🛠️ Mera Hunar

**AI-powered platform connecting skilled workers with suitable job opportunities.**

Mera Hunar is a full-stack platform designed to help skilled workers create simple digital profiles and discover relevant job opportunities, while contractors can create jobs and find workers based on occupation, skills, experience, and location.

## 🚀 Features

### 👷 Worker
- Create a worker profile using natural-language input
- Extract occupation, experience, skills, and preferred location
- Search for suitable job opportunities
- Apply for available jobs

### 🏗️ Contractor
- Create job requirements
- Specify required occupation, skills, location, and experience
- Find suitable workers for a job
- View workers who have applied

### 🤖 AI Integration
- Uses Google Gemini for AI-assisted profile processing
- Converts natural-language worker information into structured profile data
- Includes a local fallback for profile processing

### 🔧 Backend
- REST APIs built with FastAPI
- SQLite database for storing workers, jobs, and applications
- Worker-job matching based on job requirements

## 🏗️ Tech Stack

| Layer | Technologies |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, FastAPI |
| AI | Google Gemini |
| Database | SQLite |
| API | REST API |
| Development | Git, GitHub, VS Code |

## 📁 Project Structure

```text
MeraHunar/
│
├── backend/
│   ├── main.py
│   ├── ai_gemini.py
│   ├── database.py
│   ├── contractor_search.py
│   ├── job_matching.py
│   ├── worker_profile.py
│   └── requirements.txt
│
├── dashboard/
│   ├── dashboard.html
│   ├── worker.html
│   └── employer.html
│
├── README.md
└── .gitignore
```

## 🔄 How It Works

```text
Worker
   ↓
Natural-language information
   ↓
AI-assisted profile creation
   ↓
Structured worker profile
   ↓
Job matching
   ↓
Relevant job opportunities
```

For contractors:

```text
Contractor
   ↓
Create job requirements
   ↓
Occupation + Skills + Experience + Location
   ↓
Worker matching
   ↓
Suitable workers
```

## ▶️ Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/Kajal3245/MeraHunar.git
cd MeraHunar
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

Windows:

```powershell
venv\Scripts\activate
```

### 3. Install dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file inside the `backend` directory and add your Gemini API configuration.

**Never commit API keys or `.env` files to GitHub.**

### 5. Start the backend

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

## 📌 Current Status

Mera Hunar is currently available as a working prototype with:

- Worker profile creation
- Job creation
- Worker-job matching
- Job applications
- Contractor worker search
- AI-assisted profile processing
- FastAPI REST APIs
- Web-based worker and contractor dashboards

## 🔮 Future Improvements

Possible future improvements include:

- Persistent production database
- Authentication and authorization
- Worker verification
- Location-based matching
- Improved ranking of candidates
- Production deployment
- Mobile-friendly interface

## 👩‍💻 Author
