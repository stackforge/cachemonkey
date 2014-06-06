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
    cfg.StrOpt('tenant', help='Tenant name'),
    cfg.StrOpt('region', help='Region'),
    cfg.BoolOpt('insecure', default=False,
                help='Skip SSL certification validation')
]

# register 2 groups: one for a non-priviledged user, and one for an admin user
CONF.register_opts(opts, group='auth')
CONF.register_opts(opts, group='admin_auth')


class Client(object):

    def __init__(self, group='auth'):
        self.group = group
        cfg_group = getattr(CONF, group)

        kwargs = self._config(cfg_group)

        if cfg_group.tenant:
            kwargs['tenant_id'] = cfg_group.tenant

        LOG.warn(kwargs)
        self.keystoneclient = client.Client(insecure=cfg_group.insecure,
                                            debug=True,
                                            **kwargs)

    def auth(self):
        if not self.keystoneclient.authenticate():
            raise Exception('Failed to auth with keystoneclient')

    @property
    def catalog(self):
        return self.keystoneclient.service_catalog

    @property
    def tenant(self):
        cfg_group = getattr(CONF, self.group)
        return cfg_group.tenant

    @property
    def token(self):
        return self.keystoneclient.auth_token

    def _config(self, group='auth'):
        # check for presence of required config options
        kwargs = {}

        url = group.url
        if not url:
            raise ValueError('Missing required url for auth')
        kwargs['auth_url'] = url

        username = group.username
        if not username:
            raise ValueError('Missing required username for auth')
        kwargs['username'] = username

        password = group.password
        if not password:
            raise ValueError('Missing required password for auth')
        kwargs['password'] = password

        # the region scopes the catalog object for easier endpoint
        # identification
        region = group.region
        if not region:
            raise ValueError('Missing required region for auth')
        kwargs['region_name'] = region

        return kwargs
