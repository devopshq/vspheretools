# -*- coding: utf-8 -*-

import pysphere


def pytest_sessionstart(session):

    class VMInstanceWrapper(object):

        def __init__(self, status='POWERED OFF'):
            self.status = status

        def get_status(self, *args, **kwargs):
            return self.status

        def power_on(self, *args, **kwargs):
            return 'TEST POWER ON'

        def power_off(self, *args, **kwargs):
            return 'TEST POWER OFF'

        def wait_for_tools(self, *args, **kwargs):
            return 'Waiting until OS started...'

        def get_properties(self, *args, **kwargs):
            return {'ip_address': '0.0.0.0', 'test': 123, 'testSub': {'subName': {'subSubName': 'qqq'}}}

        def get_current_snapshot_name(self, *args, **kwargs):
            return ''

        def get_snapshots(self, *args, **kwargs):
            return ['current snapshot', 'another snapshot']

        def revert_to_snapshot(self, *args, **kwargs):
            return 'reverting to current snapshot...'

        def revert_to_named_snapshot(self, *args, **kwargs):
            return 'reverting to named snapshot...'

        def delete_named_snapshot(self, *args, **kwargs):
            return 'deleting named snapshot...'

        def create_snapshot(self, *args, **kwargs):
            return 'creating new snapshot...'

        def clone(self, *args, **kwargs):
            return 'cloning vm...'

        def login_in_guest(self, *args, **kwargs):
            return 'login in guest'

        def send_file(self, *args, **kwargs):
            return 'sending file...'

        def get_file(self, *args, **kwargs):
            return 'geting file...'

        def make_directory(self, *args, **kwargs):
            return 'making directory...'

    class VIServerWrapper(object):

        def connect(self, *args, **kwargs):
            return 'CONNECTED'

        def get_vm_by_name(self, *args, **kwargs):
            if 'FAKE' in args:
                raise Exception('No Name found for CloneVM test')

            else:
                return VMInstanceWrapper()

        def delete_vm_by_name(self, *args, **kwargs):
            return True, 'DELETED'

    pysphere.VIServer = VIServerWrapper
