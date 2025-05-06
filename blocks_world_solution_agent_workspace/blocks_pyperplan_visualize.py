import matplotlib; matplotlib.use('Agg')
import os
from pyperplan.pddl.parser import Parser
from pyperplan.grounding import ground
from pyperplan.search import astar_search
from pyperplan.task import Task
from pyperplan.heuristics.blind import BlindHeuristic
from pyperplan.planner import _parse, _ground, _search
import matplotlib.pyplot as plt
import matplotlib.patches as patches

DOMAIN_FILE = '/workspace/pddl/blocks-domain.pddl'
PROBLEM_FILE = '/workspace/pddl/blocks-5-problem.pddl'

# 1. Parse and ground PDDL
def plan_blocks(domain_file, problem_file):
    parser = Parser(domain_file, problem_file)
    domain = parser.parse_domain()
    problem = parser.parse_problem(domain)
    task = _parse(domain_file, problem_file)
    task = _ground(task)
    plan = _search(task, astar_search, BlindHeuristic(task))
    # only blind heuristic, FF failed to import above
    if plan is None:
        plan = _search(task, "blind")  # fallback
    return plan

def main():
    plan = plan_blocks(DOMAIN_FILE, PROBLEM_FILE)
    if not plan:
        print("No plan found!")
        return
#    print("Plan steps:")
#    for i, action in enumerate(plan):
        print(f"{i+1}. {action}")

if __name__ == "__main__":
    main()
import re
import numpy as np

BLOCKS = ["A", "B", "C", "D", "E"]
COLORS = {
    "A": "red",
    "B": "blue",
    "C": "orange",
    "D": "green",
    "E": "purple"
}


def parse_init_state():
    state = {}
    for block in BLOCKS:
        state[block] = {'on': None, 'ontable': False, 'clear': False}
    holding = None
    handempty = True
    # Defined by problem file
    state['C']['on'] = 'A'
    state['D']['on'] = 'B'
    state['A']['ontable'] = True
    state['B']['ontable'] = True
    state['E']['ontable'] = True
    state['C']['clear'] = True
    state['D']['clear'] = True
    state['E']['clear'] = True
    state['A']['clear'] = False
    state['B']['clear'] = False
    handempty = True
    return state, holding, handempty

def apply_action(state, holding, handempty, action):
    action = action.lower()
    pickup = re.match(r'\(pickup (\w)\)', action)
    putdown = re.match(r'\(putdown (\w)\)', action)
    stack = re.match(r'\(stack (\w) (\w)\)', action)
    unstack = re.match(r'\(unstack (\w) (\w)\)', action)
    state = {k: v.copy() for k, v in state.items()}  # shallow copy
    if pickup:
        x = pickup.group(1).upper()
        holding = x
        handempty = False
        state[x]['ontable'] = False
        state[x]['clear'] = False
    elif putdown:
        x = putdown.group(1).upper()
        state[x]['ontable'] = True
        state[x]['clear'] = True
        holding = None
        handempty = True
    elif stack:
        x = stack.group(1).upper()
        y = stack.group(2).upper()
        state[x]['on'] = y
        state[x]['clear'] = True
        state[y]['clear'] = False
        holding = None
        handempty = True
    elif unstack:
        x = unstack.group(1).upper()
        y = unstack.group(1).upper()
        state[x]['on'] = None
        state[x]['clear'] = True
        state[y]['clear'] = True
        holding = x
        handempty = False
    return state, holding, handempty

def build_stacks(state, holding):
    table_blocks = [b for b in BLOCKS if state[b]['ontable'] and (state[b]['on'] is None)]
    stacks = []
    for b in table_blocks:
        stack = [b]
        top = b
        while True:
            above = [bb for bb in BLOCKS if state[bb]['on'] == top]
            if above:
                stack.append(above[0])
                top = above[0]
            else:
                break
        stacks.append(stack)
    # Now add floating (held) block
    if holding:
        stacks.append([holding])
    return stacks

def draw_state(state, holding, step_idx):
    print(f"DEBUG: stacks={build_stacks(state, holding)}")
    stacks = build_stacks(state, holding)
    fig, ax = plt.subplots(figsize=(6, 4))
    w, h = 0.8, 0.5
    gap = 1.0
    for col, stack in enumerate(stacks):
        for row, b in enumerate(stack):
            x = col * gap
            y = row * h
            rect = patches.Rectangle((x, y), w, h, linewidth=2, edgecolor='black', facecolor=COLORS[b], zorder=2)
            ax.add_patch(rect)
            ax.text(x + w/2, y + h/2, b, va='center', ha='center', fontsize=18, color='white', zorder=3)
    ax.set_xlim(-0.5, max(3, len(stacks))*gap)
    ax.set_ylim(0, 5)
    ax.axis('off')
    ax.set_title(f"Step {step_idx}")
    plt.tight_layout()
    print('Writing image for step', step_idx)
    plt.savefig(f"/workspace/state_step_{step_idx:02d}.png")
    plt.close()

def explain_action(action):
    action = action.lower()
    pickup = re.match(r"\(pickup (\w)\)", action)
    if pickup:
        return f"Pick up block {pickup.group(1).upper()} from the table."
    putdown = re.match(r"\(putdown (\w)\)", action)
    if putdown:
        return f"Put down block {putdown.group(1).upper()} onto the table."
    stack = re.match(r"\(stack (\w) (\w)\)", action)
    if stack:
        return f"Stack block {stack.group(1).upper()} onto block {stack.group(1).upper()}."
    unstack = re.match(r"\(unstack (\w) (\w)\)", action)
    if unstack:
        return f"Remove block {unstack.group(1).upper()} from on top of block {unstack.group(1).upper()}."
    return "Unknown action."

def visualize_and_explain(plan):
    state, holding, handempty = parse_init_state()
    print("\nPlan with Visualization and Explanations:\n")
    print("Calling draw_state for initial state")
    draw_state(state, holding, 0)
    print(f"Step 0: Initial state.")
    for idx, act in enumerate(plan):
        expl = explain_action(str(act))
        print(f"Step {idx+1}: {expl}")
        state, holding, handempty = apply_action(state, holding, handempty, str(act))
        print(f"Calling draw_state for step {idx+1}")
        draw_state(state, holding, idx+1)

def main():
    plan = plan_blocks(DOMAIN_FILE, PROBLEM_FILE)
    if not plan:
        print("No plan found!")
        return
#    print("Plan steps:")
#    for i, action in enumerate(plan):
        print(f"{i+1}. {action}")
    # Visualize and explain next
    visualize_and_explain(plan)
if __name__ == "__main__":
    main()
