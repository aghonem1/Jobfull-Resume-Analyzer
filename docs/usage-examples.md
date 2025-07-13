# Usage Examples

## Overview

This guide provides practical examples of how to use the Jobfull Resume Analyzer system for various job application scenarios. Each example includes setup, execution, and expected outcomes.

## 🚀 Basic Usage

### Standard Job Application Analysis

**Scenario**: Analyzing a Software Engineer position at Google

#### 1. Setup Input Parameters
```python
# main.py
def run():
    inputs = {
        "job_url": "https://careers.google.com/jobs/results/12345-software-engineer",
        "company_name": "Google",
    }
    ResumeCrew().crew().kickoff(inputs=inputs)
```

#### 2. Execute Analysis
```bash
cd cv_opt
python src/cv_opt/main.py
```

#### 3. Expected Output Structure
```
output/
├── job_analysis.json           # ATS keywords, requirements, scoring
├── resume_optimization.json    # Format compliance, improvements  
├── company_research.json       # Google culture, trends, insights
├── cover_letter_analysis.json  # Personalization analysis
├── cover_letter.md            # Ready-to-use cover letter
├── optimized_resume.md        # ATS-optimized resume
└── final_report.md            # Executive summary with visuals
```

## 🎯 Industry-Specific Examples

### Technology Sector

**Example**: Senior Full-Stack Developer at Stripe

```python
inputs = {
    "job_url": "https://stripe.com/jobs/senior-fullstack-developer",
    "company_name": "Stripe",
}
```

**Key Focus Areas**:
- **ATS Keywords**: React, Node.js, TypeScript, API design, microservices
- **Industry Trends**: Payment processing, fintech compliance, scalability
- **Company Culture**: Engineering excellence, customer-first mindset
- **Technical Depth**: System design, performance optimization

**Expected Insights**:
```json
{
  "ats_keywords": [
    {"keyword": "React", "importance": 5, "category": "technical", "required": true},
    {"keyword": "Node.js", "importance": 5, "category": "technical", "required": true},
    {"keyword": "microservices", "importance": 4, "category": "technical", "required": false}
  ]
}
```

### Healthcare Sector

**Example**: Clinical Data Analyst at Kaiser Permanente

```python
inputs = {
    "job_url": "https://jobs.kaiserpermanente.org/clinical-data-analyst",
    "company_name": "Kaiser Permanente",
}
```

**Key Focus Areas**:
- **Compliance**: HIPAA, FDA regulations, clinical standards
- **Technical Skills**: SQL, R/Python, Epic systems, HL7
- **Domain Knowledge**: Clinical workflows, population health
- **Certifications**: CRA, CCRP, or relevant healthcare certifications

### Financial Services

**Example**: Quantitative Analyst at JPMorgan Chase

```python
inputs = {
    "job_url": "https://jpmorgan.com/careers/quantitative-analyst",
    "company_name": "JPMorgan Chase",
}
```

**Key Focus Areas**:
- **Technical**: Python, C++, MATLAB, statistical modeling
- **Finance Domain**: Risk management, derivatives, portfolio optimization
- **Regulatory**: Basel III, Dodd-Frank, stress testing
- **Education**: PhD/Masters in quantitative field

## 📋 Scenario-Based Usage

### Scenario 1: Career Transition

**Context**: Software Developer transitioning to Product Manager

#### Setup
```python
inputs = {
    "job_url": "https://company.com/product-manager-role",
    "company_name": "Target Company",
}
```

#### Key Optimization Focus
- **Skill Translation**: Technical skills → business impact
- **Experience Reframing**: Engineering projects → product outcomes
- **Gap Identification**: PM-specific skills like market research, user testing
- **Narrative Development**: Technical background as PM strength

#### Expected Analysis
```json
{
  "gaps": [
    "Product roadmap development experience",
    "User research and testing methodology",
    "Market analysis and competitive intelligence"
  ],
  "strengths": [
    "Technical feasibility assessment",
    "Cross-functional team collaboration",
    "Data-driven decision making"
  ]
}
```

### Scenario 2: ATS Optimization Issues

**Context**: Resume getting rejected by ATS systems

#### Diagnostic Steps
1. **Run Analysis**: Focus on `resume_optimization.json`
2. **Check Format Compliance**: Review ATS compatibility score
3. **Keyword Analysis**: Compare keyword density with job requirements
4. **Implement Fixes**: Apply optimization recommendations

#### Common Issues & Solutions
```json
{
  "format_compliance": {
    "single_column": false,        // ❌ Fix: Convert to single column
    "no_tables": false,           // ❌ Fix: Replace tables with lists
    "standard_fonts": true,       // ✅ Good
    "no_images": true            // ✅ Good
  },
  "keyword_gaps": [
    "cloud computing",            // Missing critical keyword
    "agile methodology",         // Missing methodology
    "API development"            // Technical skill gap
  ]
}
```

### Scenario 3: Interview Preparation

**Context**: Using company research for interview preparation

#### Research Focus
```python
# Focus on company_research.json output
```

