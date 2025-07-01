# 🚀 LinkedIn Sourcing Agent

An intelligent AI-powered LinkedIn candidate sourcing, scoring, and outreach generation system built with Python, FastAPI, and Groq API. This project automates the entire recruitment pipeline from finding candidates to generating personalized outreach messages.
## Demo Video
https://www.loom.com/share/10203068087242bba62e1a873da0aee9?sid=0619fcd6-34bb-4fce-a5c6-2af18e67f41f
## ✨ Features

### 🔍 **Smart Candidate Search**
- **Google Programmable Search Engine (PSE)** integration for real LinkedIn profile discovery
- **AI-powered profile analysis** using Groq/Llama models for enhanced data extraction
- **Fallback to static data** when API credentials are unavailable
- **Configurable search results** (10-30 profiles)
- **Fast search mode** without AI analysis for quick results

### 📊 **Advanced Scoring System**
- **Comprehensive scoring rubric** with 6 key dimensions:
  - **Education (20%)**: Elite schools (MIT, Stanford, etc.): 9-10, Strong schools: 7-8, Standard universities: 5-6
  - **Career Trajectory (20%)**: Steady growth: 6-8, Limited progression: 3-5
  - **Company Relevance (15%)**: Top tech companies: 9-10, Relevant industry: 7-8, Any experience: 5-6
  - **Experience Match (25%)**: Perfect skill match: 9-10, Strong overlap: 7-8, Some relevant skills: 5-6
  - **Location Match (10%)**: Exact city: 10, Same metro: 8, Remote-friendly: 6
  - **Tenure (10%)**: 2-3 years average: 9-10, 1-2 years: 6-8, Job hopping: 3-5
- **AI-enhanced scoring** for top candidates using Groq/Llama
- **Performance optimized** with pre-compiled regex patterns
- **Detailed score breakdown** for each category

### 💬 **Personalized Outreach Generation**
- **AI-generated personalized messages** based on candidate profile and job description
- **Context-aware content** that references specific skills, experience, and background
- **Professional tone** with proper formatting
- **Copy-to-clipboard functionality** for easy use

### 🎨 **Modern Web Interface**
- **Responsive design** that works on desktop and mobile
- **Elegant UI** with glass morphism effects and smooth animations
- **Real-time feedback** with loading states and success/error messages
- **Interactive candidate cards** with detailed scoring breakdown
- **Clean, professional appearance** with modern typography and color scheme

### ⚡ **Performance Optimizations**
- **Hybrid scoring approach**: Fast basic scoring for all candidates, AI enhancement for top 5
- **Efficient API usage** with proper error handling and fallbacks
- **Optimized search queries** with intelligent keyword extraction
- **Caching and pre-compilation** for better performance

## 📁 Project Structure

```
synapse_project/
├── 📄 README.md                           # Project documentation
├── 🐍 main.py                             # Basic CLI version
├── 🐍 agent.py                            # Core LinkedIn search agent
├── 🐍 scoring.py                          # Basic scoring system
├── 🐍 outreach.py                         # Basic outreach generation
├── 🐍 enhanced_scoring.py                 # Advanced scoring with AI
├── 🐍 enhanced_outreach.py                # AI-powered outreach generation
├── 🐍 groq_agent.py                       # Enhanced agent with Groq integration
├── 🧪 test_scoring.py                     # Scoring system test script
├── 📁 backend/
│   ├── 🐍 main.py                         # Basic FastAPI backend
│   └── 🐍 enhanced_main.py                # Enhanced FastAPI backend with all features
├── 📁 frontend/
│   └── 📄 index.html                      # Modern web interface
├── 📁 senv/                               # Python virtual environment
└── 📄 requirements.txt                    # Python dependencies
```

## 🔧 File Descriptions

### **Core Files**

| File | Purpose |
|------|---------|
| `main.py` | Basic CLI version for testing the pipeline |
| `agent.py` | Core LinkedIn search functionality with Google PSE |
| `scoring.py` | Basic scoring system with keyword matching |
| `outreach.py` | Basic outreach message generation |

### **Enhanced Files**

| File | Purpose |
|------|---------|
| `enhanced_scoring.py` | Advanced scoring with AI integration and performance optimizations |
| `enhanced_outreach.py` | AI-powered personalized outreach generation |
| `groq_agent.py` | Enhanced agent with Groq API for AI analysis |
| `test_scoring.py` | Test script to demonstrate scoring capabilities |

### **Backend Files**

| File | Purpose |
|------|---------|
| `backend/main.py` | Basic FastAPI server with core endpoints |
| `backend/enhanced_main.py` | Full-featured FastAPI server with all endpoints |

### **Frontend Files**

| File | Purpose |
|------|---------|
| `frontend/index.html` | Complete web interface with modern design |

## 🚀 Quick Start

### **Prerequisites**
- Python 3.8+
- Google Programmable Search Engine API key
- Groq API key (optional, for enhanced features)

