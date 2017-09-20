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


class OioProcessInfo(object):

    def run(self, **kwargs):
        out = []
        out.append(subprocess.check_output(['ps', 'auxf']))
        p = re.compile('\d+')
        for a in out[0].split('\n'):
            if kwargs.get('ns') in a:
                integer = p.search(a)
                if not integer:
                    break
                pid = integer.group(0)
                out.append(subprocess.check_output(['cat',
                                                    '/proc/%s/cmdline' % pid]))
                out.append(subprocess.check_output(['cat',
                                                    '/proc/%s/environ' % pid]))
                out.append(subprocess.check_output(['ls', '-ail',
                                                    '/proc/%s/fd' % pid]))
        return out
