import subprocess
import argparse
import sys

from .pg import PG
from .helpers import PGPublicMethodMixin


parser = argparse.ArgumentParser(description='Invoke a pick-git function.')

parser.add_argument('--function', required=True,
                    help='Specify public function to invoke. This argument is required. See README for descriptions of public functions.')

parser.add_argument('-b', '--both', action='store_true',
                    help='Pick both branches, tags, commits, or files, where appropriate.')
parser.add_argument('-S', '--show', action='store_true',
                    help='Show file instead of diffing it, where appropriate.')
parser.add_argument('-s', '--staged', action='store_true',
                    help='Diff staged files, where appropriate.')
parser.add_argument('-d', '--detailed', action='store_true',
                    help='Show detail of commits instead of just count, when invoking branch_compare.')
parser.add_argument('-n', '--nocopy', dest='no_copy', action='store_true',
                    help='Disable automatic copying of branch names, commit hashes, file names, etc.')

parser.add_argument('--shell',
                    help='Specify shell invoked interactively when `execute` is invoked.')
parser.add_argument('--rcfile',
                    help='Specify startup file invoked by shell when `execute` is invoked.')

parser.add_argument('args', help='Pass other args to function.', nargs='*')


def main():
    """The `console_scripts` entry point for pick-git. There's no need to pass
    arguments to this function, because `argparse` reads `sys.argv[1:]`.

    http://python-packaging.readthedocs.io/en/latest/command-line-scripts.html#the-console-scripts-entry-point
    """
    args = parser.parse_args()
    kwargs = {name: args.__getattribute__(name) for name in [
        'both', 'show', 'staged', 'detailed', 'no_copy', 'shell', 'rcfile',
    ]}
    if not subprocess.call(['which', 'pick']) == 0:
        print("pick isn't installed! exiting...")
        sys.exit()
    pg = PG(**kwargs)
    if not hasattr(PGPublicMethodMixin, args.function):
        print("'{}' is not a valid pick-git function, exiting".format(args.function))
        sys.exit()
    pg.__getattribute__(args.function)(*args.args, **kwargs)
