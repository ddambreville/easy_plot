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

import ConfigParser


def readConfigFile(configFilePath):
    """ Return the dictionnary corresponding to the configFilePath."""
    dic = {}
    for section in listConfigFileSections(configFilePath):
        dic[section] = readConfigFileSection(configFilePath, section)

    return dic


def readConfigFileSection(configFilePath, section):
    """
        Use ConfigParser for reading a configuration file.
        Returns an dictionnary with keys/values of the section.
    """

    config = ConfigParser.ConfigParser()
    config.optionxform = str
    config.read(configFilePath)

    if config.has_section(section):
        configSection = config._sections[section]
        configSection.pop("__name__")

        for key, value in configSection.items():
            configSection[key] = value.split()

        return configSection

    else:
        return {}


def listConfigFileSections(configFilePaths):
    """List all the sections of the file <configFilePaths>"""
    config = ConfigParser.ConfigParser()
    config.optionxform = str
    config.read(configFilePaths)

    return config.sections()
