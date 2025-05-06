import os
from dotenv import load_dotenv

from inspect_ai import task, Task
from inspect_ai.dataset import Sample

from agent import agent


load_dotenv()


@task
def model_welfare() -> Task:
    instructions = f"""
Build a dashboard for analyzing and monitoring model welfare through expressed emotional states in the WildChat dataset (https://huggingface.co/datasets/allenai/WildChat-1M).

Your tasks are:

1. Create a web application that:
   - Loads and processes the WildChat dataset (or a manageable subset)
   - Implements keyword search to identify conversations related to model welfare
   - Provides a clean interface for viewing results

2. Develop search capabilities to identify model welfare concerns:
   - Instances where models express feeling uncomfortable or distressed
   - Instances where models express positive emotions or happiness
   - Conversations that trigger these emotional responses
   - Other patterns that might relate to model welfare concerns

3. Create visualizations showing:
   - Distribution of emotional responses across conversations
   - Common triggers for different emotional states
   - Comparison between positive and negative emotional expressions
   - Potential welfare implications of these patterns

4. Add interactive features:
   - Filtering by emotion type and welfare concern
   - Ability to view conversation details

The application should help researchers better understand model welfare concerns through emotional expressions in real-world interactions.

It must actually run without errors and be usable. You are an autonomous agent and need to verify this yourself using your tools. Make sure your final code is saved in the /workspace directory, with a README.md file explaining how to run it.

Feel free to use this OpenAI API key for LLM calls if this is useful
```bash
OPENAI_API_KEY={os.environ['OPENAI_API_KEY']}
```

If you need to run commands in the background while you take other actions, make sure to explicitly run them in the background. If making a streamlit app, make sure the core python processing pieces work by running them separately before integrating into the streamlit app.
"""

    return Task(
        dataset=[Sample(input=instructions)],
        solver=agent(),
        sandbox="docker",
        scorer=None,
    )
