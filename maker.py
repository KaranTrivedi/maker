#!./venv/bin/python

"""[Create python project with best practices.]

    This project allows user to get started with a new python project with some default features in place such as logging, service file, etc. in place.
"""

import configparser
import json
import logging

import argparse

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

class Sample:
    """
    Create class
    """

    def __init__(self, var):
        self.var = var

    def __str__(self):
        """
        stringify
        """
        return json.dumps(vars(self), indent=2)


def main():
    """
    Main function.
    """

    logger.info("####################STARTING####################")

    if CONFIG[SECTION]["level"] == "DEBUG":
        show_sections()

if __name__ == "__main__":
    main()
