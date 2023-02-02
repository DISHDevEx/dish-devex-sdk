from devex_sdk import update_cwd_to_root
import os


def test_update_cwd():
    
    os.chdir('devex_sdk/update_cwd')
    print(os.getcwd())
    
    update_cwd_to_root('devex_sdk')
    cwd = os.getcwd()
    
    assert cwd.endswith('devex_sdk') == True
