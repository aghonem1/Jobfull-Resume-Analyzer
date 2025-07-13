# Configuration Guide

## Overview

This guide covers the setup, configuration, and customization of the Jobfull Resume Analyzer system. The system is built with CrewAI framework and requires proper configuration of agents, tasks, and environment variables.

## 🚀 Initial Setup

### Prerequisites
- **Python**: 3.8 or higher
- **OpenAI API Key**: Required for GPT-4o-mini
- **Internet Connection**: For web scraping and search tools
- **PDF Resume**: Source document for analysis

### Installation Steps

1. **Clone Repository**
```bash
git clone https://github.com/aghonem1/Jobfull-Resume-Analyzer.git
cd Jobfull-Resume-Analyzer/cv_opt
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Environment Variables**
Create `.env` file:
```bash
OPENAI_API_KEY=your_openai_api_key_here
SERPER_API_KEY=your_serper_api_key_here  # Optional: for enhanced search
```

4. **Resume PDF Setup**
Place your resume PDF in the knowledge folder:
```bash
cv_opt/knowledge/your_resume.pdf
```

## ⚙️ Configuration Files

### Agent Configuration (`config/agents.yaml`)

#### Structure Overview
```yaml
agent_name:
  role: "Agent Role Title"
  goal: "Primary objective statement"
  backstory: >
    Detailed backstory explaining expertise,
    capabilities, and specialization areas.
```

#### Key Agent Roles

**Job Analyzer**
```yaml
job_analyzer:
  role: "ATS-Optimized Job Requirements Analyst"
  goal: "Analyze job descriptions, extract ATS keywords, and score candidate fit"
  backstory: >
    Expert in 2025 job market analysis and ATS optimization.
    Understands modern ATS systems (Workday, Greenhouse, Lever, iCIMS).
```

**Resume Analyzer**
```yaml
resume_analyzer:
  role: "ATS-Optimized Resume Expert & Format Compliance Specialist"
  goal: "Analyze resumes for ATS compatibility, format compliance, and keyword optimization"
  backstory: >
    2025 resume optimization specialist with expertise in ATS systems
    and format compliance requirements.
```

#### Customization Options
- **Role Titles**: Modify agent specialization focus
- **Goals**: Adjust primary objectives
- **Backstory**: Update expertise areas and capabilities
- **Industry Focus**: Customize for specific industries or roles

### Task Configuration (`config/tasks.yaml`)

#### Task Structure
```yaml
task_name:
  description: >
    Detailed task description with step-by-step process
  expected_output: >
    Expected output format and content requirements
  agent: agent_name
  context: [dependency_task_1, dependency_task_2]
```

#### Critical Task Elements

**Multi-Step Process**
```yaml
analyze_job_task:
  description: >
    **STEP 1: Job Requirements & ATS Analysis**
    - Extract requirements: technical skills, soft skills, experience
    - Identify ATS system type from job posting
    
    **STEP 2: Keyword Extraction & Prioritization**
    - Primary ATS keywords: Exact matches required
    - Secondary keywords: Contextual matches
```

**Context Dependencies**
```yaml
optimize_resume_task:
  context: [analyze_job_task]

research_company_task:
  context: [analyze_job_task, optimize_resume_task]
```

#### Customization Guidelines
- **Step Details**: Modify process steps for specific requirements
- **Output Expectations**: Adjust expected deliverable format
- **Context Flow**: Change task dependencies as needed
- **Agent Assignment**: Reassign tasks to different agents

## 🔧 System Configuration (`crew.py`)

### Core Setup

#### Knowledge Source Configuration
```python
def __init__(self) -> None:
    """Configure resume PDF knowledge source"""
    self.resume_pdf = PDFKnowledgeSource(file_paths="your_resume.pdf")
```

#### Agent Configuration
```python
@agent
def job_analyzer(self) -> Agent:
    return Agent(
        config=self.agents_config["job_analyzer"],
        verbose=True,
        tools=[ScrapeWebsiteTool()],  # Web scraping capability
        llm=LLM("gpt-4o-mini"),      # Language model
    )
```

#### Task Configuration
```python
@task
def analyze_job_task(self) -> Task:
    return Task(
        config=self.tasks_config["analyze_job_task"],
        output_file="output/job_analysis.json",          # Output location
        output_pydantic=JobRequirements,                 # Data model
    )
```

### Customization Options

#### LLM Configuration
```python
# Change language model
llm=LLM("gpt-4")           # Use GPT-4 instead
llm=LLM("gpt-3.5-turbo")   # Use GPT-3.5-turbo for cost savings
```

#### Tool Integration
```python
# Add additional tools
tools=[
    ScrapeWebsiteTool(),
    SerperDevTool(),
    FileReadTool(),
    # Custom tools
]
```

#### Output Configuration
```python
# Customize output locations
output_file="custom/path/job_analysis.json"

