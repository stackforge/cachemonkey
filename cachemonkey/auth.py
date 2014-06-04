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

from keystoneclient.v2_0 import client
from oslo.config import cfg

from cachemonkey.openstack.common import log as logging

LOG = logging.getLogger(__name__)
CONF = cfg.CONF

opts = [

    cfg.StrOpt('url', help='Auth system endpoint URL'),
    cfg.StrOpt('username', help='Username for auth'),
    cfg.StrOpt('password', help='Password for auth'),
    cfg.StrOpt('region', help='Region'),
]

CONF.register_opts(opts, group='auth')


class Client(object):

    def __init__(self):
        url, username, password, region = self._config()
        self.keystoneclient = client.Client(auth_url=url, username=username,
                                            password=password,
                                            region_name=region)

    def auth(self):
        if not self.keystoneclient.authenticate():
            raise Exception('Failed to auth with keystoneclient')

    @property
    def catalog(self):
        return self.keystoneclient.service_catalog

    @property
    def token(self):
        return self.keystoneclient.auth_token

    def _config(self):
        # check for presence of required config options
        url = CONF.auth.url
        if not url:
            raise ValueError('Missing required url for auth')

        username = CONF.auth.username
        if not username:
            raise ValueError('Missing required username for auth')

        password = CONF.auth.password
        if not password:
            raise ValueError('Missing required password for auth')

        # the region scopes the catalog object for easier endpoint
        # identification
        region = CONF.auth.region
        if not region:
            raise ValueError('Missing required region for auth')

        return url, username, password, region
