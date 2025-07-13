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
    """ResumeCrew for resume optimization and interview preparation"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self) -> None:
        """Sample resume PDF for testing"""
        self.resume_pdf = PDFKnowledgeSource(file_paths="GhonemCV_2025.pdf")

    @agent
    def resume_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config["resume_analyzer"],
            verbose=True,
            llm=LLM("gpt-4o-mini"),
            knowledge_sources=[self.resume_pdf],
        )

    @agent
    def job_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config["job_analyzer"],
            verbose=True,
            tools=[ScrapeWebsiteTool()],
            llm=LLM("gpt-4o-mini"),
        )

    @agent
    def company_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["company_researcher"],
            verbose=True,
            tools=[SerperDevTool()],
            llm=LLM("gpt-4o-mini"),
            knowledge_sources=[self.resume_pdf],
        )

    @agent
    def cover_letter_generator(self) -> Agent:
        return Agent(
            config=self.agents_config["cover_letter_generator"],
            verbose=True,
            llm=LLM("gpt-4o-mini"),
            knowledge_sources=[self.resume_pdf],
        )

    @agent
    def resume_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["resume_writer"],
            verbose=True,
            llm=LLM("gpt-4o-mini"),
            knowledge_sources=[self.resume_pdf],
        )

    @agent
    def report_generator(self) -> Agent:
        return Agent(
            config=self.agents_config["report_generator"],
            verbose=True,
            llm=LLM("gpt-4o-mini"),
            knowledge_sources=[self.resume_pdf],
        )

    @task
    def analyze_job_task(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_job_task"],
            output_file="output/job_analysis.json",
            output_pydantic=JobRequirements,
        )

    @task
    def optimize_resume_task(self) -> Task:
        return Task(
            config=self.tasks_config["optimize_resume_task"],
            output_file="output/resume_optimization.json",
            output_pydantic=ResumeOptimization,
        )

    @task
    def research_company_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_company_task"],
            output_file="output/company_research.json",
            output_pydantic=CompanyResearch,
        )

    @task
    def generate_cover_letter_task(self) -> Task:
        return Task(
            config=self.tasks_config["generate_cover_letter_task"],
            output_file="output/cover_letter_analysis.json",
            output_pydantic=CoverLetterGeneration,
        )

    @task
    def generate_cover_letter_content_task(self) -> Task:
        return Task(
            config=self.tasks_config["generate_cover_letter_content_task"],
            output_file="output/cover_letter.md",
        )

    @task
    def generate_resume_task(self) -> Task:
        return Task(
            config=self.tasks_config["generate_resume_task"],
            output_file="output/optimized_resume.md",
        )

    @task
    def generate_report_task(self) -> Task:
        return Task(
            config=self.tasks_config["generate_report_task"],
            output_file="output/final_report.md",
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=True,
            process=Process.sequential,
            knowledge_sources=[self.resume_pdf],
        )
