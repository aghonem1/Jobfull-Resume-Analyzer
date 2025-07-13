"""
Jobfull Resume Analyzer - Crew Orchestration Module

This module defines the ResumeCrew class, which orchestrates the complete AI-powered
resume optimization workflow using the CrewAI framework. The class manages 6 specialized
AI agents and 7 sequential tasks to analyze jobs, optimize resumes, research companies,
and generate professional deliverables.

Architecture Overview:
    The ResumeCrew follows a sequential processing model where each agent builds upon
    the previous agent's output, creating a comprehensive optimization pipeline:

    Job Analysis → Resume Analysis → Company Research → Cover Letter Generation
    → Resume Writing → Report Generation

Key Components:
    - 6 AI Agents: Each with specialized roles and capabilities
    - 7 Tasks: Sequential workflow with context passing
    - PDF Knowledge Sources: Real resume content extraction
    - Structured Outputs: Pydantic models for data validation
    - File Outputs: JSON analysis + Markdown deliverables

Technical Dependencies:
    - CrewAI: AI agent orchestration framework
    - OpenAI GPT-4o-mini: Language model for all agents
    - Pydantic: Data validation and structured outputs
    - PDF Knowledge Sources: Resume content extraction
    - Web Scraping Tools: Job posting and company research

Author: Jobfull Team
Version: 1.0.0
"""

from crewai import LLM, Agent, Crew, Process, Task
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import ScrapeWebsiteTool, SerperDevTool

from .models import (
    CompanyResearch,
    CoverLetterGeneration,
    JobRequirements,
    ResumeOptimization,
)


