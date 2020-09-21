# Description
Simple python script for generating a python project with few basic features such as
* virtual environment
* basic logging
* configparser and config file
* basic file structure
* OPTIONAL: Generate service file to run script as a service.

Excellent guide for structuring your projects:
https://docs.python-guide.org/writing/structure/

### Requirements
python3.6+, *nix

**MAKE SURE TO INSTALL VENV before running this script if u dont have it already.
sudo apt install python3-venv

Installing venv module allows you to create the venv for projects in the future.

This script has been tested with Ubuntu 18.04 and python version 3.8
This should work with python version 3.6 and higher due to the usage of f-strings.
This should also run on any *nix sysetm.

## Getting started

Run command in a folder where you usually create projects.
```
git clone https://github.com/KaranTrivedi/maker.git
```

folder called maker should be created.
```
cd maker/
```

No installation or setup should be needed if you have python3.6+ installed as this project only uses default libs.

## Usage
You should be able to run this script with 
```
python3 maker.py -h
```

### Help
```
usage: maker.py [-h] -rd ROOT_DIR -pn PROJECT_NAME

Python project maker

optional arguments:
  -h, --help            show this help message and exit
  -rd ROOT_DIR, --root_dir ROOT_DIR
                        enter where you would like the directory to be created.
  -pn PROJECT_NAME, --project_name PROJECT_NAME
                        Enter the name of the directory this project will be under.
```

Define the root directory for your project as the absolute path is useful for things like deploying service file.
Name the project with flag -dn.

Input 'y' for options you would like.

This will set you up with a venv in a given directory with all the initial components needed to get started.

### Example
```
python3 maker.py -rd /home/user/projects/ -pn PROJECT_NAME
```

### Coming soon..

I am working to improving the logging module greatly. Will update soon.

In order for you to run this script, I must first invent the universe..