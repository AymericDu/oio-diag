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

from oiodiag import cmd, cmdraw, call, readlist, map_type


class SELinux(object):

    def run(self, **kwargs):
        try:
            return call(['getenforce'])
        except Exception:
            return ""


class Sysctl(object):

    def run(self, **kwargs):
        out = dict()
        for line in cmd(['sysctl', '-a']):
            k, v = line.split('=')
            out[k.strip()] = map_type(v.strip())
        return out


class Uptime(object):

    def run(self, **kwargs):
        return call(['uptime'])


class Uname(object):

    def run(self, **kwargs):
        return call(['uname', '-a'])


class Free(object):

    def run(self, **kwargs):
        return cmdraw(['free'])


class Mounts(object):

    def run(self, **kwargs):
        return readlist('/proc/mounts')


class Partitions(object):

    def run(self, **kwargs):
        return readlist('/proc/partitions')


class CpuInfo(object):

    def run(self, **kwargs):
        return readlist('/proc/cpuinfo')
