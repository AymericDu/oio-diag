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

import os
from oio.diag import readfile, cmd


class OioProcessInfo(object):

    def run(self, **kwargs):
        out = []
        ns = kwargs.get('ns')
        if not ns:
            return out
        for i, a in enumerate(cmd(['ps', '-o', 'pid,cmd'])):
            if i <= 1:
                continue
            tok = a.split()
            pid, cmdline = tok[0], ' '.join(tok[1:])
            if ns not in cmdline:
                continue
            pid = int(pid)
            proc = dict()
            proc['pid'] = pid
            proc['cmd'] = cmdline
            proc['env'] = dict()
            for pair in readfile('/proc/%s/environ' % pid).split('\0'):
                pair = pair.strip()
                if not pair:
                    continue
                k, v = pair.split('=', 1)
                proc['env'][k] = v
            proc['fd'] = len(os.listdir('/proc/%s/fd' % pid))
            proc['limits'] = readfile('/proc/%s/limits' % pid).split('\n')
            out.append(proc)
        return out
