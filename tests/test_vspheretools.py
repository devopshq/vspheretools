# -*- coding: utf-8 -*-

import pytest
from vspheretools import VSphereTools


class TestVSphereTools():

    @pytest.fixture(scope='class', autouse=True)
    def init(self):
        VSphereTools.LOGGER.setLevel(50)  # Disable debug logging while test

    def test_Version(self):
        assert isinstance(VSphereTools.Version(True), str), 'Input: [ True ] expected output: [ isinstance(True, str) == True]'
        assert isinstance(VSphereTools.Version(False), str), 'Input: [ False ] expected output: [ isinstance(False, str) == True]'

    def test_Constants(self):
        assert VSphereTools.VC_SERVER == ""  # empty is default
        assert VSphereTools.VC_LOGIN == ""  # empty is default
        assert VSphereTools.VC_PASSWORD == ""  # empty is default
        assert VSphereTools.VM_NAME == ""  # empty is default
        assert VSphereTools.VM_GUEST_LOGIN == ""  # empty is default
        assert VSphereTools.VM_GUEST_PASSWORD == ""  # empty is default
        assert VSphereTools.VM_CLONES_DIR == "Clones"  # "Clones" is default
        assert VSphereTools.OP_TIMEOUT == 300  # 300 is default

    def test_init(self):
        sphere = VSphereTools.Sphere()
        assert sphere.vSphereServerInstance.connect() == 'CONNECTED'
        assert isinstance(sphere, VSphereTools.Sphere)

    def test_VMStatus(self):
        sphere = VSphereTools.Sphere()
        assert sphere.VMStatus() == 'POWERED OFF'

    def test_VMStart(self):
        sphere = VSphereTools.Sphere()
        assert sphere.VMStart() == 'POWERED OFF'

    def test_VMStartWait(self):
        sphere = VSphereTools.Sphere()
        assert sphere.VMStart() == 'POWERED OFF'

    def test_VMStop(self):
        sphere = VSphereTools.Sphere()
        # TODO: How to check this method if status == 'POWERED ON'
        assert sphere.VMStop() == 'POWERED OFF'

    def test_GetVMProperties(self):
        sphere = VSphereTools.Sphere()
        assert sphere.GetVMProperties() == {'ip_address': '0.0.0.0', 'test': 123, 'testSub': {'subName': {'subSubName': 'qqq'}}}

    def test_GetVMSnapshotsList(self):
        sphere = VSphereTools.Sphere()
        assert isinstance(sphere.GetVMSnapshotsList(), list)
        assert sphere.GetVMSnapshotsList() == ['current snapshot', 'another snapshot']

    def test_CreateVMSnapshot(self):
        sphere = VSphereTools.Sphere()
        # TODO: check statusCode == 0 and statusCode == 2. How to prevent snap.get_name() call?
        assert sphere.CreateVMSnapshot(name=None) == 1  # Fail because snapshot name not define
        assert sphere.CreateVMSnapshot(name='FAKE') == -1  # Fail because an error occured while creating snapshots

    def test_GetVMIPaddress(self):
        sphere = VSphereTools.Sphere()
        assert sphere.GetVMIPaddress() == '0.0.0.0'

    def test_SetVMIPaddressIntoTeamCityParameter(self):
        sphere = VSphereTools.Sphere()
        assert sphere.SetVMIPaddressIntoTeamCityParameter(paramName=None) is None  # return None by default

    def test_VMRevertToCurrentSnapshot(self):
        sphere = VSphereTools.Sphere()
        assert sphere.VMRevertToCurrentSnapshot() == 0  # Success operation

    def test_VMRevertToSnapshot(self):
        sphere = VSphereTools.Sphere()
        # TODO: How to raise exception for check statusCode == -2
        assert sphere.VMRevertToSnapshot(snapshotName=None) == 0  # Success operation if current snapshot
        assert sphere.VMRevertToSnapshot(snapshotName='FAKE') == 0  # Success operation if named snapshot

    def test_CloneVM(self):
        sphere = VSphereTools.Sphere()
        # TODO: How to check with 'POWERED ON' status?
        assert sphere.CloneVM(cloneName='FAKE') is None  # return None by default

    def test_DeleteVM(self):
        sphere = VSphereTools.Sphere()
        assert sphere.DeleteVM() is None  # Success delete operation return None by default

    def test_CopyFileIntoVM(self):
        sphere = VSphereTools.Sphere()
        # TODO: How to check this method if status == 'POWERED ON'?
        with pytest.raises(Exception):
            sphere.CopyFileIntoVM(srcFile=None, dstFile=None, overwrite=False)
        with pytest.raises(Exception):
            sphere.CopyFileIntoVM(srcFile=None, dstFile=None, overwrite=True)
        with pytest.raises(Exception):
            sphere.CopyFileIntoVM(srcFile='SOMEPATH', dstFile='SOMEPATH', overwrite=False)
        with pytest.raises(Exception):
            sphere.CopyFileIntoVM(srcFile='SOMEPATH', dstFile='SOMEPATH', overwrite=True)

    def test_CopyFileFromVM(self):
        sphere = VSphereTools.Sphere()
        # TODO: How to check this method if status == 'POWERED ON'?
        with pytest.raises(Exception):
            sphere.CopyFileFromVM(srcFile=None, dstFile=None, overwrite=False)
        with pytest.raises(Exception):
            sphere.CopyFileFromVM(srcFile=None, dstFile=None, overwrite=True)
        with pytest.raises(Exception):
            sphere.CopyFileFromVM(srcFile='SOMEPATH', dstFile='SOMEPATH', overwrite=False)
        with pytest.raises(Exception):
            sphere.CopyFileFromVM(srcFile='SOMEPATH', dstFile='SOMEPATH', overwrite=True)

    def test_MakeDirectoryOnVM(self):
        sphere = VSphereTools.Sphere()
        # TODO: How to check this method if status == 'POWERED ON'?
        with pytest.raises(Exception):
            sphere.MakeDirectoryOnVM(dirPath=None, createSubDirs=True)
        with pytest.raises(Exception):
            sphere.MakeDirectoryOnVM(dirPath=None, createSubDirs=False)
        with pytest.raises(Exception):
            sphere.MakeDirectoryOnVM(dirPath='SOMEDIR', createSubDirs=True)
        with pytest.raises(Exception):
            sphere.MakeDirectoryOnVM(dirPath='SOMEDIR', createSubDirs=True)

    def test_MonitoringProcessOnVM(self):
        sphere = VSphereTools.Sphere()
        assert sphere.MonitoringProcessOnVM(pID=None, remoteLogFile=None) == -1  # -1 because state is 'POWERED OFF'
        assert sphere.MonitoringProcessOnVM(pID=None, remoteLogFile='SOMEFILE') == -1
        assert sphere.MonitoringProcessOnVM(pID=123, remoteLogFile=None) == -1
        assert sphere.MonitoringProcessOnVM(pID=123, remoteLogFile='SOMEFILE') == -1

    def test_ExecuteProgramOnVM(self):
        sphere = VSphereTools.Sphere()
        # TODO: How to check this method if status == 'POWERED ON'? How to check if program and if wait code blocks?
        with pytest.raises(Exception):
            sphere.ExecuteProgramOnVM()
        with pytest.raises(Exception):
            sphere.ExecuteProgramOnVM(
                program=r"C:\Windows\System32\cmd.exe",
                args=r"/T:Green /C echo %aaa% & echo %bbb%",
                env=r"aaa:10, bbb:20",
                cwd=r"C:\Windows\System32\\",
                pythonbin=r"/python32/python",
                wait=True,
            )
