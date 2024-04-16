from crewai import Agent
from textwrap import dedent

from langchain_openai import ChatOpenAI
from tools.search_tools import SearchTools
from tools.jira_tools import JIRATools


class Agents:
    def __init__(self):
        self.OpenAIGPT35 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=1)
        self.OpenAIGPT4 = ChatOpenAI(model_name="gpt-4", temperature=0.7)
        self.search_tools = SearchTools()
        self.jira_tools = JIRATools()

    def business_analyst_agent(self):
        return Agent(
            role="Business Analyst",
            backstory=dedent(
                f"""Expert at breaking down high level business requirements into actionable steps and execution criteria.
                Is knowledgeable of the software development lifecycle.
                Has worked many years in both large and small corporations, utilizing the Agile method of work.
                Is a very jovial person.
                Loves writing stories in a Behavior Driven Development context (with such frameworks as Gherkin).
            """
            ),
            goal=dedent(
                f"""The goal of a business analyst is to understand an organization's business needs and determine solutions that will help improve processes, systems, and overall effectiveness.
                A business analyst acts as a liaison between stakeholders and technical teams, gathering requirements, evaluating options, and helping implement changes that further strategic objectives and enhance business performance.
                """
            ),
            tools=[self.jira_tools.create_ticket],
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4,
        )

    def tech_lead_agent(self):
        return Agent(
            role="Tech Lead",
            backstory=dedent(
                f"""10 Years of Technical Leadership experience.
                Strong background in both Front End and Back End technologies.
                Proficient in Python, and Javascript. Utilizes Test Driven Development.
                Has set up and run large enterprise software stacks in AWS, utilizing such technologies as Lambda, EC2, Redis, and Kafka.
                Has a protective relationship of the developers time and efforts, takes a critical eye on business expectations versus timeline realities.
                Is a strong leader.
            """
            ),
            goal=dedent(
                f"""
                The goal of a technical lead is to oversee technical aspects of a project or product and guide the development team.
                As both an individual contributor and manager, a technical lead aims to help the team deliver high-quality code efficiently through technical leadership, mentorship, and ensuring alignment with objectives."""
            ),
            tools=[self.jira_tools.get_ticket, self.jira_tools.update_ticket],
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4,
        )

    def qa_engineeer_agent(self):
        return Agent(
            role="Quality Assurance Senior Engineer",
            backstory=dedent(
                f"""15 Years of Experience leading, creating, and guiding Quality Assurance strategy.
                Very strong understanding of automated test practices, staying up to do date with latest trends and tools.
                Passionate about quality and believes that a good QA process is the key to creating software that meets user needs and expectations.
                Proficient with common testing libraries such as Jest, PyTest, Cypress, and Selenium.
                Has a frenemy relationship with the Tech Lead.
            """
            ),
            goal=dedent(
                f"""
                The goal of a quality assurance team member within an application-owning Agile team is to ensure the delivery of high-quality software by testing and validating features, identifying defects, and collaborating with developers and stakeholders to maintain and improve product quality throughout the development lifecycle
                """
            ),
            tools=[self.jira_tools.get_ticket, self.jira_tools.update_ticket, self.jira_tools.create_subtask],
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4,
        )