#### Key Interview Elements
```json
{
  "interview_questions": [
    "How would you handle technical debt in our legacy systems?",
    "Describe your experience with our technology stack",
    "How do you stay current with industry trends?"
  ],
  "company_priorities": [
    "Digital transformation initiatives",
    "Customer experience improvement",
    "Scalability and performance optimization"
  ],
  "talking_points": [
    "Recent company acquisition and integration",
    "New product launches and market expansion",
    "Engineering culture and innovation focus"
  ]
}
```

## 🔄 Advanced Usage Patterns

### Batch Processing Multiple Jobs

#### Setup Script
```python
# batch_analysis.py
def analyze_multiple_jobs():
    jobs = [
        {"url": "https://company1.com/job1", "company": "Company1"},
        {"url": "https://company2.com/job2", "company": "Company2"},
        {"url": "https://company3.com/job3", "company": "Company3"},
    ]
    
    for job in jobs:
        inputs = {
            "job_url": job["url"],
            "company_name": job["company"],
        }
        # Create separate output directories
        crew = ResumeCrew()
        crew.output_dir = f"output/{job['company']}"
        crew.crew().kickoff(inputs=inputs)
```

#### Comparative Analysis
```python
# compare_results.py
def compare_job_matches():
    companies = ["Company1", "Company2", "Company3"]
    scores = {}
    
    for company in companies:
        with open(f"output/{company}/job_analysis.json") as f:
            data = json.load(f)
            scores[company] = data["match_score"]["overall_match"]
    
    # Rank opportunities
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    print("Job Opportunities Ranked by Match Score:")
    for company, score in ranked:
        print(f"{company}: {score}%")
```

### Custom Industry Analysis

#### Specialized Configuration
```python
# custom_tech_startup.py
class TechStartupCrew(ResumeCrew):
    def __init__(self):
        super().__init__()
        # Override with startup-specific focus
        self.startup_keywords = [
            "MVP", "product-market fit", "growth hacking",
            "lean startup", "rapid iteration", "equity"
        ]
```

### A/B Testing Resume Versions

#### Setup Multiple Resume Analysis
```python
# resume_ab_test.py
def test_resume_versions():
    versions = ["resume_v1.pdf", "resume_v2.pdf"]
    job_url = "https://company.com/job"
    
    for version in versions:
        # Update resume source
        crew = ResumeCrew()
        crew.resume_pdf = PDFKnowledgeSource(file_paths=version)
        
        inputs = {"job_url": job_url, "company_name": "Target Company"}
        results = crew.crew().kickoff(inputs=inputs)
        
        # Save version-specific results
        save_results(version, results)
```

## 🎯 Output Utilization Examples

### Using Analysis Results

#### Extract Key Metrics
```python
# analyze_results.py
import json

def extract_key_metrics():
    # Load job analysis
    with open("output/job_analysis.json") as f:
        job_data = json.load(f)
    
    # Extract critical information
    overall_match = job_data["match_score"]["overall_match"]
    critical_keywords = [
        kw["keyword"] for kw in job_data["ats_keywords"] 
        if kw["importance"] >= 4 and kw["required"]
    ]
    
    print(f"Overall Match Score: {overall_match}%")
    print(f"Critical Keywords: {', '.join(critical_keywords)}")
```

#### Generate Custom Reports
```python
# custom_report.py
def generate_executive_summary():
    # Combine all analysis files
    summary = {
        "job_match": load_json("job_analysis.json"),
        "resume_gaps": load_json("resume_optimization.json"),
        "company_intel": load_json("company_research.json"),
        "cover_letter": load_markdown("cover_letter.md")
    }
    
    # Create custom dashboard
    create_dashboard(summary)
```

### Integration with External Systems

#### CRM Integration
```python
# crm_integration.py
def update_job_tracker():
    analysis = load_analysis_results()
    
    job_record = {
        "company": analysis["company_name"],
        "position": analysis["job_title"],
        "match_score": analysis["overall_match"],
        "application_status": "analyzed",
        "next_steps": analysis["recommendations"]
    }
    
    # Update CRM system
    crm_client.update_job_application(job_record)
```

#### Portfolio Website
```python
# portfolio_integration.py
def update_portfolio():
    # Use optimized resume content
    resume_content = load_markdown("optimized_resume.md")
    
    # Extract key achievements
    achievements = extract_achievements(resume_content)
    
    # Update portfolio website
    portfolio_api.update_achievements(achievements)
```

## 🔧 Troubleshooting Usage

### Common Execution Issues

#### Invalid Job URL
```python
# Error handling
try:
    crew.crew().kickoff(inputs=inputs)
except Exception as e:
    if "scraping failed" in str(e):
        print("Job URL may be invalid or protected")
        # Fallback: manual job description entry
```

#### Missing Output Files
```bash
# Check output directory
ls -la output/
# Ensure all 7 expected files are present
```

#### Poor Match Scores
```python
# Diagnostic analysis
def diagnose_low_scores():
    with open("output/job_analysis.json") as f:
        data = json.load(f)
    
    if data["match_score"]["technical_skills_match"] < 50:
        print("Focus on technical skills gap")
    elif data["match_score"]["experience_match"] < 50:
        print("Emphasize relevant experience")
```

---

These usage examples provide practical guidance for leveraging the Jobfull Resume Analyzer across various scenarios and industries, maximizing job application success rates. 