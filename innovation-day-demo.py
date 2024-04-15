import os
from dotenv import load_dotenv
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

crew = Crew(
  agents=[
      Agents.business_analyst_agent(),
      Agents.tech_lead_agent(),
      Agents.qa_engineeer_agent()
  ],
  tasks=[
      Tasks.identify_gather_requirements_task(),
      Tasks.refine_requirements_feasability_task(),
      Tasks.define_story_task(),
      Tasks.define_execution_plan(),
      Tasks.define_testing_plan()
  ],
  process=Process.hierarchical,
  memory=True,
  cache=True,
  manager_llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7),
  verbose=1, # You can set it to 1 or 2 to different logging levels
)

# Get your crew to work!
result = crew.kickoff()

print("######################")
print(result)