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

from oiodiag import call, cmd, cmdraw


class Interfaces(object):

    def run(self, **kwargs):
        out = list()
        for itf in cmdraw(['ip', 'addr', 'list']):
            out.append(itf)
        return out


class Routes(object):

    def run(self, **kwargs):
        out = list()
        for r in cmd(['ip', 'route']):
            out.append(r)
        return out


class Netstat(object):

    def run(self, **kwargs):
        out = list()
        for st in cmdraw(['netstat', '-st']):
            out.append(st)
        return out


class Cnx(object):

    def run(self, **kwargs):
        udp = list()
        counters = dict()
        listen = list()
        for i, cnx in enumerate(cmd(['netstat', '-tupan'])):
            if i < 1:
                continue
            if cnx.startswith('udp'):
                udp.append(cnx)
            elif cnx.startswith('tcp'):
                st = cnx.split(None, 6)[-2]
                counters[st] = counters.get(st, 0) + 1
                if st == 'LISTEN':
                    listen.append(cnx)
        return {'udp': udp, 'tcp': {'listen': listen, 'counters': counters}}


class IpTable(object):

    def run(self, **kwargs):
        return call(['iptables-save'])


class Ip6Table(object):

    def run(self, **kwargs):
        return call(['ip6tables-save'])
