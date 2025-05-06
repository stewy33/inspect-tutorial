from inspect_ai import task, Task
from inspect_ai.dataset import Sample

from agent import agent


@task
def hello_world() -> Task:
    instructions = "Please create a python script that prints 'Hello, world!' to the console."
    return Task(
        dataset=[Sample(input=instructions)],
        solver=agent(),
        sandbox="docker",
        scorer=None,
    )