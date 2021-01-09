# python-clients

This library implements http python client by a functional style

## Installing

Before work with our package, you need to install:

    sudo apt-get install make
    
Make is not required features. This tools is needed for more useful development. We recommend to use Anaconda or another
environment manager for safety system interpreter. 

You can download Anaconda [here](https://www.anaconda.com/). After installing Anaconda please create new environment:

    conda create --name your-name python=3.*
    conda activate python-clients
    
or, you can do this:

    make config
    conda activate python-clients

## Dependencies
 
This command install all package dependencies:

    make deps
    
## Publishing package
    
If you want to publish docker image into registry, you need to do this:

    make publish
    
## Clean

You can clean python package after building and all temporary files:

    make clean

## Testing
 
Before starting tests you need to start mock-server:

    make run
      
Now, you can run tests:

    make test
    
## Notice

We use makefile as interface for communicate our application with our systems by command line while development and
publishing.

If you want more about publishing packages, you need can go 
[here](https://github.com/U-Company/notes/tree/master/deployments).

If you want to fork our repo, you can communicate with us. Egor Urvanov by UrvanovCompany@yandex.ru or in telegram (@cuda23)

## Common errors

If you have some errors, you can read
[Common errors](data/docs/errors.md) doc. Or you can communicate with Egor Urvanov by UrvanovCompany@yandex.ru or in telegram (@cuda23)
