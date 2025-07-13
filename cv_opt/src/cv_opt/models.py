"""
Jobfull Resume Analyzer - Data Models Module

This module defines the Pydantic data models used throughout the resume optimization
workflow. These models ensure type safety, data validation, and structured output
for all AI agent interactions and file outputs.

Model Hierarchy:
    1. Core Data Models:
       - ATSKeyword: Individual keyword analysis with importance scoring
       - SkillScore: Detailed skill matching and scoring
       - JobMatchScore: Comprehensive candidate-job fit analysis

    2. Agent Output Models:
       - JobRequirements: Job analysis and ATS keyword extraction
       - ResumeOptimization: Resume analysis and optimization recommendations
       - CompanyResearch: Company intelligence and market analysis
       - CoverLetterGeneration: Cover letter strategy and content analysis

    3. Supporting Models:
       - ATSOptimization: ATS-specific scoring and recommendations
       - Various scoring and analysis components

Data Validation:
    All models use Pydantic for automatic validation, type checking, and
    serialization. Field constraints ensure data integrity and consistency
    across the entire workflow.

ATS Optimization Focus:
    Models are specifically designed for 2025 ATS compatibility, including:
    - Keyword importance scoring (1-5 scale)
    - ATS system-specific compatibility (Workday, Greenhouse, etc.)
    - Format compliance verification
    - Content authenticity checks
    - Industry trend integration

Author: Jobfull Team
Version: 1.0.0
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, confloat

# ========================================
# CORE DATA MODELS
# ========================================
# Foundation models used across multiple agents


class ATSKeyword(BaseModel):
    """
    Represents a single ATS keyword with importance and categorization.

    This model captures individual keywords extracted from job postings,
    including their importance level, category, and frequency. Used by
    the Job Analyzer agent to provide structured keyword analysis.

    ATS Optimization:
        - Importance levels help prioritize keyword integration
        - Categories enable targeted optimization strategies
        - Frequency tracking supports natural density optimization

    Attributes:
        keyword (str): The actual keyword or phrase
        importance (int): Priority level from 1-5 (5 being most critical)
        category (str): Categorization for targeted optimization
        required (bool): Whether keyword is required vs. preferred
        frequency (int): Occurrence count in job description

    Example:
        ATSKeyword(
            keyword="machine learning",
            importance=5,
            category="technical",
            required=True,
            frequency=3
        )
    """

    keyword: str = Field(description="The keyword or phrase")
    importance: int = Field(description="Importance level (1-5)", ge=1, le=5)
    category: str = Field(description="Category: technical, soft, experience, industry")
    required: bool = Field(description="Whether this keyword is required or preferred")
    frequency: int = Field(
        description="Number of times mentioned in job description", default=1
    )


class ATSOptimization(BaseModel):
    """
    Comprehensive ATS optimization analysis and recommendations.

    This model captures detailed ATS compatibility assessment including
    scoring, format compliance, and specific optimization strategies.
    Used by the Resume Analyzer agent for systematic ATS evaluation.

    2025 ATS Standards:
        - Compatibility scoring across major ATS systems
        - Format compliance for modern parsing algorithms
        - Keyword density optimization for natural integration
        - AI detection avoidance strategies

    Attributes:
        ats_compatibility_score (float): Overall ATS score (0-1)
        keyword_density (Dict[str, float]): Keyword density analysis
        format_compliance (Dict[str, bool]): Format compliance checklist
        optimization_suggestions (List[str]): Specific recommendations
        parsing_warnings (List[str]): Potential parsing issues

    Example:
        ATSOptimization(
            ats_compatibility_score=0.85,
            keyword_density={"python": 2.3, "sql": 1.8},
            format_compliance={"single_column": True, "standard_fonts": True},
            optimization_suggestions=["Add SQL keyword to skills section"]
        )
    """

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
    """
    Detailed skill matching and scoring for individual competencies.

    This model provides granular analysis of how well a candidate's
    skills match job requirements, including experience context and
    ATS keyword alignment. Used for comprehensive skill gap analysis.

    Scoring Components:
        - Match level: How well experience aligns with requirements
        - Context score: Relevance of skill usage to job context
        - ATS keyword match: Whether skill matches ATS keywords
        - Experience quantification: Years of relevant experience

    Attributes:
        skill_name (str): Name of the skill being evaluated
        required (bool): Whether skill is required vs. nice-to-have
        match_level (float): Experience alignment score (0-1)
        years_experience (float): Years of relevant experience
        context_score (float): Context relevance score (0-1)
        ats_keyword_match (bool): ATS keyword alignment status

    Example:
        SkillScore(
            skill_name="Python",
            required=True,
            match_level=0.9,
            years_experience=5.0,
            context_score=0.8,
            ats_keyword_match=True
        )
    """

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
    """
    Comprehensive candidate-job fit analysis with detailed scoring.

    This model provides multi-dimensional scoring of how well a candidate
    matches job requirements, including strengths, gaps, and ATS compatibility.
    Used by the Job Analyzer agent for holistic candidate assessment.

    Scoring Dimensions:
        - Technical skills: Programming, tools, technologies
        - Soft skills: Communication, leadership, problem-solving
        - Experience: Years, industry, role level
        - Education: Degree requirements, certifications
        - Industry: Sector-specific knowledge and experience
        - ATS compatibility: Keyword and format alignment

    Attributes:
        overall_match (float): Overall fit percentage (0-100)
        technical_skills_match (float): Technical competency alignment
        soft_skills_match (float): Soft skills alignment
        experience_match (float): Experience level alignment
        education_match (float): Education requirements alignment
        industry_match (float): Industry experience alignment
        ats_compatibility (float): ATS optimization score
        skill_details (List[SkillScore]): Individual skill assessments
        strengths (List[str]): Areas of candidate strength
        gaps (List[str]): Areas needing improvement
        ats_gaps (List[str]): ATS-specific optimization needs
        scoring_factors (Dict[str, float]): Weighting factors used

    Example:
        JobMatchScore(
            overall_match=85.0,
            technical_skills_match=90.0,
            soft_skills_match=80.0,
            experience_match=85.0,
            strengths=["Strong Python skills", "ML expertise"],
            gaps=["Limited SQL experience"],
            ats_gaps=["Need to add cloud keywords"]
        )
    """

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
            "technical_skills": 0.3,
            "soft_skills": 0.2,
            "experience": 0.25,
            "education": 0.15,
            "industry": 0.1,
        },
    )


# ========================================
# AGENT OUTPUT MODELS
# ========================================
# Models representing the structured output of each AI agent


class JobRequirements(BaseModel):
    """
    Comprehensive job analysis output from the Job Analyzer agent.

    This model captures the complete analysis of a job posting including
    requirements, responsibilities, company information, and ATS optimization
    data. Serves as the foundation for all subsequent optimization tasks.

    Analysis Components:
        - Skills and requirements extraction
        - Company and role information
        - ATS keyword analysis with importance scoring
        - Candidate fit assessment and scoring
        - Industry trends and 2025 standards integration

    Key Features:
        - Structured requirement categorization
        - ATS keyword extraction with importance levels
        - Comprehensive candidate-job fit scoring
        - Industry trend integration for 2025 standards
        - Detailed company and role context

    Usage:
        Generated by the Job Analyzer agent as the first step in the
        optimization workflow. Used by all subsequent agents for
        context and optimization guidance.

    Example:
        JobRequirements(
            job_title="Senior Data Scientist",
            technical_skills=["Python", "SQL", "Machine Learning"],
            ats_keywords=[ATSKeyword(keyword="python", importance=5, ...)],
            match_score=JobMatchScore(overall_match=85.0, ...)
        )
    """

    # Core job requirements
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

    # Job and company context
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

    # Compensation and benefits
    compensation: Dict[str, str] = Field(
        description="Salary range and compensation details if provided",
        default_factory=dict,
    )
    benefits: List[str] = Field(
        description="List of benefits and perks", default_factory=list
    )

    # Technical and industry context
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

    # Team and organizational context
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

    # Growth and development
    career_growth: List[str] = Field(
        description="Career development and growth opportunities", default_factory=list
    )
    training_provided: List[str] = Field(
        description="Training or development programs offered", default_factory=list
    )

    # Company culture and values
    diversity_inclusion: Optional[str] = Field(
        description="D&I statements or requirements", default=None
    )
    company_values: List[str] = Field(
        description="Company values mentioned in the job posting", default_factory=list
    )

    # Job posting metadata
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

    # ATS-specific enhancements for 2025 standards
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

    # Candidate fit analysis
    match_score: JobMatchScore = Field(
        description="Detailed scoring of how well the candidate matches the job requirements",
        default_factory=JobMatchScore,
    )
    score_explanation: List[str] = Field(
        description="Detailed explanation of the scoring rationale",
        default_factory=list,
    )


class ResumeOptimization(BaseModel):
    """
    Resume analysis and optimization recommendations from the Resume Analyzer agent.

    This model captures comprehensive resume analysis including ATS compatibility,
    format compliance, keyword optimization, and specific improvement suggestions.
    Used to guide the Resume Writer agent in creating optimized content.

    Analysis Components:
        - Content optimization with before/after examples
        - Skills highlighting based on job requirements
        - Achievement enhancement recommendations
        - ATS keyword integration strategies
        - Format compliance and improvement suggestions

    ATS Optimization:
        - Compatibility scoring across major ATS systems
        - Format compliance verification for 2025 standards
        - Keyword density optimization strategies
        - Content authenticity verification
        - Section-specific optimization recommendations

    Usage:
        Generated by the Resume Analyzer agent after job analysis.
        Used by the Resume Writer agent to implement optimizations
        and by the Report Generator for comprehensive reporting.

    Example:
        ResumeOptimization(
            content_suggestions=[{"before": "Managed team", "after": "Led 8-person team"}],
            skills_to_highlight=["Python", "Machine Learning"],
            ats_optimization=ATSOptimization(ats_compatibility_score=0.85, ...)
        )
    """

    # Content optimization recommendations
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

    # ATS-specific enhancements for 2025 standards
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

    # Advanced optimization features
    industry_alignment: Dict[str, str] = Field(
        description="Industry-specific alignment recommendations",
        default_factory=dict,
    )
    competitive_positioning: List[str] = Field(
        description="Recommendations for competitive differentiation",
        default_factory=list,
    )
    quantification_opportunities: List[str] = Field(
        description="Opportunities to add metrics and quantified achievements",
        default_factory=list,
    )


class CompanyResearch(BaseModel):
    """
    Comprehensive company intelligence from the Company Researcher agent.

    This model captures detailed company analysis including recent developments,
    culture, market position, and strategic insights. Used to personalize
    cover letters and provide interview preparation intelligence.

    Research Components:
        - Recent company developments and news
        - Culture and values assessment
        - Market positioning and competitive analysis
        - Growth trajectory and strategic initiatives
        - Leadership team and organizational insights

    Intelligence Features:
        - Strategic interview questions and talking points
        - Company priorities and focus areas
        - Competitive advantages and differentiation
        - Cultural fit assessment indicators
        - Market trends and industry context

    Usage:
        Generated by the Company Researcher agent after resume analysis.
        Used by the Cover Letter Generator for personalization and
        by the Report Generator for comprehensive intelligence reporting.

    Example:
        CompanyResearch(
            recent_developments=["AI product launch", "Series C funding"],
            culture_and_values=["Innovation", "Diversity", "Sustainability"],
            market_position={"competitors": ["Company A", "Company B"]},
            interview_questions=["Tell me about your AI experience"]
        )
    """

    # Core company intelligence
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

    # Enhanced intelligence for cover letter generation
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
        description="Notable company achievements and milestones",
        default_factory=list,
    )

    # Strategic insights and intelligence
    strategic_initiatives: List[str] = Field(
        description="Major strategic initiatives and investments",
        default_factory=list,
    )
    technology_focus: List[str] = Field(
        description="Technology areas and innovation focus",
        default_factory=list,
    )
    market_challenges: List[str] = Field(
        description="Current market challenges and competitive pressures",
        default_factory=list,
    )
    expansion_plans: List[str] = Field(
        description="Geographic or market expansion plans",
        default_factory=list,
    )

    # Cultural and workplace insights
    employee_sentiment: Dict[str, str] = Field(
        description="Employee satisfaction and sentiment analysis",
        default_factory=dict,
    )
    workplace_culture: Dict[str, str] = Field(
        description="Workplace culture characteristics and environment",
        default_factory=dict,
    )
    diversity_initiatives: List[str] = Field(
        description="Diversity, equity, and inclusion initiatives",
        default_factory=list,
    )


class CoverLetterGeneration(BaseModel):
    """
    Cover letter strategy and content analysis from the Cover Letter Generator agent.

    This model captures the strategic approach to cover letter creation including
    personalization elements, key selling points, company connections, and
    optimization metrics. Used to guide content creation and measure effectiveness.

    Content Strategy:
        - Personalization elements and company-specific insights
        - Key selling points and value proposition
        - Company connections and cultural alignment
        - Professional tone and style characteristics
        - ATS optimization and keyword integration

    Quality Metrics:
        - Customization level vs. template usage
        - Impact score based on personalization and relevance
        - Length metrics and professional presentation
        - ATS compatibility and keyword density

    Usage:
        Generated by the Cover Letter Generator agent after company research.
        Used to create the actual cover letter content and measure
        effectiveness of personalization strategies.

    Example:
        CoverLetterGeneration(
            personalization_elements=["Company name", "Recent product launch"],
            key_selling_points=["5 years ML experience", "Leadership skills"],
            company_connections=["Shared values on innovation"],
            customization_level=0.9,
            impact_score=0.85
        )
    """

    # Core cover letter content
    cover_letter_content: str = Field(
        description="Complete cover letter content in markdown format"
    )

    # Personalization and strategy
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

    # Style and presentation
    tone_and_style: Dict[str, str] = Field(
        description="Tone and style characteristics (formal/casual, industry-appropriate, etc.)",
        default_factory=dict,
    )

    # ATS optimization and metrics
    ats_optimization: Dict[str, Any] = Field(
        description="ATS optimization elements included (keywords, formatting, etc.)",
        default_factory=dict,
    )
    length_metrics: Dict[str, int] = Field(
        description="Length metrics (word count, paragraph count, etc.)",
        default_factory=dict,
    )

    # Quality and effectiveness measures
    customization_level: confloat(ge=0, le=1) = Field(
        description="Level of customization vs template usage (0=template, 1=fully custom)",
        default=0.8,
    )
    impact_score: confloat(ge=0, le=1) = Field(
        description="Predicted impact score based on personalization and relevance",
        default=0.7,
    )
