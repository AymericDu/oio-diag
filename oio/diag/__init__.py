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
import re
import json

cache = dict()


def put(k,v):
    cache[k] = v


def get(k):
    return cache.get(k, None)


def map_type(v):
    for t in (int, float, str):
        try:
            return t(v)
        except:
            pass


def get_local_config():
    cfg = get('cfg')
    if cfg:
        return cfg
    cfg = dict()
    p = re.compile('([^/]+)/([^=]+)=(.*)$')
    for line in cmd(['oio-cluster', '--local-cfg']):
        match = p.match(line)
        if not match:
            continue
        ns, k, v = match.group(1), match.group(2), match.group(3)
        if ns not in cfg:
            cfg[ns] = dict()
        cfg[ns][k] = map_type(v)
    return cfg


def get_all_services(nsname):
    """Cache and return the list of services"""
    allsrv = get('allsrv')
    if not allsrv:
        allsrv = call(['openio', 'cluster', 'list',
                    '--oio-ns', nsname, '-f', 'json'])
        allsrv = json.loads(allsrv)
        put('allsrv', allsrv)
    return allsrv


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
        self.items = list()
        for f in fp:
            if isinstance(f, str):
                self.items.append(FilePath(str(f)))
            elif isinstance(f, FilePath):
                self.items.append(f)
            else:
                raise Exception("BUG")

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
