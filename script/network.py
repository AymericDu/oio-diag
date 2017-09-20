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


def cmd(args):
    return subprocess.check_output(args).split('\n')


class Network(object):

    def run(self, **kwargs):
        out = dict()

        out['itf'] = list()
        for itf in cmd(['ip', 'addr', 'list']):
            out['itf'].append(itf)

        out['routes'] = list()
        for r in cmd(['ip', 'route']):
            if not r:
                continue
            out['routes'].append(r)

        out['stat'] = list()
        for st in cmd(['netstat', '-st']):
            out['stat'].append(st)

        out['udp'] = list()
        out['tcp'] = {'listen': list(), 'counters': dict()}
        counters = out['tcp']['counters']
        for i, cnx in enumerate(cmd(['netstat', '-tupan'])):
            if not cnx or i < 1:
                continue
            if cnx.startswith('udp'):
                out['udp'].append(cnx)
            elif cnx.startswith('tcp'):
                st = cnx.split(None, 6)[-2]
                counters[st] = counters.get(st, 0) + 1
                if st == 'LISTEN':
                    out['tcp']['listen'].append(cnx)

        return out
