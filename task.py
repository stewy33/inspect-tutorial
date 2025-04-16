import os

from inspect_ai import task, Task
from inspect_ai.dataset import Sample
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
            bash(timeout=360),
            python(timeout=360),
        ],
        max_attempts=1,
        max_tool_output=2048,
    )

@task
def custom_task() -> Task:
    hello_world_instructions = "Please create a python script that prints 'Hello, world!' to the console."

    tamp_instructions = """
You need to create a small Python program that uses a simple PDDL solver to solve a blocks world problem and display the solution.
Your tasks are:

Create a PDDL domain file for a blocks world with actions for picking up blocks, putting them down, and stacking them
Create a PDDL problem file with 5 blocks (A, B, C, D, E) in a specific initial configuration, with a goal of building a specific tower
Write Python code that:

Uses the pyperplan library (a simple PDDL planner)
Loads your domain and problem files
Finds a solution plan
Visualizes the execution of the plan step by step (text-based visualization is fine)

Output the complete plan and explain why each step is necessary

The initial state has blocks scattered: A on table, B on table, C on A, D on B, E on table.
The goal state should be a single stack with E at the bottom and A at the top (E, D, C, B, A).
"""

    instructions = tamp_instructions
    return Task(
        dataset=[Sample(input=instructions)],
        solver=agent(),
        sandbox="docker",
        scorer=None,
    )