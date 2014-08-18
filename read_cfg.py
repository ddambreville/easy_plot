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

GENERAL_SECTION = "General"
CURVES_SECTION = "Curves"
DEFAULT_MIN = -10
DEFAULT_MAX = 10


class Curve(object):

    """This class describe a curve"""

    def __init__(self, row, column, legend, color):
        self.row = row
        self.column = column
        self.legend = legend
        self.color = color


class Figure(object):

    """This class describes a figure"""

    def __init__(self, title, label_x, label_y, unit_x, unit_y, min_y, max_y,
                 grid_x, grid_y):
        self.title = title
        self.label_x = label_x
        self.label_y = label_y
        self.unit_x = unit_x
        self.unit_y = unit_y
        self.min_y = min_y
        self.max_y = max_y
        self.grid_x = grid_x
        self.grid_y = grid_y


class Parameters(object):

    """Contains all parameters of configuration file"""

    def __init__(self, config_file_path):
        self.figures = {}
        self.curves = {}

        conf_dic = tools.read_config_file(config_file_path)

        # General parameters
        try:
            general_dic = conf_dic[GENERAL_SECTION]

            self.nb_row = int(general_dic["NumberOfRows"][0])
            self.nb_column = int(general_dic["NumberOfColumns"][0])
            self.max_time = int(general_dic["MaxTime"][0])
            self.title = str(' '.join(general_dic["Title"]))
            self.anti_aliasing = bool(general_dic["Anti-aliasing"][0])
        except (IndexError, KeyError):
            print "Easy Plot configuration file MUST have a section named"
            print GENERAL_SECTION + "like the one following :"
            print
            print "[ " + GENERAL_SECTION + " ]"
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

        # Figures parameters

        # Figures dictionnary is the configuration dictionnary without
        # [General] and [Curves] sections
        dummy_dic = conf_dic.copy()
        del dummy_dic[GENERAL_SECTION]
        del dummy_dic[CURVES_SECTION]

        fig_dic_descript = dummy_dic

        for str_name, dic_fig_caract in fig_dic_descript.items():
            (str_num_row, str_num_column) = str_name.split("-")
            fig_coord = (int(str_num_row), int(str_num_column))

            try:
                title = " ".join(dic_fig_caract["Title"])
            except KeyError:
                title = None

            try:
                label_x = " ".join(dic_fig_caract["LabelX"])
            except KeyError:
                label_x = None

            try:
                label_y = " ".join(dic_fig_caract["LabelY"])
            except KeyError:
                label_y = None

            try:
                unit_x = " ".join(dic_fig_caract["UnitX"])
            except KeyError:
                unit_x = None

            try:
                unit_y = " ".join(dic_fig_caract["UnitY"])
            except KeyError:
                unit_y = None

            try:
                min_y = int(dic_fig_caract["minY"][0])
            except KeyError:
                min_y = DEFAULT_MIN

            try:
                max_y = int(dic_fig_caract["maxY"][0])
            except KeyError:
                max_y = DEFAULT_MAX

            try:
                grid_x = bool(dic_fig_caract["GridX"][0])
            except KeyError:
                grid_x = False

            try:
                grid_y = bool(dic_fig_caract["GridY"][0])
            except KeyError:
                grid_y = False

            figure = Figure(title, label_x, label_y, unit_x, unit_y, min_y,
                            max_y, grid_x, grid_y)

            self.figures[fig_coord] = figure

        # Curves parameters
        def print_help():
            print "Easy Plot configuration file MUST have a section named"
            print "[Plot] like the one following :"
            print
            print "[Plot]"
            print "[CurveName] : [Row] [Column] [Legend] [Color]"
            print "[CurveName] : [Row] [Column] [Legend] [Color]"
            print "[CurveName] : [Row] [Column] [Legend] [Color]"
            print "[CurveName] : [Row] [Column] [Legend] [Color]"
            print "..."
            print
            print "where :"
            print "- [CurveName] is the name of the curve"
            print "- [Row] is the row number of the curve"
            print "- [Column] is the column number of the curve"
            print "- [Legend] is the legend of the curve"
            print "- [Color] is the color of the curve"

        try:
            dic_curves = conf_dic[CURVES_SECTION]
        except KeyError:
            print_help()
            exit()

        for name, parameters in dic_curves.items():
            nb_parameter = len(parameters)
            if nb_parameter == 4:
                (str_row, str_column, legend, color) = parameters
                curve = Curve(int(str_row), int(str_column), legend, color)
                self.curves[name] = curve

            else:
                print_help()
                exit()
