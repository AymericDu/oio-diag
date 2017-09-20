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


def map_type(v):
    for t in (int, float, str):
        try:
            return t(v)
        except:
            pass


class SELinux(object):

    def run(self, **kwargs):
        try:
            return subprocess.check_output(['getenforce'])
        except:
            return ""


class Sysctl(object):

    def run(self, **kwargs):
        out = dict()
        for line in cmd(['sysctl', '-a']):
            line = line.strip()
            if not line:
                continue
            k, v = line.split('=')
            out[k.strip()] = map_type(v.strip())
        return out
