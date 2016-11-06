import subprocess, os, sys
from subprocess import STDOUT, PIPE
from functools import wraps


def add_new_line(b):
    if sys.version_info < (3, 0, 0):
        if b[-1] != '\n':
            b += '\n'
    else:
        if b[-1:] != bytes('\n', 'utf-8'):
            b += bytes('\n', 'utf-8')
    return b

def repository_root():
    return subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).strip().decode('utf-8')

def cd_repository_root():
    os.chdir(repository_root())

def current_branch():
    return subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).strip().decode('utf-8')


def exit_on_keyboard_interrupt(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except KeyboardInterrupt:
            sys.exit()
    return wrapper

@exit_on_keyboard_interrupt
def pick_branch():
    branches = subprocess.Popen(['git', 'branch', '-a'], stdout=PIPE)
    branch = subprocess.check_output(['pick'], stdin=branches.stdout)
    return branch.split()[-1].decode('utf-8')

@exit_on_keyboard_interrupt
def pick_commit(*args):
    commits = subprocess.check_output(('git', 'log', "--pretty=format:%h %ad | %s%d [%an]", '--date=short') + args)
    commits = add_new_line(commits)
    p = subprocess.Popen(['pick'], stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    commit = p.communicate(input=commits)[0]
    return commit.split()[0].decode('utf-8')

@exit_on_keyboard_interrupt
def pick_commit_reflog(*args):
    commits = subprocess.check_output(('git', 'reflog', '--all', '--date=short') + args)
    commits = add_new_line(commits)
    p = subprocess.Popen(['pick'], stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    commit = p.communicate(input=commits)[0]
    return commit.split()[0].decode('utf-8')

@exit_on_keyboard_interrupt
def pick_modified_file(branch_or_commit):
    files = subprocess.Popen(['git', 'diff', '--name-only', branch_or_commit], stdout=PIPE)
    file = subprocess.check_output(['pick'], stdin=files.stdout)
    return file.strip().decode('utf-8')

@exit_on_keyboard_interrupt
def pick_file(*args):
    files = subprocess.Popen(('git', 'ls-tree', '-r', 'master', '--name-only') + args, stdout=PIPE)
    file = subprocess.check_output(['pick'], stdin=files.stdout)
    return file.strip().decode('utf-8')
