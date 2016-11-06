import subprocess, os
from subprocess import STDOUT, PIPE

import pyperclip


def add_new_line(b):
    if b[-1:] != bytes('\n', 'utf-8'):
        return b + bytes('\n', 'utf-8')
    return b

def repository_root():
    return subprocess.check_output(('git', 'rev-parse', '--show-toplevel',)).strip()

def cd_repository_root():
    os.chdir(repository_root())

def current_branch():
    return subprocess.check_output(('git', 'rev-parse', '--abbrev-ref', 'HEAD',)).strip()


def pick_branch():
    branches = subprocess.Popen(('git', 'branch', '-a',), stdout=PIPE)
    branch = subprocess.check_output(('pick',), stdin=branches.stdout)
    return branch.split()[-1]

def pick_commit(*args):
    commits = subprocess.check_output(('git', 'log', "--pretty=format:'%h %ad | %s%d [%an]'", '--date=short', *args))
    commits = add_new_line(commits)
    p = subprocess.Popen(['pick',], stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    commit = p.communicate(input=commits)[0]
    return commit.split()[0]

def pick_commit_reflog(*args):
    commits = subprocess.check_output(('git', 'reflog', '--all', '--date=short', *args))
    commits = add_new_line(commits)
    p = subprocess.Popen(['pick',], stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    commit = p.communicate(input=commits)[0]
    return commit.split()[0]

def pick_file(*args):
    files = subprocess.Popen(('git', 'ls-tree', '-r', 'master', '--name-only', *args), stdout=PIPE)
    file = subprocess.check_output(('pick',), stdin=files.stdout)
    return file.strip()
