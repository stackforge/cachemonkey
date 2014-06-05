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

from cachemonkey import glance
from cachemonkey.openstack.common import log as logging

LOG = logging.getLogger(__name__)


class GlanceFetcher(object):
    """Fetch image data via Glance."""

    def __init__(self):
        self.client = glance.Client()

    def fetch(self, image, filename):
        LOG.debug('Fetching image %s' % image['id'])

        # glance client returns a iterator over the response
        # downloads 64KB at a time.
        resp = self.client.images.data(image['id'], do_checksum=True)

        f = open(filename, 'wb')
        for chunk in resp:
            f.write(chunk)
        f.close()
