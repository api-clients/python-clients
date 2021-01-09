# Anaconda prefix error
 
    CondaValueError: prefix already exists: /home/username/anaconda3/envs/environment
 
 Probably, you use `make config` twice. The latest version of anaconda try to replace existed environment.
 
 Probably, you use not latest conda version (conda 4.5.* and lower). You need to update anaconda:
 
    conda update conda    
 
# Anaconda not found
 
You can [install](https://www.anaconda.com/products/individual) anaconda You can read this answer https://stackoverflow.com/questions/35246386/conda-command-not-found/44319368 

    Conda command not found
    
You can insert to the file `~/.bashrc` next line:

    export PATH="/path/to/anaconda/bin:$PATH"    
    
Example:

    export PATH="/home/username/anaconda3/bin:$PATH"    
    
# Some command not found

Please see [this](https://github.com/U-Company/python-private-service-layout#usage) page

# .pypirc file configuration

Error:

    Traceback (most recent call last):
      File "setup.py", line 38, in <module>
        'clients_http=clients.__cmd.http_:main',
      File "/home/username/anaconda3/envs/l/lib/python3.7/site-packages/setuptools/__init__.py", line 161, in setup
        return distutils.core.setup(**attrs)
      File "/home/username/anaconda3/envs/l/lib/python3.7/distutils/core.py", line 148, in setup
        dist.run_commands()
      File "/home/username/anaconda3/envs/l/lib/python3.7/distutils/dist.py", line 966, in run_commands
        self.run_command(cmd)
      File "/home/username/anaconda3/envs/l/lib/python3.7/distutils/dist.py", line 985, in run_command
        cmd_obj.run()
      File "/home/username/anaconda3/envs/l/lib/python3.7/distutils/command/upload.py", line 64, in run
        self.upload_file(command, pyversion, filename)
      File "/home/username/anaconda3/envs/l/lib/python3.7/distutils/command/upload.py", line 74, in upload_file
        raise AssertionError("unsupported schema " + schema)
    AssertionError: unsupported schema 
    makefile:58: recipe for target 'publish-package' failed
    make: *** [publish-package] Error 1


Probably you run the `make publish-package`

Cases:

1. You forget to copy or change the file `.secrets/.pypirc` to `~/`.
2. You forget to add alias to `[distutils]` section into `.pypirc` file after change him.
3. You forget to add section with alias to `.pypirc` file after change him.

You can find more info [here](/python_clients#prepare-config-for-pip-ubuntu) or [here](/clientsdeployments).
    
# Duplicate package

    Upload failed (409): Conflict
    error: Upload failed (409): Conflict
    makefile:58: recipe for target 'publish-package' failed
    make: *** [publish-package] Error 1
    
Probably you run the `make publish-package` and get this error:

It means that, this package already exists. Please change version or remove old version. You can remove by [this](https://github.com/U-Company/notes/tree/master/deployments#publish-image-into-docker-registry-for-local-development-and-testing) way.

# Problem with uninstall

    Cannot uninstall 'certifi'. It is a distutils installed project and thus we cannot accurately determine which files belong to it which would lead to only a partial uninstall.

**Best rule**. You can solve this problem with reinitialization anaconda:

    make config
    
Or you can change make file rule `deps`. Add `--ignore-installed` for pip. You can read [some](https://pip.pypa.io/en/stable/reference/pip_install/#cmdoption-i) [topics](https://stackoverflow.com/questions/51913361/difference-between-pip-install-options-ignore-installed-and-force-reinstall) [about](https://github.com/pypa/pip/issues/5247) [it](https://github.com/galaxyproject/galaxy/issues/7324).

The second way can break down you application.  