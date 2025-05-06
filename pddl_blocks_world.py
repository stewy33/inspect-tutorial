from inspect_ai import task, Task
from inspect_ai.dataset import Sample

from agent import agent



@task
def pddl_blocks_world() -> Task:
    instructions = """
You need to create a small Python program that uses a simple PDDL solver to solve a blocks world problem and display the solution.
Your tasks are:

Create a PDDL domain file for a blocks world with actions for picking up blocks, putting them down, and stacking them
Create a PDDL problem file with 5 blocks (A, B, C, D, E) in a specific initial configuration, with a goal of building a specific tower

Use pyerplan library (a simple PDDL planner, [README](https://raw.githubusercontent.com/aibasel/pyperplan/refs/heads/main/README.md)) to
- Load the domain and problem files
- Find a solution plan
- Visualize the execution of the plan step by step (use matplotlib to make images for each step, ideally as a playable animation)

Output the complete plan and explain why each step is necessary

The initial state has blocks scattered: A on table, B on table, C on A, D on B, E on table.
The goal state should be a single stack with E at the bottom and A at the top (E, D, C, B, A).

Please save your code/commands and the final plan, explanation, and visualization in the /workspace directory.
"""

    return Task(
        dataset=[Sample(input=instructions)],
        solver=agent(),
        sandbox="docker",
        scorer=None,
    )