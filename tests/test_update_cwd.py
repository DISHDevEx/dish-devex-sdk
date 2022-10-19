from msspackages import update_cwd_to_root
import os


def test_update_cwd():
    
    os.chdir('msspackages/update_cwd')
    print(os.getcwd())
    
    update_cwd_to_root('msspackages')
    cwd = os.getcwd()
    
    assert cwd.endswith('msspackages') == True
