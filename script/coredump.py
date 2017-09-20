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


class CoreDump(object):

    def run(self, **kwargs):
        out = {}
        tmp = subprocess.check_output(['cat', '/proc/sys/kernel/core_pattern'])
        if '|' in tmp:
            return
        for a in subprocess.check_output(['ls', '/tmp']).split('\n'):
            if 'core.' in a:
                out[a] = (subprocess.check_output(['cat', '/tmp/%s' % a]))
        return out
