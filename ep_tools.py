#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Created on 2014/05/03

@author: Emmanuel NALEPA
@contact: enalepa[at]aldebaran-robotics.com
@copyright: Aldebaran Robotics 2014

@platform : - Windows, Linux (PC or robot), OS X

@summary: This file contains general functions usefull for logging and plotting

@pep8 : Complains without rules R0912, R0913, R0915 and W0212


"""

try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser


def read_config_file(config_file_path):
    """Return the dictionnary corresponding to the config_file_path."""
    dic = {}
    for section in list_config_file_sections(config_file_path):
        dic[section] = read_config_file_section(config_file_path, section)

    return dic


def read_config_file_section(config_file_path, section):
    """
        Use ConfigParser for reading a configuration file.
        Returns an dictionnary with keys/values of the section.
    """

    config = ConfigParser.ConfigParser()
    config.optionxform = str
    config.read(config_file_path)

    if config.has_section(section):
        configSection = config._sections[section]

        configSection.pop("__name__")

        for key, value in configSection.items():
            configSection[key] = value.split()

        return configSection

    else:
        return {}


def list_config_file_sections(config_file_path):
    """List all the sections of the file <config_file_path>"""
    config = ConfigParser.ConfigParser()
    config.optionxform = str
    config.read(config_file_path)

    return config.sections()
