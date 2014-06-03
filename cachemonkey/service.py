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

from cachemonkey import cacher
from cachemonkey.openstack.common import log as logging
from cachemonkey.openstack.common import service

LOG = logging.getLogger(__name__)

opts = [
    cfg.IntOpt('periodic_delay', default=30, help='Delay between cacher runs')
]

CONF = cfg.CONF
CONF.register_opts(opts)


class Service(service.Service):

    def __init__(self):
        super(Service, self).__init__()
        self.cacher = cacher.Cacher()

    def start(self):
        super(Service, self).start()
        LOG.info("Cachemonkey service initializing...")
        self.tg.add_timer(CONF.periodic_delay, self.cacher.cache)

    def stop(self):
        LOG.info("Cachemonkey service shutting down...")
        super(Service, self).stop()
