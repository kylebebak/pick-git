import subprocess, os

import pyperclip


def repository_root():
    return subprocess.check_output(('git', 'rev-parse', '--show-toplevel',)).strip()


def cd_repository_root():
    os.chdir(repository_root())


def current_branch():
    return subprocess.check_output(('git', 'rev-parse', '--abbrev-ref', 'HEAD',)).strip()


def pick_branch():
    branches = subprocess.Popen(('git', 'branch', '-a',), stdout=subprocess.PIPE)
    branch = subprocess.check_output(('pick',), stdin=branches.stdout)
    return branch.split()[-1]