### **Installation**

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd synapse_project
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv senv
   source senv/bin/activate  # On Windows: senv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the root directory:
   ```env
   GOOGLE_API_KEY=your_google_api_key
   GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id
   GROQ_API_KEY=your_groq_api_key
   ```

### **Running the Application**

#### **Option 1: Enhanced Web Interface (Recommended)**
```bash
cd backend
python enhanced_main.py
```
Then open `http://localhost:8000/frontend` in your browser.

#### **Option 2: Basic Web Interface**
```bash
cd backend
python main.py
```
Then open `http://localhost:8000/frontend` in your browser.

#### **Option 3: CLI Version**
```bash
python main.py
```

#### **Option 4: Test Scoring System**
```bash
python test_scoring.py
```

## 🎯 Usage Guide

### **Web Interface**

1. **Enter Job Description**: Paste your job description in the text area
2. **Select Profile Count**: Choose how many candidates to search (10-30)
3. **Choose Search Mode**:
   - **Run Full Pipeline**: Complete search → score → outreach generation
   - **Search Only**: Just find and display candidates
   - **Fast Search**: Quick search without AI analysis

### **API Endpoints**

#### **Enhanced Backend (`/enhanced_main.py`)**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API health check |
| `/frontend` | GET | Serve web interface |
| `/search` | POST | Search candidates with AI analysis |
| `/search-fast` | POST | Fast search without AI |
| `/score` | POST | Score candidates with AI enhancement |
| `/score-fast` | POST | Fast scoring without AI |
| `/outreach` | POST | Generate outreach messages |
| `/full-pipeline` | POST | Complete pipeline execution |
| `/health` | GET | System health status |

#### **Basic Backend (`/main.py`)**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API health check |
| `/frontend` | GET | Serve web interface |
| `/search` | POST | Basic candidate search |
| `/score` | POST | Basic candidate scoring |
| `/outreach` | POST | Basic outreach generation |
| `/full-pipeline` | POST | Complete basic pipeline |

### **Example API Usage**

```bash
# Search candidates
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"description": "Software Engineer role", "profile_count": 15}'

# Full pipeline
curl -X POST "http://localhost:8000/full-pipeline" \
  -H "Content-Type: application/json" \
  -d '{"description": "ML Engineer role", "profile_count": 20}'
```

## 🔑 API Configuration

### **Google Programmable Search Engine**

1. Go to [Google Programmable Search Engine](https://programmablesearchengine.google.com/)
2. Create a new search engine
3. Configure it to search LinkedIn profiles
4. Get your API key and Search Engine ID
5. Add to `.env` file

### **Groq API (Optional)**

1. Sign up at [Groq](https://console.groq.com/)
2. Get your API key
3. Add to `.env` file for enhanced AI features

## 🎨 UI Features

### **Design Highlights**
- **Glass morphism effects** with backdrop blur
- **Smooth animations** with cubic-bezier transitions
- **Responsive grid layouts** that adapt to screen size
- **Modern typography** using Inter font family
- **Gradient backgrounds** and elegant color scheme
- **Interactive hover effects** and visual feedback

### **User Experience**
- **Progressive disclosure**: Results only show after search
- **Loading states** with elegant spinners
- **Error handling** with user-friendly messages
- **Copy-to-clipboard** functionality for outreach messages
- **Mobile-responsive** design for all devices

## 🔧 Technical Details

### **Scoring Algorithm**

The scoring system uses a weighted approach across 6 dimensions:

```python
total_score = (
    education_score * 0.20 +
    trajectory_score * 0.20 +
    company_score * 0.15 +
    experience_score * 0.25 +
    location_score * 0.10 +
    tenure_score * 0.10
)
```

### **Performance Optimizations**

- **Pre-compiled regex patterns** for faster text processing
- **Set-based lookups** for school and company matching
- **Hybrid AI approach**: Basic scoring for all, AI enhancement for top candidates
- **Efficient API usage** with proper error handling

### **Data Flow**

1. **Search**: Google PSE → LinkedIn profiles → AI analysis (optional)
2. **Scoring**: Profile data → Basic scoring → AI enhancement (top 5)
3. **Outreach**: Scored candidates → AI-generated personalized messages

## 🐛 Troubleshooting

### **Common Issues**

1. **"Google API credentials not found"**
   - Check your `.env` file has correct API keys
   - Verify Google PSE is configured for LinkedIn

2. **"Groq API key not found"**
   - Add GROQ_API_KEY to `.env` file
   - System will fall back to basic scoring

3. **No search results**
   - Check internet connection
   - Verify Google PSE configuration
   - System will show static data as fallback

4. **Slow performance**
   - Use "Fast Search" mode
   - Reduce profile count
   - Check API rate limits

### **Debug Mode**

Enable debug logging by setting environment variable:
```bash
export DEBUG=1
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Google Programmable Search Engine** for LinkedIn profile discovery
- **Groq** for AI-powered analysis and generation
- **FastAPI** for the modern web framework
- **FontAwesome** for the beautiful icons

---

**Built with ❤️ for modern recruitment teams** 
