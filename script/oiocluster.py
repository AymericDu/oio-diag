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

import re
import json
from oio.diag import cmd, call


class Gridinit(object):

    def run(self, **kwargs):
        sock = kwargs.get('gridinit_sock')
        if not sock:
            return []
        return cmd(['gridinit_cmd', '-S', sock, 'status2'])


class ClusterList(object):

    def run(self, **kwargs):
        nsname = kwargs.get('ns')
        if not nsname:
            return []
        out = call(['openio', 'cluster', 'list',
                    '--oio-ns', nsname, '-f', 'json'])
        return json.loads(out)


class LocalConfig(object):

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
