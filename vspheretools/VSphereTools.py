# -*- coding: utf-8 -*-
#
# Author: Timur Gilmullin, tim55667757@gmail.com


# This module realize some functions for work with vSphere and virtual machines.
# Home wiki-page: http://devopshq.github.io/vspheretools/


import os

import argparse
import traceback
from datetime import datetime
import time

from pysphere import VIServer
from vspheretools.Logger import *


# ssl compatibilities:
if sys.platform is not 'win32':
    if sys.version_info >= (2, 7, 9):
        import ssl
        ssl._create_default_https_context = ssl._create_unverified_context


def Version(onlyPrint=False):
    """
    Return current version of FuzzyClassificator build
    """
    import pkg_resources  # part of standart setuptools

    try:
        version = pkg_resources.get_distribution('vspheretools').version

    except Exception:
        if onlyPrint:
            LOGGER.setLevel(logging.CRITICAL)
            print('unknown')

        return 'unknown'

    if onlyPrint:
        LOGGER.setLevel(logging.CRITICAL)
        print(version)

    return version


# ----------------------------------------------------------------------------------------------------------------------
# Global variables:
VC_SERVER = r""  # e.g. vcenter-01.example.com
VC_LOGIN = r""  # login to Sphere
VC_PASSWORD = r""  # password to Sphere
VM_NAME = r""  # name of virtual machine
VM_GUEST_LOGIN = r""  # login to VM guest OS
VM_GUEST_PASSWORD = r""  # password to VM guest
VM_CLONES_DIR = "Clones"  # directory for cloning vm
OP_TIMEOUT = 300  # operations timeout in seconds
__version__ = Version()  # set version of current vSphereTools build
# ----------------------------------------------------------------------------------------------------------------------


def ParseArgsMain():
    """
    Function get and parse command line keys.
    """
    parser = argparse.ArgumentParser()  # command-line string parser

    parser.description = 'vSphereTools version: {}. vSphereTools is a set of scripts from DevOpsHQ to support working with vSphere and virtual machines (VMs) on it, which are based on the pysphere library.'.format(__version__)
    parser.epilog = 'See examples on GitHub: http://devopshq.github.io/vspheretools/'
    parser.usage = 'vspheretools [options] [command]'

    parser.add_argument('-v', '--version', action='store_true', help='Show current version of vSphereTools.')

    # --- server options:
    parser.add_argument('-s', '--server', type=str, help='main vSphere Server Cluster, e.g. vcenter-01.example.com.')
    parser.add_argument('-l', '--login', type=str, help='Username for work with vSphere.')
    parser.add_argument('-p', '--password', type=str, help='Sphere Userpass.')

    parser.add_argument('-n', '--name', type=str, help='Name of virtual machine.')

    parser.add_argument('-gl', '--guest-login', type=str, help='Guest Username for work with Guest OS on VM.')
    parser.add_argument('-gp', '--guest-password', type=str, help='VM Guest Userpass.')

    parser.add_argument('-d', '--clone-dir', type=str, help='Directory name on vSphere for clonning virtual machine. "Clones" by default.')
    parser.add_argument('-t', '--timeout', type=str, help='Operations timeout in seconds, 300s. by default.')

    # --- commands:
    parser.add_argument('--status', action='store_true', help='Get virtual machine status.')
    parser.add_argument('--start', action='store_true', help='Starting virtual machine.')
    parser.add_argument('--start-wait', action='store_true', help='Starting virtual machine and wait while guest OS started.')
    parser.add_argument('--stop', action='store_true', help='Stopping virtual machine.')

    parser.add_argument('--snapshots', action='store_true', help='Get list of all snapshots of virtual machine.')
    parser.add_argument('--create-snapshot', type=str, nargs='+', help='Create snapshot of VM with options. Example: --create-snapshot name="Snapshot name" rewrite=True fail-if-exist=False')
    parser.add_argument('--revert-to-current-snapshot', action='store_true', help='Revert virtual machine to current snapshot.')
    parser.add_argument('--revert-to-snapshot', type=str, help='Revert virtual machine to snapshot by name.')

    parser.add_argument('--properties', action='store_true', help='Get all avaliable properties of virtual machine.')
    parser.add_argument('--get-ip', action='store_true', help='Get ip address of virtual machine.')
    parser.add_argument('--set-ip-into-teamcity-param', type=str, help='Set up ip address of virtual machine into predefine TeamCity parameter, vm_ip by default.')

    parser.add_argument('--clone', type=str, help='Clone virtual machine into directory VM_CLONES_DIR with given name.')

    parser.add_argument('--delete', action='store_true', help='Remove virtual machine by name.')

    parser.add_argument('--upload-file', type=str, nargs='+', help='Copy file into virtual machine with True to overwrite. Example: --upload-file srcFile dstFile True')
    parser.add_argument('--download-file', type=str, nargs='+', help='Download file from virtual machine with True to overwrite local file. Example: --download-file srcFile dstFile True')

    parser.add_argument('--mkdir', type=str, nargs='+', help='Creating directory and all sub-directory in given path with True to create sub-dirs. Example: --mkdir dir_path True')
    parser.add_argument('--execute', type=str, nargs='+', help=r'Execute program on guest OS with parameters. Example: --execute program="C:\Windows\System32\cmd.exe" args="/T:Green /C echo %%aaa%% & echo %%bbb%%" env="aaa:10, bbb:20" cwd="C:\Windows\System32" pythonbin="c:\python27\python.exe" wait=True')

    parser.add_argument('--not-skip-run', type=str, help='This is parameter for TeamCity support. Scripts executed if "TRUE". Scripts skipped if "FALSE". Otherwise exception raised.')

    return parser.parse_args()


