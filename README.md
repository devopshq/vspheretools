# vspheretools

[![vspheretools build status](https://travis-ci.org/devopshq/vspheretools.svg)](https://travis-ci.org/devopshq/vspheretools) [![vspheretools code quality](https://api.codacy.com/project/badge/Grade/185f7c8a13c84f88bf8b93280e457ffc)](https://www.codacy.com/app/tim55667757/vspheretools/dashboard) [![vspheretools code coverage](https://api.codacy.com/project/badge/Coverage/185f7c8a13c84f88bf8b93280e457ffc)](https://www.codacy.com/app/tim55667757/vspheretools/dashboard) [![vspheretools on PyPI](https://img.shields.io/pypi/v/vspheretools.svg)](https://pypi.python.org/pypi/vspheretools) [![vspheretools license](https://img.shields.io/pypi/l/vspheretools.svg)](https://github.com/devopshq/vspheretools/blob/master/LICENSE)


***Russian README: https://github.com/devopshq/vspheretools/blob/master/README_RUS.md*** 

***Index:***
- [Introduction](#Chapter_1)
    - [Environment requirements](#Chapter_1_1)
    - [Setup](#Chapter_1_2)
- [Console mode](#Chapter_2)
    - [Options](#Chapter_2_1)
    - [Commands](#Chapter_2_2)
    - [Usage examples](#Chapter_2_3)
- [vspheretools and TeamCity metarunners](#Chapter_3)
    - [How to add vspheretools-metarunners](#Chapter_3_1)
- [API usage](#Chapter_4)
    - [Global variables](#Chapter_4_1)
    - [API methods](#Chapter_4_2)
- [Troubleshooting](#Chapter_5)


# Introduction <a name="Chapter_1"></a>
**vSphereTools** - vSphereTools is a set of scripts from DevOpsHQ to support working with vSphere and virtual machines (VMs) on it, which are based on the pysphere library. These scripts were written for the purpose of integrating vSphere with TeamCity through meta-runners. It is also possible to use the vSphereTools tools from the console or by importing the necessary modules and methods into their projects.

How does it work? Let see the process scheme below.

![vSphereTools work process](vspheretools.png "vSphereTools work process")


## Environment requirements <a name="Chapter_1_1"></a>

1. The service account for access to the vSphere, whose login and password you will substitute in scripts. Only letters and numbers are recommended in login and password.
2. From the machine where you are running scripts vSphere and the ESX must be available.
3. The VMvare Tools tool should be installed on the VM (VM -> Guest -> Install / Upgrade VMvare Tools context menu).
4. On the machine where you are running scripts, Python 2 *, version 2.7 or later is installed.


## Setup <a name="Chapter_1_2"></a>

1. Download vSphereTools from the git repository: https://github.com/devopshq/vspheretools and unpack it to some directory.
2. Either you can install the tool through pip:

    pip install vspheretools


# Console mode <a name="Chapter_2"></a>

Use (if you did not install the tool via pip, but simply downloaded and unpacked):

    python -m vspheretools [options] [command]

If the tool is installed via pip, then simply type:

    vspheretools [options] [command]

It is possible to specify many options and only one command to be executed on the Sphere.

In the examples below, we will assume that vspheretools is installed via pip and the keyword python omited.


## Options <a name="Chapter_2_1"></a>

    -s SERVER_NAME, --server SERVER_NAME - Specify a cluster on the vSphere server. For example, vcenter-01.example.com.

    -l USERLOGIN, --login USERLOGIN - Specify the login of the user who has the rights to work with the project on the Sphere. The default value is undefined.

    -p USERPASSWORD, --password USERPASSWORD - Specify the user password. The default value is undefined.

    -n VM_NAME, --name VM_NAME - Specify the name of the VM with which to perform the actions. The default value is undefined.

    -gl GUESTLOGIN, --guest-login GUESTLOGIN - Specify the user login for the OS installed on the VM. The default value is undefined.

    -gp GUESTPASSWORD, --password GUESTPASSWORD - Specify the user password for the OS installed on the VM. The default value is undefined.

    -d CLONE_DIRECTORY, --clone-dir CLONE_DIRECTORY - Specify the name of the directory in the Sphere to which the user has the write permission. The default value is the "Clones" directory - it must be created on the Sphere.

    -t TIMEOUT_SEC, --timeout TIMEOUT_SEC - Specify the timeout in seconds for certain operations. The default value is 300s.


## Commands <a name="Chapter_2_2"></a>

    --status - Get the status of the VM, given by the --name key. The available statuses are: 'POWERING ON', 'POWERING OFF', 'SUSPENDING', 'RESETTING', 'BLOCKED ON MSG', 'REVERTING TO SNAPSHOT', 'UNKNOWN'.

    --start - Start the VM, given by the --name key.

    --start-wait - Start the VM, given by the --name key, and wait until the OS is fully loaded. The timeout is specified by the --timeout key.

    --stop - Stop the VM, given by the --name key.

    --snapshots - Display the list of snapshots for the VM, specified by the --name key.

    --create-snapshot SNAPSHOT_NAME - Create a named snapshot for the VM.

    --revert-to-current-snapshot - Revert VM to the current (active) snapshot.

    --revert-to-snapshot SNAPSHOT_NAME - Revert VM to the named snapshot.

    --properties - Display the list of available VM properties.

    --get-ip - Display the IP address of the VM if it has it.

    --set-ip-into-teamcity-param TEAMCITY_PARAMETER - Write the TEAMCITY_PARAMETER with the ip-address of the VM. By default, TEAMCITY_PARAMETER name is "vm_ip".

    --clone CLONE_NAME - Clone VM to the directory defined by --clone-dir key.

    --delete - Deletes the VM. Before deleting, it is checked that the VM is off, and if not, it is attempted to stop it, then delete it. ATTENTION! Be careful with this option! 

    --upload-file SCR DST REWRITE - Copies a local file to the VM. The full paths of both files must be specified. REWRITE = True is specified to overwrite an existing file.

    --download-file SCR DST REWRITE - Copies a file from the VM to the specified local path. The full paths of both files must be specified. REWRITE = True is specified to overwrite an existing file.

    --mkdir DIR_PATH CREATESUBS - Creates the specified directory on the VM. If CREATESUBS = True, then all intermediate subdirectories are created.

    --execute PROGRAM ARGS ENV CWD PYTHONBIN WAIT - Starts the specified PROGRAM on the VM and returns its PID. ARGS - list of additional parameters, separated by commas. ENV - environment variables NAME:VALUE, separated by commas. CWD is the working directory of the program. PYTHONBIN - the full path to the python 2.* on the VM. WAIT or no the end of the program after is starts.


## Usage examples <a name="Chapter_2_3"></a>

If spaces are used in the input parameters, then use theirs value with double quotes, e.g. "VM name with space"

Get the current VM status:

    vspheretools --server vcenter-01.example.com --login <Domain_account> --password <userpass> --name <full_VM_name> --status

Start VM:

    vspheretools --server vcenter-01.example.com --login <Domain_account> --password <userpass> --name <full_VM_name> --start

Start VM and wait until guest OS loaded with 5 minute timeout:

    vspheretools --server vcenter-01.example.com --login <Domain_account> --password <userpass> --name <full_VM_name> --timeout 300 --start-wait

Stop VM:

    vspheretools --server vcenter-01.example.com --login <Domain_account> --password <userpass> --name <full_VM_name> --stop
 
Get VM snapshots:

    vspheretools --server vcenter-01.example.com --login <Domain_account> --password <userpass> --name <full_VM_name> --snapshots

Create named snapshot of the VM state:

    vspheretools --server vcenter-01.example.com --login <Domain_account> --password <userpass> --name <full_VM_name> --create-snapshot name="Snapshot name" rewrite=True fail-if-exist=False

Revert VM to the current (active) snapshot:

    vspheretools --server vcenter-01.example.com --login <Domain_account> --password <userpass> --name <full_VM_name> --revert-to-current-snapshot
 
Revert VM to the named snapshot:

    vspheretools --server vcenter-01.example.com --login <Domain_account> --password <userpass> --name <full_VM_name> --revert-to-snapshot <full_snapshot_name>

Get VM properties:

    vspheretools --server vcenter-01.example.com --login <Domain_account> --password <userpass> --name <full_VM_name> --properties

Get an ip-address of the VM with 10 seconds timeout:

    vspheretools --server vcenter-01.example.com --login <Domain_account> --password <userpass> --name <full_VM_name> --timeout 10 --get-ip
 
Get an ip-address of the VM and save it to the TeamCity "vm_ip"-named parameter with 10 seconds timeout:

    vspheretools --server vcenter-01.example.com --login <Domain_account> --password <userpass> --name <full_VM_name> --timeout 10 --set-ip-into-teamcity-param vm_ip
  
Create VM clone:

    vspheretools --server vcenter-01.example.com --login <Domain_account> --password <userpass> --name <full_VM_name> --clone-dir Clones --clone new_clone_name
 
Delete VM:

    vspheretools --server vcenter-01.example.com --login <Domain_account> --password <userpass> --name <full_VM_name> --delete
 
Copy local file to VM:

    vspheretools --server vcenter-01.example.com --login <Domain_account> --password <userpass> --name <full_VM_name> -gl <guest-login> -gp <guest-password> --upload-file <source_file> <destination_file> True

Copy file from VM to the local path:

    vspheretools --server vcenter-01.example.com --login <Domain_account> --password <userpass> --name <full_VM_name> -gl <guest-login> -gp <guest-password> --download-file <source_file> <destination_file>
 
Create a directory and all intermediate subdirectories (by default):

    vspheretools --server vcenter-01.example.com --login <Domain_account> --password <userpass> --name <full_VM_name> -gl <guest-login> -gp <guest-password> --mkdir <dir_path>
 
Start the Windows console with options:

    vspheretools --server vcenter-01.example.com --login <Domain_account> --password <userpass> --name <full_VM_name> -gl <guest-login> -gp <guest-password> --execute program="C:\Windows\System32\cmd.exe" args="/T:Green /C echo %aaa% & echo %bbb%" env="aaa:10, bbb:20" cwd="C:\Windows\System32" pythonbin="c:\python27\python.exe" wait=True


# vspheretools and TeamCity metarunners <a name="Chapter_3"></a>

To work with the Sphere in TemCity, you can add the following metarunners:

* DevOps-runner: vspheretools - Show VM status
* DevOps-runner: vspheretools - Start VM
* DevOps-runner: vspheretools - Start VM and waiting until guest OS started
* DevOps-runner: vspheretools - Stop VM
* DevOps-runner: vspheretools - Show VM snapshots
* DevOps-runner: vspheretools - Create VM snapshot
* DevOps-runner: vspheretools - Revert VM to current snapshot
* DevOps-runner: vspheretools - Revert VM to named snapshot 
* DevOps-runner: vspheretools - Show VM properties
* DevOps-runner: vspheretools - Show VM ip-address
* DevOps-runner: vspheretools - Set VM ip-address into TC parameter
* DevOps-runner: vspheretools - Clone VM into directory
* DevOps-runner: vspheretools - Delete VM
* DevOps-runner: vspheretools - Upload file to VM
* DevOps-runner: vspheretools - Download file from VM
* DevOps-runner: vspheretools - Create directory on VM
* DevOps-runner: vspheretools - Execute command on VM


## How to add vspheretools-metarunners <a name="Chapter_3_1"></a>

* Install (or copy) xml metarunners from vspheretools-metarunners directory on your TeamCity admin page: https://[teamcity_server]/admin/editProject.html?projectId=_Root&tab=metaRunner (Administration - Root project - Meta-Runners)
* Create new VCS from vspheretools project: https://github.com/devopshq/vspheretools
* Attach new VCS to your TeamCity project and set up checkout rules: 
+:.=>%default_devops_tools_path_local%/vspheretools
* Create variable default_devops_tools_path_local in your TeamCity project and set value, e.g. "devops-tools". It is local path for devops-tools repository.


# API usage <a name="Chapter_4"></a>

Make import of the vspheretools module. When using the module, you need to determine the basic constants. Let's consider the simplest examples:

    from vspheretools import VSphereTools as vs

    version = vs.Version()
    print(version)

    vs.VC_SERVER = r"VSPHERE NAME"
    vs.VC_LOGIN = r"VSPHERE USER LOGIN"
    vs.VC_PASSWORD = r"PASSWORD"
    vs.VM_NAME = r"VIRTUAL MACHINE"

    sphere = vs.Sphere()

    sphere.VMStatus()

The remaining variables and commands that you can use to work through the API are shown below.


## Global variables <a name="Chapter_4_1"></a>

    VC_SERVER = r"vcenter-01.example.com"

    VC_LOGIN = r"login"

    VC_PASSWORD = r"password"

    VM_NAME = r"VM name"

    VM_GUEST_LOGIN = r"os_login"

    VM_GUEST_PASSWORD = r"os_password"

    VM_CLONES_DIR = "Clones"

    OP_TIMEOUT = 300

To work with the sphere, you need to initialize any variable of the Sphere() class, which initializes the connection to the Sphere, the necessary cluster and the virtual machine, and contains the basic methods.


## API methods <a name="Chapter_4_2"></a>

    VMStatus() - State of the VM_NAME virtual machine

    VMStart() - Start VM_NAME virtual machine with POWERED OFF status
    
    VMStartWait() - Start VM_NAME virtual machine with POWERED OFF status and wait until OS loaded

    VMStop() - Stop VM_NAME virtual machine with POWERED ON status

    GetVMProperties() - Get dictionary with properties of VM_NAME virtual machine

    GetVMSnapshotsList() - list of virtual machine snapshot instances

    CreateVMSnapshot() - Create named snapshot of the VM_NAME virtual machine

    GetVMIPaddress() - Return an ip-address of VM_NAME virtual machine

    SetVMIPaddressIntoTeamCityParameter(paramName) - Get an ip-address of the VM and save it to the TeamCity "vm_ip"-named parameter

    VMRevertToCurrentSnapshot() - Revert VM_NAME virtual machine to current (active) snapshot

    VMRevertToSnapshot(snapshotName) - Revert VM_NAME virtual machine to snapshotName snapshot

    CloneVM(cloneName) - Cloning VM_NAME virtual machine to the VM_CLONES_DIR directory

    DeleteVM() - Delete VM_NAME virtual machine

    CopyFileIntoVM(srcFile, dstFile, overwrite) - Copy from local srcFile path to dstFile on VM

    CopyFileFromVM(srcFile, dstFile, overwrite) - Copy from VM srcFile to local dstFile path

    MakeDirectoryOnVM(dirPath, createSubDirs) - Create dirPath directory on VM

    ExecuteProgramOnVM(\*\*kwargs) - Run program with some parameters on VM. Arguments: program e.g. r"C:\Windows\System32\cmd.exe"; args e.g. r"/T:Green /C echo %aaa% & echo %bbb%"; env e.g. r"aaa:10, bbb:20"; cwd e.g. r"C:\Windows\System32\"


# Troubleshooting <a name="Chapter_5"></a>

**1. If you see errors in the log:**

    VSphereTools.py       [Line:89] ERROR     [2015-08-28 16:48:44,490] Can not connect to vSphere! server = vcenter-01.example.com,
    VIApiException: [InvalidLoginFault]: Cannot complete login due to an incorrect user name or password,
    pysphere.resources.vi_exception.VIApiException: [GuestOperationsUnavailableFault]: The guest operations agent could not be contacted.

and other authorization problems: check that you correctly specify the login and password: the domain login should look like: domain\login, e.g. .\administartor for the local administrator. The password and the login should not contain special characters or be escaped with quotes.

**2. ValueError**

If you see an error in the log similar to:

    exitCode = sphere.ExecuteProgramOnVM(**dict(kw.split('=') for kw in args.execute))
    ValueError: dictionary update sequence element #3 has length 4; 2 is required

then check the "Command-line arguments" field is correct. Separate variables are separated by commas! 
