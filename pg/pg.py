from os import getenv
from subprocess import Popen

from .helpers import PGMethodMixin


class PG(PGMethodMixin):

    def __init__(self, shell='', rcfile='', **kwargs):
        self.shell = shell or getenv('SHELL')
        self.rcfile = rcfile
        self._copy = lambda text: None

        # import pyperclip if it's installed, use `pyperclip.copy` if it works
        try:
            import pyperclip
        except ImportError:
            print('install pyperclip for a better experience')
        else:
            try:
                pyperclip.copy('')
            except pyperclip.exceptions.PyperclipException:
                print("pyperclip is installed but it's missing a dependency, see pyperclip repo for details")
            else:
                self._copy = pyperclip.copy

    def copy(self, s):
        """Copy `s` using `_copy`, which is `pyperclip.copy`, or a NOOP if
        `pyperclip` doesn't work.
        """
        self._copy(s.decode('utf-8') if type(s) is bytes else s)

    def execute(self, command):
        """Make sure `command` is a string, and execute it using the global `shell`
        var, the shell specified by the $SHELL env var, or by the default shell.

        Also prints `command`.
        """
        if not isinstance(command, str):
            command = ' '.join(command)
        print(command)

        rcfile = ['--rcfile', self.rcfile] if self.rcfile else []
        if self.shell:
            p = Popen([self.shell] + rcfile + ['-i', '-c', command])
            p.communicate()
        else:
            p = Popen(command)
            p.communicate()
