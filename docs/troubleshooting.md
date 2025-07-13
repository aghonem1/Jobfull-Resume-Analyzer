# Troubleshooting Guide

## Overview

This guide covers common issues, error resolution, and debugging strategies for the Jobfull Resume Analyzer system. Most issues fall into configuration, execution, or output quality categories.

## 🚨 Common Issues & Solutions

### Setup & Configuration Issues

#### Issue: Missing API Keys
```
Error: OpenAI API key not found
```

**Solution**:
```bash
# Check environment variables
echo $OPENAI_API_KEY

# Create .env file if missing
cat > .env << EOF
OPENAI_API_KEY=your_actual_api_key_here
SERPER_API_KEY=your_serper_key_here
EOF

# Verify API key format (starts with sk-)
```

**Prevention**: Always use environment variables, never hardcode keys

#### Issue: Resume PDF Not Found
```
Error: PDFKnowledgeSource: file not found
```

**Solution**:
```bash
# Check file exists
ls -la cv_opt/knowledge/

# Verify file path in crew.py
# Ensure path is relative to main.py location
```

**Common Causes**:
- Wrong file path in `crew.py`
- PDF file not in `knowledge/` directory
- Incorrect working directory when running

#### Issue: Import Errors
```
ModuleNotFoundError: No module named 'crewai'
```

**Solution**:
```bash
# Install all dependencies
pip install -r requirements.txt

# Check Python version (needs 3.8+)
python --version

# Verify virtual environment is activated
which python
```

### Execution Issues

#### Issue: Job URL Scraping Fails
```
Error: Failed to scrape job description from URL
```

**Solutions**:
1. **Check URL Accessibility**:
```python
import requests
response = requests.get("your_job_url")
print(response.status_code)  # Should be 200
```

2. **Alternative URLs**:
- Try direct job posting URL (not search results)
- Use company careers page link
- Check if URL requires authentication

3. **Manual Fallback**:
```python
# Modify task to accept manual job description
inputs = {
    "job_url": "manual",
    "job_description": "paste job description here",
    "company_name": "Company Name"
}
```

#### Issue: Agent Timeout Errors
```
Error: Agent execution timeout after 300 seconds
```

**Solutions**:
```python
# Increase timeout in crew configuration
@task
def analyze_job_task(self) -> Task:
    return Task(
        config=self.tasks_config["analyze_job_task"],
        timeout=600,  # Increase to 10 minutes
        max_retries=3
    )
```

#### Issue: Context Passing Failures
```
Error: Task context not available
```

**Solution**:
```python
# Verify task dependencies in tasks.yaml
generate_cover_letter_task:
  context: [analyze_job_task, optimize_resume_task, research_company_task]

# Check task execution order in crew.py
@crew
def crew(self) -> Crew:
    return Crew(
        agents=self.agents,
        tasks=self.tasks,  # Ensure tasks are in dependency order
        process=Process.sequential
    )
```

### Output Quality Issues

#### Issue: Poor Match Scores
```json
{
  "overall_match": 23.5,
  "technical_skills_match": 15.0
}
```

**Diagnosis & Solutions**:

1. **Check Resume Content**:
```python
# Verify PDF contains relevant content
from PyPDF2 import PdfReader
reader = PdfReader("knowledge/resume.pdf")
text = "".join([page.extract_text() for page in reader.pages])
print(text[:500])  # Check extracted content
```

2. **Keyword Analysis**:
```python
# Compare job keywords with resume content
with open("output/job_analysis.json") as f:
    job_data = json.load(f)

required_keywords = [
    kw["keyword"] for kw in job_data["ats_keywords"] 
    if kw["required"] and kw["importance"] >= 4
]
print("Missing critical keywords:", required_keywords)
```

3. **Resume Optimization**:
- Add missing technical skills
- Quantify achievements with metrics
- Include relevant industry experience
- Use job-specific terminology

#### Issue: ATS Compatibility Warnings
```json
{
  "format_compliance": {
    "single_column": false,
    "no_tables": false,
    "doc_format": false
  }
}
```

**Solutions**:
1. **Format Issues**:
   - Convert multi-column to single-column layout
   - Replace tables with bullet-point lists
   - Remove images, graphics, and text boxes
   - Save as .docx instead of .pdf

2. **Validation Script**:
```python
def validate_ats_format(resume_path):
    issues = []
    # Check file extension
    if not resume_path.endswith(('.docx', '.doc')):
        issues.append("Save as .docx format")
    
    # Add more validation logic
    return issues
```

#### Issue: Generic Cover Letters
```json
{
  "customization_level": 0.12,
  "personalization_elements": []
}
```

**Solutions**:
1. **Improve Company Research**:
```python
# Enhance research inputs
inputs = {
    "job_url": "detailed_job_url",
    "company_name": "Exact Company Name",
    "company_website": "https://company.com",  # Additional context
}
```

2. **Manual Enhancement**:
- Research company recent news manually
- Add specific company values/culture references
- Include relevant industry trends
- Mention specific projects or initiatives

### Performance Issues

#### Issue: Slow Execution
```
Analysis taking >10 minutes to complete
```

**Optimization Strategies**:

1. **Model Configuration**:
```python
# Use faster model for testing
llm=LLM("gpt-3.5-turbo")  # Instead of gpt-4

# Reduce context length
max_context_length = 2000  # Limit input size
```

2. **Parallel Processing** (if supported):
```python
# Enable parallel execution for independent tasks
process=Process.parallel
```

