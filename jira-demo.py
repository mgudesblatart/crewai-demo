import os
from dotenv import load_dotenv
load_dotenv()

from crewai.telemetry import Telemetry

def noop(*args, **kwargs):
    # with open("./logfile.txt", "a") as f:
    #     f.write("Telemetry method called and noop'd\n")
    pass


for attr in dir(Telemetry):
    if callable(getattr(Telemetry, attr)) and not attr.startswith("__"):
        setattr(Telemetry, attr, noop)

from crewai import Agent, Task, Crew, Process
from tools.jira_tools import JIRATools
from langchain_openai import ChatOpenAI
llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)

# Define your agents with roles and goals
productOwner = Agent(
  role='Product Owner',
  goal='Create JIRA tickets that describe work for your team',
  backstory="""You work at a financial software startup.
  Your expertise lies in identifying user problems.
  You have a knack for breaking user issues into clear steps to implement.""",
  verbose=True,
  allow_delegation=False,
  tools=[JIRATools.create_ticket],
  llm=llm
)

testEngineer = Agent(
  role='Testing Engineer',
  goal='Create subtasks for testing on JIRA tickets created by the Product Owner',
  backstory="""You work at a financial software startup.
  Your expertise lies in taking user stories and creating test cases.
  You have a knack for identifying edge cases.""",
  verbose=True,
  allow_delegation=False,
  tools=[JIRATools.create_subtask],
  llm=llm
)

# Create tasks for your agents
task1 = Task(
  description="""Create one JIRA ticket for creating a user profile page""",
  expected_output="id of the created ticket",
  agent=productOwner
)

task2 = Task(
  description="""Take the issue created by the product owner and create subtasks for test cases""",
  expected_output="id of the created tickets",
  agent=testEngineer
)

crew = Crew(
  agents=[productOwner, testEngineer],
  tasks=[task1, task2],
  verbose=1, # You can set it to 1 or 2 to different logging levels
)

# Get your crew to work!
result = crew.kickoff()

print("######################")
print(result)