def TeamCityParamSetter(keyName, value):
    """
    Printing string to set new TeamCity parameter value.
    """
    print("##teamcity[setParameter name='{}' value='{}']".format(keyName, value))


class Sphere():
    """
    Routins for work with vSphere.
    """

    def __init__(self):
        try:
            self.vSphereServerInstance = VIServer()  # Initialize main vSphere Server
            self.vSphereServerInstance.connect(VC_SERVER, VC_LOGIN, VC_PASSWORD)  # Connect vSphere Client
            self.vmInstance = self.vSphereServerInstance.get_vm_by_name(VM_NAME)  # Get instance of virtual machine

        except Exception as e:
            LOGGER.debug(e)
            LOGGER.error(traceback.format_exc())
            self.vSphereServerInstance = None
            self.vm = None
            LOGGER.error('Can not connect to vSphere! Maybe incorrect command? Show examples: vspheretools -h')

    def VMStatus(self):
        """
        Get status of virtual machine.
        """
        status = None
        try:
            status = self.vmInstance.get_status()

        except Exception as e:
            status = None
            LOGGER.debug(e)
            LOGGER.error(traceback.format_exc())
            LOGGER.error('An error occured while getting status of virtual machine "{}"!'.format(VM_NAME))

        finally:
            LOGGER.info('Current status of virtual machine "{}": {}'.format(VM_NAME, status))
            return status

    def VMStart(self):
        """
        Starting virtual machine.
        """
        status = None
        try:
            status = self.VMStatus()
            if status == 'POWERED OFF':
                LOGGER.debug('Trying to start VM...')
                self.vmInstance.power_on()

                status = self.VMStatus()

            else:
                LOGGER.warning('Virtual machine "{}" powered on already!'.format(VM_NAME))

        except:
            status = None
            LOGGER.error(traceback.format_exc())
            LOGGER.error('An error occured while starting virtual machine "{}"!'.format(VM_NAME))

        finally:
            return status

    def VMStartWait(self):
        """
        Starting virtual machine and wait while guest OS started.
        """
        status = None
        try:
            status = self.VMStatus()
            if status == 'POWERED OFF':
                LOGGER.debug('Trying to start VM...')
                self.vmInstance.power_on()

                status = self.VMStatus()

                LOGGER.debug('Waiting until OS started...')
                self.vmInstance.wait_for_tools(timeout=OP_TIMEOUT)

            else:
                LOGGER.warning('Virtual machine "{}" powered on already!'.format(VM_NAME))

        except:
            status = None
            LOGGER.error(traceback.format_exc())
            LOGGER.error('An error occured while starting virtual machine "{}" and waiting for guest OS start!'.format(VM_NAME))

        finally:
            return status

    def VMStop(self):
        """
        Stopping virtual machine.
        """
        status = None
        try:
            status = self.VMStatus()
            if status == 'POWERED ON':
                LOGGER.debug('Trying to stop VM...')
                self.vmInstance.power_off()

                status = self.VMStatus()

            else:
                LOGGER.warning('Virtual machine "{}" powered off already!'.format(VM_NAME))

        except:
            status = None
            LOGGER.error(traceback.format_exc())
            LOGGER.error('An error occured while stopping virtual machine "{}"!'.format(VM_NAME))

        finally:
            return status

    def GetVMProperties(self):
        """
        Read all VM properties and return dictionary.
        """
        properties = {}
        try:
            properties = self.vmInstance.get_properties(from_cache=False)

            LOGGER.info('All properties of virtual machine "{}":'.format(VM_NAME))
            for key in properties.keys():
                if isinstance(properties[key], dict):

                    LOGGER.info('    {}:'.format(key))
                    for subKey in properties[key].keys():
                        if isinstance(properties[key], dict):

                            LOGGER.info('        {}:'.format(subKey))
                            for subSubKey in properties[key][subKey].keys():
                                LOGGER.info('            {}: {}'.format(subSubKey, properties[key][subKey][subSubKey]))

                        else:
                            LOGGER.info('        {}: {}'.format(subKey, properties[key][subKey]))

                else:
                    LOGGER.info('    {}: {}'.format(key, properties[key]))

        except:
            properties = None
            LOGGER.error(traceback.format_exc())
            LOGGER.error('An error occured while getting properties of virtual machine "{}"!'.format(VM_NAME))

        finally:
            return properties

    def GetVMSnapshotsList(self):
        """
        Read and return list of all VM snapshots.
        """
        snapshots = []
        try:
            current = self.vmInstance.get_current_snapshot_name()
            snapshots = self.vmInstance.get_snapshots()

            if current and snapshots:
                LOGGER.info('Name of current snapshot of virtual machine "{}": "{}"'.format(VM_NAME, current))
                LOGGER.info('List of all snapshots:')

                for i, snap in enumerate(snapshots):
                    LOGGER.info('    {}. "'.format(i + 1) + snap.get_name() + '"')

            else:
                LOGGER.warning('No snapshots found for virtual machine "{}"!'.format(VM_NAME))

        except:
            snapshots = None
            LOGGER.error(traceback.format_exc())
            LOGGER.error('An error occured while getting list of snapshots of virtual machine "{}"!'.format(VM_NAME))

        finally:
            return snapshots

    def CreateVMSnapshot(self, **kwargs):
        """
        Creating VM snapshots.
            snapshotName - Snapshot name,
            rewrite - rewriting snapshot if True and snapshot name exist already,
            fail-if-exist - fail script or not if rewrite=False and snapshot name exist already.
        """
        statusCode = 0  # process exit code
        snapshotName = None
        rewrite = True
        failIfExist = False

        try:
            # --- Checking parameters:
            LOGGER.debug('Initialization parameters:')

            if 'name' in kwargs.keys():
                snapshotName = kwargs['name']
                LOGGER.debug('    Parameter "name" = {}'.format(snapshotName))

            else:
                LOGGER.error('    Parameter "name" not define!')

            if 'rewrite' in kwargs.keys():
                if kwargs['rewrite'].lower() == 'true':
                    rewrite = True

                else:
                    rewrite = False

            LOGGER.debug('    Parameter "rewrite" = {}'.format(rewrite))

            if 'fail-if-exist' in kwargs.keys():
                if kwargs['fail-if-exist'].lower() == 'true':
                    failIfExist = True

                else:
                    failIfExist = False

            LOGGER.debug('    Parameter "fail-if-exist" = {}'.format(failIfExist))

            # --- Creating snapshot from current state:
            if snapshotName:
                snapshots = self.GetVMSnapshotsList()
                snapshotList = [snap.get_name() for snap in snapshots]

                if snapshotName in snapshotList:
                    LOGGER.warning('Snapshot "{}" already exist!'.format(snapshotName))

                    if rewrite:
                            LOGGER.info('Removing exist snapshot because rewrite = True, "fail-if-exist" - ignored.')
                            self.vmInstance.delete_named_snapshot(snapshotName)
                            LOGGER.info('Old snapshot "{}" of virtual machine deleted.'.format(snapshotName))

                    else:
                        if failIfExist:
                            LOGGER.error('Fail because fail-if-exist = True and rewrite = False.')
                            statusCode = 2

                        else:
                            statusCode = None  # To do nothing, see next code "if statusCode is None:" ...

            else:
                LOGGER.error('Fail because snapshot name not define!')
                statusCode = 1

            if statusCode == 0:
                LOGGER.info('New snapshot "{}" creating in progress...'.format(snapshotName))
                self.vmInstance.create_snapshot(snapshotName)
                LOGGER.info('New snapshot from current state of virtual machine created successful.')

            if statusCode is None:
                LOGGER.warning('To do nothing because snapshot already exist and not rewrite and not fail enabled.')
                statusCode = 0

        except:
            statusCode = -1
            LOGGER.error(traceback.format_exc())
            LOGGER.error('An error occured while creating snapshots of virtual machine "{}"!'.format(VM_NAME))

        finally:
            return statusCode

    def GetVMIPaddress(self):
        """
        Read VM property and return ip-adress.
        """
        ip = None
        try:
            ip = None
            startTime = datetime.now()

            while not ip and (datetime.now() - startTime).seconds <= OP_TIMEOUT:
                LOGGER.debug('Trying to get ip-address (timeout = {})...'.format(OP_TIMEOUT))
                properties = self.vmInstance.get_properties(from_cache=False)
                ip = None if 'ip_address' not in properties.keys() else properties['ip_address']
                time.sleep(5)

            if ip:
                LOGGER.info('Virtual machine "{}" has ip-adress: {}'.format(VM_NAME, ip))

            else:
                LOGGER.info('Virtual machine "{}" has no ip-adress.'.format(VM_NAME))

        except:
            ip = '0.0.0.0'
            LOGGER.error(traceback.format_exc())
            LOGGER.error('Can not set up ip-address of virtual machine "{}" into TeamCity!'.format(VM_NAME))

        finally:
            return ip

    def SetVMIPaddressIntoTeamCityParameter(self, paramName):
        """
        Read VM property, get ip-adress and then set up ip into predefine TeamCity parameter, 'vm_ip' by default.
        """
        ip = self.GetVMIPaddress()

        key = 'vm_ip' if not paramName else paramName

        if ip:
            TeamCityParamSetter(keyName=str(key), value=ip)

        else:
            LOGGER.warning('Parameter {} does not set to {}!'.format(key, ip))

    def VMRevertToCurrentSnapshot(self):
        """
        Revert VM to current snapshot.
        """
        statusCode = 0  # process exit code

        LOGGER.debug('Trying to revert virtual machine "{}" into current snapshot...'.format(VM_NAME))

        try:
            current = self.vmInstance.get_current_snapshot_name()
            LOGGER.info('Current snapshot: "{}"'.format(current))

            self.vmInstance.revert_to_snapshot()
            LOGGER.info('Virtual machine "{}" revert to current snapshot successful.'.format(VM_NAME))

            self.VMStatus()

        except:
            statusCode = -1

            LOGGER.error(traceback.format_exc())
            LOGGER.error('An error occured while revert virtual machine "{}" into current snapshot!'.format(VM_NAME))

        finally:
            return statusCode

    def VMRevertToSnapshot(self, snapshotName=None):
        """
        Revert VM to first snapshot by part of its name. If snapshotName not define then used current snapshot.
        """
        statusCode = 0  # process exit code

        try:
            if snapshotName:
                LOGGER.debug('Trying to revert virtual machine "{}" into snapshot "{}"...'.format(VM_NAME, snapshotName))

                self.vmInstance.revert_to_named_snapshot(name=snapshotName)
                LOGGER.info('Virtual machine "{}" revert to snapshot "{}" successful.'.format(VM_NAME, snapshotName))

                self.VMStatus()

            else:
                statusCode = self.VMRevertToCurrentSnapshot()

        except:
            statusCode = -2

            LOGGER.error(traceback.format_exc())
            LOGGER.error('An error occured while revert virtual machine "{}" into snapshot "{}"!'.format(VM_NAME, snapshotName))

        finally:
            return statusCode

    def CloneVM(self, cloneName=None):
        """
        Clone VM into directory VM_CLONES_DIR. If cloneName not define then name creates automatic.
        """
        LOGGER.debug('Trying to clone virtual machine "{}" into directory "{}"...'.format(VM_NAME, VM_CLONES_DIR))
        try:
            if cloneName:
                try:
                    self.vSphereServerInstance.get_vm_by_name(cloneName)
                    LOGGER.debug('Name already used: {}'.format(cloneName))
                    cloneName = None

                except:
                    LOGGER.debug('Name not used: {}'.format(cloneName))

            i = 1
            while not cloneName:
                try:
                    cloneName = 'clone-{}-'.format(i) + VM_NAME
                    self.vSphereServerInstance.get_vm_by_name(cloneName)
                    LOGGER.debug('Name already used: {}'.format(cloneName))
                    cloneName = None
                    i += 1

                except:
                    LOGGER.debug('Name not used: {}'.format(cloneName))

            LOGGER.debug('Cloning in progress...')
            self.vmInstance.clone(name=cloneName, folder=VM_CLONES_DIR, power_on=False)

            LOGGER.info('Virtual machine "{}" successful clone into directory "{}" with new name "{}".'.format(VM_NAME, VM_CLONES_DIR, cloneName))

        except:
            LOGGER.error(traceback.format_exc())
            LOGGER.error('An error occured while cloning virtual machine "{}" into directory "{}"!'.format(VM_NAME, VM_CLONES_DIR))

    def DeleteVM(self):
        """
        Delete VM by name (VM_NAME).
        """
        status = self.VMStatus()

        if status != 'POWERED OFF':
            LOGGER.warning('Virtual machine must be stopped before deleting!')
            status = self.VMStop()

        if status != 'POWERED OFF':
            LOGGER.error('An error occured while stopping virtual machine "{}"!'.format(VM_NAME))

        else:
            LOGGER.debug('Trying to delete virtual machine "{}"...'.format(VM_NAME))
            try:
                oK, msg = self.vSphereServerInstance.delete_vm_by_name(VM_NAME, remove_files=True)

                if oK:
                    LOGGER.info('Virtual machine "{}" deleted successful with message: "{}".'.format(VM_NAME, msg))

                else:
                    LOGGER.warning('Virtual machine "{}" NOT delete with message: "{}".'.format(VM_NAME, msg))

            except:
                LOGGER.error(traceback.format_exc())
                LOGGER.error('An error occured while deleting virtual machine "{}"!'.format(VM_NAME))

    def CopyFileIntoVM(self, srcFile=None, dstFile=None, overwrite=False):
        """
        Copy file srcFile into VM with full path dstFile.
        """
        status = self.VMStatus()

        if status != 'POWERED ON':
            raise Exception('Virtual machine must be started before copy operation!')

        if srcFile and dstFile:
            LOGGER.debug(r'Trying to login in guest OS...')
            self.vmInstance.login_in_guest(VM_GUEST_LOGIN, VM_GUEST_PASSWORD)

            LOGGER.debug(r'Trying to copy source file "{}" into destination file "{}" inside virtual machine "{}"...'.format(srcFile, dstFile, VM_NAME))
            try:
                self.vmInstance.send_file(srcFile, dstFile, overwrite)

                LOGGER.info('File "{}" on guest OS successful copied as file "{}".'.format(srcFile, dstFile))

            except:
                LOGGER.error(traceback.format_exc())
                LOGGER.error('An error occured while copying file "{}" into destination file "{}" inside virtual machine "{}"!'.format(srcFile, dstFile, VM_NAME))

        else:
            LOGGER.warning('Source file and/or destination file not specified!')

    def CopyFileFromVM(self, srcFile=None, dstFile=None, overwrite=False):
        """
        Copy file srcFile on VM to local file dstFile.
        """
        status = self.VMStatus()

        if status != 'POWERED ON':
            raise Exception('Virtual machine must be started before copy operation!')

        if srcFile and dstFile:
            LOGGER.debug(r'Trying to login in guest OS...')
            self.vmInstance.login_in_guest(VM_GUEST_LOGIN, VM_GUEST_PASSWORD)

            LOGGER.debug(r'Trying to copy source file "{}" from virtual machine "{}" into destination local file "{}"...'.format(srcFile, VM_NAME, dstFile))
            try:
                self.vmInstance.get_file(srcFile, dstFile, overwrite)

                LOGGER.info('File "{}" successful copied from VM guest OS as local file "{}".'.format(srcFile, dstFile))

            except:
                LOGGER.error(traceback.format_exc())
                LOGGER.error('An error occured while copying file "{}" from virtual machine "{}" into destination file "{}"!'.format(srcFile, VM_NAME, dstFile))

        else:
            LOGGER.warning('Source file and/or destination file not specified!')

    def MakeDirectoryOnVM(self, dirPath=None, createSubDirs=True):
        """
        Create directory on VM with full path dirPath. If createSubDirs=True all sub-directories in path will create.
        """
        status = self.VMStatus()

        if status != 'POWERED ON':
            raise Exception('Virtual machine must be started before creating directory!')

        if dirPath:
            LOGGER.debug(r'Trying to login in guest OS...')
            self.vmInstance.login_in_guest(VM_GUEST_LOGIN, VM_GUEST_PASSWORD)

            LOGGER.debug(r'Trying to create directory "{}" inside virtual machine "{}"...'.format(dirPath, VM_NAME))
            try:
                self.vmInstance.make_directory(dirPath, createSubDirs)

                LOGGER.info('Directory "{}" on guest OS successful created.'.format(dirPath))

            except:
                trace = traceback.format_exc()
                if 'FileAlreadyExistsFault' not in trace:
                    LOGGER.error(traceback.format_exc())
                    LOGGER.error('An error occured while directory "{}" created inside virtual machine "{}"!'.format(dirPath, VM_NAME))

                else:
                    LOGGER.warning('Directory "{}" already exist on VM.'.format(dirPath))

        else:
            LOGGER.warning('Directory path not specified!')

    def MonitoringProcessOnVM(self, pID, remoteLogFile=None):
        """
        Search process with given pID on VM and waiting for process finished. Then return stderr, stdout and exit-code.
        """
        statusCode = 0  # process exit code
        timeTick = 6  # delay time to check process

        try:
            status = self.VMStatus()

            if status != 'POWERED ON':
                raise Exception('Virtual machine must be started before process monitoring!')

            LOGGER.info('Starting process [PID = {}] monitoring...'.format(pID))
            print("##teamcity[progressStart 'Executing process with PID = {} on virtual machine']".format(pID))

            processActive = True
            timeCount = 0
            while processActive:
                time.sleep(timeTick)
                timeCount += timeTick

                processList = self.vmInstance.list_processes()

                for item in processList:
                    if str(item['pid']) == str(pID):
                        LOGGER.debug(r'    Process status-line given by VM-tools: {}'.format(item))
                        if item['exit_code'] is not None:
                            statusCode = item['exit_code']
                            processActive = False

                        break

            print("##teamcity[progressFinish 'Executing process with PID = {} on virtual machine']".format(pID))
            LOGGER.info('Process finished successful with exit code = {}. Duration: ~{} sec.'.format(statusCode, timeCount))

            LOGGER.debug('Downloading process log-file from VM...')
            logFile = os.path.abspath(os.path.join(os.curdir, os.path.basename(remoteLogFile)))  # local log file

            if remoteLogFile:
                if os.path.exists(logFile):
                    os.remove(logFile)

                self.CopyFileFromVM(srcFile=remoteLogFile, dstFile=logFile, overwrite=True)

                if os.path.exists(logFile):
                    with open(logFile, 'r') as fH:
                        output = fH.readlines()

                    if output and len(output) > 0:
                            LOGGER.debug('Process output:')
                            for line in output:
                                    LOGGER.debug('    {}'.format(line.strip()))

        except:
            LOGGER.error('Unknown exception occurred while process executing!')
            LOGGER.error(traceback.format_exc())
            statusCode = -1

        finally:
            return statusCode

    def ExecuteProgramOnVM(self, **kwargs):
        """
        Execute program with given parameters:
            program - string path to executable file, e.g. r"C:\Windows\System32\cmd.exe",
            args - comma-separated strings with arguments to the program, e.g. r"/T:Green /C echo %aaa% & echo %bbb%",
            env - comma-separated strings with environment variables, e.g. r"aaa:10, bbb:20",
            cwd - string path to working directory, e.g. r'C:\Windows\System32\',
            pythonbin - path to python binary on VM, e.g. r'/python32/python'
            wait - wait for process end and then return stderr, stdout and exit code.
        """
        returnCode = 0  # process return code
        if kwargs:
            program = []
            cmdArgs = []
            env = {}
            cwd = ''
            wait = False
            pythonbin = r'/python32/python'

            LOGGER.debug('Initialization parameters:')
            if 'program' in kwargs.keys():
                program = [r'{}'.format(kwargs['program'])]
            LOGGER.debug('    Parameter "program" = {}'.format(program))

            if 'args' in kwargs.keys() and kwargs['args']:
                cmdArgs = [r'{}'.format(x.strip()) for x in kwargs['args'].split(',')]  # separate items "arg1, arg2" by comma
            LOGGER.debug('    Parameter "args" = {}'.format(cmdArgs))

            if 'env' in kwargs.keys() and kwargs['env']:
                envList = [x.strip() for x in kwargs['env'].split(',')]  # separate items "foo: bar, varB: B" by comma
                for item in envList:
                    env[item.split(':')[0]] = item.split(':')[1]  # separate one item "foo: bar" by :
            LOGGER.debug('    Parameter "env" = {}'.format(env))

            if 'cwd' in kwargs.keys():
                cwd = kwargs['cwd']
            LOGGER.debug('    Parameter "cwd" = {}'.format(cwd))

            if 'pythonbin' in kwargs.keys():
                pythonbin = kwargs['pythonbin']
            LOGGER.debug('    Parameter "pythonbin" = {}'.format(pythonbin))

            if 'wait' in kwargs.keys():
                if kwargs['wait'].lower() == 'true':
                    wait = True
            LOGGER.debug('    Parameter "wait" = {}'.format(wait))

            scriptFile = os.path.abspath(os.path.join(os.curdir, 'script.py'))  # wrapper on local machine
            remoteLogFile = os.path.join(os.path.dirname(program[0]), 'vm_process.log')  # log file on VM
            remoteScriptFile = os.path.join(os.path.dirname(program[0]), os.path.basename(scriptFile))  # wrapper on VM

            script = r"""# -*- coding: utf-8 -*-
#
# Author: Timur Gilmullin, tim55667757@gmail.com
# This is script wrapper using for run user-command on VM side.


import os, sys, subprocess, traceback

returnCode = 0
output = []

if os.path.exists(r'{log}'):
    os.remove(r'{log}')

try:
    proc = subprocess.Popen(args={args}, shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, env={env}, cwd={cwd})
    proc.wait()

    for line in proc.stdout:
        line = bytes(line).decode(encoding='utf-8', errors='ignore').strip()

        lines = line.split('\r')
        for item in lines:
            item = item.strip()
            if item:
                output.append('    ' + item)

    returnCode = proc.returncode

except:
    output += traceback.format_exc().splitlines()
    output.append('Unknown error occured!')
    returnCode = -1

finally:
    with open(r'{log}', 'w') as fH:
        for item in output:
            fH.write(item + '\n')

    sys.exit(returnCode)
            """.format(args=program + cmdArgs, env=env if env else None, cwd="r'{}'".format(cwd) if cwd else None, log=remoteLogFile)

            with open(scriptFile, 'w') as fH:
                fH.write(script)

            status = self.VMStatus()

            if status != 'POWERED ON':
                raise Exception('Virtual machine must be started before starting task!')

            if program:
                LOGGER.debug(r'Trying to login in guest OS...')
                self.vmInstance.login_in_guest(VM_GUEST_LOGIN, VM_GUEST_PASSWORD)

                LOGGER.info('Preparing script to execute...')

                self.CopyFileIntoVM(srcFile=scriptFile, dstFile=remoteScriptFile, overwrite=True)

                LOGGER.debug(r'Trying to execute program "{}" with args "{}", env "{}" and cwd "{}" inside virtual machine "{}"...'.format(program, cmdArgs, env, cwd, VM_NAME))

                try:
                    LOGGER.debug(r'Path to wrapper script file on VM: {}'.format(remoteScriptFile))
                    LOGGER.debug(r'Process log file on VM: {}'.format(remoteLogFile))

                    pid = self.vmInstance.start_process(program_path=pythonbin, args=[remoteScriptFile], cwd=os.path.dirname(pythonbin))

                    LOGGER.info('Command successful executed. Parent program has PID = {}'.format(pid))

                    if wait:
                        LOGGER.info('Wait for process finished.')

                        returnCode = self.MonitoringProcessOnVM(pid, remoteLogFile)

                except:
                    returnCode = -1
                    LOGGER.error(traceback.format_exc())
                    LOGGER.error('An error occured while executing command inside virtual machine!')

            else:
                LOGGER.warning('Path of program to execute not specified!')

        else:
            raise Exception('You must specify at least one argument "program" with path to the program!')

        return returnCode


