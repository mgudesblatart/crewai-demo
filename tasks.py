from textwrap import dedent
from crewai import Task


class Tasks:
    def identify_gather_requirements_task(self, agent, user_requirements):
        return Task(
            description=dedent(
                f"""
        Based on the given {user_requirements}, collaborate with the rest of the team to understand and assess any gaps in understanding.
        Create a "Jira Story Ticket" to expand upon the feature request.
        Utilize best practices to define the feature and all of the Acceptance Criteria.
        Work with the Tech Lead to ensure feasibility of the feature and refine Acceptance Criteria for Developer understanding.
        The template for the story will be provided in the Best Practices document.
        Query the user to further develop a holistic understanding of the requirements for the feature, including deadlines. Output a first draft of the "Jira Story Ticket". Save it to Jira.
        Remember the Jira Ticket ID.

        This feature has a large impact on the organization's success. Doing a good job here will lead to promotions and accolades for the team.
      """
            ),
            agent=agent,
            human_input=True,
        )

    def refine_requirements_feasability_task(self, agent):
        return Task(
            description=dedent(
                f"""
        Review the requirements set out by the Business Analyst in the "Jira Story Ticket" for development feasibility.
        Identify steps for implementation.
        Append technical thoughts and details onto the "Jira Story Ticket" that will be communicated to the development team.
        Add additional notes/challenges based on experience handling similar features in the past.
        Outline dependencies on additional teams (such as UX, QA, DevOps, etc.) to ensure that all potential impediments are considered.
        Ensure that feature delivery is achievable for a team of two Senior Full Stack Developers and three Junior Full Stack Developers.
        Ensure that the scope of the work can be accomplished in the timelines provided, challenge what is absolutely required versus what are nice to haves.
        Update the "Jira Story Ticket" accordingly.

        Ensuring the work-life balance of your developers is important to consider against the impact of the work to the organization as a whole.
      """
            ),
            agent=agent,
            context=[self.identify_gather_requirements_task]
        )

    def define_story_task(self, agent):
        return Task(
            description=dedent(
                f"""
        Now that the Tech Lead has had a say on the "Jira Story Ticket", come up with a final draft of the story.
        Use best practices for BDD and the user story template.
        Save the final draft of the story to Jira.

        Clean, legible, and actionable Acceptance Criteria reflect well upon your performance.
      """
            ),
            agent=agent,
            context=[self.refine_requirements_feasability_task]
        )

    def define_execution_plan(self, agent):
        return Task(
            description=dedent(
                f"""
        Come up with the development steps required to achieve the Acceptance Criteria outlined in the "Jira Story Ticket".
        Update the ticket in Jira in the "Technical Details" section.
        Ensure that each step of the technical execution plan has a rough estimate of delivery time.
      """
            ),
            agent=agent,
            context=[self.refine_requirements_feasability_task]
        )

    def define_testing_plan(self, agent):
        return Task(
            description=dedent(
                f"""
        Review the business requirements and development steps to create a step by step Testing Plan.
        The testing plan will ensure that all of the Acceptance Criteria are met.
        The testing plan will ensure that the code that is produced by the development team satisfies the requirements laid out in the "Jira Story Ticket".
        The testing plan will also identify edge cases to ensure that the full gamut of user experience is accounted for.
        The Testing Plan steps will be broken down into individual "Sub Tasks", and added to the "Jira Story Ticket".
        Include additional tests for User edge cases to cover unconsidered user inputs and interactions.
        Consider the unhappy paths to ensure that those are tested as well.
        Update the "Jira Story Ticket" with the testing plan in the "Testing Plan" section.
        Create subtasks for each step in the testing plan.

        For every bug you find, you get to brag to the tech lead for not having addressed it.
      """
            ),
            agent=agent,
            context=[self.refine_requirements_feasability_task]
        )
