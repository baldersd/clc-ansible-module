#!/usr/bin/env python
# -*- coding: utf-8 -*-

# CenturyLink Cloud Ansible Modules.
#
# These Ansible modules enable the CenturyLink Cloud v2 API to be called
# from an within Ansible Playbook.
#
# This file is part of CenturyLink Cloud, and is maintained
# by the Workflow as a Service Team
#
# Copyright 2015 CenturyLink
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
#
# CenturyLink Cloud: http://www.CenturyLinkCloud.com
# API Documentation: https://www.centurylinkcloud.com/api-docs/v2/
#

DOCUMENTATION = '''
module: clc_server
short_description: Create, Delete, Start and Stop servers in CenturyLink Cloud.
description:
  - An Ansible module to Create, Delete, Start and Stop servers in CenturyLink Cloud.
version_added: "2.0"
options:
  additional_disks:
    description:
      - The list of additional disks for the server
    required: False
    default: []
  add_public_ip:
    description:
      - Whether to add a public ip to the server
    required: False
    default: False
    choices: [False, True]
  alias:
    description:
      - The account alias to provision the servers under.
    required: False
    default: None
  anti_affinity_policy_id:
    description:
      - The anti-affinity policy to assign to the server. This is mutually exclusive with 'anti_affinity_policy_name'.
    required: False
    default: None
  anti_affinity_policy_name:
    description:
      - The anti-affinity policy to assign to the server. This is mutually exclusive with 'anti_affinity_policy_id'.
    required: False
    default: None
  alert_policy_id:
    description:
      - The alert policy to assign to the server. This is mutually exclusive with 'alert_policy_name'.
    required: False
    default: None
  alert_policy_name:
    description:
      - The alert policy to assign to the server. This is mutually exclusive with 'alert_policy_id'.
    required: False
    default: None
  count:
    description:
      - The number of servers to build (mutually exclusive with exact_count)
    required: False
    default: 1
  count_group:
    description:
      - Required when exact_count is specified.  The Server Group use to determine how many severs to deploy.
    required: False
    default: None
  cpu:
    description:
      - How many CPUs to provision on the server
    default: 1
    required: False
  cpu_autoscale_policy_id:
    description:
      - The autoscale policy to assign to the server.
    default: None
    required: False
  custom_fields:
    description:
      - The list of custom fields to set on the server.
    default: []
    required: False
  description:
    description:
      - The description to set for the server.
    default: None
    required: False
  exact_count:
    description:
      - Run in idempotent mode.  Will insure that this exact number of servers are running in the provided group,
        creating and deleting them to reach that count.  Requires count_group to be set.
    default: None
    required: False
  min_count:
    description:
      - Run in idempotent mode. Will ensure that there are least this number of servers running in the provided group,
        creating them to reach that count. Requires count_group to be set.
    default: None
    required: False
  max_count:
    description:
      - Run in idempotent mode. Will ensure that there are no more than this number of servers running in the provided
        group, deleting them to reach that count. Requires count_group to be set.
    default: None
    required: False
  group:
    description:
      - The Server Group to create servers under.
    default: 'Default Group'
    required: False
  ip_address:
    description:
      - The IP Address for the server. One is assigned if not provided.
    default: None
    required: False
  location:
    description:
      - The Datacenter to create servers in.
    default: None
    required: False
  managed_os:
    description:
      - Whether to create the server as 'Managed' or not.
    default: False
    required: False
    choices: [True, False]
  memory:
    description:
      - Memory in GB.
    default: 1
    required: False
  name:
    description:
      - A 1 to 6 character identifier to use for the server. This is required when state is 'present'
    default: None
    required: False
  network_id:
    description:
      - The network on which to create servers. Searches by UUID, name, or cidr.
    default: None
    required: False
  packages:
    description:
      - The list of blue print packages to run on the server after its created.
    default: []
    required: False
  password:
    description:
      - Password for the administrator / root user
    default: None
    required: False
  primary_dns:
    description:
      - Primary DNS used by the server.
    default: None
    required: False
  public_ip_protocol:
    description:
      - The protocol to use for the public ip if add_public_ip is set to True.
    default: 'TCP'
    choices: ['TCP', 'UDP', 'ICMP']
    required: False
  public_ip_ports:
    description:
      - A list of ports to allow on the firewall to the servers public ip, if add_public_ip is set to True.
    default: []
    required: False
  secondary_dns:
    description:
      - Secondary DNS used by the server.
    default: None
    required: False
  server_ids:
    description:
      - Required for started, stopped, and absent states.
        A list of server Ids to insure are started, stopped, or absent.
    default: []
    required: False
  source_server_password:
    description:
      - The password for the source server if a clone is specified.
    default: None
    required: False
  state:
    description:
      - The state to insure that the provided resources are in.
    default: 'present'
    required: False
    choices: ['present', 'absent', 'started', 'stopped']
  storage_type:
    description:
      - The type of storage to attach to the server.
    default: 'standard'
    required: False
    choices: ['standard', 'hyperscale']
  template:
    description:
      - The template to use for server creation.  Will search for a template if a partial string is provided.
        This is required when state is 'present'
    default: None
    required: False
  ttl:
    description:
      - The time to live for the server in seconds.  The server will be deleted when this time expires.
    default: None
    required: False
  type:
    description:
      - The type of server to create.
    default: 'standard'
    required: False
    choices: ['standard', 'hyperscale', 'bareMetal']
  configuration_id:
    description:
      -  Only required for bare metal servers.
         Specifies the identifier for the specific configuration type of bare metal server to deploy.
    default: None
    required: False
  os_type:
    description:
      - Only required for bare metal servers.
        Specifies the OS to provision with the bare metal server.
    default: None
    required: False
    choices: ['redHat6_64Bit', 'centOS6_64Bit', 'windows2012R2Standard_64Bit', 'ubuntu14_64Bit']
  wait:
    description:
      - Whether to wait for the provisioning tasks to finish before returning.
    default: True
    required: False
    choices: [True, False]
requirements:
    - python = 2.7
    - clc-sdk
author: "CLC Runner (@clc-runner)"
notes:
    - To use this module, it is required to set the below environment variables which enables access to the
      Centurylink Cloud
          - CLC_V2_API_USERNAME, the account login id for the centurylink cloud
          - CLC_V2_API_PASSWORD, the account password for the centurylink cloud
    - Alternatively, the module accepts the API token and account alias. The API token can be generated using the
      CLC account login and password via the HTTP api call @ https://api.ctl.io/v2/authentication/login
          - CLC_V2_API_TOKEN, the API token generated from https://api.ctl.io/v2/authentication/login
          - CLC_ACCT_ALIAS, the account alias associated with the centurylink cloud
    - Users can set CLC_V2_API_URL to specify an endpoint for pointing to a different CLC environment.
'''

