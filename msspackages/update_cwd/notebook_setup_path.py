import os

def update_cwd_to_root(root_repository = 'understanding-eks-data'):
    
    """
    This function changes the path of the current working directory to the specified input parameter.
    
    Parameters
    ----------
    root_repository : str
        Root repository name
    
    Returns
    -------
    err_msg : str or None
        Path does not exist

    """
    
    cwd = os.getcwd()
    print('current repository:', cwd)
    
    if root_repository not in cwd.split('/'):
        #in case root_repository does not exist
        raise IOError(f'Path does not exist, please check root_repository name entered: {root_repository}')
        
    else:
        
        while not(cwd.endswith(root_repository)):
            os.chdir("..")
            cwd = os.getcwd()
            print('current repository:', cwd)
