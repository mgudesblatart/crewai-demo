from crewai import Task

class TestTask:
  def identify_gather_requirements_task(self, agent, user_requirements):
    return Task(
      description="""
        Based on the given {user_requirements}, collaborate with the rest of the 
        team to understand and assess any gaps in understanding. Query the user to 
        further develop a holistic understanding of the requirements for the feature, 
        including deadlines. Output a first draft of the Jira Story Ticket. Save it 
        to Jira. Remember the Jira Ticket ID.
      """,
      agent=agent,
      human_input=True,
    )
  
  def refine_requirements_feasability_task(self, agent):
    return Task(
      description="""
        Review the draft of the Jira Story Ticket for developer feasibility.
        Add additional notes/challenges based on experience handling similar features in the past.
        Outline dependencies on additional teams (such as UX, QA, DevOps, etc.) to ensure that all potential impediments are considered.
        Ensure that feature delivery is achievable for a team of two Senior Full Stack Developers and three Junior Full Stack Developers.
        Ensure that the scope of the work can be accomplished in the timelines provided, challenge what is absolutely required versus what are nice to haves.
        Update the Jira Story Ticket accordingly.
      """,
      agent=agent,
    )
    
  def define_story_task(self, agent):
    return Task(
      description="""
        Now that the Tech Lead has had a say on the Jira Story Ticket, come up with a final draft of the story.
        Use best practices for BDD and the user story template.
        Save the final draft of the story to Jira.
      """,
      agent=agent,
    )  
    
  def define_execution_plan(self, agent):
    return Task(
      description="""
        Come up with the development steps required to achieve the Acceptance Criteria outlined in the Jira Story Ticket.
        Update the ticket in Jira in the "Technical Details" section.
        Ensure that each step of the technical execution plan has a rough estimate of delivery time.
      """,
      agent=agent,
    )
    
  def define_testing_plan(self, agent):
    return Task(
      description="""
        Come up with a testing plan to ensure that all of the Acceptance Criteria are met.
        Include additional tests for User edge cases to cover unconsidered user inputs and interactions.
        Consider the unhappy paths to ensure that those are tested as well.
        Update the Jira ticket with the testing plan in the "Testing Plan" section.
        Create subtasks for each step in the testing plan.
      """,
      agent=agent
    )        
