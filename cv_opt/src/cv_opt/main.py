#!/usr/bin/env python
"""
Jobfull Resume Analyzer - Main Entry Point

This module serves as the primary entry point for the Jobfull Resume Analyzer system,
a comprehensive AI-powered resume optimization tool built with CrewAI.

The system employs 6 specialized AI agents working in a coordinated sequential workflow:
1. Job Analyzer - Extracts ATS keywords and analyzes job requirements
2. Resume Analyzer - Evaluates resume format and ATS compatibility
3. Company Researcher - Conducts comprehensive company and industry research
4. Cover Letter Generator - Creates personalized cover letters
5. Resume Writer - Optimizes resume content with real candidate data
6. Report Generator - Produces executive-level intelligence reports

Key Features:
- ATS optimization for 2025 industry standards
- Real PDF resume content extraction (no placeholders)
- Comprehensive company intelligence gathering
- Visual reporting with Mermaid diagrams
- Professional deliverables: optimized resume, cover letter, and reports

Technical Stack:
- CrewAI framework for AI agent orchestration
- OpenAI GPT-4o-mini for all language model tasks
- Pydantic for structured data validation
- PDF knowledge sources for resume parsing
- Web scraping tools for job and company research

Example Usage:
    python main.py

    # Or programmatically:
    from cv_opt.main import run
    run()

Author: Jobfull Team
Version: 1.0.0
License: MIT
"""

import warnings
from typing import Any, Dict

from cv_opt.crew import ResumeCrew

# Suppress specific warning that can occur during PDF processing
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run(custom_inputs: Dict[str, Any] = None) -> None:
    """
    Execute the complete resume optimization workflow.

    This function initializes and runs the ResumeCrew system with either default
    or custom inputs. The system will process the job posting, analyze the resume,
    research the company, and generate optimized outputs.

    Args:
        custom_inputs (Dict[str, Any], optional): Custom input parameters.
            Expected keys:
            - job_url (str): URL of the job posting to analyze
            - company_name (str): Name of the target company

            If None, uses default NVIDIA job posting for demonstration.

    Returns:
        None: The function executes the workflow and saves outputs to files.

    Raises:
        ValueError: If required inputs are missing or invalid
        ConnectionError: If unable to access job URL or company information
        FileNotFoundError: If resume PDF is not found in the expected location

    Output Files Generated:
        - output/job_analysis.json: Job requirements and ATS keyword analysis
        - output/resume_optimization.json: Resume optimization recommendations
        - output/company_research.json: Company intelligence and research
        - output/cover_letter_analysis.json: Cover letter generation analysis
        - output/cover_letter.md: Personalized cover letter content
        - output/optimized_resume.md: ATS-optimized resume content
        - output/final_report.md: Executive intelligence report with visuals

    Example:
        # Run with default inputs
        run()

        # Run with custom inputs
        custom_inputs = {
            "job_url": "https://company.com/careers/job-123",
            "company_name": "TechCorp"
        }
        run(custom_inputs)
    """

    # Use custom inputs if provided, otherwise use default demonstration inputs
    if custom_inputs is None:
        # Default inputs for demonstration - NVIDIA GPU Silicon Architect position
        inputs = {
            "job_url": "https://www.google.com/about/careers/applications/jobs/results/105532306164196038-gpu-silicon-architect",
            "company_name": "NVIDIA",
        }
        print("🚀 Running Jobfull Resume Analyzer with default inputs...")
        print(f"📄 Job URL: {inputs['job_url']}")
        print(f"🏢 Company: {inputs['company_name']}")
    else:
        inputs = custom_inputs
        print("🚀 Running Jobfull Resume Analyzer with custom inputs...")
        print(f"📄 Job URL: {inputs.get('job_url', 'Not specified')}")
        print(f"🏢 Company: {inputs.get('company_name', 'Not specified')}")

    # Validate required inputs
    required_keys = ["job_url", "company_name"]
    missing_keys = [
        key for key in required_keys if key not in inputs or not inputs[key]
    ]

    if missing_keys:
        raise ValueError(f"Missing required input parameters: {missing_keys}")

    print("🤖 Initializing AI agents and starting workflow...")
    print("📊 This process typically takes 3-5 minutes to complete...")

    try:
        # Initialize the ResumeCrew system and execute the workflow
        crew_instance = ResumeCrew()
        result = crew_instance.crew().kickoff(inputs=inputs)

        print("✅ Resume optimization workflow completed successfully!")
        print("📁 Check the 'output/' directory for generated files:")
        print("   - job_analysis.json (ATS keyword analysis)")
        print("   - resume_optimization.json (optimization recommendations)")
        print("   - company_research.json (company intelligence)")
        print("   - cover_letter_analysis.json (cover letter analysis)")
        print("   - cover_letter.md (personalized cover letter)")
        print("   - optimized_resume.md (ATS-optimized resume)")
        print("   - final_report.md (executive intelligence report)")

        return result

    except Exception as e:
        print(f"❌ Error during workflow execution: {str(e)}")
        print("🔧 Please check your inputs and try again.")
        raise


if __name__ == "__main__":
    # Entry point when script is run directly
    print("=" * 60)
    print("🎯 JOBFULL RESUME ANALYZER")
    print("   AI-Powered Resume Optimization for 2025 ATS Standards")
    print("=" * 60)

    run()
