#!/usr/bin/env python
import warnings

from cv_opt.crew import ResumeCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the resume optimization crew.
    """
    inputs = {
        "job_url": "https://www.google.com/about/careers/applications/jobs/results/105532306164196038-gpu-silicon-architect",
        "company_name": "NVIDIA",
    }
    ResumeCrew().crew().kickoff(inputs=inputs)


if __name__ == "__main__":
    run()
