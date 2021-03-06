#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2016 CenturyLink
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import unittest
from uuid import UUID
import clc as clc_sdk
from clc import CLCException
from clc import APIFailedResponse
import mock
from mock import patch, create_autospec

import clc_ansible_module.clc_server_fact as clc_server_fact
from clc_ansible_module.clc_server_fact import ClcServerFact


class TestClcServerFactFunctions(unittest.TestCase):

    def setUp(self):
        self.clc = mock.MagicMock()
        self.module = mock.MagicMock()
        self.datacenter = mock.MagicMock()

    def test_requests_module_not_found(self):
        # Setup Mock Import Function
        real_import = __import__

        def mock_import(name, *args):
            if name == 'requests':
                args[0]['requests'].__version__ = '2.7.0'
                raise ImportError
            return real_import(name, *args)
        # Under Test
        with mock.patch('__builtin__.__import__', side_effect=mock_import):
            reload(clc_server_fact)
            ClcServerFact(self.module)
        # Assert Expected Behavior
        self.module.fail_json.assert_called_with(
            msg='requests library is required for this module')

        # Reset
        reload(clc_server_fact)

    def test_process_request(self):
        pass

    def test_define_argument_spec(self):
        result = ClcServerFact._define_module_argument_spec()
        self.assertIsInstance(result, dict)
        self.assertTrue('argument_spec' in result)
        self.assertEqual(
            result['argument_spec'],
            {'server_id': {'required': True},
             'credentials': {'default': False}})

    def test_get_server_credentials(self):
        under_test = ClcServerFact(self.module)
        under_test.api_url = 'http://unittest.example.com'
        under_test.clc_alias = 'test_alias'
        # Mock request response from endpoint

    def test_get_endpoint(self):
        under_test = ClcServerFact(self.module)
        under_test.api_url = 'http://unittest.example.com'
        under_test.clc_alias = 'test_alias'
        self.assertEqual(
            under_test._get_endpoint('test_server'),
            'http://unittest.example.com/v2/servers/test_alias/test_server')

    def test_set_clc_credentials_from_env(self):
        # Required combination of credentials not passed
        with patch.dict(
                'os.environ', {
                    'CLC_V2_API_URL': 'http://unittest.example.com',
                },
                clear=True):
            under_test = ClcServerFact(self.module)
            under_test._set_clc_credentials_from_env()
        self.module.fail_json.assert_called_with(
            msg='You must set the CLC_V2_API_USERNAME and CLC_V2_API_PASSWD '
                'environment variables')
        # Token and alias
        with patch.dict(
                'os.environ', {
                    'CLC_V2_API_URL': 'http://unittest.example.com',
                    'CLC_V2_API_TOKEN': 'dummy_token',
                    'CLC_ACCT_ALIAS': 'dummy_alias',
                },
                clear=True):
            under_test = ClcServerFact(self.module)
            under_test._set_clc_credentials_from_env()
        self.assertEqual(under_test.v2_api_token, 'dummy_token')
        self.assertEqual(under_test.clc_alias, 'dummy_alias')
        # Username and password
        # Mock requests response from endpoint


if __name__ == '__main__':
    unittest.main()
