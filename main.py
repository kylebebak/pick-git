import argparse, sys

from pg.pg import (branch, branch_file, branch_compare, commit, commit_file,
                   commit_reflog, commit_reflog_file, file_commit,)


functions = {f.__name__: f for f in [
    branch, branch_file, branch_compare, commit, commit_file,
    commit_reflog, commit_reflog_file, file_commit
]}

parser = argparse.ArgumentParser(description='Invoke a pick-git function.')

parser.add_argument('--show', action='store_true',
                    help='show file instead of diffing it, where appropriate')
parser.add_argument('--both', action='store_true',
                    help='pick both branches or files, where appropriate')
parser.add_argument('--detailed', action='store_true',
                    help='show detail of commits instead of just count, where appropriate')
parser.add_argument('--shell',
                    help='specify shell invoked interactively when `execute` is invoked')
parser.add_argument('--rcfile',
                    help='specify startup file invoked by shell when `execute` is invoked')
parser.add_argument('function')
parser.add_argument('args', help='other args to pass to function', nargs='*')


if __name__ == '__main__':
    args = parser.parse_args()
    kwargs = {name: args.__getattribute__(name) for name in [
        'show', 'both', 'detailed', 'shell', 'rcfile',
    ]}
    try:
        f = functions[args.function]
    except KeyError as e:
        print('{} is not a registered pick-git function'.format(e))
        sys.exit()
    f(*args.args, **kwargs)