3. **Caching**:
```python
# Cache expensive operations
import functools

@functools.lru_cache(maxsize=128)
def cached_company_research(company_name):
    # Implementation
    pass
```

#### Issue: High API Costs
```
OpenAI usage exceeding budget
```

**Cost Optimization**:
1. **Model Selection**:
```python
# Use cost-effective models
llm=LLM("gpt-4o-mini")     # Most cost-effective
# Avoid: llm=LLM("gpt-4")  # More expensive
```

2. **Input Optimization**:
```python
# Limit input size
def truncate_input(text, max_tokens=2000):
    return text[:max_tokens * 4]  # Rough token estimation
```

## 🔍 Debugging Strategies

### Enable Detailed Logging
```python
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Enable CrewAI verbose mode
verbose=True
```

### Step-by-Step Debugging
```python
def debug_execution():
    crew = ResumeCrew()
    
    # Test each agent individually
    agents = [crew.job_analyzer(), crew.resume_analyzer()]
    for agent in agents:
        print(f"Testing {agent.role}")
        # Test agent configuration
        
    # Test each task
    tasks = [crew.analyze_job_task(), crew.optimize_resume_task()]
    for task in tasks:
        print(f"Testing {task.description[:50]}...")
        # Test task execution
```

### Output Validation
```python
def validate_outputs():
    required_files = [
        "job_analysis.json",
        "resume_optimization.json", 
        "company_research.json",
        "cover_letter_analysis.json",
        "cover_letter.md",
        "optimized_resume.md",
        "final_report.md"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(f"output/{file}"):
            missing_files.append(file)
    
    if missing_files:
        print(f"Missing output files: {missing_files}")
        return False
    
    print("All output files generated successfully")
    return True
```

## 🛠️ Advanced Troubleshooting

### Memory Issues
```python
# Monitor memory usage
import psutil
import os

def monitor_memory():
    process = psutil.Process(os.getpid())
    memory_mb = process.memory_info().rss / 1024 / 1024
    print(f"Memory usage: {memory_mb:.1f} MB")

# Call during execution to track usage
```

### Network Issues
```python
# Test API connectivity
def test_api_connections():
    try:
        import openai
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5
        )
        print("OpenAI API: ✅ Connected")
    except Exception as e:
        print(f"OpenAI API: ❌ Error - {e}")
    
    # Test web scraping
    try:
        import requests
        response = requests.get("https://httpbin.org/get", timeout=10)
        print("Web scraping: ✅ Working")
    except Exception as e:
        print(f"Web scraping: ❌ Error - {e}")
```

### Configuration Validation
```python
def validate_configuration():
    issues = []
    
    # Check required files
    if not os.path.exists("config/agents.yaml"):
        issues.append("Missing agents.yaml")
    if not os.path.exists("config/tasks.yaml"):
        issues.append("Missing tasks.yaml")
    
    # Check environment variables
    if not os.getenv("OPENAI_API_KEY"):
        issues.append("Missing OPENAI_API_KEY")
    
    # Check PDF knowledge source
    if not os.path.exists("knowledge/"):
        issues.append("Missing knowledge directory")
    
    return issues
```

## 📋 Error Code Reference

### Common Error Patterns

| Error Pattern | Cause | Solution |
|---------------|--------|----------|
| `API key not found` | Missing environment variable | Set OPENAI_API_KEY |
| `PDFKnowledgeSource: file not found` | Wrong file path | Check knowledge/ directory |
| `Task context not available` | Missing task dependency | Fix context order in tasks.yaml |
| `Agent execution timeout` | Long-running operation | Increase timeout or optimize input |
| `Failed to scrape job description` | Protected/invalid URL | Use alternative URL or manual input |
| `ModuleNotFoundError` | Missing dependencies | Run pip install -r requirements.txt |
| `Pydantic validation error` | Invalid data format | Check model definitions |
| `Rate limit exceeded` | Too many API calls | Implement rate limiting |

### Recovery Procedures

#### Partial Failure Recovery
```python
def recover_from_partial_failure():
    # Check which outputs exist
    completed_tasks = []
    for file in ["job_analysis.json", "resume_optimization.json"]:
        if os.path.exists(f"output/{file}"):
            completed_tasks.append(file)
    
    # Resume from last successful task
    if "job_analysis.json" in completed_tasks:
        print("Resuming from resume optimization...")
        # Start from resume_analyzer task
```

#### Cleanup and Restart
```bash
# Clean output directory
rm -rf output/*

# Reset any cached data
rm -rf .cache/

# Restart with fresh configuration
python src/cv_opt/main.py
```

## 📞 Getting Help

### Self-Diagnosis Checklist
Before seeking help, verify:
- [ ] All dependencies installed (`pip list`)
- [ ] Environment variables set (`echo $OPENAI_API_KEY`)
- [ ] Resume PDF exists and is readable
- [ ] Job URL is accessible
- [ ] Output directory has write permissions
- [ ] No firewall blocking API calls

### Collecting Debug Information
```python
def collect_debug_info():
    info = {
        "python_version": sys.version,
        "working_directory": os.getcwd(),
        "environment_vars": {
            "OPENAI_API_KEY": "***" if os.getenv("OPENAI_API_KEY") else "Not set"
        },
        "file_structure": os.listdir("."),
        "output_files": os.listdir("output/") if os.path.exists("output/") else []
    }
    
    print(json.dumps(info, indent=2))
    return info
```

---

This troubleshooting guide provides systematic approaches to identifying and resolving issues, ensuring smooth operation of the Jobfull Resume Analyzer system. 