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

import mock

from cachemonkey import glance
from cachemonkey.tests import base


class GlanceTestCase(base.BaseTestCase):

    def setUp(self):
        super(GlanceTestCase, self).setUp()

        self.endpoints = ['http://1.2.3.4:1234', 'http://2.3.4.5:2345']
        self.flags(endpoints=self.endpoints, group='glance')

        class FakeAuthClient(object):
            token = 'token'

            def auth(self):
                return

        fake_auth_client = FakeAuthClient()
        self.client = glance.Client(auth_client=fake_auth_client)

    @mock.patch('glanceclient.Client')
    def test_endpoint_round_robin(self, mock_glanceclient):
        api_version = 2

        for i in range(len(self.endpoints)):
            self.client.dosomething()

            call = mock.call(api_version, self.endpoints[i], token='token')
            self.assertEqual(call, mock_glanceclient.call_args)

        # call once more to confirm first endpoint is used again
        self.client.dosomething()

        call = mock.call(api_version, self.endpoints[0], token='token')
        self.assertEqual(call, mock_glanceclient.call_args)
