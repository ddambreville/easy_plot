#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2014/08/08
Last Update on 2014/09/04

Author: Renaud CARRIERE
        Emmanuel NALEPA
Contact: rcarriere@aldebaran.com
         enalepa@aldebaran.com
Copyright: Aldebaran Robotics 2014
"""

import tools

try:
    import pyqtgraph as pg
except ImportError:
    print "Well that's embarrassing !"
    print "I can't find pyqtgraph on your computer. Please install pyqtgraph."
    print 'You can visit the section "Installation" of www.pyqtgraph.org.'
    print 'If pip is already installed on your computer, you can just type'
    print '"pip install pyqtgraph" in a command line interface.'
    exit()

GENERAL_SECTION = "General"
CURVES_SECTION = "Curves"
DEFAULT_MIN = None
DEFAULT_MAX = None


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
                 grid_x, grid_y, link):
        self.title = title
        self.label_x = label_x
        self.label_y = label_y
        self.unit_x = unit_x
        self.unit_y = unit_y
        self.min_y = min_y
        self.max_y = max_y
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.link = link


class Parameters(object):

    """Contains all parameters of configuration file"""

    def __init__(self, config_file_path):
        self.figures = {}
        self.curves = {}

        try:
            conf_dic = tools.read_config_file(config_file_path)
        except BaseException:
            print "Oops ! An error occured during configuration file reading"
            print "Please, check configuration file's syntaxe"
            exit()

        # General parameters
        try:
            general_dic = conf_dic[GENERAL_SECTION]
            self.max_time = int(general_dic["MaxTime"][0])
            self.title = str(' '.join(general_dic["Title"]))

            try:
                rep = "True" in general_dic["Anti-aliasing"][0]
                self.anti_aliasing = rep
            except BaseException:
                self.anti_aliasing = False

            try:
                rep = "True" in general_dic["LinkXAll"][0]
                self.link_x_all = rep
            except BaseException:
                self.link_x_all = False

        except (IndexError, KeyError):
            print "Easy Plot configuration file MUST have a section named"
            print GENERAL_SECTION + " like the one following :"
            print
            print "[" + GENERAL_SECTION + "]"
            print "MaxTime         : [maximum time]"
            print "Title           : [title]"
            print "Anti-aliasing   : [anti aliasing]"
            print "LinkXAll        : [link all x axis]"
            print
            print "where :"
            print "- [number of rows] is the number of rows"
            print "- [number of columns] is the number of colums"
            print "- [maximum time] is the maximum time of each curve"
            print "- [title] is the title of the window"
            print "- [anti aliasing] is True if you want anti aliasing to be"
            print "  applied to the window, False else"
            print "- [link all x axis] is True if you want to link all x axis,"
            print "  False else"
            exit()

        except (ValueError, TypeError):
            print "There is a no valid value on " + GENERAL_SECTION + " section"
            print "Please, respect the following format :"
            print "- [number of rows] is an integer"
            print "- [number of columns] is an integer"
            print "- [maximum time] is an integer"
            print "- [title] is a string"
            print "- [anti aliasing] is True if you want anti aliasing to be"
            print "  applied to the window, False else"
            print "- [UpdateServeur] is the time between two windows refresh"

            exit()

        # Figures parameters

        # Figures dictionnary is the configuration dictionnary without
        # [General] and [Curves] sections

        # Curves parameters
        def print_help():
            """Print help"""
            print "Easy Plot configuration file MUST have a section named"
            print "[Curves] like the one following :"
            print
            print "[Curves]"
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
            dummy_dic = conf_dic.copy()
            del dummy_dic[GENERAL_SECTION]
            del dummy_dic[CURVES_SECTION]
        except KeyError:
            print_help()
            exit()

        fig_dic_descript = dummy_dic

        for str_name, dic_fig_caract in fig_dic_descript.items():

            try:
                (str_num_row, str_num_column) = str_name.split("-")
                fig_coord = (int(str_num_row), int(str_num_column))
            except BaseException:
                print "ERROR: A section name is not good"
                print "       Please, check configuration file"
                exit()

            try:
                title = " ".join(dic_fig_caract["Title"])
            except (KeyError, IndexError):
                title = None

            try:
                label_x = " ".join(dic_fig_caract["LabelX"])
            except (KeyError, IndexError):
                label_x = None

            try:
                label_y = " ".join(dic_fig_caract["LabelY"])
            except (KeyError, IndexError):
                label_y = None

            try:
                unit_x = " ".join(dic_fig_caract["UnitX"])
            except (KeyError, IndexError):
                unit_x = None

            try:
                unit_y = " ".join(dic_fig_caract["UnitY"])
            except (KeyError, IndexError):
                unit_y = None

            try:
                min_y = int(dic_fig_caract["MinY"][0])
            except (KeyError, IndexError):
                min_y = DEFAULT_MIN
            except (ValueError, TypeError):
                print "ERROR : an error occured on MinY"
                print "          in \
                      [" + str_num_row + "-" + str_num_column + "] section"
                print "          -> MinY is set to default value"
                print
                min_y = DEFAULT_MIN

            try:
                max_y = int(dic_fig_caract["MaxY"][0])
            except (KeyError, IndexError):
                max_y = DEFAULT_MAX
            except (ValueError, TypeError):
                print "ERROR : an error occured on MaxY"
                print "          in [\
                      " + str_num_row + "-" + str_num_column + "] section"
                print "          -> MaxY is set to default value"
                print
                max_y = DEFAULT_MAX

            try:
                rep = "True" in dic_fig_caract["GridX"][0]
                grid_x = rep
            except (KeyError, IndexError):
                grid_x = False
            except (ValueError, TypeError):
                print "ERROR : an error occured on GridX"
                print "          in [\
                      " + str_num_row + "-" + str_num_column + "] section"
                print "          -> GridX is set to False"
                print
                grid_x = False

            try:
                rep = "True" in dic_fig_caract["GridY"][0]
                grid_y = rep
            except (KeyError, IndexError):
                grid_y = False
            except (ValueError, TypeError):
                print "ERROR : an error occured on GridY"
                print "          in [\
                      " + str_num_row + "-" + str_num_column + "] section"
                print "          -> GridY is set to False"
                print
                grid_y = False

            try:
                if self.link_x_all is False:
                    (link_row, link_col) = dic_fig_caract["Link"]
                    link = (int(link_row), int(link_col))
                else:
                    link = None
            except (KeyError, IndexError):
                link = None
            except (ValueError, TypeError):
                print "ERROR : an error occured on Link"
                print "          in [\
                      " + str_num_row + "-" + str_num_column + "] section"
                print "          -> Link is set to None"
                print
                link = None

            figure = Figure(title, label_x, label_y, unit_x, unit_y, min_y,
                            max_y, grid_x, grid_y, link)

            self.figures[fig_coord] = figure

            dic_curves = conf_dic[CURVES_SECTION]

        for name, parameters in dic_curves.items():
            nb_parameter = len(parameters)
            if nb_parameter == 4:
                try:
                    (str_row, str_column, legend, color) = parameters
                    curve = Curve(int(str_row), int(str_column), legend, color)
                    self.curves[name] = curve
                    # to test if color has a correct format
                    color = pg.mkColor(color)
                except (ValueError, TypeError):
                    print "There is a no valid value on [Curves] section"
                    print "Please, respect the following format :"
                    print
                    print " [CurveName] : [Row] [Column] [Legend] [Color]"
                    print
                    print "where:"
                    print "- [CurveName] is a string"
                    print "- [Row] is an integer"
                    print "- [Column] is an integer"
                    print "- [Legend] is a string"
                    print "- [Color] must be :"
                    print "          r for red"
                    print "          g for green"
                    print "          b for blue"
                    print "          c for cyan"
                    print "          m for magenta"
                    print "          y for yellow"
                    print "          k for black"
                    print "          w for white"
                    print "          (R, G, B, [A]) tuple of integers 0-255"
                    print "          hexadecimal strings; may begin with #"
                    exit()

            else:
                print_help()
                exit()


def print_configfile_struct():
    """Print Configuration File's structure"""

    print "[" + GENERAL_SECTION + "]"
    print "MaxTime         : [maximum time]"
    print "Title           : [title]"
    print "Anti-aliasing   : [anti aliasing]"
    print "LinkXAll        : [link all x axis]"
    print
    print "[[row of figure]-[column of figure]]"
    print "Title  : [title of figure]"
    print "LabelX : [label on X axis]"
    print "UnitX  : [unit of X axis]"
    print "LabelY : [label on Y axis]"
    print "UnitY  : [unit on Y axis]"
    print "GridX  : [grid on X]"
    print "GridY  : [grid on Y]"
    print "MinY   : [minimum Value on Y]"
    print "MaxY   : [maximum Value on X]"
    print "Link   : [row figure to link location] [col figure to link location]"
    print
    print "[[row of figure]-[column of figure]]"
    print "Title  : [title of figure]"
    print "LabelX : [label on X axis]"
    print "UnitX  : [unit of X axis]"
    print "LabelY : [label on Y axis]"
    print "UnitY  : [unit on Y axis]"
    print "GridX  : [grid on X]"
    print "GridY  : [grid on Y]"
    print "MinY   : [minimum Value on Y]"
    print "MaxY   : [maximum Value on Y]"
    print "Link   : [row figure to link location] [col figure to link location]"
    print
    print "..."
    print
    print "[Curves]"
    print "[CurveName] : [Row] [Column] [Legend] [Color]"
    print "[CurveName] : [Row] [Column] [Legend] [Color]"
    print "..."
    print
    print "where :"
    print "- [maximum time] is the maximum time of each curve"
    print "- [title] is the title of the window"
    print "- [anti aliasing] is True if you want anti aliasing to be"
    print "  applied to the window, False else"
    print "- [link all x axis] is True if you want to link all x axis,"
    print "  False else"
    print
    print "- [[row of figure]-[column of figure]] is the location of"
    print "  the figure on the window. For example [1-1] is the first"
    print "  figure"
    print "- [title of figure] is the title of the figure"
    print "- [label on X axis] is the label on the X axis"
    print "- [unit of X axis] is the unity of data on the X axis"
    print "- [label on Y axis] is the label on the Y axis"
    print "- [unit on Y axis] is the unity of data on the Y axis"
    print "- [grid on X] is True if you want grid on X axis, False else"
    print "- [grid on Y] is True if you want grid on Y axis, False else"
    print "- [minimum Value on Y] is the minimum value of Y axis"
    print "- [maximum Value on Y] is the maximum value of Y axis"
    print "- [figure to link location] is the coordonate of figure to link"
    print
    print "- [CurveName] is the name of the curve"
    print "- [Row] is the row number of the curve"
    print "- [Column] is the column number of the curve"
    print "- [Legend] is the legend of the curve"
    print "- [Color] is the color of the curve"
