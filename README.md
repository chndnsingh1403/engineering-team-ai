# Engineering Team AI 🚀

A comprehensive AI-powered engineering team that can design, code, test, and document complete software projects. Built with React TypeScript frontend and Python FastAPI backend.

![Engineering Team AI](https://img.shields.io/badge/AI-Engineering%20Team-blue) ![React](https://img.shields.io/badge/React-18.2.0-61dafb) ![TypeScript](https://img.shields.io/badge/TypeScript-5.0-3178c6) ![Python](https://img.shields.io/badge/Python-3.12+-3776ab) ![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688)

## ✨ Features

### 🤖 AI Engineering Team
- **🎯 Lead Agent**: Creates system design and architecture documents
- **💻 Frontend Agent**: Develops modern React/TypeScript applications  
- **🔧 Backend Agent**: Builds robust APIs (FastAPI, Node.js, etc.)
- **🧪 Test Agent**: Creates comprehensive test suites
- **📚 Documentation Agent**: Writes complete project documentation

### 🎨 Modern Frontend
- **React 18** with TypeScript
- **Tailwind CSS** for beautiful, responsive styling
- **Real-time updates** via WebSockets and polling
- **File upload** support for requirements
- **Voice input** for project descriptions
- **ChatGPT-style interface** with progress tracking
- **Download** generated projects as ZIP files

### ⚡ Powerful Backend
- **FastAPI** with async support
- **WebSocket** real-time communication
- **Multi-agent orchestration** system
- **File generation** and project packaging
- **Flexible LLM integration** (OpenAI, Gemini, Anthropic, Ollama)
- **Mock mode** for development and demos

## 🏗️ Project Structure

```
EngineeringTeam/
├── 📁 frontend/              # React TypeScript frontend
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   ├── pages/           # Main application pages
│   │   ├── services/        # API integration
│   │   └── types/           # TypeScript definitions
│   ├── public/              # Static assets
│   ├── package.json         # Frontend dependencies
│   └── vite.config.ts       # Vite configuration
├── 📁 backend/              # Python FastAPI backend
│   ├── agents/              # AI agents for different tasks
│   │   ├── base_agent.py    # Base agent class with LLM integration
│   │   ├── lead_agent.py    # System design & architecture
│   │   ├── frontend_dev_agent.py # Frontend development
│   │   ├── backend_dev_agent.py  # Backend development
│   │   ├── test_dev_agent.py     # Test creation
│   │   └── documentation_agent.py # Documentation writing
│   ├── output/              # Generated project files
│   ├── uploads/             # User uploaded files
│   ├── main.py              # FastAPI application entry point
│   ├── orchestrator.py      # Agent coordination and workflow
│   ├── models.py            # Pydantic data models
│   ├── config.py            # Configuration management
│   ├── requirements.txt     # Python dependencies
│   └── .env                 # Environment variables (create from .env.example)
├── .env.example             # Sample environment configuration
├── start.sh                 # Quick start script
└── README.md               # This documentation
```

## 🚀 Quick Start

### Prerequisites
- **Node.js** 18+ and npm
- **Python** 3.12+ and pip
- **LLM API Key** (OpenAI, Gemini, or Anthropic)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd EngineeringTeam
```

### 2. Environment Setup
```bash
# Copy the sample environment file
cp .env.example backend/.env

# Edit the .env file with your API key
nano backend/.env
```

### 3. Backend Setup
```bash
cd backend

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start backend server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Frontend Setup
```bash
# In a new terminal
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 5. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## ⚙️ Configuration

### Environment Variables
Configure your LLM provider in `backend/.env`:

#### For OpenAI:
```env
LLM_PROVIDER=openai
LLM_MODEL=gpt-4-turbo-preview
LLM_API_KEY=your_openai_api_key
LLM_BASE_URL=https://api.openai.com/v1
MOCK_MODE=false
```

#### For Google Gemini:
```env
LLM_PROVIDER=gemini
LLM_MODEL=gemini-2.0-flash
LLM_API_KEY=your_gemini_api_key
LLM_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
MOCK_MODE=false
```

#### For Anthropic Claude:
```env
LLM_PROVIDER=anthropic
LLM_MODEL=claude-3-sonnet-20240229
LLM_API_KEY=your_anthropic_api_key
LLM_BASE_URL=https://api.anthropic.com/v1
MOCK_MODE=false
```

#### For Demo/Development:
```env
MOCK_MODE=true  # Uses mock responses, no API calls
```

## 📖 Usage Guide

### 1. Submit a Project
1. Open the frontend at http://localhost:3000
2. Enter a detailed project description
3. Select your preferred programming language
4. Optionally upload requirement files
5. Click "Start Engineering" 🚀

### 2. Monitor Progress
- **Real-time updates** show agent progress
- **Live activity logs** display current tasks
- **Progress indicators** track completion
- **Connection status** shows update mechanism

### 3. Download Results
- Once complete, download the generated project as a ZIP file
- Includes all source code, tests, and documentation
- Ready-to-run project structure

### Example Project Descriptions
```
📱 Mobile App: "Create a React Native todo app with user authentication, 
task categories, push notifications, and offline sync"

🌐 Web Application: "Build a full-stack e-commerce platform with React 
frontend, Node.js backend, payment integration, and admin dashboard"

🔧 API Service: "Develop a REST API for a blog platform with user management, 
post CRUD operations, comments, and search functionality"

🎮 Game: "Create a web-based puzzle game with levels, scoring, 
leaderboards, and responsive design"
```
- Language selection for projects

### Robust Backend
- FastAPI with async support
- OpenAI GPT-4 integration
- Real-time WebSocket updates
- File upload and processing
- Project ZIP generation
- Comprehensive error handling

### Generated Output
- Complete, working applications
- Comprehensive test suites
- Full documentation (README, API docs, user guides)
- Deployment guides
- Project ZIP downloads

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+
- OpenAI API key

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

4. **Start the backend:**
   ```bash
   python main.py
   ```

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```

### Access the Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Usage

1. **Open the frontend** in your browser
2. **Describe your project** in detail in the text area
3. **Select the programming language** for your project
4. **Upload any additional files** (optional) like requirements or specifications
5. **Click "Start Engineering"** to begin the process
6. **Watch the agents work** in real-time through the status updates
7. **Download your complete project** once processing is finished

## Environment Configuration

### Backend (.env)
```env
OPENAI_API_KEY=your_openai_api_key_here
HOST=localhost
PORT=8000
DEBUG=True
CORS_ORIGINS=http://localhost:3000
MAX_FILE_SIZE=10485760
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000
```

## Supported Languages

- JavaScript/TypeScript (React + Node.js/Express)
- Python (FastAPI + Streamlit)
- Java (Spring Boot)
- C# (ASP.NET Core)
- Go (Gin framework)
- PHP (Laravel)
- Ruby (Ruby on Rails)
- And more...

## AI Agents Workflow

1. **Lead Agent** analyzes the project description and creates:
   - System design document
   - Architecture diagrams
   - Implementation roadmap
   - Technology recommendations

2. **Frontend Agent** develops:
   - Modern UI components
   - Responsive layouts
   - API integration
   - State management
   - User interactions

3. **Backend Agent** creates:
   - REST APIs
   - Database models
   - Business logic
   - Authentication
   - File handling

4. **Test Agent** generates:
   - Unit tests
   - Integration tests
   - End-to-end tests
   - Test configuration
   - Testing documentation

5. **Documentation Agent** writes:
   - README files
   - API documentation
   - User guides
   - Developer setup guides
   - Deployment instructions

## Generated Project Structure

Each generated project includes:
- Complete source code (frontend + backend)
- Comprehensive test suites
- Full documentation
- Configuration files
- Deployment scripts
- README and setup instructions

## API Endpoints

- `POST /api/projects/submit` - Submit new project
- `GET /api/projects/{id}/status` - Get project status
- `GET /api/projects/{id}/output` - Get generated files
- `GET /api/projects/{id}/download` - Download project ZIP
- `WS /ws/{id}` - Real-time updates

## Development

### Adding New Agents

1. Create a new agent class inheriting from `BaseAgent`
2. Implement the `execute` method
3. Add the agent to the orchestrator
4. Update the frontend to display the new agent

### Customizing Output

Agents can be customized by modifying their prompts and execution logic in the respective agent files.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues, feature requests, or questions:
- Open an issue on GitHub
- Check the documentation in the `docs/` folder
- Review the API documentation at `/docs`

## Architecture

The system uses a multi-agent architecture where each agent specializes in a specific aspect of software development:

- **Orchestrator**: Coordinates agents and manages project workflow
- **WebSocket System**: Provides real-time updates to the frontend
- **File Management**: Handles uploads, processing, and ZIP generation
- **OpenAI Integration**: Powers all AI agents with GPT-4

The frontend provides a modern, responsive interface for interacting with the engineering team, while the backend manages the complex orchestration of multiple AI agents working together to create complete software projects.
