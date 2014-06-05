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

import os

from oslo.config import cfg

from cachemonkey.openstack.common import importutils
from cachemonkey.openstack.common import log as logging

LOG = logging.getLogger(__name__)
CONF = cfg.CONF

opts = [
    cfg.StrOpt('lister_class',
               default='cachemonkey.lister.glance.GlanceLister',
               help='Class to determine which images get pre-cached'),
    cfg.StrOpt('fetcher_class',
               default='cachemonkey.fetcher.glance.GlanceFetcher',
               help='Class to determine how to fetch images.'),
    cfg.StrOpt('data_dir', default='/var/lib/cachemonkey',
               help='Directory containing image data'),

]

CONF.register_opts(opts, group='cachemonkey')


class Cacher(object):

    def __init__(self):
        self.lister = importutils.import_object(CONF.cachemonkey.lister_class)
        self.fetcher = importutils.import_object(
            CONF.cachemonkey.fetcher_class)

    def cache(self):
        images = self.lister.images()
        for image in images:
            self._get(image)
            # TODO(belliott) distribute to hosts

    def _get(self, image):
        # first see if the image was previously downloaded
        d = os.path.join(CONF.cachemonkey.data_dir)
        if not os.path.exists(d):
            os.makedirs(d)

        filename = os.path.join(d, image['id'])
        if os.path.exists(filename):
            LOG.debug("Image %s was previously downloaded." % image['id'])
            # TODO(belliott) also verify checksum
        else:
            self.fetcher.fetch(image, filename)

        return filename
