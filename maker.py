#!./venv/bin/python

"""
Create python project with best practices.

This project allows user to get started with a new python project with
some default features in place such as logging, service file, etc. in place.
"""

import argparse
import configparser
import logging
import sys
from os import path
from pathlib import Path
import subprocess

#Define config and logger.
CONFIG = configparser.ConfigParser()
CONFIG.read("conf/config.ini")
SECTION = "maker"

logging.basicConfig(filename=CONFIG[SECTION]["log"],\
                    level=CONFIG[SECTION]["level"],\
                    format='%(asctime)s::%(name)s::%(funcName)s::%(levelname)s::%(message)s',\
                    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger(SECTION)

def show_sections():
    """
    Output all options for given section
    """

    conf_str = "\n\n"
    for sect in CONFIG.sections():
        conf_str += "[" + sect + "]\n"
        for var in list(CONFIG[sect]):
            conf_str += var + "\t\t=\t" + CONFIG[sect][var] + "\n"
    logger.info(conf_str)

# class Sample:
#     """
#     Create class
#     """

#     def __init__(self, var):
#         self.var = var

#     def __str__(self):
#         """
#         stringify
#         """
#         return json.dumps(vars(self), indent=2)

def create_dirs(args):
    """Create given directory under given root dir.

    Args:
        args (dict): get args from user input flags.
    """
    root_dir = Path(args["root_dir"])
    proj_path = Path(args["root_dir"]) / args["dir_name"]

    # Check if directory exists.

    if not path.exists(root_dir):
        print(f"{args['root_dir']} not a valid path.")
        sys.exit()
    elif path.exists(proj_path):
        print(f"{proj_path} already exists.")
        sys.exit()
    else:
        create = input(f"Press y to create '{proj_path}': ")
        # create = 'y'
        if create == 'y':
            proj_path.mkdir()
            (proj_path / "tests").mkdir()
            (proj_path / "docs").mkdir()
            (proj_path / "conf").mkdir()
            (proj_path / "logs").mkdir()
            (proj_path / "data").mkdir()
            (proj_path / "service").mkdir()

        else:
            sys.exit()

def create_config(args):

    conf_string = """[global]
path    = """ + str(Path(args["root_dir"]) / args["dir_name"]) + """

[""" + args["dir_name"]+ """]
log     = logs/""" + args["dir_name"]+ """.log
level   = DEBUG
#level   = INFO
"""

    config_path = Path(args["root_dir"]) / args["dir_name"] / "conf" / "config.ini"
    config_path.write_text(conf_string)

def create_bin(args):
    """
    Create sample bin file, set up class, logging, config etc.

    Args:
        args (dict): get args from user input flags.
    """
    bin_string = """#!./venv/bin/python

import configparser
import json
import logging

#Define config and logger.
CONFIG = configparser.ConfigParser()
CONFIG.read("conf/config.ini")
SECTION = \"""" + args["dir_name"] + """\"

logging.basicConfig(filename=CONFIG[SECTION]['log'],\\
                    level=CONFIG[SECTION]['level'],\\
                    format='%(asctime)s::%(name)s::%(funcName)s::%(levelname)s::%(message)s',\\
                    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger(SECTION)

def show_sections():
    \"\"\"
    Output all options for given section
    \"\"\"

    conf_str = "\\n\\n"
    for sect in CONFIG.sections():
        conf_str += "[" + sect + "]\\n"
        for var in list(CONFIG[sect]):
            conf_str += var + "\\t\\t=\\t" + CONFIG[sect][var] + "\\n"
    logger.info(conf_str)

class """ + args["dir_name"].capitalize() + """:
    \"\"\"
    Create sample class
    \"\"\"

    def __init__(self, var):
        self.var = var

    def __str__(self):
        \"\"\"
        stringify
        \"\"\"
        return json.dumps(vars(self), indent=2)


def main():
    \"\"\"
    Main function.
    \"\"\"
    logger.info("####################STARTING####################")

    if CONFIG[SECTION]["level"] == "DEBUG":
        show_sections()

if __name__ == "__main__":
    main()"""

    bin_path = Path(args["root_dir"]) / args["dir_name"] / (args["dir_name"] + ".py")
    bin_path.write_text(bin_string)

def create_service(args):
    """
    Create service file.

    Args:
        args (dict): get args from user input flags.
    """
    user = input("Input user name that you would like to run the service as: ")
    group = input("Input group namefor user: ")

    proj_path = str(Path(args["root_dir"]) / args["dir_name"])
    service_string= """[Unit]
Description=Service
#After=multi-user.target

[Service]
Type=simple
WorkingDirectory=""" + proj_path + """
ExecStart=""" + proj_path + """/venv/bin/python """ + proj_path + """/""" + args["dir_name"] + """.py
ExecReload=/bin/kill -HUP $MAINPID
User=""" + user + """
Group=""" + group + """

[Install]
WantedBy=multi-user.target

#Move this file from the service folder using these commands
#sudo mv . /lib/systemd/system/

#sudo sysmtemctl enable """ + args["dir_name"] + """.service
#sudo sysmtemctl start """ + args["dir_name"] + """.service
#sudo sysmtemctl status """ + args["dir_name"] + """.service
"""

    service_path = Path(args["root_dir"]) / args["dir_name"] / "service" / (args["dir_name"] + ".service")
    service_path.write_text(service_string)

def create_gitignore(args):
    """
    Create gitignore file for python.

    Args:
        args (dict): get args from user input flags.
    """

    gitignore_string = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# PEP 582; used by e.g. github.com/David-OConnor/pyflow
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/
    """
    gitignore_path = Path(args["root_dir"]) / args["dir_name"] / ".gitignore"
    gitignore_path.write_text(gitignore_string)

def main():
    """
    Main function.
    """

    logger.info("####################STARTING####################")

    if CONFIG[SECTION]["level"] == "DEBUG":
        show_sections()

    parser = argparse.ArgumentParser(description='Python project maker')

    # Add the arguments
    parser.add_argument('-rd', '--root_dir', action='store', required=True,
        help="enter where you would like the directory to be created.")
    parser.add_argument('-dn', '--dir_name', action='store', required=True,
        help="Enter the name of the directory this project will be under.")

    args = vars(parser.parse_args())
    # print(args)

    create_dirs(args)
    create_config(args)
    create_bin(args)
    create = input("Press y to create service file: ")
    # create = 'n'
    if create == 'y':
        create_service(args)

    create_gitignore(args)
 
    # python3.8 -m venv venv
    proj_path = Path(args["root_dir"]) / args["dir_name"]
    subprocess.run(["python3", "-m", "venv", str(proj_path / "venv")])

    # Set up some libs for env like pylint.

    pip_path = proj_path / "venv" / "bin" / "pip"
    subprocess.run([pip_path, "install", "--upgrade", "pip"])
    subprocess.run([pip_path, "install", "pylint", "wheel"])

    print("Copy/Paste this line to activate environment.")
    # source "$root_dir"/$dir/venv/bin/activate;cd "$root_dir"/$dir;clear;ls -lrt
    print(f"cd {str(proj_path)};source venv/bin/activate;clear;ls -lrt")
    

if __name__ == "__main__":
    main()
