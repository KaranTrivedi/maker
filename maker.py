#!./venv/bin/python

"""
Create python project with best practices.

This project allows user to get started with a new python project with
some default features in place such as logging, service file, etc. in place.
"""

# TODO: Read which user/group is running command, use that for creating service file as an option.
# TODO: Create status file for steps. Continue where setup left off.
# TODO: Check if python bin exists.

import argparse
import configparser
import logging
import sys
from os import path
from pathlib import Path
import subprocess

# Define config and logger.
CONFIG = configparser.ConfigParser()
CONFIG.read("conf/config.ini")
SECTION = "maker"

logger = logging.getLogger(SECTION)

def create_dirs(args):
    """Create given directory under given root dir.

    Args:
        args (dict): get args from user input flags.
    """
    root_dir = Path(args["root_dir"])
    proj_path = Path(args["root_dir"]) / args["project_name"]

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
        if create == "y":
            proj_path.mkdir()
            (proj_path / "tests").mkdir()
            (proj_path / "docs").mkdir()
            (proj_path / "conf").mkdir()
            (proj_path / "libs").mkdir()
            (proj_path / "logs").mkdir()
            (proj_path / "utils").mkdir()
            (proj_path / "sample").mkdir()
            #Path(proj_path / "logs" / ".gitkeep").touch()
            (proj_path / "data").mkdir()
            Path(proj_path / "README.md").touch()
            Path(proj_path / "requirements.txt").touch()
            Path(proj_path / "setup.py").touch()

        else:
            sys.exit()


def create_config(args):
    """
    Create config file.
    """

    conf_string = (
        """[global]
path    = """
        + str(Path(args["root_dir"]) / args["project_name"])
        + """

["""
        + args["project_name"]
        + """]
log     = logs/"""
        + args["project_name"]
        + """.log
level   = DEBUG
#level   = INFO
"""
    )

    config_path = Path(args["root_dir"]) / args["project_name"] / "conf" / "config.ini"
    config_path.write_text(conf_string)


def create_bin(args):
    """
    Create sample bin file, set up class, logging, config etc.
    ALSO create a copy of the file under sample/ for future reference/use

    Args:
        args (dict): get args from user input flags.
    """
    bin_string = (
        """#!./venv/bin/python

\"\"\"
Docstring should be written for each file.
run `pylint filename.py` to find recommendations on improving format.
\"\"\"
import configparser
import json
import logging

#Define config and logger.
CONFIG = configparser.ConfigParser()
CONFIG.read("conf/config.ini")
SECTION = \""""
        + args["project_name"]
        + """\"


class """
        + args["project_name"].capitalize()
        + """:
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

    logging.basicConfig(filename=CONFIG[SECTION]['log'],\\
                    level=CONFIG[SECTION]['level'],\\
                    format='%(asctime)s::%(name)s::%(funcName)s::%(levelname)s::%(message)s',\\
                    datefmt="%Y-%m-%dT%H:%M:%S%z")

    logger = logging.getLogger(SECTION)

    logger.info("####################STARTING####################")

if __name__ == "__main__":
    main()
"""
    )

    bin_path = (
        Path(args["root_dir"]) / args["project_name"] / (args["project_name"] + ".py")
    )
    sample_path = (
        Path(args["root_dir"]) / args["project_name"] / "sample" / (args["project_name"] + ".py")
    )
    bin_path.write_text(bin_string)
    sample_path.write_text(bin_string)

