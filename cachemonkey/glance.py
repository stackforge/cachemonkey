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

import glanceclient
from oslo.config import cfg

from cachemonkey import auth
from cachemonkey.openstack.common import log as logging

LOG = logging.getLogger(__name__)
CONF = cfg.CONF

opts = [
    cfg.ListOpt('endpoints', help='Glance endpoint (override catalog)'),
    cfg.StrOpt('scheme', help='Glance endpoint URL scheme', default='http')
]
CONF.register_opts(opts, group='glance')


class Client(object):
    """Glance client wrapper that handles auth and config."""

    def __init__(self, auth_client=None):

        if auth_client:
            self.authclient = auth_client
        else:
            self.authclient = auth.Client()

        self.authclient.auth()

        self.endpoints = self._endpoints()
        self.next_ = 0

    def __getattr__(self, key):
        client = self._client()
        return getattr(client, key)

    def _client(self):
        # pick a glance endpoint via round-robin
        endpoint = self.endpoints[self.next_]
        self.next_ = (self.next_ + 1) % len(self.endpoints)

        api_version = 2
        token = self.authclient.token
        return glanceclient.Client(api_version, endpoint, token=token)

    def _endpoints(self):
        # prefer endpoints provided via config
        if CONF.glance.endpoints:
            endpoints = CONF.glance.endpoints
        else:
            # fallback to getting a glance endpoint from the service catalog
            catalog = self.authclient.catalog
            image_endpoints = catalog.get_endpoints()['image']

            LOG.debug('Image endpoints: %s' % image_endpoints)
            if len(image_endpoints) > 1:
                LOG.warn('Expected a single image endpoint, but there are %d' %
                         len(image_endpoints))

            endpoint = image_endpoints[0]['publicURL']
            endpoints = [endpoint]

        if endpoints[0].find('://') == -1:
            # prepend a scheme to each endpoint
            scheme = CONF.glance.scheme
            endpoints = map(lambda e: "%s://%s" % (scheme, e), endpoints)

        return endpoints
