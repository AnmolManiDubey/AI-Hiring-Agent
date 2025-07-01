# 🚀 LinkedIn AI Sourcing Agent

An AI-powered tool that automates the hiring pipeline — from sourcing LinkedIn profiles to scoring candidates and generating personalized outreach — using **FastAPI**, **Groq API**, and **Google Programmable Search**.

> ✅ **Frontend Live**: [ai-hiring-agent.vercel.app](https://ai-hiring-agent.vercel.app)
> ⚙️ **Backend API**: [Hugging Face Space](https://AMD8-Agent.hf.space)

## 🎥 Demo

▶️ [Watch on Loom](https://www.loom.com/share/10203068087242bba62e1a873da0aee9?sid=0619fcd6-34bb-4fce-a5c6-2af18e67f41f)

---

## 🧱 Tech Stack & APIs

### 🖥️ **Frontend**

* **HTML + CSS **: UI layout & styling
* **JavaScript**: Interactivity and API communication
* **Hosted on Vercel**

### ⚙️ **Backend**

* **FastAPI**: RESTful API development
* **Python**: Core logic, AI integration, data processing
* **Hosted on Hugging Face Spaces**

### 🤖 **AI & APIs**

* **Groq API** (with LLaMA 3-70B): Candidate analysis & message generation
* **Google Programmable Search Engine (PSE)**: Sourcing real LinkedIn profiles
* **OpenAI Compatible Interface** (optional future extension)

### 🧪 Dev Tools

* **venv**: Python virtual environment
* **Requests / httpx**: API communication
* **Regex + Sets**: Fast, rule-based scoring system
* **Environment Variables (`.env`)**: Secure API key management

---

## ✨ Key Features

### 🔍 Smart Candidate Search

* LinkedIn profile discovery using Google PSE
* Optional Groq/LLaMA-based AI profile analysis
* Fallback dummy data when APIs are unavailable
* Fast search mode for lightweight usage

### 📊 Intelligent Scoring

* Weighted rubric: education, experience, company, location, tenure, trajectory
* AI-enhanced scoring for top candidates
* Efficient pattern matching & regex optimization

### 💬 Personalized Outreach

* Groq API-based outreach message generation
* Customized, context-aware messages
* Copy-to-clipboard enabled

### 🖥️ Clean UI

* Modern, mobile-friendly design
* Real-time status indicators & error handling
* Animated cards, loading spinners, and smooth UX

---

## ⚙️ Hosted Deployment

| Component      | Link                                                                     |
| -------------- | ------------------------------------------------------------------------ |
| 🌐 Frontend    | [https://ai-hiring-agent.vercel.app](https://ai-hiring-agent.vercel.app) |
| ⚙️ Backend API | [https://AMD8-Agent.hf.space](https://AMD8-Agent.hf.space)               |
| 📦 API Docs    | [OpenAPI `/docs`](https://AMD8-Agent.hf.space/docs)                      |

---

## 🚀 Quick Start (Local)

### 1. Clone & Setup

```bash
git clone <repo-url>
cd synapse_project
python -m venv senv
source senv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment

`.env` file in root:

```env
GOOGLE_API_KEY=your_google_key
GOOGLE_SEARCH_ENGINE_ID=your_engine_id
GROQ_API_KEY=your_groq_key
```

### 3. Run Locally

```bash
cd backend
python enhanced_main.py
# Open http://localhost:8000/frontend
```

---

## 📡 API Endpoints

| Endpoint         | Method | Description                    |
| ---------------- | ------ | ------------------------------ |
| `/search`        | POST   | AI-powered candidate search    |
| `/score`         | POST   | Candidate scoring with AI      |
| `/outreach`      | POST   | Generate personalized outreach |
| `/full-pipeline` | POST   | End-to-end pipeline            |
| `/health`        | GET    | API health check               |

Open [API Docs](https://AMD8-Agent.hf.space/docs) for full details.

---

## 🧠 Data Flow

```
Job Description ➝ Search Candidates ➝ Score Profiles ➝ Generate Outreach
           ⬑─────────────── AI-enhanced via Groq & Google APIs ────────────────⬎
```
## 🧠 How It Works
1. Search: Google PSE → LinkedIn profiles → optional AI parsing

2. Score: Keyword + AI-based rubric scoring

3. Outreach: Personalized messaging using candidate-job match

---

## 🛠 Project Structure (Simplified)

```
synapse_project/
├── agent.py              # LinkedIn search logic
├── scoring.py            # Rule-based scoring
├── outreach.py           # Outreach generation
├── backend/              # FastAPI server (enhanced_main.py)
├── frontend/             # Web UI (served from Vercel)
├── requirements.txt      # Python dependencies
```

---

## 🙌 Contributing

1. Fork the repo
2. Create a feature branch
3. Submit a PR with clear commits

---

## 📄 License

This project is licensed under the [MIT License](./LICENSE).

---

**Built with ❤️ to accelerate technical hiring.**

---

Let me know if you’d like:

* A **badge section** (build passing, hosted on Vercel, etc.)
* A **GitHub project board**
* **User docs** (e.g. for recruiters using the web interface)
  and I can help you add that too.
