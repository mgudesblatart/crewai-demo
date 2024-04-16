import os
from dotenv import load_dotenv
from textwrap import dedent

load_dotenv()

from crewai.telemetry import Telemetry


def noop(*args, **kwargs):
    pass


for attr in dir(Telemetry):
    if callable(getattr(Telemetry, attr)) and not attr.startswith("__"):
        setattr(Telemetry, attr, noop)

from crewai import Crew, Process
from agents import Agents
from tasks import Tasks
from langchain_openai import ChatOpenAI


class DevelopmentCrew:
    def __init__(self, user_requirements):
        self.user_requirements = user_requirements

    def run(self):
        agents = Agents()
        tasks = Tasks()

        business_analyst_agent = agents.business_analyst_agent()
        tech_lead_agent = agents.tech_lead_agent()
        qa_engineer_agent = agents.qa_engineeer_agent()

        identify_gather_requirements_task = tasks.identify_gather_requirements_task(business_analyst_agent, self.user_requirements)
        refine_requirements_feasability_task = tasks.refine_requirements_feasability_task(tech_lead_agent,identify_gather_requirements_task)
        # define_story_task = tasks.define_story_task(business_analyst_agent, refine_requirements_feasability_task)
        # define_execution_plan = tasks.define_execution_plan(tech_lead_agent, refine_requirements_feasability_task)
        define_testing_plan = tasks.define_testing_plan(qa_engineer_agent, refine_requirements_feasability_task)

        crew = Crew(
            agents=[business_analyst_agent, tech_lead_agent, qa_engineer_agent],
            tasks=[
                identify_gather_requirements_task,
                refine_requirements_feasability_task,
                # define_story_task,
                # define_execution_plan,
                define_testing_plan,
            ],
            process=Process.sequential,
            memory=True,
            cache=False,
            # manager_llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7),
            verbose=1,  # You can set it to 1 or 2 to different logging levels
        )

        # Get your crew to work!
        result = crew.kickoff()
        return result


if __name__ == "__main__":
    print("## Welcome to Your Dev Team")
    print('-------------------------------')
    user_requirements = input(
    dedent("""
        What are your requirements for the feature?
    """))

    dev_crew = DevelopmentCrew(user_requirements)
    result = dev_crew.run()
    print("\n\n########################")
    print("##  All done! Here are the results")
    print("########################\n")
    print(result)