def create_service(args):
    """
    Create service file.

    Args:
        args (dict): get args from user input flags.
    """

    proj_path = Path(args["root_dir"]) / args["project_name"]
    (proj_path / "service").mkdir()

    while True:

        user = input("Input user name that you would like to run the service as: ")
        group = input("Input group name for user: ")

        check = "n"
        check = input(
            f"User/group selected: {user}:{group} Proceed? [y/n/-1 to exit.] "
        )
        if check == "y":
            break
        if check == "-1":
            sys.exit()

    proj_path = str(proj_path)
    service_string = (
        """[Unit]
Description=Service
#After=multi-user.target

[Service]
Type=simple
WorkingDirectory="""
        + proj_path
        + """
ExecStart="""
        + proj_path
        + """/venv/bin/python """
        + proj_path
        + """/"""
        + args["project_name"]
        + """.py
ExecReload=/bin/kill -HUP $MAINPID
User="""
        + user
        + """
Group="""
        + group
        + """

[Install]
WantedBy=multi-user.target

# Optional settings to allow your script to auto restart incase of failure.
# Restart=always
# TimeoutStartSec=10
# RestartSec=10

# Copy this file from the service folder using these commands
# Edit the file here for future uses, and use issue the command to override the existing file.
# sudo cp """
        + str(
            Path(args["root_dir"])
            / args["project_name"]
            / "service"
            / args["project_name"]
        )
        + """.service /lib/systemd/system/

# sudo systemctl daemon-reload
# sudo sysmtemctl restart """
        + args["project_name"]
        + """.service
# Use above commands to reload and restart service.

# Issue this command once to make your script wake up and run on startup.
# sudo sysmtemctl enable """
        + args["project_name"]
        + """.service

# Commands for starting, stopping, restarting and checking status of your script.
# sudo sysmtemctl start """
        + args["project_name"]
        + """.service
# sudo sysmtemctl stop """
        + args["project_name"]
        + """.service
# sudo sysmtemctl restart """
        + args["project_name"]
        + """.service
# sudo sysmtemctl status """
        + args["project_name"]
        + """.service

"""
    )

    service_path = (
        Path(args["root_dir"])
        / args["project_name"]
        / "service"
        / (args["project_name"] + ".service")
    )
    service_path.write_text(service_string)


def create_gitignore(args):
    """
    Create gitignore file for python.

    Args:
        args (dict): get args from user input flags.
    """

    gitignore_string = """!somefolder/.gitkeep
# Byte-compiled / optimized / DLL files
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
    gitignore_path = Path(args["root_dir"]) / args["project_name"] / ".gitignore"
    gitignore_path.write_text(gitignore_string)


def main():
    """
    Main function.
    """

    logging.basicConfig(
        filename=CONFIG[SECTION]["log"],
        level=CONFIG[SECTION]["level"],
        format="%(asctime)s::%(name)s::%(funcName)s::%(levelname)s::%(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z",
    )


    parser = argparse.ArgumentParser(
        description="Python project maker",
        epilog=f"""Suggested: python3 maker.py --root_dir {str(Path.cwd().parent)} --project_name PROJECT_NAME""",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # Add the arguments
    parser.add_argument(
        "-r",
        "--root_dir",
        action="store",
        required=True,
        help="enter where you would like the directory to be created.",
    )
    parser.add_argument(
        "-p",
        "--project_name",
        action="store",
        required=True,
        help="Enter the name of the directory this project will be under.",
    )
    parser.add_argument(
        "-b",
        "--python_bin_path",
        action="store",
        help="Enter path to python binary to be used. Optional.",
    )
    parser.add_argument("-j", "--jupyter", action="store_true")

    args = vars(parser.parse_args())
    # print(args)

    create_dirs(args)
    create_config(args)
    create_bin(args)
    create = "n"
    create = input("Press y to create service file: ")
    if create == "y":
        create_service(args)

    create_gitignore(args)

    # python3.8 -m venv venv
    proj_path = Path(args["root_dir"]) / args["project_name"]

    # Pick python to run..
    if not args["python_bin_path"]:
        print("Searching for installed python instances in /usr/bin/ ..")
        print(
            subprocess.check_output(["ls /usr/bin/python[0-9].[0-9]"], shell=True).decode(
                "utf-8"
            )
        )

        instance = input("select a python instance from above or set your own path: ")
        subprocess.run([instance, "-m", "venv", str(proj_path / "venv")], check=True)
    else:
        instance = args["python_bin_path"]
        subprocess.run([instance, "-m", "venv", str(proj_path / "venv")], check=True)

    # Set up some libs for env like pylint.
    pip_path = proj_path / "venv" / "bin" / "pip"

    # Install jupyter
    if args["jupyter"]:
        subprocess.run([pip_path, "install", "notebook"], check=True)

    subprocess.run([pip_path, "install", "--upgrade", "pip"], check=True)
    subprocess.run([pip_path, "install", "pylint", "wheel"], check=True)

    print(
        "*****************************************************************************"
    )
    print("Copy/Paste this line to terminal to go to project and activate environment.")
    print(
        "*****************************************************************************"
    )

    # source "$root_dir"/$dir/venv/bin/activate;cd "$root_dir"/$dir;clear;ls -lrt
    print(f"deactivate;cd {str(proj_path)};source venv/bin/activate;clear;ls -lrt;pwd")


if __name__ == "__main__":
    main()
