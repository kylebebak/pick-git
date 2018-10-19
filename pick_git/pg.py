from os import getenv
from subprocess import Popen

from .helpers import PGPublicMethodMixin


class PG(PGPublicMethodMixin):

    def __init__(self, no_copy=False, shell='', rcfile='', **kwargs):
        self.shell = shell or getenv('SHELL')
        self.rcfile = rcfile

        self._copy = lambda text: None
        if no_copy:  # don't attempt to use pyperclip
            return
        try:  # import pyperclip if it's installed, use `pyperclip.copy` if it works
            import pyperclip
        except ImportError:
            print('install pyperclip for a better experience')
        else:
            try:
                pyperclip.paste()
            except pyperclip.exceptions.PyperclipException:
                print("pyperclip is installed but it's missing a dependency, see pyperclip repo for details")
            else:
                self._copy = pyperclip.copy

    def copy(self, s):
        """Copy `s` using `_copy`, which is `pyperclip.copy`, or a NOOP if
        `pyperclip` doesn't work.
        """
        self._copy(s.decode('utf-8') if type(s) is bytes else s)

    def execute(self, *commands):
        """Convert `commands` to a string, and execute them using the global
        `shell` var, the shell specified by the $SHELL env var, or by the default
        shell.
        """
        commands = ' '.join(commands)
        print(commands)
        rcfile = ['--rcfile', self.rcfile] if self.rcfile else []
        if self.shell:
            p = Popen([self.shell] + rcfile + ['-i', '-c', commands])
            p.communicate()
        else:
            p = Popen(commands)
            p.communicate()
