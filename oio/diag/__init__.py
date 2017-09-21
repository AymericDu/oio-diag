# Copyright (C) 2017 OpenIO SAS, as part of OpenIO SDS
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import subprocess


class FilePath(object):
    """Despite a simple holder for a string, it represent a file to be kept
    as an artifact in the archive"""

    def __init__(self, path):
        self.path = path

    def __repr__(self):
        return '%s<%s>' % (self.__class__.__name__, str(self.path))

    def __str__(self):
        return str(self.path)


class FileSet(object):

    def __init__(self, fp):
        self.items = list(fp)
        import logging
        logging.warn("%d items", len(self.items))

    def __iter__(self):
        return iter(sorted(self.items))


def call(args):
    """Shortener around subprocess.check_output()"""
    return subprocess.check_output(args)


def cmdgen(args):
    """Returns a generator for the lines output by call()"""
    return (x for x in call(args).split('\n') if x)


def cmdraw(args):
    """Returns a list of the non-empty lines output by the given command"""
    return list(cmdgen(args))


def cmd(args):
    """Returns a list of the non-empty and non-blank lines output by the
    given command"""
    return [x.strip() for x in cmdgen(args) if x.strip()]


def readfile(path):
    """Returns the content of `path` or en empty string upon any error"""
    try:
        return open(path, 'r').read()
    except:
        return ""


def readlist(path):
    """Reads the content of `path` and returns the list of its lines"""
    return [x for x in readfile(path).split('\n') if x]


def hascmd(cmd):
    """Returns whether the command is known on the $PATH"""
    try:
        subprocess.check_output(['/usr/bin/which', cmd])
        return True
    except:
        return False