@CrewBase
class ResumeCrew:
    """
    Main orchestration class for the Jobfull Resume Analyzer system.

    This class manages the complete AI-powered resume optimization workflow,
    coordinating 6 specialized AI agents through 7 sequential tasks. Each agent
    has specific expertise and contributes to the overall optimization process.

    Agent Workflow:
        1. Job Analyzer: Extracts ATS keywords and analyzes job requirements
        2. Resume Analyzer: Evaluates current resume format and ATS compatibility
        3. Company Researcher: Conducts comprehensive company and industry research
        4. Cover Letter Generator: Creates personalized cover letters with company insights
        5. Resume Writer: Optimizes resume content using real candidate data
        6. Report Generator: Produces executive-level intelligence reports with visuals

    Task Outputs:
        - JSON Files: Structured analysis data for each phase
        - Markdown Files: Professional deliverables (resume, cover letter, report)
        - Visual Elements: Mermaid diagrams and progress indicators

    Configuration:
        - Agent configurations loaded from config/agents.yaml
        - Task configurations loaded from config/tasks.yaml
        - Resume PDF processed through knowledge sources
        - All agents use GPT-4o-mini for consistency

    Attributes:
        agents_config (str): Path to agent configuration file
        tasks_config (str): Path to task configuration file
        resume_pdf (PDFKnowledgeSource): PDF knowledge source for resume content

    Example:
        # Initialize and run the crew
        crew = ResumeCrew()
        inputs = {
            "job_url": "https://company.com/job-posting",
            "company_name": "TechCorp"
        }
        result = crew.crew().kickoff(inputs=inputs)
    """

    # Configuration file paths - these files define agent roles and task specifications
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self) -> None:
        """
        Initialize the ResumeCrew with PDF knowledge source.

        Sets up the PDF knowledge source for resume content extraction.
        The resume PDF is made available to all agents that need access
        to candidate information for personalization and optimization.

        Note:
            The PDF path is currently hardcoded for demonstration purposes.
            In production, this should be configurable or passed as a parameter.

        Raises:
            FileNotFoundError: If the resume PDF file is not found
            ValueError: If the PDF file is corrupted or unreadable
        """
        # Initialize PDF knowledge source for resume content extraction
        # This enables all agents to access real candidate information
        self.resume_pdf = PDFKnowledgeSource(file_paths="GhonemCV_2025.pdf")

    # ========================================
    # AI AGENT DEFINITIONS
    # ========================================
    # Each agent is specialized for a specific aspect of the optimization process

    @agent
    def resume_analyzer(self) -> Agent:
        """
        Create the Resume Analyzer agent.

        This agent specializes in ATS compatibility analysis, format compliance,
        and keyword optimization strategies. It evaluates the current resume
        against 2025 ATS standards and provides detailed optimization recommendations.

        Capabilities:
            - ATS compatibility scoring (Workday, Greenhouse, Lever, iCIMS)
            - Format compliance verification (fonts, layout, sections)
            - Keyword density analysis and optimization
            - AI content detection and authenticity verification
            - Parsing optimization for maximum ATS compatibility

        Tools:
            - PDF Knowledge Source: Access to candidate's resume content
            - GPT-4o-mini: Advanced language understanding for analysis

        Returns:
            Agent: Configured Resume Analyzer agent instance
        """
        return Agent(
            config=self.agents_config["resume_analyzer"],
            verbose=True,
            llm=LLM("gpt-4o-mini"),
            knowledge_sources=[self.resume_pdf],
        )

    @agent
    def job_analyzer(self) -> Agent:
        """
        Create the Job Analyzer agent.

        This agent specializes in job description analysis, ATS keyword extraction,
        and candidate fit scoring. It forms the foundation for all subsequent
        optimization by understanding job requirements and industry standards.

        Capabilities:
            - Job description parsing and analysis
            - ATS keyword extraction with importance scoring
            - Technical and soft skill requirement identification
            - Industry trend analysis for 2025 standards
            - Candidate-job fit scoring and gap analysis

        Tools:
            - ScrapeWebsiteTool: Web scraping for job posting content
            - GPT-4o-mini: Advanced language understanding for analysis

        Returns:
            Agent: Configured Job Analyzer agent instance
        """
        return Agent(
            config=self.agents_config["job_analyzer"],
            verbose=True,
            tools=[ScrapeWebsiteTool()],
            llm=LLM("gpt-4o-mini"),
        )

    @agent
    def company_researcher(self) -> Agent:
        """
        Create the Company Researcher agent.

        This agent specializes in comprehensive company intelligence gathering,
        market analysis, and competitive positioning. It provides critical
        insights for personalizing applications and interview preparation.

        Capabilities:
            - Company culture and values research
            - Recent developments and news analysis
            - Market positioning and competitive intelligence
            - Leadership team and organizational structure analysis
            - Industry trends and company growth trajectory assessment

        Tools:
            - SerperDevTool: Web search for company intelligence
            - PDF Knowledge Source: Candidate context for alignment
            - GPT-4o-mini: Advanced reasoning for strategic insights

        Returns:
            Agent: Configured Company Researcher agent instance
        """
        return Agent(
            config=self.agents_config["company_researcher"],
            verbose=True,
            tools=[SerperDevTool()],
            llm=LLM("gpt-4o-mini"),
            knowledge_sources=[self.resume_pdf],
        )

    @agent
    def cover_letter_generator(self) -> Agent:
        """
        Create the Cover Letter Generator agent.

        This agent specializes in creating personalized, ATS-optimized cover letters
        that integrate company research and demonstrate authentic candidate value.
        It extracts real contact information and crafts compelling narratives.

        Capabilities:
            - Authentic contact information extraction from PDF
            - Personalized content creation with company insights
            - ATS-optimized keyword integration
            - Professional business letter formatting
            - Achievement-focused storytelling with quantified results

        Tools:
            - PDF Knowledge Source: Real candidate information extraction
            - GPT-4o-mini: Advanced language generation for personalization

        Returns:
            Agent: Configured Cover Letter Generator agent instance
        """
        return Agent(
            config=self.agents_config["cover_letter_generator"],
            verbose=True,
            llm=LLM("gpt-4o-mini"),
            knowledge_sources=[self.resume_pdf],
        )

    @agent
    def resume_writer(self) -> Agent:
        """
        Create the Resume Writer agent.

        This agent specializes in content integration and optimization, applying
        all previous recommendations to create an ATS-optimized resume using
        real candidate information without placeholders.

        Capabilities:
            - Real candidate information extraction and processing
            - ATS optimization implementation from previous analysis
            - Natural keyword integration without stuffing
            - Achievement amplification with quantified results
            - Professional formatting and presentation

        Tools:
            - PDF Knowledge Source: Real candidate data extraction
            - GPT-4o-mini: Advanced content optimization and enhancement

        Returns:
            Agent: Configured Resume Writer agent instance
        """
        return Agent(
            config=self.agents_config["resume_writer"],
            verbose=True,
            llm=LLM("gpt-4o-mini"),
            knowledge_sources=[self.resume_pdf],
        )

    @agent
    def report_generator(self) -> Agent:
        """
        Create the Report Generator agent.

        This agent specializes in executive-level reporting with data visualization,
        predictive analytics, and comprehensive career intelligence. It synthesizes
        all previous analysis into actionable insights with visual elements.

        Capabilities:
            - Executive-level report generation
            - Data visualization with Mermaid diagrams
            - Interactive dashboards and progress indicators
            - Predictive career analytics and trend analysis
            - Comprehensive intelligence synthesis

        Tools:
            - PDF Knowledge Source: Candidate context for personalization
            - GPT-4o-mini: Advanced reasoning for strategic insights

        Returns:
            Agent: Configured Report Generator agent instance
        """
        return Agent(
            config=self.agents_config["report_generator"],
            verbose=True,
            llm=LLM("gpt-4o-mini"),
            knowledge_sources=[self.resume_pdf],
        )

    # ========================================
    # TASK DEFINITIONS
    # ========================================
    # Each task represents a specific phase in the optimization workflow

    @task
    def analyze_job_task(self) -> Task:
        """
        Create the job analysis task.

        This foundational task analyzes the job posting to extract requirements,
        ATS keywords, and scoring criteria. It provides the foundation for all
        subsequent optimization tasks.

        Process:
            1. Job posting content extraction and parsing
            2. ATS keyword identification and categorization
            3. Requirement analysis (technical, soft skills, experience)
            4. Industry trend integration for 2025 standards
            5. Candidate fit scoring and gap analysis

        Output:
            - File: output/job_analysis.json
            - Structure: JobRequirements Pydantic model
            - Contains: ATS keywords, requirements, scoring, and analysis

        Returns:
            Task: Configured job analysis task instance
        """
        return Task(
            config=self.tasks_config["analyze_job_task"],
            output_file="output/job_analysis.json",
            output_pydantic=JobRequirements,
        )

    @task
    def optimize_resume_task(self) -> Task:
        """
        Create the resume optimization task.

        This task analyzes the current resume for ATS compatibility and provides
        detailed optimization recommendations based on job requirements.

        Process:
            1. Resume format and structure analysis
            2. ATS compatibility scoring across major systems
            3. Keyword density and optimization analysis
            4. Content authenticity verification
            5. Specific improvement recommendations

        Output:
            - File: output/resume_optimization.json
            - Structure: ResumeOptimization Pydantic model
            - Contains: ATS scores, optimization suggestions, and improvements

        Returns:
            Task: Configured resume optimization task instance
        """
        return Task(
            config=self.tasks_config["optimize_resume_task"],
            output_file="output/resume_optimization.json",
            output_pydantic=ResumeOptimization,
        )

    @task
    def research_company_task(self) -> Task:
        """
        Create the company research task.

        This task conducts comprehensive company intelligence gathering to provide
        context for personalized applications and interview preparation.

        Process:
            1. Company profile and financial health analysis
            2. Recent developments and news research
            3. Culture and values assessment
            4. Market positioning and competitive analysis
            5. Strategic insights and interview intelligence

        Output:
            - File: output/company_research.json
            - Structure: CompanyResearch Pydantic model
            - Contains: Company insights, culture, market position, and intelligence

        Returns:
            Task: Configured company research task instance
        """
        return Task(
            config=self.tasks_config["research_company_task"],
            output_file="output/company_research.json",
            output_pydantic=CompanyResearch,
        )

    @task
    def generate_cover_letter_task(self) -> Task:
        """
        Create the cover letter analysis task.

        This task analyzes cover letter requirements and generates metadata
        for the cover letter creation process, including personalization
        strategies and ATS optimization approaches.

        Process:
            1. Cover letter strategy development
            2. Personalization element identification
            3. ATS optimization planning
            4. Tone and style determination
            5. Content structure and approach analysis

        Output:
            - File: output/cover_letter_analysis.json
            - Structure: CoverLetterGeneration Pydantic model
            - Contains: Strategy, personalization, and optimization metadata

        Returns:
            Task: Configured cover letter analysis task instance
        """
        return Task(
            config=self.tasks_config["generate_cover_letter_task"],
            output_file="output/cover_letter_analysis.json",
            output_pydantic=CoverLetterGeneration,
        )

    @task
    def generate_cover_letter_content_task(self) -> Task:
        """
        Create the cover letter content generation task.

        This task generates the actual cover letter content using real candidate
        information, company research, and personalization strategies.

        Process:
            1. Contact information extraction from PDF
            2. Personalized content creation with company insights
            3. Achievement integration with quantified results
            4. ATS keyword optimization
            5. Professional business letter formatting

        Output:
            - File: output/cover_letter.md
            - Format: Professional markdown cover letter
            - Contains: Complete personalized cover letter content

        Returns:
            Task: Configured cover letter content generation task instance
        """
        return Task(
            config=self.tasks_config["generate_cover_letter_content_task"],
            output_file="output/cover_letter.md",
        )

    @task
    def generate_resume_task(self) -> Task:
        """
        Create the resume generation task.

        This task generates the optimized resume content by applying all
        previous recommendations and using real candidate information.

        Process:
            1. Real candidate information extraction
            2. ATS optimization implementation
            3. Keyword integration and enhancement
            4. Achievement amplification with metrics
            5. Professional formatting and presentation

        Output:
            - File: output/optimized_resume.md
            - Format: ATS-optimized markdown resume
            - Contains: Complete optimized resume with real candidate data

        Returns:
            Task: Configured resume generation task instance
        """
        return Task(
            config=self.tasks_config["generate_resume_task"],
            output_file="output/optimized_resume.md",
        )

    @task
    def generate_report_task(self) -> Task:
        """
        Create the final report generation task.

        This task synthesizes all previous analysis into an executive-level
        intelligence report with visual elements and strategic insights.

        Process:
            1. Comprehensive analysis synthesis
            2. Data visualization with Mermaid diagrams
            3. Interactive dashboard creation
            4. Predictive analytics and insights
            5. Strategic recommendations and action items

        Output:
            - File: output/final_report.md
            - Format: Executive markdown report with visuals
            - Contains: Complete intelligence report with diagrams and insights

        Returns:
            Task: Configured final report generation task instance
        """
        return Task(
            config=self.tasks_config["generate_report_task"],
            output_file="output/final_report.md",
        )

    # ========================================
    # CREW ORCHESTRATION
    # ========================================

    @crew
    def crew(self) -> Crew:
        """
        Create and configure the complete crew for resume optimization.

        This method assembles all agents and tasks into a cohesive workflow
        that processes sequentially through the optimization pipeline.

        Workflow Order:
            1. Job Analysis → Extract requirements and ATS keywords
            2. Resume Analysis → Evaluate current resume and compatibility
            3. Company Research → Gather intelligence and market insights
            4. Cover Letter Analysis → Plan personalization strategy
            5. Cover Letter Generation → Create personalized content
            6. Resume Generation → Apply optimizations with real data
            7. Report Generation → Synthesize insights into executive report

        Configuration:
            - Process: Sequential (each task builds on previous results)
            - Verbose: Enabled for detailed execution logging
            - Knowledge Sources: Shared PDF resume across all agents
            - Context Passing: Automatic between sequential tasks

        Returns:
            Crew: Configured crew instance ready for execution

        Example:
            crew = ResumeCrew()
            inputs = {"job_url": "...", "company_name": "..."}
            result = crew.crew().kickoff(inputs=inputs)
        """
        return Crew(
            agents=self.agents,  # All 6 specialized agents
            tasks=self.tasks,  # All 7 sequential tasks
            verbose=True,  # Enable detailed logging
            process=Process.sequential,  # Sequential task execution
            knowledge_sources=[self.resume_pdf],  # Shared PDF knowledge
        )
