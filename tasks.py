import os
from textwrap import dedent
from crewai import Task
from tools.jira_tools import JIRATools
from tools.human_tools import HumanTools
from crewai_tools import DirectoryReadTool, TXTSearchTool, WebsiteSearchTool

class Tasks:
    def __init__(self):
        current_file_path = os.path.realpath(__file__)
        current_directory = os.path.dirname(current_file_path)
        relative_path = os.path.join(current_directory, 'templates')
        self.jira_tools = JIRATools()
        self.directory_tool = DirectoryReadTool(relative_path)
        self.text_tool = TXTSearchTool(txt=os.path.join(relative_path, 'jiraTemplate.txt'))
        # self.website_tool = WebsiteSearchTool(website="https://www.jira-templates.com/issues/story-template")
        self.human_tools = HumanTools()

    def identify_gather_requirements_task(self, agent, user_requirements):
        return Task(
            description=dedent(
                f"""\
        Based on the given {user_requirements}, create a "Jira Ticket" to implement the feature request.
        The ticket description should include the expected value this will bring to the users.
        The ticket description should include detailed acceptance critera in a numbered list. The acceptance criteria should be written in a Given, When, Then format.
        Use the template provided in jiraTemplate.txt as a starting point.
        You can ask the user for additional context if necessary, make sure that your questions are specific.
      """
            ),
            expected_output="JIRA ticket key",
            agent=agent,
            # human_input=True,
            tools=[self.jira_tools.create_ticket, self.text_tool, self.human_tools.get_user_input],
        )

    def refine_requirements_feasability_task(self, agent, context_task):
        return Task(
            description=dedent(
                f"""\
        Review the requirements set out by the Business Analyst in the "Jira Ticket" for development feasibility.
        
        Make sure to use appropriate, efficient, and cost effective technologies to accomplish this feature. The simpler the stack the better.

        Update JIRA ticket with implementation steps for the requested feature and additional notes/challenges based on experience handling similar features in the past.

        Use the "Update JIRA ticket" tool to append additional information to the original description of the Jira ticket.
        Do NOT overwrite what was there previously.

        Please make sure to pass on the JIRA ticket key that was worked on.
      """
            ),
            expected_output="JIRA ticket key",
            agent=agent,
            context=[context_task],
            tools=[self.jira_tools.get_ticket, self.jira_tools.update_ticket],
        )

    def define_story_task(self, agent, context_task):
        return Task(
            description=dedent(
                f"""\
        Come up with a final draft of the story.
        Use best practices for BDD and the user story template.

        Use the "Update JIRA ticket" tool to append additional information to the original description of the Jira ticket.
        Do NOT overwrite what was there previously.
      """
            ),
            expected_output="JIRA key of updated ticket",
            agent=agent,
            context=[context_task],
            tools=[self.jira_tools.get_ticket, self.jira_tools.update_ticket],
        )

    def define_execution_plan(self, agent, context_task):
        return Task(
            description=dedent(
                f"""\
        Come up with the development steps required to achieve the Acceptance Criteria outlined in the "Jira Ticket".
        Update the ticket in Jira in the "Technical Details" section.

        Get the description of the ticket and update the ticket with your notes appended to the existing description. Do NOT overwrite what was there previously.
      """
            ),
            expected_output="JIRA key of updated ticket",
            agent=agent,
            context=[context_task],
            tools=[self.jira_tools.get_ticket, self.jira_tools.update_ticket],
        )

    def define_testing_plan(self, agent, context_task):
        return Task(
            description=dedent(
                f"""\
        Review the acceptance criteria in the JIRA ticket and use the "Create JIRA subtask" tool 
        to create a subtask for each step in the testing plan with descriptions in a "given, when, then" format.
      """
            ),
            expected_output="Jira keys of the new created subtasks",
            agent=agent,
            context=[context_task],
            tools=[self.jira_tools.get_ticket, self.jira_tools.create_subtask],
        )
