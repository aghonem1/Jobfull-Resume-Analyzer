from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, confloat


class ATSKeyword(BaseModel):
    keyword: str = Field(description="The keyword or phrase")
    importance: int = Field(description="Importance level (1-5)", ge=1, le=5)
    category: str = Field(description="Category: technical, soft, experience, industry")
    required: bool = Field(description="Whether this keyword is required or preferred")
    frequency: int = Field(
        description="Number of times mentioned in job description", default=1
    )


class ATSOptimization(BaseModel):
    ats_compatibility_score: confloat(ge=0, le=1) = Field(
        description="Overall ATS compatibility score (0-1)"
    )
    keyword_density: Dict[str, float] = Field(
        description="Keyword density analysis (keyword: density_percentage)",
        default_factory=dict,
    )
    format_compliance: Dict[str, bool] = Field(
        description="Format compliance checklist",
        default_factory=lambda: {
            "single_column": True,
            "standard_fonts": True,
            "no_tables": True,
            "no_images": True,
            "no_headers_footers": True,
            "standard_sections": True,
            "doc_format": True,
        },
    )
    optimization_suggestions: List[str] = Field(
        description="Specific ATS optimization recommendations", default_factory=list
    )
    parsing_warnings: List[str] = Field(
        description="Potential parsing issues to address", default_factory=list
    )


class SkillScore(BaseModel):
    skill_name: str = Field(description="Name of the skill being scored")
    required: bool = Field(description="Whether this skill is required or nice-to-have")
    match_level: confloat(ge=0, le=1) = Field(
        description="How well the candidate's experience matches (0-1)"
    )
    years_experience: Optional[float] = Field(
        description="Years of experience with this skill", default=None
    )
    context_score: confloat(ge=0, le=1) = Field(
        description="How relevant the skill usage context is to the job requirements",
        default=0.5,
    )
    ats_keyword_match: bool = Field(
        description="Whether this skill matches ATS keywords", default=False
    )


class JobMatchScore(BaseModel):
    overall_match: confloat(ge=0, le=100) = Field(
        description="Overall match percentage (0-100)"
    )
    technical_skills_match: confloat(ge=0, le=100) = Field(
        description="Technical skills match percentage"
    )
    soft_skills_match: confloat(ge=0, le=100) = Field(
        description="Soft skills match percentage"
    )
    experience_match: confloat(ge=0, le=100) = Field(
        description="Experience level match percentage"
    )
    education_match: confloat(ge=0, le=100) = Field(
        description="Education requirements match percentage"
    )
    industry_match: confloat(ge=0, le=100) = Field(
        description="Industry experience match percentage"
    )
    ats_compatibility: confloat(ge=0, le=100) = Field(
        description="ATS compatibility score", default=0
    )
    skill_details: List[SkillScore] = Field(
        description="Detailed scoring for each skill", default_factory=list
    )
    strengths: List[str] = Field(
        description="List of areas where candidate exceeds requirements",
        default_factory=list,
    )
    gaps: List[str] = Field(
        description="List of areas needing improvement", default_factory=list
    )
    ats_gaps: List[str] = Field(
        description="List of ATS-specific gaps and recommendations",
        default_factory=list,
    )
    scoring_factors: Dict[str, float] = Field(
        description="Weights used for different scoring components",
        default_factory=lambda: {
            "technical_skills": 0.35,
            "soft_skills": 0.20,
            "experience": 0.25,
            "education": 0.10,
            "industry": 0.10,
        },
    )


class JobRequirements(BaseModel):
    technical_skills: List[str] = Field(
        description="List of required technical skills", default_factory=list
    )
    soft_skills: List[str] = Field(
        description="List of required soft skills", default_factory=list
    )
    experience_requirements: List[str] = Field(
        description="List of experience requirements", default_factory=list
    )
    key_responsibilities: List[str] = Field(
        description="List of key job responsibilities", default_factory=list
    )
    education_requirements: List[str] = Field(
        description="List of education requirements", default_factory=list
    )
    nice_to_have: List[str] = Field(
        description="List of preferred but not required skills", default_factory=list
    )
    job_title: str = Field(description="Official job title", default="")
    department: Optional[str] = Field(
        description="Department or team within the company", default=None
    )
    reporting_structure: Optional[str] = Field(
        description="Who this role reports to and any direct reports", default=None
    )
    job_level: Optional[str] = Field(
        description="Level of the position (e.g., Entry, Senior, Lead)", default=None
    )
    location_requirements: Dict[str, str] = Field(
        description="Location details including remote/hybrid options",
        default_factory=dict,
    )
    work_schedule: Optional[str] = Field(
        description="Expected work hours and schedule flexibility", default=None
    )
    travel_requirements: Optional[str] = Field(
        description="Expected travel frequency and scope", default=None
    )
    compensation: Dict[str, str] = Field(
        description="Salary range and compensation details if provided",
        default_factory=dict,
    )
    benefits: List[str] = Field(
        description="List of benefits and perks", default_factory=list
    )
    tools_and_technologies: List[str] = Field(
        description="Specific tools, software, or technologies used",
        default_factory=list,
    )
    industry_knowledge: List[str] = Field(
        description="Required industry-specific knowledge", default_factory=list
    )
    certifications_required: List[str] = Field(
        description="Required certifications or licenses", default_factory=list
    )
    security_clearance: Optional[str] = Field(
        description="Required security clearance level if any", default=None
    )
    team_size: Optional[str] = Field(
        description="Size of the immediate team", default=None
    )
    key_projects: List[str] = Field(
        description="Major projects or initiatives mentioned", default_factory=list
    )
    cross_functional_interactions: List[str] = Field(
        description="Teams or departments this role interacts with",
        default_factory=list,
    )
    career_growth: List[str] = Field(
        description="Career development and growth opportunities", default_factory=list
    )
    training_provided: List[str] = Field(
        description="Training or development programs offered", default_factory=list
    )
    diversity_inclusion: Optional[str] = Field(
        description="D&I statements or requirements", default=None
    )
    company_values: List[str] = Field(
        description="Company values mentioned in the job posting", default_factory=list
    )
    job_url: str = Field(description="URL of the job posting", default="")
    posting_date: Optional[str] = Field(
        description="When the job was posted", default=None
    )
    application_deadline: Optional[str] = Field(
        description="Application deadline if specified", default=None
    )
    special_instructions: List[str] = Field(
        description="Any special application instructions or requirements",
        default_factory=list,
    )
    # ATS-specific enhancements
    ats_keywords: List[ATSKeyword] = Field(
        description="Extracted ATS keywords with importance and categorization",
        default_factory=list,
    )
    ats_system_type: Optional[str] = Field(
        description="Detected ATS system (Workday, Greenhouse, etc.)", default=None
    )
    format_requirements: Dict[str, str] = Field(
        description="Specific format requirements for this job/company",
        default_factory=dict,
    )
    industry_trends_2025: List[str] = Field(
        description="2025 industry-specific trending keywords", default_factory=list
    )
    match_score: JobMatchScore = Field(
        description="Detailed scoring of how well the candidate matches the job requirements",
        default_factory=JobMatchScore,
    )
    score_explanation: List[str] = Field(
        description="Detailed explanation of how scores were calculated",
        default_factory=list,
    )


