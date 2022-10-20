import os     
import subprocess
from subprocess import Popen, PIPE


def setup_runner(setup_type = 'notebook' , project = 'understanding-eks-data'):
    
    if project == 'understanding-eks-data':
        if setup_type == 'notebook':
            process = subprocess.Popen([os.path.join(os.path.dirname(__file__), "notebook_setup_run.sh")], stdout=PIPE, stderr=PIPE, shell=True)
        elif setup_type == 'console':
             process = subprocess.Popen([os.path.join(os.path.dirname(__file__), "console_setup_run.sh")], stdout=PIPE, stderr=PIPE, shell=True)

    stdout, stderr = process.communicate()
    if stdout:
        print(stdout)
    # if stderr:
    #     raise Exception("Error "+str(stderr))
        