# Change data models
output_pydantic=CustomJobRequirements
```

## 📁 File Structure Configuration

### Required Directories
```
cv_opt/
├── src/cv_opt/
│   ├── config/
│   │   ├── agents.yaml     # Agent configurations
│   │   └── tasks.yaml      # Task configurations
│   ├── models.py           # Pydantic data models
│   ├── crew.py             # CrewAI orchestration
│   └── main.py             # Entry point
├── knowledge/
│   └── resume.pdf          # Source resume
└── output/                 # Generated files
```

### Output Directory Structure
```
output/
├── job_analysis.json              # Job requirements analysis
├── resume_optimization.json       # Resume improvement recommendations
├── company_research.json          # Company intelligence
├── cover_letter_analysis.json     # Cover letter analysis
├── cover_letter.md                # Generated cover letter
├── optimized_resume.md            # Optimized resume
└── final_report.md                # Executive report
```

## 🎯 Input Configuration

### Main Execution (`main.py`)
```python
def run():
    inputs = {
        "job_url": "https://company.com/careers/job-posting",
        "company_name": "Target Company Name",
    }
    ResumeCrew().crew().kickoff(inputs=inputs)
```

### Customizable Inputs
- **job_url**: Direct link to job posting
- **company_name**: Target company for research
- **Additional parameters**: Can be added for specific requirements

### Dynamic Configuration
```python
# Environment-based configuration
import os

def run():
    inputs = {
        "job_url": os.getenv("JOB_URL", "default_url"),
        "company_name": os.getenv("COMPANY_NAME", "default_company"),
        "industry": os.getenv("INDUSTRY", "technology"),  # Custom field
    }
```

## 🔍 Advanced Configuration

### Model Customization (`models.py`)

#### Adding Custom Fields
```python
class JobRequirements(BaseModel):
    # Standard fields
    technical_skills: List[str]
    
    # Custom additions
    remote_work_policy: Optional[str] = None
    salary_range: Optional[Dict[str, float]] = None
    custom_requirements: List[str] = Field(default_factory=list)
```

#### Validation Rules
```python
class ATSKeyword(BaseModel):
    importance: int = Field(ge=1, le=5)  # 1-5 range validation
    category: str = Field(regex="^(technical|soft|experience|industry)$")
```

### Performance Configuration

#### Concurrent Processing
```python
# For faster execution (if supported)
process=Process.parallel  # Instead of sequential
```

#### Memory Optimization
```python
# Limit context size for large documents
max_context_length = 4000  # Adjust based on needs
```

### Integration Configuration

#### External APIs
```python
# Custom tool configuration
class CustomResearchTool(BaseTool):
    api_key: str = os.getenv("CUSTOM_API_KEY")
    base_url: str = "https://api.custom-service.com"
```

#### Database Integration
```python
# Optional: Save results to database
def save_results(results):
    # Implementation for database storage
    pass
```

## 🔒 Security Configuration

### API Key Management
- **Environment Variables**: Never hardcode API keys
- **Key Rotation**: Regularly update API keys
- **Access Control**: Limit API key permissions

### Data Privacy
- **PDF Security**: Ensure resume PDFs are handled securely
- **Output Security**: Protect generated analysis files
- **Logging**: Configure appropriate logging levels

### Rate Limiting
```python
# Configure API rate limits
llm=LLM(
    model="gpt-4o-mini",
    max_requests_per_minute=50,
    max_tokens_per_minute=10000
)
```

## 🧪 Testing Configuration

### Test Environment Setup
```python
# test_config.py
TEST_INPUTS = {
    "job_url": "https://example.com/test-job",
    "company_name": "Test Company",
}

# Use smaller models for testing
TEST_LLM = LLM("gpt-3.5-turbo")
```

### Validation Testing
```python
# Validate configuration
def validate_config():
    assert os.path.exists("config/agents.yaml")
    assert os.path.exists("config/tasks.yaml")
    assert os.path.exists("knowledge/resume.pdf")
```

## 🔧 Troubleshooting Configuration

### Common Issues
- **Missing API Keys**: Check environment variables
- **File Paths**: Verify relative paths from project root
- **Model Availability**: Ensure access to specified LLM models
- **Tool Dependencies**: Confirm all required tools are installed

### Debug Configuration
```python
# Enable detailed logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Verbose mode for all agents
verbose=True
```

---

This configuration guide ensures proper setup and customization of the Jobfull Resume Analyzer for various use cases and requirements. 