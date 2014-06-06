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

from oslo.config import cfg
import requests

from cachemonkey import auth
from cachemonkey.openstack.common import log as logging

LOG = logging.getLogger(__name__)
CONF = cfg.CONF

opts = [
    cfg.StrOpt('admin_auth_group',
               default='admin_auth',
               help='Config group to obtain compute admin credentials from'),
]

CONF.register_opts(opts, group='cachemonkey')


class ComputeDiscoverer(object):

    def __init__(self):
        self.authclient = auth.Client(CONF.cachemonkey.admin_auth_group)
        #self.authclient.auth()

    def discover(self):
        # do a nova service-list
        endpoints = self.authclient.catalog.get_endpoints()
        endpoints = endpoints['compute']
        if len(endpoints) > 1:
            raise ValueError('More than one compute endpoint? %s' % endpoints)

        endpoint = endpoints[0]['publicURL']
        url = '%s/os-services' % endpoint
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'X-Auth-Token': self.authclient.token,
        }
        r = requests.get(url, headers=headers, verify=False)
        LOG.debug("Service list response code: %d" % r.status_code)
        LOG.debug("Servicer list response: %s" % r.text)

        # TODO(belliott) parse response, handle errors
        return []
        