def Main():
    """
    Main entry point.
    """
    global VC_SERVER
    global VC_LOGIN
    global VC_PASSWORD
    global VM_NAME
    global VM_GUEST_LOGIN
    global VM_GUEST_PASSWORD
    global VM_CLONES_DIR
    global OP_TIMEOUT

    args = ParseArgsMain()  # get and parse command-line parameters

    if args.version:
        Version(onlyPrint=True)  # Show current version of vSphereTools
        sys.exit(0)

    if args.not_skip_run:
        if args.not_skip_run == "TRUE":
            LOGGER.info('--not-skip-run="TRUE". All scripts will be execute (parameter _execute_step_0_if = "TRUE" in TeamCity metaranner).')

        elif args.not_skip_run == "FALSE":
            LOGGER.warning('--not-skip-run="FALSE". All scripts execution skipped (parameter _execute_step_0_if = "FALSE" in TeamCity metaranner).')
            sys.exit(0)

        else:
            LOGGER.error('--not-skip-run key must be "TRUE" or "FALSE" (parameter _execute_step_0_if not define in TeamCity metaranners)!')
            sys.exit(-1)

    exitCode = 0

    if args.server:
        VC_SERVER = args.server

    if args.login:
        VC_LOGIN = args.login

    if args.password:
        VC_PASSWORD = args.password

    if args.name:
        VM_NAME = args.name

    if args.guest_login:
        VM_GUEST_LOGIN = args.guest_login

    if args.guest_password:
        VM_GUEST_PASSWORD = args.guest_password

    if args.clone_dir:
        VM_CLONES_DIR = args.clone_dir

    if args.timeout:
        OP_TIMEOUT = int(args.timeout)

    sphere = Sphere()
    if not sphere.vSphereServerInstance:
        exitCode = 1

    if exitCode == 0:
        if args.status:
            if sphere.VMStatus() is None:
                exitCode = 255

            else:
                exitCode = 0

        elif args.start:
            if sphere.VMStart() is None:
                exitCode = 254

            else:
                exitCode = 0

        elif args.start_wait:
            if sphere.VMStartWait() is None:
                exitCode = 253

            else:
                exitCode = 0

        elif args.stop:
            if sphere.VMStop() is None:
                exitCode = 252

            else:
                exitCode = 0

        elif args.properties:
            sphere.GetVMProperties()

        elif args.snapshots:
            sphere.GetVMSnapshotsList()

        elif args.create_snapshot:
            exitCode = sphere.CreateVMSnapshot(**dict(kw.split('=') for kw in args.create_snapshot))

        elif args.get_ip:
            sphere.GetVMIPaddress()

        elif args.set_ip_into_teamcity_param:
            sphere.SetVMIPaddressIntoTeamCityParameter(args.set_ip_into_teamcity_param)

        elif args.revert_to_current_snapshot:
            exitCode = sphere.VMRevertToCurrentSnapshot()

        elif args.revert_to_snapshot:
            exitCode = sphere.VMRevertToSnapshot(args.revert_to_snapshot)

        elif args.clone:
            if args.clone and args.clone != "None":
                sphere.CloneVM(cloneName=args.clone)

            else:
                sphere.CloneVM()

        elif args.delete:
            sphere.DeleteVM()

        elif args.upload_file:
            if len(args.upload_file) == 3:
                if args.upload_file[2].lower() == 'true':
                    sphere.CopyFileIntoVM(srcFile=args.upload_file[0], dstFile=args.upload_file[1], overwrite=True)

                else:
                    sphere.CopyFileIntoVM(srcFile=args.upload_file[0], dstFile=args.upload_file[1], overwrite=False)

            elif len(args.upload_file) == 2:
                sphere.CopyFileIntoVM(srcFile=args.upload_file[0], dstFile=args.upload_file[1])

            else:
                LOGGER.warning('Please, specify source file (local) and destination file (remote) and possible flag (True/False) to rewrite!')

        elif args.download_file:
            if len(args.download_file) == 3:
                if args.download_file[2].lower() == 'true':
                    sphere.CopyFileFromVM(srcFile=args.download_file[0], dstFile=args.download_file[1], overwrite=True)

                else:
                    sphere.CopyFileFromVM(srcFile=args.download_file[0], dstFile=args.download_file[1], overwrite=False)

            elif len(args.download_file) == 2:
                sphere.CopyFileFromVM(srcFile=args.download_file[0], dstFile=args.download_file[1])

            else:
                LOGGER.warning('Please, specify source file (remote) and destination file (local) and possible flag (True/False) to rewrite!')

        elif args.mkdir:
            if len(args.mkdir) == 2:
                if args.mkdir[1].lower() == 'true':
                    sphere.MakeDirectoryOnVM(args.mkdir[0], True)

                else:
                    sphere.MakeDirectoryOnVM(args.mkdir[0], False)

            else:
                sphere.MakeDirectoryOnVM(args.mkdir[0])

        elif args.execute:
            exitCode = sphere.ExecuteProgramOnVM(**dict(kw.split('=') for kw in args.execute))

        else:
            LOGGER.warning('Please, select command!')

    sys.exit(exitCode)


if __name__ == "__main__":
    Main()