class ResumeOptimization(BaseModel):
    content_suggestions: List[Dict[str, str]] = Field(
        description="List of content optimization suggestions with 'before' and 'after' examples"
    )
    skills_to_highlight: List[str] = Field(
        description="List of skills that should be emphasized based on job requirements"
    )
    achievements_to_add: List[str] = Field(
        description="List of achievements that should be added or modified"
    )
    keywords_for_ats: List[str] = Field(
        description="List of important keywords for ATS optimization"
    )
    formatting_suggestions: List[str] = Field(
        description="List of formatting improvements"
    )
    # ATS-specific enhancements
    ats_optimization: ATSOptimization = Field(
        description="ATS-specific optimization analysis and recommendations",
        default_factory=ATSOptimization,
    )
    keyword_integration_strategy: Dict[str, List[str]] = Field(
        description="Strategy for integrating keywords into specific resume sections",
        default_factory=dict,
    )
    content_originality_check: Dict[str, bool] = Field(
        description="Check for original content vs AI-generated or copied text",
        default_factory=dict,
    )
    section_optimization: Dict[str, List[str]] = Field(
        description="Section-specific optimization recommendations",
        default_factory=dict,
    )


class CompanyResearch(BaseModel):
    recent_developments: List[str] = Field(
        description="List of recent company news and developments"
    )
    culture_and_values: List[str] = Field(
        description="Key points about company culture and values"
    )
    market_position: Dict[str, List[str]] = Field(
        description="Information about market position, including competitors and industry standing"
    )
    growth_trajectory: List[str] = Field(
        description="Information about company's growth and future plans"
    )
    interview_questions: List[str] = Field(
        description="Strategic questions to ask during the interview"
    )
    # Enhanced for cover letter generation
    company_priorities: List[str] = Field(
        description="Current company priorities and focus areas", default_factory=list
    )
    leadership_team: List[str] = Field(
        description="Key leadership team members and their backgrounds",
        default_factory=list,
    )
    competitive_advantages: List[str] = Field(
        description="What sets this company apart from competitors",
        default_factory=list,
    )
    recent_achievements: List[str] = Field(
        description="Recent company achievements and milestones", default_factory=list
    )


class CoverLetterGeneration(BaseModel):
    """Model for cover letter generation output"""

    cover_letter_content: str = Field(
        description="Complete cover letter content in markdown format"
    )

    personalization_elements: List[str] = Field(
        description="List of personalized elements included (company name, specific role, achievements, etc.)",
        default_factory=list,
    )

    key_selling_points: List[str] = Field(
        description="Top 3-5 selling points highlighted in the cover letter",
        default_factory=list,
    )

    company_connections: List[str] = Field(
        description="Specific company values, culture, or projects mentioned",
        default_factory=list,
    )

    call_to_action: str = Field(
        description="Specific call to action used in the closing paragraph", default=""
    )

    tone_and_style: Dict[str, str] = Field(
        description="Tone and style characteristics (formal/casual, industry-appropriate, etc.)",
        default_factory=dict,
    )

    ats_optimization: Dict[str, Any] = Field(
        description="ATS optimization elements included (keywords, formatting, etc.)",
        default_factory=dict,
    )

    length_metrics: Dict[str, int] = Field(
        description="Length metrics (word count, paragraph count, etc.)",
        default_factory=dict,
    )

    customization_level: confloat(ge=0, le=1) = Field(
        description="Level of customization vs template usage (0=template, 1=fully custom)",
        default=0.8,
    )

    impact_score: confloat(ge=0, le=1) = Field(
        description="Predicted impact score based on personalization and relevance",
        default=0.7,
    )
