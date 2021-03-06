from subprocess import Popen, PIPE
import re
import sys
import os


def step(title, level=0, body=[]):
    '''
    Print nicely formatted description of the step.

        Parameters:
            title (string): Heading of the step
            level (int): Indentation of the step (optional) (default = 0)
            body (string[]): Description of the step (optional) (default = [])
        
        Example:
            ==> Heading

                Body line 1
                Body line 2
    '''
    spaces = 2 * level * ' '
    print(spaces + '==> ' + title)

    if body:
        spaces += 4 * ' '
        print()
        for line in body:
            print(spaces + line)
        print()


def semver_compare(a, b):
    '''
    Compare two semantic version strings.

        Parameters:
            a (string): Semantic version string
            b (string): Semantic version string
        
        Returns:
            -1 (int): a is less than b
            0 (int): a is equal to b
            1 (int): a is greater than b
    '''
    pa = a.split('.')
    pb = b.split('.')

    for i in range(3):
        na = int(pa[i])
        nb = int(pb[i])

        if na > nb:
            return 1
        if na < nb:
            return -1
    return 0


def check_requirements(req):
    '''
    Check whether system has all required packages installed or not.

        Parameters:
            req (<string, string>{}): Map of package's name and version
        
        Returns:
            True (bool): all requirements satisfied
            False (bool): failed to satisfy one or more requirements
    '''
    for (n, v) in req.items():
        installed_version = None

        try:
            output, error = Popen([n, '--version'], stdout=PIPE,
                                  stderr=PIPE).communicate()
            installed_version = re.findall('(\d+\.\d+(?:\.\d+|))',
                                           (output + error).decode('utf-8'))[0]
        except:
            return False

        if installed_version.count('.') == 2:
            installed_version += '.0'

        if semver_compare(installed_version, v) == -1:
            return False
    return True


def eprint(title):
    '''
    Print string to stderr.
    '''
    print('[x] ' + title, file=sys.stderr)


def cmd(c):
    '''
    Execute the shell command.

        Parameters:
            c (string[]): Command
        
        Returns:
            '' (string): if the execution was unsuccessful
            output (string): if the execution was successful
    '''
    output = None
    try:
        output = Popen(c, stdout=PIPE,
                       stderr=PIPE).communicate()[0].decode('utf-8')
    except:
        return str()
    return output


def home():
    '''
    Get current user's home directory.

        Returns:
            path (string): home directory path
    '''
    return os.path.expanduser('~')