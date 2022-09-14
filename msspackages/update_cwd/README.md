**Description**: update_cwd_to_root(root_repository) function changes the path of the current working directory to the specified *root_repository*.

**Use case**: when running jupyter notebook in nested folder structure, e.g. *root/research/eda_analysis*, run this function to access root level libraries.

**Expected Behavior**: Changes current working directory to the specified *root_repository*.
In case *root_repository* specified does not exist it raises IOError. 