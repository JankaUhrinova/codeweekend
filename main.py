import sys

from code.runner import run_solver_on_dir
from solvers.quickest_kill import solve


input_dir = sys.argv[1]
OUTPUT_DIR = sys.argv[2] if len(sys.argv) >= 3 else "output/"

run_solver_on_dir(input_dir, OUTPUT_DIR, solve, True)
