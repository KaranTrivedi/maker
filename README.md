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
```
sudo apt install python3-venv
```

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

```
python3 maker.py -r /home/user/projects/ -p PROJECT_NAME
```
Define the root directory for your project as the absolute path is useful for things like deploying service file.
This will set you up with a venv in a given directory with all the initial components needed to get started.

Input 'y' for options you would like.

### Help

You can see the help menu with the following command.
```
python3 maker.py -h
```

Output:
```
usage: maker.py [-h] -r ROOT_DIR -p PROJECT_NAME

Python project maker

optional arguments:
  -h, --help            show this help message and exit
  -r ROOT_DIR, --root_dir ROOT_DIR
                        enter where you would like the directory to be created.
  -p PROJECT_NAME, --project_name PROJECT_NAME
                        Enter the name of the directory this project will be under.

Suggested: python3 maker.py --root_dir */PATH/OF/WORKING/DIR* --project_name PROJECT_NAME
```

As you can see in the help output, the last line shows a "suggested" command. 
This string will detect which folder you are in and give a sample command that you can run, you only need to edit the PROJECT_NAME
and a project will be created in the parent dir.

For example:
You would be in the maker directory running this command:
```
/home/USER/projects_dir/maker
```

And you would get the command:
```
python3 maker.py --root_dir /home/USER/projects_dir/ --project_name some_project
```

You get:
```
/home/USER/projects_dir/some_project
```

### Known Issues
Relative paths in inputs will not work as intended. 
### Coming soon..
 
-

*In order for you to run this script, I must first invent the universe..*
