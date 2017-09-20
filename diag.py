#!/usr/bin/env python
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

import argparse
import os
import json
import logging
import pkg_resources
import shutil
import tarfile
import tempfile

output_list = ['json', 'file', 'tar']


def load_modules(group_name):
    modules = []
    for entry_point in pkg_resources.iter_entry_points(group_name):
        logging.debug("Entry point found: %s", entry_point)
        modules.append(entry_point.load(require=False))
    return modules


def env(*vars, **kwargs):
    """Search for the first defined of possibly many env vars
    Returns the first environment variable defined in vars, or
    returns the default defined in kwargs.
    """
    for v in vars:
        value = os.environ.get(v, None)
        if value:
            return value
    return kwargs.get('default', '')


def build_arg_parser():
    log_parser = argparse.ArgumentParser(add_help=False)
    parser = argparse.ArgumentParser(parents=[log_parser])
    parser.add_argument(
            '--oio-ns',
            dest='ns',
            default=env('OIO_NS'),
            help='Namespace name (Env: OIO_NS)',
    )

    parser.add_argument(
            '--gridinit-sock',
            dest='gridinit_sock',
            help='the fullpath of the gridinit socket',
    )

    parser.add_argument(
            '--output',
            dest='output',
            default=output_list[0],
            choices=output_list,
            help='select the ouput method'
    )
    return parser


class JsonOutputManager(object):

    def __init__(self):
        self.obj = dict()

    def create_output(self, module, result):
        if isinstance(result, dict) or isinstance(result, list):
            self.obj[module] = result
        elif isinstance(result, basestring) or isinstance(result, buffer):
            self.obj[module] = result
        else:
            logging.debug("Unmanageable output: %s", repr(result))

    def finalize(self):
        print json.dumps(self.obj, indent=2)


class FilesOutputManager(object):

    def __init__(self):
        self.directory = tempfile.mkdtemp(prefix='oio-diag-')

    def create_output(self, module, result):
        if isinstance(result, dict) or isinstance(result, list):
            with open('%s/%s' % (self.directory, module), 'w') as f:
                json.dump(result, f, indent=2)
        elif isinstance(result, basestring) or isinstance(result, buffer):
            with open('%s/%s' % (self.directory, module), 'w') as f:
                f.write(result)
        else:
            logging.debug("Unmanageable output: %s", repr(result))

    def finalize(self):
        print self.directory


class ArchiveOutputManager(FilesOutputManager):

    def finalize(self):
        archive = '%s.tar' % self.directory
        with tarfile.open(archive, 'w') as tar:
            tar.add(self.directory)
        shutil.rmtree(self.directory)
        print archive


class MailOutputManager(ArchiveOutputManager):

    def finalize(self):
        super(MailOutputManager, self).finalize()


def make_output_manager(name):
    if name == 'json':
        return JsonOutputManager()
    if name == 'file':
        return FilesOutputManager()
    if name == 'tar':
        return ArchiveOutputManager()
    assert False, "OutputManager not available"


def main():
    logging.basicConfig(format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S',
                        level=logging.DEBUG)
    args = build_arg_parser().parse_args()
    kwargs = {}
    if args.ns is not None:
        kwargs['ns'] = args.ns
    if args.gridinit_sock is not None:
        kwargs['gridinit_sock'] = args.gridinit_sock

    tools_modules = load_modules("oio.tools")
    outputManager = make_output_manager(args.output)
    for tool in tools_modules:
        logging.debug("Running tool %s", repr(tool))
        result = tool().run(**kwargs)
        outputManager.create_output(tool.__name__, result)

    outputManager.finalize()


if __name__ == '__main__':
    main()
