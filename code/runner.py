from copy import deepcopy
from typing import Callable
from dataclasses import dataclass
import os

from code.input_output import read_input, write_output
from code.checker import check_and_score
from code.world import Action, World

SolverFunction = Callable[[World], list[Action]]


def run_world_with_solver(world: World, solver: SolverFunction) -> list[Action]:
    return solver(deepcopy(world))


@dataclass
class RunData:
    world: World
    actions: list[Action]
    score: int
    error: str


def run_solver_and_check(world: World, solver: SolverFunction) -> RunData:
    actions = run_world_with_solver(world, solver)
    score, error = check_and_score(world, actions)
    return RunData(world, actions, score, error)


def run_solver_on_file(
    input_file: str, solver: SolverFunction, debug: bool = False
) -> RunData:

    if debug:
        print("Running solver on", input_file)

    world = read_input(input_file)

    run_data = run_solver_and_check(world, solver)

    if run_data.error:
        print(f"Solver failed on {input_file} with error: {run_data.error}")
        return

    print(f"Solved {input_file} with score {run_data.score}")

    return run_data


def run_solver_on_dir(
    input_dir: str, output_dir: str, solver: SolverFunction, debug: bool = False
) -> None:

    paths = os.listdir(input_dir)
    paths.sort()

    for path in paths:
        input_path = os.path.join(input_dir, path)
        output_path = os.path.join(output_dir, path)
        run_data = run_solver_on_file(input_path, solver, debug)

        if run_data.error:
            continue

        if debug:
            print(f"Writing output to {output_path}")

        write_output(output_path, run_data.actions)
