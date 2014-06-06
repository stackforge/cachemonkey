# Copyright 2014 Rackspace Hosting
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import sys

from oslo.config import cfg
import pbr.version

from cachemonkey.openstack.common import log as logging

project = 'cachemonkey'


def _version():
    vinfo = pbr.version.VersionInfo(project)
    return vinfo.version_string()


def main():
    version = _version()
    cfg.CONF(sys.argv[1:], project=project, version=version)
    logging.setup(project, version=version)

    from IPython import embed
    embed()
