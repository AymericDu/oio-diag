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

import json
import urllib3
from oiodiag import cmd, get_all_services, get_local_config, map_type

http = urllib3.PoolManager()


class Gridinit(object):

    def run(self, **kwargs):
        sock = kwargs.get('gridinit_sock')
        if not sock:
            return []
        return cmd(['gridinit_cmd', '-S', sock, 'status2'])


class LiveConfig(object):

    def _run(self, nsname):
        out = dict()
        cfg = get_local_config()
        allsrv = get_all_services(nsname)
        proxy = cfg[nsname]['proxy']
        url = 'http://%s/v3.0/forward/config?id=' % proxy
        for srv in allsrv:
            if not srv['Type'].startswith('meta'):
                continue
            r = http.request('GET', ''.join((url, srv['Id'])),
                             headers={'Connection': 'close'},
                             fields={})
            parsed = json.loads(r.data)
            for k in parsed.keys():
                parsed[k] = map_type(parsed[k])
            out[srv['Id']] = parsed
        return out

    def run(self, **kwargs):
        nsname = kwargs.get('ns')
        if not nsname:
            return []
        try:
            return self._run(nsname)
        except Exception:
            return "namespace down: %s" % nsname


class LiveVersions(object):

    def _run(self, nsname):
        out = dict()
        cfg = get_local_config()
        allsrv = get_all_services(nsname)
        proxy = cfg[nsname]['proxy']
        url = 'http://%s/v3.0/forward/version?id=' % proxy
        for srv in allsrv:
            if not srv['Type'].startswith('meta'):
                continue
            r = http.request('POST', ''.join((url, srv['Id'])),
                             headers={'Connection': 'close'},
                             fields={})
            out[srv['Id']] = r.data
        return out

    def run(self, **kwargs):
        nsname = kwargs.get('ns')
        if not nsname:
            return []
        try:
            return self._run(nsname)
        except Exception:
            return "namespace down: %s" % nsname


class ClusterList(object):

    def run(self, **kwargs):
        nsname = kwargs.get('ns')
        if not nsname:
            return []
        return get_all_services(nsname)


class LocalConfig(object):

    def run(self, **kwargs):
        return get_local_config()
