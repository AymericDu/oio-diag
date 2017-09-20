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
import os


def cmd(args):
    return subprocess.check_output(args).split('\n')


def readfile(path):
    try:
        return open(path, 'r').read()
    except:
        return ""


class OioProcessInfo(object):

    def run(self, **kwargs):
        out = []
        ns = kwargs.get('ns')
        if not ns:
            return out
        for a in cmd(['ps', '-o', 'pid,cmd'])[1:]:
            a = a.strip()
            if not a:
                continue
            tok = a.split()
            pid, cmdline = tok[0], ' '.join(tok[1:])
            if ns not in cmdline:
                continue
            pid = int(pid)
            proc = dict()
            proc['pid'] = pid
            proc['cmd'] = cmdline
            proc['env'] = readfile('/proc/%s/environ' % pid)
            proc['fd'] = os.listdir('/proc/%s/fd' % pid)
            proc['limits'] = readfile('/proc/%s/limits' % pid)
            out.append(proc)
        return out


class OioLocalConfig(object):

    def run(self, **kwargs):
        out = dict()
        p = re.compile('([^/]+)/([^=]+)=(.*)$')
        for line in cmd(['oio-cluster', '--local-cfg']):
            match = p.match(line)
            if not match:
                continue
            ns, k, v = match.group(1), match.group(2), match.group(3)
            if ns not in out:
                out[ns] = dict()
            out[ns][k] = v
        return out
