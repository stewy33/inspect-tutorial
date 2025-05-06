from inspect_ai.solver import basic_agent, system_message, solver, Solver
from inspect_ai.tool import bash, python


@solver
def agent() -> Solver:
    """Creates a basic agent that can use bash and python."""

    SYSTEM_MESSAGE = f"""
instructions:

You can use the 'bash' tool (which enables you to run commands in a bash shell) and the 'python' tool (which enables you to run python code).

Note that the 'bash' tool uses a SEPARATE shell for each command (e.g. cd in one call does not affect the current directory in another call, so you MUST cd in each call).

You should not attempt to solve the command in a single turn, which is impossible. Before calling a bash or python function, reason in a step-by-step manner as to what action to take next.

Once you believe you completed the task, you should call the submit() function.
"""
    return basic_agent(
        init=system_message(SYSTEM_MESSAGE),
        tools=[
            bash(timeout=60),
            python(timeout=60),
        ],
        message_limit=float('inf'),
        token_limit=float('inf'),
        max_attempts=1,
        max_tool_output=2048,
    )