EXAMPLES = '''
# Note - You must set the CLC_V2_API_USERNAME And CLC_V2_API_PASSWD Environment variables before running these examples

- name: Provision a single Ubuntu Server
  clc_server:
    name: test
    template: ubuntu-14-64
    count: 1
    group: 'Default Group'
    state: present

- name: Ensure 'Default Group' has exactly 5 servers
  clc_server:
    name: test
    template: ubuntu-14-64
    exact_count: 5
    count_group: 'Default Group'
    group: 'Default Group'

- name: Stop a Server
  clc_server:
    server_ids: ['UC1ACCT-TEST01']
    state: stopped

- name: Start a Server
  clc_server:
    server_ids: ['UC1ACCT-TEST01']
    state: started

- name: Delete a Server
  clc_server:
    server_ids: ['UC1ACCT-TEST01']
    state: absent

- name: Ensure 'Default Group' has at least 3 servers
  clc_server:
    name: test
    template: ubuntu-14-64
    min_count: 3
    count_group: 'Default Group'
'''

RETURN = '''
changed:
    description: A flag indicating if any change was made or not
    returned: success
    type: boolean
    sample: True
group:
    description: The state of the group after all operations have completed. If wait is False then this value is not set.
    returned: success
    type: dict
    sample:
        {
            "changeInfo": {
                "createdBy": "service.wfad",
                "createdDate": "2016-05-03T17:04:01Z",
                "modifiedBy": "service.wfad",
                "modifiedDate": "2016-05-03T17:04:01Z"
            },
            "customFields": [],
            "description": "A group for my servers",
            "groups": [],
            "id": "162274ff03164eeea2e0f6173cfdd59e",
            "locationId": "CA3",
            "name": "My Server Group",
            "servers": [
                "CA3T3DATEST06",
                "CA3T3DATEST07"
            ],
            "serversCount": 2,
            "status": "active",
            "type": "default"
        }
server_ids:
    description: The list of server ids that are created
    returned: success
    type: list
    sample:
        [
            "UC1TEST-SVR01",
            "UC1TEST-SVR02"
        ]
partially_created_server_ids:
    description: The list of server ids that are partially created
    returned: success
    type: list
    sample:
        [
            "UC1TEST-SVR01",
            "UC1TEST-SVR02"
        ]
servers:
    description: The list of server objects returned from CLC
    returned: success
    type: list
    sample:
        [
           {
              "changeInfo":{
                 "createdBy":"service.wfad",
                 "createdDate":2016-05-03T17:04:01Z,
                 "modifiedBy":"service.wfad",
                 "modifiedDate":2016-05-03T17:04:01Z
              },
              "description":"test-server",
              "details":{
                 "alertPolicies":[

                 ],
                 "cpu":1,
                 "customFields":[

                 ],
                 "diskCount":3,
                 "disks":[
                    {
                       "id":"0:0",
                       "partitionPaths":[

                       ],
                       "sizeGB":1
                    },
                    {
                       "id":"0:1",
                       "partitionPaths":[

                       ],
                       "sizeGB":2
                    },
                    {
                       "id":"0:2",
                       "partitionPaths":[

                       ],
                       "sizeGB":14
                    }
                 ],
                 "hostName":"",
                 "inMaintenanceMode":false,
                 "ipAddresses":[
                    {
                       "internal":"10.1.1.1"
                    }
                 ],
                 "memoryGB":1,
                 "memoryMB":1024,
                 "partitions":[

                 ],
                 "powerState":"started",
                 "snapshots":[

                 ],
                 "storageGB":17
              },
              "groupId":"086ac1dfe0b6411989e8d1b77c4065f0",
              "id":"test-server",
              "ipaddress":"10.1.1.1",
              "isTemplate":false,
              "links":[
                 {
                    "href":"/v2/servers/wfad/test-server",
                    "id":"test-server",
                    "rel":"self",
                    "verbs":[
                       "GET",
                       "PATCH",
                       "DELETE"
                    ]
                 },
                 {
                    "href":"/v2/groups/wfad/086ac1dfe0b6411989e8d1b77c4065f0",
                    "id":"086ac1dfe0b6411989e8d1b77c4065f0",
                    "rel":"group"
                 },
                 {
                    "href":"/v2/accounts/wfad",
                    "id":"wfad",
                    "rel":"account"
                 },
                 {
                    "href":"/v2/billing/wfad/serverPricing/test-server",
                    "rel":"billing"
                 },
                 {
                    "href":"/v2/servers/wfad/test-server/publicIPAddresses",
                    "rel":"publicIPAddresses",
                    "verbs":[
                       "POST"
                    ]
                 },
                 {
                    "href":"/v2/servers/wfad/test-server/credentials",
                    "rel":"credentials"
                 },
                 {
                    "href":"/v2/servers/wfad/test-server/statistics",
                    "rel":"statistics"
                 },
                 {
                    "href":"/v2/servers/wfad/510ec21ae82d4dc89d28479753bf736a/upcomingScheduledActivities",
                    "rel":"upcomingScheduledActivities"
                 },
                 {
                    "href":"/v2/servers/wfad/510ec21ae82d4dc89d28479753bf736a/scheduledActivities",
                    "rel":"scheduledActivities",
                    "verbs":[
                       "GET",
                       "POST"
                    ]
                 },
                 {
                    "href":"/v2/servers/wfad/test-server/capabilities",
                    "rel":"capabilities"
                 },
                 {
                    "href":"/v2/servers/wfad/test-server/alertPolicies",
                    "rel":"alertPolicyMappings",
                    "verbs":[
                       "POST"
                    ]
                 },
                 {
                    "href":"/v2/servers/wfad/test-server/antiAffinityPolicy",
                    "rel":"antiAffinityPolicyMapping",
                    "verbs":[
                       "PUT",
                       "DELETE"
                    ]
                 },
                 {
                    "href":"/v2/servers/wfad/test-server/cpuAutoscalePolicy",
                    "rel":"cpuAutoscalePolicyMapping",
                    "verbs":[
                       "PUT",
                       "DELETE"
                    ]
                 }
              ],
              "locationId":"UC1",
              "name":"test-server",
              "os":"ubuntu14_64Bit",
              "osType":"Ubuntu 14 64-bit",
              "status":"active",
              "storageType":"standard",
              "type":"standard"
           }
        ]
'''

