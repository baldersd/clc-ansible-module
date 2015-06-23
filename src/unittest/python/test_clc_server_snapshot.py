#!/usr/bin/python

import clc_ansible_module.clc_server_snapshot as clc_server_snapshot
from clc_ansible_module.clc_server_snapshot import ClcSnapshot
import clc as clc_sdk
from clc import CLCException
import mock
from mock import patch
from mock import create_autospec
import unittest

class TestClcServerSnapshotFunctions(unittest.TestCase):


    def setUp(self):
        self.clc = mock.MagicMock()
        self.module = mock.MagicMock()
        reload(clc_server_snapshot)


    @patch.object(ClcSnapshot, 'clc')
    def test_set_clc_credentials_from_env(self, mock_clc_sdk):
        with patch.dict('os.environ', {'CLC_V2_API_TOKEN': 'dummyToken',
                                       'CLC_ACCT_ALIAS': 'TEST'}):
            under_test = ClcSnapshot(self.module)
            under_test._set_clc_credentials_from_env()
        self.assertEqual(under_test.clc._LOGIN_TOKEN_V2, 'dummyToken')
        self.assertFalse(mock_clc_sdk.v2.SetCredentials.called)
        self.assertEqual(self.module.fail_json.called, False)

    @patch.object(clc_server_snapshot, 'clc_sdk')
    def test_set_user_agent(self, mock_clc_sdk):
        clc_server_snapshot.__version__ = "1"
        ClcSnapshot._set_user_agent(mock_clc_sdk)

        self.assertTrue(mock_clc_sdk.SetRequestsSession.called)

    @patch.object(ClcSnapshot, 'clc')
    def test_set_clc_credentials_w_creds(self, mock_clc_sdk):
        with patch.dict('os.environ', {'CLC_V2_API_USERNAME': 'dummyuser', 'CLC_V2_API_PASSWD': 'dummypwd'}):
            under_test = ClcSnapshot(self.module)
            under_test._set_clc_credentials_from_env()
            mock_clc_sdk.v2.SetCredentials.assert_called_once_with(api_username='dummyuser', api_passwd='dummypwd')

    @patch.object(ClcSnapshot, 'clc')
    def test_set_clc_credentials_w_api_url(self, mock_clc_sdk):
        with patch.dict('os.environ', {'CLC_V2_API_URL': 'dummyapiurl'}):
            under_test = ClcSnapshot(self.module)
            under_test._set_clc_credentials_from_env()
            self.assertEqual(under_test.clc.defaults.ENDPOINT_URL_V2, 'dummyapiurl')

    def test_set_clc_credentials_w_no_creds(self):
        with patch.dict('os.environ', {}, clear=True):
            under_test = ClcSnapshot(self.module)
            under_test._set_clc_credentials_from_env()
        self.assertEqual(self.module.fail_json.called, True)


    def test_define_argument_spec(self):
        result = ClcSnapshot.define_argument_spec()
        self.assertIsInstance(result, dict)

    @patch.object(ClcSnapshot, 'ensure_server_snapshot_present')
    @patch.object(ClcSnapshot, '_set_clc_credentials_from_env')
    def test_process_request_state_present(self, mock_set_clc_creds, mock_server_snapshot):
        test_params = {
            'server_ids': ['TESTSVR1', 'TESTSVR2']
            ,'expiration_days': 7
            ,'wait': True
            , 'state': 'present'
        }
        mock_server_snapshot.return_value = True, mock.MagicMock(), ['TESTSVR1']
        self.module.params = test_params
        self.module.check_mode = False

        under_test = ClcSnapshot(self.module)
        under_test.process_request()

        self.module.exit_json.assert_called_once_with(changed=True, server_ids=['TESTSVR1'])
        self.assertFalse(self.module.fail_json.called)

    @patch.object(ClcSnapshot, 'ensure_server_snapshot_absent')
    @patch.object(ClcSnapshot, '_set_clc_credentials_from_env')
    def test_process_request_state_absent(self, mock_set_clc_creds, mock_server_snapshot):
        test_params = {
            'server_ids': ['TESTSVR1', 'TESTSVR2']
            ,'expiration_days': 7
            ,'wait': True
            , 'state': 'absent'
        }
        mock_server_snapshot.return_value = True, mock.MagicMock(), ['TESTSVR1','TESTSVR2']
        self.module.params = test_params
        self.module.check_mode = False

        under_test = ClcSnapshot(self.module)
        under_test.process_request()

        self.module.exit_json.assert_called_once_with(changed=True, server_ids=['TESTSVR1', 'TESTSVR2'])
        self.assertFalse(self.module.fail_json.called)

    @patch.object(ClcSnapshot, 'ensure_server_snapshot_restore')
    @patch.object(ClcSnapshot, '_set_clc_credentials_from_env')
    def test_process_request_state_restore(self, mock_set_clc_creds, mock_server_snapshot):
        test_params = {
            'server_ids': ['TESTSVR1', 'TESTSVR2']
            ,'expiration_days': 7
            ,'wait': True
            , 'state': 'restore'
        }
        mock_server_snapshot.return_value = True, mock.MagicMock(), ['TESTSVR1']
        self.module.params = test_params
        self.module.check_mode = False

        under_test = ClcSnapshot(self.module)
        under_test.process_request()

        self.module.exit_json.assert_called_once_with(changed=True, server_ids=['TESTSVR1'])
        self.assertFalse(self.module.fail_json.called)


    @patch.object(ClcSnapshot, 'ensure_server_snapshot_present')
    @patch.object(ClcSnapshot, '_set_clc_credentials_from_env')
    def test_process_request_state_invalid(self, mock_set_clc_creds, mock_server_snapshot):
        test_params = {
            'server_ids': ['TESTSVR1', 'TESTSVR2']
            ,'expiration_days': 7
            ,'wait': True
            , 'state': 'INVALID'
        }

        self.module.params = test_params
        under_test = ClcSnapshot(self.module)
        under_test.process_request()
        self.assertFalse(mock_server_snapshot.called)
        self.module.fail_json.assert_called_once_with(msg='Unknown State: INVALID')
        self.assertFalse(self.module.exit_json.called)

    @patch.object(ClcSnapshot, '_get_servers_from_clc')
    def test_ensure_server_snapshot_present_w_mock_server(self,mock_get_servers):
        server_ids = ['TESTSVR1']
        mock_get_servers.return_value=[mock.MagicMock()]
        exp_days = 7
        self.module.check_mode = False
        under_test = ClcSnapshot(self.module)
        under_test.ensure_server_snapshot_present(server_ids, exp_days)
        self.assertFalse(self.module.fail_json.called)

    @patch.object(ClcSnapshot, '_get_servers_from_clc')
    def test_ensure_server_snapshot_absent_w_mock_server(self,mock_get_servers):
        server_ids = ['TESTSVR1']
        mock_server = mock.MagicMock()
        mock_server.id = 'TESTSVR1'
        mock_server.GetSnapshots.return_value = '123'
        mock_get_servers.return_value=[mock_server]
        self.module.check_mode = False

        under_test = ClcSnapshot(self.module)
        under_test.ensure_server_snapshot_absent(server_ids)
        self.assertFalse(self.module.fail_json.called)

    def test_wait_for_requests_w_mock_request(self):
        mock_r1 = mock.MagicMock()
        mock_r1.WaitUntilComplete.return_value = True
        mock_r2 = mock.MagicMock()
        mock_r2.WaitUntilComplete.return_value = True
        requests = [mock_r1, mock_r2]
        self.module.wait = True

        under_test = ClcSnapshot(self.module)
        under_test._wait_for_requests_to_complete(requests)
        self.assertFalse(self.module.fail_json.called)

    def test_wait_for_requests_w_mock_request_fail(self):
        mock_request = mock.MagicMock()
        mock_request.WaitUntilComplete.return_value = True
        mock_response = mock.MagicMock()
        mock_response.Status.return_value = 'Failed'
        mock_request.requests = [mock_response]
        requests = [mock_request]
        self.module.wait = True

        under_test = ClcSnapshot(self.module)
        under_test._wait_for_requests_to_complete(requests)
        self.assertTrue(self.module.fail_json.called)

    @patch.object(ClcSnapshot, '_get_servers_from_clc')
    def test_ensure_server_snapshot_restore_w_mock_server(self,mock_get_servers):
       server_ids = ['TESTSVR1']
       mock_server = mock.MagicMock()
       mock_server.id = 'TESTSVR1'
       mock_server.GetSnapshots.return_value = '123'
       mock_get_servers.return_value=[mock_server]
       self.module.check_mode = False
       under_test = ClcSnapshot(self.module)
       under_test.ensure_server_snapshot_restore(server_ids)
       self.assertFalse(self.module.fail_json.called)

    @patch.object(ClcSnapshot, 'clc')
    def test_get_servers_from_clc(self, mock_clc_sdk):
        mock_clc_sdk.v2.Servers.side_effect = CLCException("Server Not Found")
        under_test = ClcSnapshot(self.module)
        under_test._get_servers_from_clc(['TESTSVR1', 'TESTSVR2'], 'FAILED TO OBTAIN LIST')
        self.module.fail_json.assert_called_once_with(msg='FAILED TO OBTAIN LIST: Server Not Found')

    @patch.object(ClcSnapshot, '_get_servers_from_clc')
    def test_wait_for_requests_to_complete(self,mock_get_servers):
        server_ids = ['INVALID']
        mock_get_servers.return_value=[mock.MagicMock()]
        under_test = ClcSnapshot(self.module)
        under_test._wait_for_requests_to_complete (mock.MagicMock())
        self.assertFalse(self.module.fail_json.called)

    @patch.object(clc_server_snapshot, 'AnsibleModule')
    @patch.object(clc_server_snapshot, 'ClcSnapshot')
    def test_main(self, mock_ClcSnapshot, mock_AnsibleModule):
        mock_ClcSnapshot_instance       = mock.MagicMock()
        mock_AnsibleModule_instance     = mock.MagicMock()
        mock_ClcSnapshot.return_value   = mock_ClcSnapshot_instance
        mock_AnsibleModule.return_value = mock_AnsibleModule_instance

        clc_server_snapshot.main()

        mock_ClcSnapshot.assert_called_once_with(mock_AnsibleModule_instance)
        mock_ClcSnapshot_instance.process_request.assert_called_once()

if __name__ == '__main__':
    unittest.main()
