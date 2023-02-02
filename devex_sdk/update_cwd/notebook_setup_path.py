"""
This function, intended to be run in jupyter notebooks/labs,
changes the path of the current working directory to
the specified input parameter.
"""


import os


def update_cwd_to_root(root_repository = 'understanding-eks-data'):

    """
    Change the current working directory of jupyter notebook/lab.

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
        raise IOError('The requested directory, '
                      + f'{root_repository} does not exist.')

    while not cwd.endswith(root_repository):
        os.chdir("..")
        cwd = os.getcwd()
        print('The new current working directory is', cwd)
