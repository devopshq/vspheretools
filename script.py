# -*- coding: utf-8 -*-
#
# Author: Timur Gilmullin, tim55667757@gmail.com


# This is script wrapper using for run user-command on VM side.


import os
import sys
import subprocess
import traceback

returnCode = 0
output = []

if os.path.exists(r'C:\temp\vm_process.log'):
    os.remove(r'C:\temp\vm_process.log')

try:
    proc = subprocess.Popen(args=['C:\\temp\\MPXSiemSetup.exe', '/silent /norestart /log c:\\log\\siem\\log.txt'], shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, env=None, cwd=r'c:\temp')
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
    with open(r'C:\temp\vm_process.log', 'w') as fH:
        for item in output:
            fH.write(item + '\n')

    sys.exit(returnCode)