from textwrap import dedent

from crewai_tools import tool


class HumanTools:

    @tool("Ask the user for input")
    def get_user_input(prompt: str) -> str:
        """Used to prompt the user for additonal input. Returns user's input."""
        print("+++++++++++++++++++++ Prompting user for more information ++++++++++++++++++++++++++")
        user_input = input(
            dedent(
                f"""
                            {prompt}
                        """
            )
        )
        return user_input
