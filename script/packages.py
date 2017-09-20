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


def hascmd(cmd):
    try:
        subprocess.check_output(['/usr/bin/which', cmd])
        return True
    except:
        return False


class Packages(object):

    def run(self, **kwargs):
        out = {'pkg': [], 'diff': []}
        if hascmd('rpm'):
            out['pkg'] = sorted(cmd(['rpm', '-qa', '--last']))
            out['diff'] = cmd(['rpm', '-aV'])
        elif hascmd('dpkg'):
            for e in sorted(cmd(['dpkg', '-l'])):
                if not e.startswith('ii'):
                    # Skip packages uninstalled with config leftover
                    continue
                tok = e.split()
                out['pkg'].append('%s %s %s' % (tok[1], tok[2], tok[3]))
        return out
