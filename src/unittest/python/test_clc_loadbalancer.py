#!/usr/bin/python

import clc_ansible_module.clc_loadbalancer as clc_loadbalancer
from clc_ansible_module.clc_loadbalancer import ClcLoadBalancer
import clc as clc_sdk
import mock
from mock import patch
import unittest

class TestClcLoadbalancerFunctions(unittest.TestCase):

    def setUp(self):
        self.clc = mock.MagicMock()
        self.module = mock.MagicMock()
        self.datacenter=mock.MagicMock()

    @patch.object(clc_loadbalancer, 'clc_sdk')
    @patch.object(ClcLoadBalancer, '_set_clc_credentials_from_env')
    def test_process_request_state_present(self,
                                           mock_set_clc_credentials,
                                           mock_clc_sdk):

        # Setup
        self.module.params = {
            'name': 'test',
            'port': 80,
            'nodes':[{ 'ipAddress': '10.82.152.15', 'privatePort': 80 }],
            'state': 'present'
        }
        mock_loadbalancer_response = [{'name': 'TEST_LB'}]

        mock_clc_sdk.v2.API.Call.side_effect = [
            [{'name': 'test'}],
            {'id': 'test', 'name': 'test'},
            [],
            {'id': 'test', 'name': 'test'},
            []
        ]
        # TODO: Mock a response to API.Call('POST')
        self.module.check_mode = False
        # Under Test
        under_test = ClcLoadBalancer(self.module)
        under_test.process_request()

        # Assert
        self.module.exit_json.assert_called_once_with(changed=False, loadbalancer = {'id': 'test', 'name': 'test'})
        self.assertFalse(self.module.fail_json.called)

    @patch.object(clc_loadbalancer, 'clc_sdk')
    def test_set_user_agent(self, mock_clc_sdk):
        clc_loadbalancer.__version__ = "1"
        ClcLoadBalancer._set_user_agent(mock_clc_sdk)

        self.assertTrue(mock_clc_sdk.SetRequestsSession.called)

    @patch.object(clc_loadbalancer, 'clc_sdk')
    @patch.object(ClcLoadBalancer, '_set_clc_credentials_from_env')
    def test_process_request_state_absent(self,
                                          mock_set_clc_credentials,
                                          mock_clc_sdk):
        #Setup
        self.module.params = {
            'name': 'test',
            'state': 'absent'
        }
        mock_loadbalancer_response = [{'name': 'test', 'id': 'test'}]
        mock_clc_sdk.v2.API.Call.return_value = mock_loadbalancer_response
        self.module.check_mode = False
        test = ClcLoadBalancer(self.module)
        test.process_request()

        #Assertions
        self.module.exit_json.assert_called_once_with(changed=True, loadbalancer=[{'name': 'test', 'id': 'test'}])
        self.assertFalse(self.module.fail_json.called)

    @patch.object(clc_loadbalancer, 'clc_sdk')
    @patch.object(ClcLoadBalancer, '_set_clc_credentials_from_env')
    def test_process_request_state_port_absent(self,
                                          mock_set_clc_credentials,
                                          mock_clc_sdk):
        #Setup
        self.module.params = {
            'name': 'test',
            'port': 80,
            'state': 'port_absent'
        }

        mock_clc_sdk.v2.API.Call.side_effect = [
            [{'id': 'test', 'name': 'test'}],
            [{'port': '80', 'id':'test'}],
            {}
        ]
        self.module.check_mode = False
        test = ClcLoadBalancer(self.module)
        test.process_request()

        #Assertions
        self.module.exit_json.assert_called_once_with(changed=True, loadbalancer={})
        self.assertFalse(self.module.fail_json.called)

    @patch.object(clc_loadbalancer, 'clc_sdk')
    @patch.object(ClcLoadBalancer, '_set_clc_credentials_from_env')
    def test_process_request_state_nodes_present(self,
                                          mock_set_clc_credentials,
                                          mock_clc_sdk):
        #Setup
        self.module.params = {
            'name': 'test',
            'port': 80,
            'nodes':[{ 'ipAddress': '10.82.152.15', 'privatePort': 80, 'status': 'enabled' }],
            'state': 'nodes_present'
        }

        mock_clc_sdk.v2.API.Call.side_effect = [
            [{'id': 'test', 'name': 'test'}],
            [{'port': '80', 'id':'test'}],
            [{ 'ipAddress': '10.82.152.15', 'privatePort': 80, 'status': 'enabled' }]
        ]

        test = ClcLoadBalancer(self.module)
        test.process_request()

        #Assertions
        self.module.exit_json.assert_called_once_with(changed=False, loadbalancer={})
        self.assertFalse(self.module.fail_json.called)

    @patch.object(clc_loadbalancer, 'clc_sdk')
    @patch.object(ClcLoadBalancer, '_set_clc_credentials_from_env')
    def test_process_request_state_nodes_present_no_lb(self,
                                          mock_set_clc_credentials,
                                          mock_clc_sdk):
        #Setup
        self.module.params = {
            'name': 'test',
            'port': 80,
            'nodes':[{ 'ipAddress': '10.82.152.15', 'privatePort': 80, 'status': 'enabled' }],
            'state': 'nodes_present'
        }

        mock_clc_sdk.v2.API.Call.side_effect = [
            [{'id': 'test1', 'name': 'test1'}],
            [{'port': '80', 'id':'test'}],
            [{ 'ipAddress': '10.82.152.15', 'privatePort': 80, 'status': 'enabled' }]
        ]

        test = ClcLoadBalancer(self.module)
        test.process_request()

        #Assertions
        self.module.exit_json.assert_called_once_with(changed=False, loadbalancer='Load balancer doesn\'t Exist')
        self.assertFalse(self.module.fail_json.called)

    @patch.object(clc_loadbalancer, 'clc_sdk')
    @patch.object(ClcLoadBalancer, '_set_clc_credentials_from_env')
    def test_process_request_state_nodes_present_no_pool(self,
                                          mock_set_clc_credentials,
                                          mock_clc_sdk):
        #Setup
        self.module.params = {
            'name': 'test',
            'port': 80,
            'nodes':[{ 'ipAddress': '10.82.152.15', 'privatePort': 80, 'status': 'enabled' }],
            'state': 'nodes_present'
        }

        mock_clc_sdk.v2.API.Call.side_effect = [
            [{'id': 'test', 'name': 'test'}],
            [{'port': '81', 'id':'test'}],
            [{ 'ipAddress': '10.82.152.15', 'privatePort': 80, 'status': 'enabled' }]
        ]

        test = ClcLoadBalancer(self.module)
        test.process_request()

        #Assertions
        self.module.exit_json.assert_called_once_with(changed=False, loadbalancer='Pool doesn\'t exist')
        self.assertFalse(self.module.fail_json.called)

    @patch.object(clc_loadbalancer, 'clc_sdk')
    @patch.object(ClcLoadBalancer, '_set_clc_credentials_from_env')
    def test_process_request_state_nodes_absent_no_lb(self,
                                          mock_set_clc_credentials,
                                          mock_clc_sdk):
        #Setup
        self.module.params = {
            'name': 'test',
            'port': 80,
            'nodes':[{ 'ipAddress': '10.82.152.15', 'privatePort': 80 }],
            'state': 'nodes_absent'
        }

        mock_clc_sdk.v2.API.Call.side_effect = [
            [{'id': 'test1', 'name': 'test1'}],
            [{'port': '80', 'id':'test'}],
            [{ 'ipAddress': '10.82.152.15', 'privatePort': 80}]
        ]

        test = ClcLoadBalancer(self.module)
        test.process_request()

        #Assertions
        self.module.exit_json.assert_called_once_with(changed=False, loadbalancer='Load balancer doesn\'t Exist')
        self.assertFalse(self.module.fail_json.called)

    @patch.object(clc_loadbalancer, 'clc_sdk')
    @patch.object(ClcLoadBalancer, '_set_clc_credentials_from_env')
    def test_process_request_state_nodes_absent_no_pool(self,
                                          mock_set_clc_credentials,
                                          mock_clc_sdk):
        #Setup
        self.module.params = {
            'name': 'test',
            'port': 80,
            'nodes':[{ 'ipAddress': '10.82.152.15', 'privatePort': 80, 'status': 'enabled' }],
            'state': 'nodes_absent'
        }

        mock_clc_sdk.v2.API.Call.side_effect = [
            [{'id': 'test', 'name': 'test'}],
            [{'port': '81', 'id':'test'}],
            [{ 'ipAddress': '10.82.152.15', 'privatePort': 80, 'status': 'enabled' }]
        ]

        test = ClcLoadBalancer(self.module)
        test.process_request()

        #Assertions
        self.module.exit_json.assert_called_once_with(changed=False, loadbalancer='Pool doesn\'t exist')
        self.assertFalse(self.module.fail_json.called)

    @patch.object(clc_loadbalancer, 'clc_sdk')
    @patch.object(ClcLoadBalancer, '_set_clc_credentials_from_env')
    def test_process_request_state_nodes_absent(self,
                                          mock_set_clc_credentials,
                                          mock_clc_sdk):
        #Setup
        self.module.params = {
            'name': 'test',
            'port': 80,
            'nodes':[{ 'ipAddress': '10.82.152.15', 'privatePort': 82, 'status': 'enabled' }],
            'state': 'nodes_absent'
        }

        mock_clc_sdk.v2.API.Call.side_effect = [
            [{'id': 'test', 'name': 'test'}],
            [{'port': '80', 'id':'test'}],
            [{ 'ipAddress': '10.82.152.15', 'privatePort': 81, 'status': 'enabled' }]
        ]

        test = ClcLoadBalancer(self.module)
        test.process_request()

        #Assertions
        self.module.exit_json.assert_called_once_with(changed=False, loadbalancer={})
        self.assertFalse(self.module.fail_json.called)

    @patch.object(clc_loadbalancer, 'clc_sdk')
    @patch.object(ClcLoadBalancer, '_get_lbpool_nodes')
    @patch.object(ClcLoadBalancer, 'set_loadbalancernodes')
    def test_add_lbpool_nodes(self, mock_set_pool_nodes, mock_get_pool_nodes, mock_clc_sdk):
        #Setup
        self.module.params = {
            'name': 'test',
            'port': 80,
            'nodes':[{ 'ipAddress': '10.82.152.15', 'privatePort': 82, 'status': 'enabled' }],
            'state': 'nodes_absent'
        }
        self.module.check_mode = False
        test = ClcLoadBalancer(self.module)
        mock_get_pool_nodes.return_value = [{ 'ipAddress': '10.82.152.15', 'privatePort': 80, 'status': 'enabled' }]
        mock_set_pool_nodes.return_value = 'success'
        result = test.add_lbpool_nodes('alias','location','lb_id','pool_id',
                                       [{'ipAddress': '1.1.1.1', 'privatePort': 80}])
        self.assertFalse(self.module.fail_json.called)
        self.assertEqual(result, (True, 'success'))

    @patch.object(clc_loadbalancer, 'clc_sdk')
    @patch.object(ClcLoadBalancer, '_get_lbpool_nodes')
    @patch.object(ClcLoadBalancer, 'set_loadbalancernodes')
    def test_remove_lbpool_nodes(self, mock_set_pool_nodes, mock_get_pool_nodes, mock_clc_sdk):
        #Setup
        self.module.params = {
            'name': 'test',
            'port': 80,
            'nodes':[{ 'ipAddress': '10.82.152.15', 'privatePort': 80, 'status': 'enabled' }],
            'state': 'nodes_absent'
        }
        self.module.check_mode = False
        test = ClcLoadBalancer(self.module)
        mock_get_pool_nodes.return_value = [{ 'ipAddress': '10.82.152.15', 'privatePort': 80, 'status': 'enabled' }]
        mock_set_pool_nodes.return_value = 'success'
        result = test.remove_lbpool_nodes('alias','location','lb_id','pool_id',
                                       [{ 'ipAddress': '10.82.152.15', 'privatePort': 80}])
        self.assertFalse(self.module.fail_json.called)
        self.assertEqual(result, (True, 'success'))

    @patch.object(clc_loadbalancer, 'clc_sdk')
    def test_set_loadbalancernodes_pool_id(self, mock_clc_sdk):

        mock_clc_sdk.v2.API.Call.side_effect = [
            [{'id': 'test', 'name': 'test'}],
            [{'port': '80', 'id':'test'}],
            [{ 'ipAddress': '10.82.152.15', 'privatePort': 81, 'status': 'enabled' }]
        ]
        self.module.check_mode = False
        test = ClcLoadBalancer(self.module)
        result = test.set_loadbalancernodes('alias', 'location', 'lb_id', 'pool_id', [1,2,3])
        self.assertIsNotNone(result)
        self.assertEqual(result[0].get('id'), 'test')

    @patch.object(clc_loadbalancer, 'clc_sdk')
    def test_set_loadbalancernodes_lb_id_none(self, mock_clc_sdk):

        mock_clc_sdk.v2.API.Call.side_effect = [
            [{'id': 'test', 'name': 'test'}],
            [{'port': '80', 'id':'test'}],
            [{ 'ipAddress': '10.82.152.15', 'privatePort': 81, 'status': 'enabled' }]
        ]
        self.module.check_mode = False
        test = ClcLoadBalancer(self.module)
        result = test.set_loadbalancernodes('alias', 'location', None, 'pool_id', [1,2,3])
        self.assertIsNone(result)

    @patch.object(clc_loadbalancer, 'clc_sdk')
    @patch.object(ClcLoadBalancer, '_get_lbpool_nodes')
    def test_loadbalancerpool_nodes_exists_true(self, mock_get_pool_nodes, mock_clc_sdk):
        #Setup
        self.module.params = {
            'name': 'test',
            'port': 80,
            'nodes':[{ 'ipAddress': '10.82.152.15', 'privatePort': 80, 'status': 'enabled' }],
            'state': 'nodes_absent'
        }
        self.module.check_mode = False
        test = ClcLoadBalancer(self.module)
        mock_get_pool_nodes.return_value = [{ 'ipAddress': '10.82.152.15', 'privatePort': 80, 'status': 'enabled' }]
        result = test._loadbalancerpool_nodes_exists('alias','location',80,'lb_id','pool_id',
                                       [{ 'ipAddress': '10.82.152.15', 'privatePort': 80}])
        self.assertEqual(result, True)

    @patch.object(clc_loadbalancer, 'clc_sdk')
    @patch.object(ClcLoadBalancer, '_get_lbpool_nodes')
    def test_loadbalancerpool_nodes_exists_false(self, mock_get_pool_nodes, mock_clc_sdk):
        #Setup
        self.module.params = {
            'name': 'test',
            'port': 80,
            'nodes':[{ 'ipAddress': '10.82.152.15', 'privatePort': 80, 'status': 'enabled' }],
            'state': 'nodes_absent'
        }
        self.module.check_mode = False
        test = ClcLoadBalancer(self.module)
        mock_get_pool_nodes.return_value = [{ 'ipAddress': '10.82.152.15', 'privatePort': 80, 'status': 'enabled' }]
        result = test._loadbalancerpool_nodes_exists('alias','location',80,'lb_id','pool_id',
                                       [{ 'ipAddress': '10.82.152.15', 'privatePort': 90}])
        self.assertEqual(result, False)

    @patch.object(clc_loadbalancer, 'clc_sdk')
    @patch.object(ClcLoadBalancer, '_loadbalancer_exists')
    @patch.object(ClcLoadBalancer, '_get_loadbalancer_id')
    @patch.object(ClcLoadBalancer, '_loadbalancerpool_exists')
    @patch.object(ClcLoadBalancer, '_loadbalancerpool_nodes_exists')
    @patch.object(ClcLoadBalancer, 'set_loadbalancernodes')
    def test_ensure_lbpool_nodes_set(self, set_lb_nodes, lbpool_nodes_exists, lbpool_exists, get_lb_id, lb_exists, mock_clc_sdk):
        lb_exists.return_value = True
        get_lb_id.return_value = '123'
        lbpool_exists.retrun_value = True
        lbpool_nodes_exists.return_value = False
        set_lb_nodes.return_value = 'success'
        self.module.check_mode = False
        test = ClcLoadBalancer(self.module)
        result = test.ensure_lbpool_nodes_set('alias', 'location', 'name', 80, [1,2,3])
        self.assertEqual(result, (True, 'success'))

    def test_clc_module_not_found(self):
        # Setup Mock Import Function
        import __builtin__ as builtins
        real_import = builtins.__import__
        def mock_import(name, *args):
            if name == 'clc': raise ImportError
            return real_import(name, *args)
        # Under Test
        with mock.patch('__builtin__.__import__', side_effect=mock_import):
            reload(clc_loadbalancer)
            clc_loadbalancer.ClcLoadBalancer(self.module)
        # Assert Expected Behavior
        self.module.fail_json.assert_called_with(msg='clc-python-sdk required for this module')

        # Reset clc_group
        reload(clc_loadbalancer)

    @patch.object(ClcLoadBalancer, 'clc')
    def test_set_clc_credentials_from_env(self, mock_clc_sdk):
        with patch.dict('os.environ', {'CLC_V2_API_TOKEN': 'dummyToken',
                                       'CLC_ACCT_ALIAS': 'TEST'}):
            under_test = ClcLoadBalancer(self.module)
            under_test._set_clc_credentials_from_env()
        self.assertEqual(under_test.clc._LOGIN_TOKEN_V2, 'dummyToken')
        self.assertFalse(mock_clc_sdk.v2.SetCredentials.called)
        self.assertEqual(self.module.fail_json.called, False)

    @patch.object(ClcLoadBalancer, 'clc')
    def test_set_clc_credentials_w_api_url(self, mock_clc_sdk):
        with patch.dict('os.environ', {'CLC_V2_API_URL': 'dummyapiurl'}):
            under_test = ClcLoadBalancer(self.module)
            under_test._set_clc_credentials_from_env()
            self.assertEqual(under_test.clc.defaults.ENDPOINT_URL_V2, 'dummyapiurl')


    def test_clc_set_credentials_w_no_creds(self):
        with patch.dict('os.environ', {}, clear=True):
            under_test = ClcLoadBalancer(self.module)
            under_test._set_clc_credentials_from_env()

        self.assertEqual(self.module.fail_json.called, True)

    def test_define_argument_spec(self):
        result = ClcLoadBalancer.define_argument_spec()
        self.assertIsInstance(result, dict)

    @patch.object(clc_loadbalancer, 'AnsibleModule')
    @patch.object(clc_loadbalancer, 'ClcLoadBalancer')
    def test_main(self, mock_ClcLoadBalancer, mock_AnsibleModule):
        mock_ClcLoadBalancer_instance          = mock.MagicMock()
        mock_AnsibleModule_instance     = mock.MagicMock()
        mock_ClcLoadBalancer.return_value      = mock_ClcLoadBalancer_instance
        mock_AnsibleModule.return_value = mock_AnsibleModule_instance

        clc_loadbalancer.main()

        mock_ClcLoadBalancer.assert_called_once_with(mock_AnsibleModule_instance)
        mock_ClcLoadBalancer_instance.process_request.assert_called_once

if __name__ == '__main__':
    unittest.main()
