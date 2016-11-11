import subprocess, argparse, sys

from pg.pg import PG


parser = argparse.ArgumentParser(description='Invoke a pick-git function.')

parser.add_argument('-b', '--both', action='store_true',
                    help='pick both branches, commits, or files, where appropriate')
parser.add_argument('-s', '--show', action='store_true',
                    help='show file instead of diffing it, where appropriate')
parser.add_argument('-d', '--detailed', action='store_true',
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
        'both', 'show', 'detailed', 'shell', 'rcfile',
    ]}
    if not subprocess.call(['which', 'pick']) == 0:
        print("pick isn't installed! exiting...")
        sys.exit()
    pg = PG(**kwargs)
    try:
        f = pg.__getattribute__(args.function)(*args.args, **kwargs)
    except AttributeError as e:
        print("'{}' is not a valid pick-git function, exiting".format(args.function))
        sys.exit()
