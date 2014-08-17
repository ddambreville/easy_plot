#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2014/08/08
Last Update on 2014/08/13

Author: Renaud CARRIERE
Contact: rcarriere@presta.aldebaran-robotics.fr
Copyright: Aldebaran Robotics 2014
"""

import tools

#========================Class Definitions=====================================


class GeneralParameter(object):

    """
    GeneralParameter class
    This class permits to structurate the general parameters of config file
    """

    def __init__(self, dic):

        try:
            self.nb_row = int(dic["General"]["NumberOfRows"][0])
            self.nb_column = int(dic["General"]["NumberOfColumns"][0])
            self.max_time = int(dic["General"]["MaxTime"][0])
            self.title = str(' '.join(dic["General"]["Title"]))
            self.anti_aliasing = bool(dic["General"]["Anti-aliasing"][0])
        except (IndexError, KeyError):
            print "Easy Plot configuration file MUST have a section named"
            print "[General] like the one following :"
            print
            print "[General]"
            print "NumberOfRows    : [number of rows]"
            print "NumberOfColumns : [number of columns]"
            print "MaxTime         : [maximum time]"
            print "Title           : [title]"
            print "Anti-aliasing   : [anti aliasing]"
            print
            print "where :"
            print "- [number of rows] is the number of rows"
            print "- [number of columns] is the number of colums"
            print "- [maximum time] is the maximum time of each curve"
            print "- [title] is the title of the window"
            print "- [anti aliasing] is True if you want anti aliasing to be"
            print "  applied to the window, False else"

            exit()


class figureParameter(object):

    """
    figureParameter class
    This class permits to structurate the figure parameters of config file
    """

    def __init__(self, dic, row, column):

        self.row = row
        self.column = column

        if str(row) + "-" + str(column) in dic:
            if "minY" in dic[str(row) + "-" + str(column)]:
                self.minY = int(dic[str(row) + "-" + str(column)]["minY"][0])
            else:
                self.minY = -10

            if "maxY" in dic[str(row) + "-" + str(column)]:
                self.maxY = int(dic[str(row) + "-" + str(column)]["maxY"][0])
            else:
                self.maxY = 10

            if "GridX" in dic[str(row) + "-" + str(column)]:
                self.gridX = bool(
                    dic[str(row) + "-" + str(column)]["GridX"][0])
            else:
                self.gridX = False

            if "GridY" in dic[str(row) + "-" + str(column)]:
                self.gridY = bool(
                    dic[str(row) + "-" + str(column)]["GridY"][0])
            else:
                self.gridY = False

            if "Title" in dic[str(row) + "-" + str(column)]:
                self.title = str(
                    ' '.join(dic[str(row) + "-" + str(column)]["Title"]))
            else:
                self.title = ''

            if "LabelX" in dic[str(row) + "-" + str(column)]:
                self.labelX = str(
                    ' '.join(dic[str(row) + "-" + str(column)]["LabelX"]))
            else:
                self.labelX = ''

            if "UnitX" in dic[str(row) + "-" + str(column)]:
                self.unitX = str(
                    ' '.join(dic[str(row) + "-" + str(column)]["UnitX"]))
            else:
                self.unitX = ''

            if "LabelY" in dic[str(row) + "-" + str(column)]:
                self.labelY = str(
                    ' '.join(dic[str(row) + "-" + str(column)]["LabelY"]))
            else:
                self.labelY = ''

            if "UnitY" in dic[str(row) + "-" + str(column)]:
                self.unitY = str(
                    ' '.join(dic[str(row) + "-" + str(column)]["UnitY"]))
            else:
                self.unitY = ''
        else:
            print "WARNING : [" + str(row) + "-" + str(column) + "] not found -> set to default"
            self.minY = -10
            self.maxY = 10
            self.gridX = False
            self.gridY = False
            self.title = ''
            self.labelX = ''
            self.unitX = ''
            self.labelY = ''
            self.unitY = ''


class curveParametersData(object):

    def __init__(self, name, row, column, legend, color):

        self.name = name
        self.row = row
        self.column = column
        self.legend = legend
        self.color = color


class curveParameters(object):

    def __init__(self, dic):

        self.curve_data = []

        for key in dic["Plot"].keys():
            if len(dic["Plot"][key]) >= 4:
                self.curve_data.append(curveParametersData(key, dic["Plot"][key][
                                       0], dic["Plot"][key][1], dic["Plot"][key][2], dic["Plot"][key][3]))
            else:
                print "WARNING: Argument missing for key " + str(key)

        self.number_of_curves = len(self.curve_data)

        if self.number_of_curves == 0:
            print "WARNING: No curve detected"


class allParameters(object):

    """
    AllParameters class
    This class permits to regroup general_parameter and figure_parameter
    """

    def __init__(self, general_parameters, figures_parameters, curves_parameters):
        self.general_parameters = general_parameters
        self.figures_parameters = figures_parameters
        self.curves_parameters = curves_parameters


#========================Function Definition===================================


def defineParameters(config_file):
    """
    Use readConfigFile from tools to put all datas from config file in an
    allParameters class
    """
    conf = tools.readConfigFile(config_file)

    general_parameters = GeneralParameter(conf)
    curve_parameters = curveParameters(conf)
    figures_parameters = []

    for i in range(general_parameters.nb_row):
        for j in range(general_parameters.nb_column):
            figures_parameters.append(figureParameter(conf, i + 1, j + 1))

    return allParameters(general_parameters, figures_parameters, curve_parameters)