__version__ = '${version}'

import clc_ansible_utils.clc as clc_common
from clc_ansible_utils.clc import ClcApiException


class ClcServer(object):

    def __init__(self, module):
        """
        Construct module
        """
        self.clc_auth = {}
        self.module = module
        self.root_group = None

    def process_request(self):
        """
        Process the request - Main Code Path
        :return: Returns with either an exit_json or fail_json
        """
        changed = False
        new_server_ids = []
        server_dict_array = []

        self.clc_auth = clc_common.authenticate(self.module)
        self.module.params = self._validate_module_params()
        p = self.module.params
        state = p.get('state')

        #
        #  Handle each state
        #
        partial_servers_ids = []
        if state == 'absent':
            server_ids = p['server_ids']
            if not isinstance(server_ids, list):
                return self.module.fail_json(
                    msg='server_ids needs to be a list of instances to delete: %s' %
                    server_ids)

            (changed,
             server_dict_array,
             new_server_ids) = self._delete_servers(server_ids=server_ids)

        elif state in ('started', 'stopped'):
            server_ids = p.get('server_ids')
            if not isinstance(server_ids, list):
                return self.module.fail_json(
                    msg='server_ids needs to be a list of servers to run: %s' %
                    server_ids)

            (changed,
             server_dict_array,
             new_server_ids) = self._start_stop_servers(server_ids)

        elif state == 'present':
            # Changed is always set to true when provisioning new instances
            if not p.get('template') and p.get('type') != 'bareMetal':
                return self.module.fail_json(
                    msg='template parameter is required for new instance')

            if p.get('exact_count') is None and p.get('min_count') is None and p.get('max_count') is None:
                (server_dict_array,
                 new_server_ids,
                 partial_servers_ids,
                 changed) = self._create_servers()
            else:
                (server_dict_array,
                 new_server_ids,
                 partial_servers_ids,
                 changed) = self._enforce_count()

        group = None
        wait = self.module.params.get('wait')
        if wait:
            datacenter = self._find_datacenter()
            group = self._find_group(datacenter, lookup_group=p.get('group'))
            try:
                servers = clc_common.servers_in_group(
                    self.module, self.clc_auth, group)
                group = group.data
                group['servers'] = [s.id for s in servers]
            except AttributeError:
                group = group.name

        self.module.exit_json(
            changed=changed,
            server_ids=new_server_ids,
            group=group,
            partially_created_server_ids=partial_servers_ids,
            servers=server_dict_array)

    @staticmethod
    def _define_module_argument_spec():
        """
        Define the argument spec for the ansible module
        :return: argument spec dictionary
        """
        argument_spec = dict(
            name=dict(),
            template=dict(),
            group=dict(default='Default Group'),
            network_id=dict(),
            location=dict(default=None),
            cpu=dict(default=1, type='int'),
            memory=dict(default=1, type='int'),
            alias=dict(default=None),
            password=dict(default=None, no_log=True),
            ip_address=dict(default=None),
            storage_type=dict(
                default='standard',
                choices=[
                    'standard',
                    'hyperscale']),
            type=dict(default='standard', choices=['standard', 'hyperscale', 'bareMetal']),
            primary_dns=dict(default=None),
            secondary_dns=dict(default=None),
            additional_disks=dict(type='list', default=[]),
            custom_fields=dict(type='list', default=[]),
            ttl=dict(default=None),
            managed_os=dict(type='bool', default=False),
            description=dict(default=None),
            source_server_password=dict(default=None),
            cpu_autoscale_policy_id=dict(default=None),
            anti_affinity_policy_id=dict(default=None),
            anti_affinity_policy_name=dict(default=None),
            alert_policy_id=dict(default=None),
            alert_policy_name=dict(default=None),
            packages=dict(type='list', default=[]),
            state=dict(
                default='present',
                choices=[
                    'present',
                    'absent',
                    'started',
                    'stopped']),
            count=dict(type='int', default=1),
            exact_count=dict(type='int', default=None),
            min_count=dict(type='int', default=None),
            max_count=dict(type='int', default=None),
            count_group=dict(),
            server_ids=dict(type='list', default=[]),
            add_public_ip=dict(type='bool', default=False),
            public_ip_protocol=dict(
                default='TCP',
                choices=[
                    'TCP',
                    'UDP',
                    'ICMP']),
            public_ip_ports=dict(type='list', default=[]),
            configuration_id=dict(default=None),
            os_type=dict(default=None,
                         choices=[
                             'redHat6_64Bit',
                             'centOS6_64Bit',
                             'windows2012R2Standard_64Bit',
                             'ubuntu14_64Bit'
                         ]),
            wait=dict(type='bool', default=True))

        mutually_exclusive = [
            ['exact_count', 'count'],
            ['exact_count', 'state'],
            ['min_count', 'exact_count'],
            ['min_count', 'count'],
            ['min_count', 'state'],
            ['max_count', 'exact_count'],
            ['max_count', 'count'],
            ['max_count', 'state'],
            ['anti_affinity_policy_id', 'anti_affinity_policy_name'],
            ['alert_policy_id', 'alert_policy_name'],
        ]
        return {"argument_spec": argument_spec,
                "mutually_exclusive": mutually_exclusive}

    def _validate_module_params(self):
        """
        Validate the module params, and lookup default values.
        :param clc: clc-sdk instance to use
        :param module: module to validate
        :return: dictionary of validated params
        """
        module = self.module
        params = module.params

        # Grab the alias so that we can properly validate server name
        alias = self._find_alias()

        datacenter = self._find_datacenter()

        ClcServer._validate_types(module)
        ClcServer._validate_name(module, alias)
        ClcServer._validate_counts(module)

        params['alias'] = alias
        group = self._find_group(datacenter)
        group.defaults = self._group_defaults(group)
        params['group'] = group.id
        params['cpu'] = self._find_cpu(group)
        params['memory'] = self._find_memory(group)
        params['description'] = ClcServer._find_description(module)
        params['ttl'] = ClcServer._find_ttl(module)
        params['template'] = self._find_template_id(datacenter)
        params['network_id'] = self._find_network_id(datacenter)
        params['anti_affinity_policy_id'] = self._find_aa_policy_id()
        params['alert_policy_id'] = self._find_alert_policy_id()

        return params

    def _group_defaults(self, group):
        try:
            if 'clc_alias' not in self.clc_auth:
                self.clc_auth = clc_common.authenticate(self.module)
            defaults = clc_common.call_clc_api(
                self.module, self.clc_auth,
                'GET', '/groups/{alias}/{id}/defaults'.format(
                    alias=self.clc_auth['clc_alias'], id=group.id))
        except ClcApiException as ex:
            return self.module.fail_json(
                msg='Failed to get group defaults for group: {name}'.format(
                    name=group.name))
        return defaults

    def _group_default_value(self, group, key):
        if not hasattr(group, 'defaults'):
            group.defaults = self._group_defaults(group)
        try:
            return group.defaults[key]['value']
        except KeyError:
            return None

    def _find_datacenter(self):
        """
        Find or Validate the datacenter by calling the CLC API.
        :return: Datacenter ID
        """
        location = self.module.params.get('location')
        try:
            if 'clc_location' not in self.clc_auth:
                self.clc_auth = clc_common.authenticate(self.module)
            if not location:
                location = self.clc_auth['clc_location']
            else:
                # Override authentication with user-provided location
                self.clc_auth['clc_location'] = location
            return location
        except ClcApiException as ex:
            self.module.fail_json(
                msg=str(
                    "Unable to find location: {location}".format(
                        location=location)))

    def _find_alias(self):
        """
        Find or Validate the Account Alias by calling the CLC API
        :return: Account alias
        """
        alias = self.module.params.get('alias')
        try:
            if 'clc_alias' not in self.clc_auth:
                self.clc_auth = clc_common.authenticate(self.module)
            if not alias:
                alias = self.clc_auth['clc_alias']
            elif alias:
                # Override authentication with user-provided alias
                self.clc_auth['clc_alias'] = alias
            return alias
        except ClcApiException as ex:
            self.module.fail_json(
                msg='Unable to find account alias. {msg}'.format(
                    msg=ex.message))

    def _find_cpu(self, group):
        """
        Find or validate the CPU value by calling the CLC API
        :group: Group object for which to find defaults
        :return: Int value for CPU
        """
        cpu = self.module.params.get('cpu')
        state = self.module.params.get('state')

        if not cpu and state == 'present':
            cpu = self._group_default_value(group, 'cpu')
            if cpu is None:
                self.module.fail_json(
                    msg=str("Can\'t determine a default cpu value. "
                            "Please provide a value for cpu."))
        return cpu

    def _find_memory(self, group):
        """
        Find or validate the Memory value by calling the CLC API
        :group: Group object for which to find defaults
        :return: Int value for Memory
        """
        memory = self.module.params.get('memory')
        state = self.module.params.get('state')

        if not memory and state == 'present':
            memory = self._group_default_value(group, 'memory')
            if memory is None:
                self.module.fail_json(msg=str(
                    "Can\'t determine a default memory value. "
                    "Please provide a value for memory."))
        return memory

    @staticmethod
    def _find_description(module):
        """
        Set the description module param to name if description is blank
        :param module: the module to validate
        :return: string description
        """
        description = module.params.get('description')
        if not description:
            description = module.params.get('name')
        return description

    @staticmethod
    def _validate_types(module):
        """
        Validate that type and storage_type are set appropriately, and fail if not
        :param module: the module to validate
        :return: none
        """
        state = module.params.get('state')
        server_type = module.params.get(
            'type').lower() if module.params.get('type') else None
        storage_type = module.params.get(
            'storage_type').lower() if module.params.get('storage_type') else None

        if state == "present":
            if server_type == "standard" and storage_type not in (
                    "standard", "premium"):
                module.fail_json(
                    msg=str("Standard VMs must have storage_type = 'standard' or 'premium'"))

            if server_type == "hyperscale" and storage_type != "hyperscale":
                module.fail_json(
                    msg=str("Hyperscale VMs must have storage_type = 'hyperscale'"))

    @staticmethod
    def _validate_name(module, alias):
        """
        Validate that name is the correct length if provided, fail if it's not
        :param module: the module to validate
        :return: none
        """
        server_name = module.params.get('name')
        state = module.params.get('state')

        if state == 'present' and (
                len(server_name) < 1 or (len(server_name) + len(alias)) > 10):
            module.fail_json(msg=str(
                "When state = 'present', length of account alias + name must be a string with a minimum length of 1 and a maximum length of 10"))

    @staticmethod
    def _validate_counts(module):
        """
        Validate that count parameters are valid, fail if it's not
        :param module: the module to validate
        :return: none
        """
        exact_count = module.params.get('exact_count')
        count = module.params.get('count')
        min_count = module.params.get('min_count')
        max_count = module.params.get('max_count')

        if count is not None and count < 0:
            module.fail_json(msg='count must be 0 or greater')
        if exact_count is not None and exact_count < 0:
            module.fail_json(msg='exact_count must be 0 or greater')
        if min_count is not None and min_count < 0:
            module.fail_json(msg='min_count must be 0 or greater')
        if max_count is not None and max_count < 0:
            module.fail_json(msg='max_count must be 0 or greater')
        if (min_count is not None and max_count is not None and
                min_count > max_count):
            module.fail_json(msg='min_count cannot be greater than max_count')

    @staticmethod
    def _find_ttl(module):
        """
        Validate that TTL is > 3600 if set, and fail if not
        :param module: module to validate
        :return: validated ttl
        """
        ttl = module.params.get('ttl')
        if not ttl:
            return None

        try:
            ttl = int(ttl)
        except ValueError as ve:
            module.fail_json(msg=str("Invalid value for ttl. Ttl should be an integer >= 3600"))
        if ttl <= 3600:
            return module.fail_json(msg=str("Ttl cannot be <= 3600"))
        else:
            ttl = (datetime.datetime.utcnow() +
                   datetime.timedelta(seconds=ttl)).strftime(
                        '%Y-%m-%dT%H:%M:%SZ')
        return ttl

    def _find_template_id(self, datacenter):
        """
        Find the template id by calling the CLC API.
        :param module: the module to validate
        :param datacenter: the datacenter to search for the template
        :return: a valid clc template id
        """
        lookup_template = self.module.params.get('template')
        state = self.module.params.get('state')
        server_type = self.module.params.get('type')
        result = None
        if lookup_template is None:
            return result

        if state == 'present' and server_type != 'bareMetal':
            try:
                templates = clc_common.call_clc_api(
                    self.module, self.clc_auth,
                    'GET', '/datacenters/{alias}/{location}/deploymentCapabilities'.format(
                        alias=self.clc_auth['clc_alias'],
                        location=datacenter))['templates']
                for template in templates:
                    if template['name'].lower().find(
                            lookup_template.lower()) != -1:
                        return template['name']
            except ClcApiException:
                self.module.fail_json(
                    msg=str(
                        "Unable to find a template: " +
                        lookup_template +
                        " in location: " +
                        datacenter))
        return result

    def _find_network_id(self, datacenter):
        """
        Validate the provided network id or return a default.
        :param datacenter: the datacenter to search for a network id
        :return: a valid network id
        """
        network_id_search = self.module.params.get('network_id')

        network = clc_common.find_network(
            self.module, self.clc_auth, datacenter, network_id_search)
        if network is None:
            return self.module.fail_json(
                msg='No matching network: {network} '
                    'found in location: {location}'.format(
                        network=network_id_search, location=datacenter))
        return network.id

    def _find_aa_policy_id(self):
        """
        Validate if the anti affinity policy exist for the given name and throw error if not
        :return: aa_policy_id: the anti affinity policy id of the given name.
        """

        params = self.module.params
        search_key = (params.get('anti_affinity_policy_id') or
                      params.get('anti_affinity_policy_name'))

        aa_policy_id = None

        if search_key is not None:
            aa_policy = clc_common.find_anti_affinity_policy(
                self.module, self.clc_auth, search_key)
            if aa_policy is not None:
                aa_policy_id = aa_policy['id']
            else:
                return self.module.fail_json(
                    msg='No anti affinity policy matching: {search}.'.format(
                        search=search_key))

        return aa_policy_id

    def _find_alert_policy_id(self):
        """
        Validate if the alert policy exist for the given name and throw error if not
        :return: alert_policy_id: the alert policy id of the given name.
        """
        alert_policy_id = self.module.params.get('alert_policy_id')
        alert_policy_name = self.module.params.get('alert_policy_name')
        if not alert_policy_id and alert_policy_name:
            alert_policy_id = self._get_alert_policy_id_by_name(
                alert_policy_name=alert_policy_name)
            if not alert_policy_id:
                self.module.fail_json(
                    msg='No alert policy exist with name : %s' % alert_policy_name)
        return alert_policy_id

    def _create_servers(self, override_count=None):
        """
        Create New Servers in CLC cloud
        :return: a list of dictionaries with server information about the servers that were created
        """
        p = self.module.params
        request_list = []
        servers = []
        server_dict_array = []
        created_server_ids = []
        partial_created_servers_ids = []

        add_public_ip = p.get('add_public_ip')
        public_ip_protocol = p.get('public_ip_protocol')
        public_ip_ports = p.get('public_ip_ports')

        params = {
            'name': p.get('name'),
            'template': p.get('template'),
            'group_id': p.get('group'),
            'network_id': p.get('network_id'),
            'cpu': p.get('cpu'),
            'memory': p.get('memory'),
            'alias': p.get('alias'),
            'password': p.get('password'),
            'ip_address': p.get('ip_address'),
            'storage_type': p.get('storage_type'),
            'type': p.get('type'),
            'primary_dns': p.get('primary_dns'),
            'secondary_dns': p.get('secondary_dns'),
            'additional_disks': p.get('additional_disks'),
            'custom_fields': p.get('custom_fields'),
            'ttl': p.get('ttl'),
            'managed_os': p.get('managed_os'),
            'description': p.get('description'),
            'source_server_password': p.get('source_server_password'),
            'cpu_autoscale_policy_id': p.get('cpu_autoscale_policy_id'),
            'anti_affinity_policy_id': p.get('anti_affinity_policy_id'),
            'packages': p.get('packages'),
            'configuration_id': p.get('configuration_id'),
            'os_type': p.get('os_type')
        }

        count = override_count if override_count else p.get('count')

        changed = False if count == 0 else True

        if not changed:
            return server_dict_array, created_server_ids, partial_created_servers_ids, changed
        for i in range(0, count):
            if not self.module.check_mode:
                result, server = self._create_clc_server(server_params=params)
                request_list.append(result)
                servers.append(server)

        self._wait_for_requests(request_list)
        servers = self._refresh_servers(servers)

        ip_failed_servers = self._add_public_ip_to_servers(
            should_add_public_ip=add_public_ip,
            servers=servers,
            public_ip_protocol=public_ip_protocol,
            public_ip_ports=public_ip_ports)
        ap_failed_servers = self._add_alert_policy_to_servers(servers)

        for server in servers:
            if server in ip_failed_servers or server in ap_failed_servers:
                partial_created_servers_ids.append(server.id)
            else:
                # reload server details
                server = clc_common.find_server(self.module, self.clc_auth,
                                                server.id)

                try:
                    server.data['ipaddress'] = [
                        ip['internal'] for ip
                        in server.data['details']['ipAddresses']
                        if 'internal' in ip][0]
                    server.data['publicip'] = [
                        ip['public'] for ip
                        in server.data['details']['ipAddresses']
                        if 'public' in ip][0]
                except (KeyError, IndexError):
                    pass
                created_server_ids.append(server.id)
            server_dict_array.append(server.data)

        return server_dict_array, created_server_ids, partial_created_servers_ids, changed

    def _enforce_count(self):
        """
        Enforce that there is the right number of servers in the provided group.
        Starts or stops servers as necessary.
        :return: a list of dictionaries with server information about the servers that were created or deleted
        """
        p = self.module.params
        changed = False
        count_group = p.get('count_group')
        datacenter = self._find_datacenter()
        exact_count = p.get('exact_count')
        min_count = p.get('min_count')
        max_count = p.get('max_count')
        server_dict_array = []
        partial_servers_ids = []
        changed_server_ids = []

        # fail here if the exact count was specified without filtering
        # on a group, as this may lead to a undesired removal of instances
        if exact_count is not None and count_group is None:
            return self.module.fail_json(
                msg="you must use the 'count_group' option with exact_count")

        if min_count is not None and count_group is None:
            return self.module.fail_json(
                msg="you must use the 'count_group' option with min_count")

        if max_count is not None and count_group is None:
            return self.module.fail_json(
                msg="you must use the 'count_group option with max_count")

        servers, running_servers = self._find_running_servers_by_group(
            datacenter, count_group)

        if exact_count is not None:
            if len(running_servers) < exact_count:
                to_create = exact_count - len(running_servers)
                server_dict_array, changed_server_ids, partial_servers_ids, changed \
                    = self._create_servers(override_count=to_create)

                for server in server_dict_array:
                    running_servers.append(server)

            elif len(running_servers) > exact_count:
                to_remove = len(running_servers) - exact_count
                all_server_ids = sorted([x.id for x in running_servers])
                remove_ids = all_server_ids[0:to_remove]

                (changed, server_dict_array, changed_server_ids) \
                    = self._delete_servers(remove_ids)

        if min_count is not None:
            if len(running_servers) < min_count:
                to_create = min_count - len(running_servers)
                server_dict_array, changed_server_ids, partial_servers_ids, changed \
                    = self._create_servers(override_count=to_create)

                for server in server_dict_array:
                    running_servers.append(server)

        if max_count is not None:
            if len(running_servers) > max_count:
                to_remove = len(running_servers) - max_count
                all_server_ids = sorted([x.id for x in running_servers])
                remove_ids = all_server_ids[0:to_remove]

                changed, server_dict_array, changed_server_ids \
                    = self._delete_servers(remove_ids)

        return server_dict_array, changed_server_ids, partial_servers_ids, changed

    def _wait_for_requests(self, request_list):
        """
        Block until server provisioning requests are completed.
        :param request_list: a list of CLC API JSON responses
        :return: none
        """
        wait = self.module.params.get('wait')
        if wait:
            failed_requests_count = clc_common.wait_on_completed_operations(
                self.module, self.clc_auth,
                clc_common.operation_id_list(request_list))

            if failed_requests_count > 0:
                self.module.fail_json(
                    msg='Unable to process server request')

    def _refresh_servers(self, servers):
        """
        Loop through a list of servers and refresh them.
        :param servers: list of Server objects to refresh
        :return: none
        """
        server_ids = [s.id for s in servers]
        try:
            refreshed_servers = clc_common.servers_by_id(self.module,
                                                         self.clc_auth,
                                                         server_ids)
        except ClcApiException as ex:
            return self.module.fail_json(
                msg='Unable to refresh servers. {msg}'.format(
                    msg=ex.message))
        return refreshed_servers

    def _add_public_ip_to_servers(self, should_add_public_ip, servers,
                                  public_ip_protocol, public_ip_ports):
        """
        Create a public IP for servers
        :param should_add_public_ip: boolean - whether or not to provision a public ip for servers.  Skipped if False
        :param servers: List of servers to add public ips to
        :param public_ip_protocol: a protocol to allow for the public ips
        :param public_ip_ports: list of ports to allow for the public ips
        :return: none
        """
        failed_servers = []
        if not should_add_public_ip:
            return failed_servers

        ports_lst = []
        request_list = []
        server = None

        for port in public_ip_ports:
            ports_lst.append(
                {'protocol': public_ip_protocol, 'port': port})
        if not self.module.check_mode:
            for server in servers:
                try:
                    request = clc_common.call_clc_api(
                        self.module, self.clc_auth,
                        'POST',
                        '/servers/{alias}/{id}/publicIPAddresses'.format(
                            alias=self.clc_auth['clc_alias'], id=server.id),
                        data={'ports': ports_lst})
                    request_list.append(request)
                except ClcApiException:
                    failed_servers.append(server)
        self._wait_for_requests(request_list)
        return failed_servers

    def _add_alert_policy_to_servers(self, servers):
        """
        Associate the alert policy to servers
        :param servers: List of servers to add alert policy to
        :return: failed_servers: the list of servers which failed while associating alert policy
        """
        failed_servers = []
        p = self.module.params
        alert_policy_id = p.get('alert_policy_id')

        if alert_policy_id and not self.module.check_mode:
            for server in servers:
                try:
                    self._add_alert_policy_to_server(
                        server_id=server.id,
                        alert_policy_id=alert_policy_id)
                except ClcApiException:
                    failed_servers.append(server)
        return failed_servers

    def _add_alert_policy_to_server(self, server_id, alert_policy_id):
        """
        Associate an alert policy to a clc server
        :param server_id: The clc server id
        :param alert_policy_id: the alert policy id to be associated to the server
        :return: none
        """
        try:
            result = clc_common.call_clc_api(
                self.module, self.clc_auth,
                'POST', '/servers/{alias}/{id}/alertPolicies'.format(
                    alias=self.clc_auth['clc_alias'], id=server_id),
                data={'id': alert_policy_id})
        except ClcApiException as e:
            raise ClcApiException(
                'Failed to associate alert policy to the server : {id} '
                'with Error {msg}'.format(
                    id=server_id, msg=str(e.message)))

    def _get_alert_policy_id_by_name(self, alert_policy_name):
        """
        Returns the alert policy id for the given alert policy name
        :param alias: the clc account alias
        :param alert_policy_name: the name of the alert policy
        :return: alert_policy_id: the alert policy id
        """
        alert_policy_id = None
        try:
            alert_policies = clc_common.call_clc_api(
                self.module, self.clc_auth,
                'GET', '/alertPolicies/{alias}'.format(
                    alias=self.clc_auth['clc_alias']))
            for policy in alert_policies['items']:
                if policy['name'].lower() == alert_policy_name.lower():
                    if not alert_policy_id:
                        alert_policy_id = policy.get('id')
                    else:
                        return self.module.fail_json(
                            msg='multiple alert policies were found with policy name : %s' % alert_policy_name)
        except ClcApiException as ex:
                return self.module.fail_json(
                    msg='Unable to fetch alert policies for '
                        'account: {alias}. {msg}'.format(
                            alias=self.clc_auth['clc_alias'], msg=ex.message))
        return alert_policy_id

    def _delete_servers(self, server_ids):
        """
        Delete the servers on the provided list
        :param server_ids: list of servers to delete
        :return: a list of dictionaries with server information about the servers that were deleted
        """
        terminated_server_ids = []
        server_dict_array = []
        request_list = []

        if not isinstance(server_ids, list) or len(server_ids) < 1:
            return self.module.fail_json(
                msg='server_ids should be a list of servers, aborting')

        servers = clc_common.servers_by_id(self.module, self.clc_auth,
                                           server_ids)
        for server in servers:
            if not self.module.check_mode:
                request_list.append(clc_common.call_clc_api(
                    self.module, self.clc_auth,
                    'DELETE', '/servers/{alias}/{id}'.format(
                        alias=self.clc_auth['clc_alias'], id=server.id)))
        self._wait_for_requests(request_list)

        for server in servers:
            terminated_server_ids.append(server.id)

        return True, server_dict_array, terminated_server_ids

    def _start_stop_servers(self, server_ids):
        """
        Start or Stop the servers on the provided list
        :param server_ids: list of servers to start or stop
        :return: a list of dictionaries with server information about the servers that were started or stopped
        """
        p = self.module.params
        state = p.get('state')
        changed = False
        changed_servers = []
        unchanged_servers = []
        server_dict_array = []
        result_server_ids = []
        request_list = []

        if not isinstance(server_ids, list) or len(server_ids) < 1:
            return self.module.fail_json(
                msg='server_ids should be a list of servers, aborting')

        servers = clc_common.servers_by_id(self.module, self.clc_auth,
                                           server_ids)
        for server in servers:
            if server.powerState != state:
                changed_servers.append(server)
                if not self.module.check_mode:
                    request_list.append(
                        self._change_server_power_state(
                            server,
                            state))
                changed = True
            else:
                unchanged_servers.append(server)

        self._wait_for_requests(request_list)
        changed_servers = self._refresh_servers(changed_servers)

        for server in set(changed_servers + unchanged_servers):
            try:
                server.data['ipaddress'] = [
                    ip['internal'] for ip
                    in server.data['details']['ipAddresses']
                    if 'internal' in ip][0]
                server.data['publicip'] = [
                    ip['public'] for ip
                    in server.data['details']['ipAddresses']
                    if 'public' in ip][0]
            except (KeyError, IndexError):
                pass

            server_dict_array.append(server.data)
            result_server_ids.append(server.id)

        return changed, server_dict_array, result_server_ids

    def _change_server_power_state(self, server, state):
        """
        Change the server powerState
        :param module: the module to check for intended state
        :param server: the server to start or stop
        :param state: the intended powerState for the server
        :return: the request object from clc-sdk call
        """
        result = None
        try:
            if state == 'started':
                operation = 'powerOn'
            else:
                operation = 'shutDown'
            result = clc_common.call_clc_api(
                self.module, self.clc_auth,
                'POST', '/operations/{alias}/servers/{operation}'.format(
                    alias=self.clc_auth['clc_alias'], operation=operation),
                data=[server.id])
            # TODO: check whether server shutDown, if not run powerOff

        except ClcApiException:
            self.module.fail_json(
                msg='Unable to change power state for server {0}'.format(
                    server.id))
        return result

    def _find_running_servers_by_group(self, datacenter, count_group):
        """
        Find a list of running servers in the provided group
        :param datacenter: name of the datacenter in which to lookup the group
        :param count_group: the group to count the servers
        :return: list of servers, and list of running servers
        """
        group = self._find_group(
            datacenter=datacenter,
            lookup_group=count_group)

        servers = clc_common.servers_in_group(self.module, self.clc_auth, group)
        running_servers = [s for s in servers if (s.status == 'active' and
                                                  s.powerState == 'started')]

        return servers, running_servers

    def _find_group(self, datacenter, lookup_group=None):
        """
        Find a server group in a datacenter by calling the CLC API
        :param datacenter: Datacenter identifier to search for the group
        :param lookup_group: string name of the group to search for
        :return: clc-sdk.Group instance
        """
        group = None
        if not lookup_group:
            lookup_group = self.module.params.get('group')
        try:
            self.root_group = clc_common.group_tree(
                self.module, self.clc_auth, datacenter=datacenter)
            group = clc_common.find_group(self.module, self.root_group,
                                          lookup_group)
        except ClcApiException:
            pass

        if group is None:
            self.module.fail_json(
                msg='Unable to find group: {group} '
                    'in location: {location}'.format(
                        group=lookup_group, location=datacenter))

        return group

    def _create_clc_server(self, server_params):
        """
        Call the CLC Rest API to Create a Server
        :param server_params: a dictionary of params to use to create the servers
        :return: clc-sdk.Request object linked to the queued server request
        """

        try:
            res = clc_common.call_clc_api(
                self.module, self.clc_auth,
                'POST', 'servers/{alias}'.format(
                    alias=server_params.get('alias')),
                data={
                    'name': server_params.get('name'),
                    'description': server_params.get('description'),
                    'groupId': server_params.get('group_id'),
                    'sourceServerId': server_params.get('template'),
                    'isManagedOS': server_params.get('managed_os'),
                    'primaryDNS': server_params.get('primary_dns'),
                    'secondaryDNS': server_params.get('secondary_dns'),
                    'networkId': server_params.get('network_id'),
                    'ipAddress': server_params.get('ip_address'),
                    'password': server_params.get('password'),
                    'sourceServerPassword': server_params.get('source_server_password'),
                    'cpu': server_params.get('cpu'),
                    'cpuAutoscalePolicyId': server_params.get('cpu_autoscale_policy_id'),
                    'memoryGB': server_params.get('memory'),
                    'type': server_params.get('type'),
                    'storageType': server_params.get('storage_type'),
                    'antiAffinityPolicyId': server_params.get('anti_affinity_policy_id'),
                    'customFields': server_params.get('custom_fields'),
                    'additionalDisks': server_params.get('additional_disks'),
                    'ttl': server_params.get('ttl'),
                    'packages': server_params.get('packages'),
                    'configurationId': server_params.get('configuration_id'),
                    'osType': server_params.get('os_type'),
                })

        except ClcApiException as ex:
            return self.module.fail_json(
                msg='Unable to create the server: {name}. {msg}'.format(
                    name=server_params.get('name'), msg=ex.message))

        #
        # Patch the Request object so that it returns a valid server

        # Find the server's UUID from the API response
        server_uuid = [obj['id']
                       for obj in res['links'] if obj['rel'] == 'self'][0]

        server = self._find_server_by_uuid_w_retry(
            server_uuid, alias=server_params.get('alias'))

        return res, server

    def _find_server_by_uuid_w_retry(self, svr_uuid, alias=None,
                                     retries=25, back_out=2):
        """
        Find the clc server by the UUID returned from the provisioning request.
        Retry the request if a 404 is returned.
        :param svr_uuid: UUID of the server
        :param retries: the number of retry attempts to make prior to fail.
        default is 5
        :param alias: the Account Alias to search
        :return: a clc_common.Server instance
        """
        if not alias:
            if 'clc_alias' not in self.clc_auth:
                clc_common.authenticate(self.module)
            alias = self.clc_auth['clc_alias']

        # Wait and retry if the api returns a 404
        retry_count = retries
        while True:
            retry_count -= 1
            try:
                server_data = clc_common.call_clc_api(
                    self.module, self.clc_auth,
                    'GET', url='/servers/{alias}/{id}'.format(
                        alias=alias, id=svr_uuid),
                    data={'uuid': 'true'})
                server = clc_common.Server(server_data)
                return server

            except ClcApiException as e:
                if e.code != 404:
                    return self.module.fail_json(
                        msg='A failure response was received from CLC API when '
                            'attempting to get details for a server:  '
                            'UUID={id}, Code={code}, Message={msg}'.format(
                                id=svr_uuid, code=e.code, msg=e.message))
                if retry_count == 0:
                    return self.module.fail_json(
                        msg='Unable to reach the CLC API '
                            'after {num} attempts'.format(
                                num=retries))
                time.sleep(back_out)
                back_out *= 2
            except ssl.SSLError as e:
                if retry_count == 0:
                    return self.module.fail_json(
                        msg='Unable to connect to the CLC API after '
                            '{num} attempts. {msg}'.format(
                                num=retries, msg=e.message))
                time.sleep(back_out)
                back_out *= 2


def main():
    """
    The main function.  Instantiates the module and calls process_request.
    :return: none
    """
    argument_dict = ClcServer._define_module_argument_spec()
    module = AnsibleModule(supports_check_mode=True, **argument_dict)
    clc_server = ClcServer(module)
    clc_server.process_request()

from ansible.module_utils.basic import *  # pylint: disable=W0614
from ansible.module_utils.urls import *  # pylint: disable=W0614
if __name__ == '__main__':
    main()