#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2014/08/08
Last Update on 2014/09/04

Author: Renaud CARRIERE
        Emmanuel NALEPA
        Jason LETORT
Contact: rcarriere@aldebaran.com
         enalepa@aldebaran.com
         jletort@presta.aldebaran-robotics.fr
Copyright: Aldebaran Robotics 2014
@pep8 : Complains without rules R0902, R0912, R0913, R0914, R0915 and W0212
"""
import random
import pyqtgraph as pg

try:
    import tools
except ImportError:
    print ("Well that's embarrassing !")
    print ("I can't find tools on your computer.")
    print ("Please put tools.py on easy_plot folder")
    exit()


GENERAL_SECTION = "General"
CURVES_SECTION = "Curves"
DEFAULT_MIN = None
DEFAULT_MAX = None

MAX_COLOR_VALUE = 250
MIN_COLOR_VALUE = 75

def random_color(mini, maxi, minimum_luminosity, last_color_list = None):

    """return rgb value for random color"""
    continu = True

    while continu:
        red = random.randint(mini, maxi)
        blue = random.randint(mini, maxi)
        green = random.randint(mini, maxi)

        if ((red + blue + green)/3) >= minimum_luminosity:
            if last_color_list is not None and len(last_color_list) > 0:
                for color in last_color_list:
                    if (color['red']-25 <= red and red <= color['red']+25)\
                      and (color['green']-25 <= green and\
                                              green <= color['green']+25)\
                      and (color['blue']-25 <= blue and\
                                                blue <= color['blue']+25):
                        pass
                    else:
                        continu = False
            else:
                continu = False

    dic_color = {'red':red, 'green':green, 'blue':blue}
    return dic_color


class Curve(object):

    """This class describe a curve"""

    def __init__(self, row, column, legend, color):
        self.row = row
        self.column = column
        self.legend = legend
        self.color = color


class Figure(object):

    """This class describes a figure"""

    def __init__(self, title, label_y, unit_y, min_y, max_y,
                 grid_x, grid_y, link):
        self.title = title
        self.label_y = label_y
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
            print ("Oops ! An error occured during configuration file reading")
            print ("Please, check configuration file's syntaxe")
            exit()

        # General parameters
        try:
            general_dic = conf_dic[GENERAL_SECTION]

            try:
                self.max_time = int(general_dic["MaxTime"][0])
            except BaseException:
                self.max_time = None

            try:
                self.title = str(' '.join(general_dic["Title"]))
            except BaseException:
                self.title = None

            try:
                rep = "True" in general_dic["Anti-aliasing"][0]
                self.anti_aliasing = rep
            except BaseException:
                self.anti_aliasing = True

            try:
                rep = "True" in general_dic["LinkXAll"][0]
                self.link_x_all = rep
            except BaseException:
                self.link_x_all = False

            try:
                self.abscissa = " ".join(general_dic["Abscissa"])
            except (KeyError, IndexError):
                self.abscissa = "Time"

            try:
                self.label_x = " ".join(general_dic["LabelX"])
            except (KeyError, IndexError):
                self.label_x = self.abscissa

            try:
                self.unit_x = " ".join(general_dic["UnitX"])
            except (KeyError, IndexError):
                self.unit_x = None

        except (IndexError, KeyError):
            print ("Easy Plot configuration file MUST have a section named")
            print (GENERAL_SECTION + " like the one following :")
            print
            print ("[" + GENERAL_SECTION + "]")
            print ("MaxTime         : [maximum time]")
            print ("Title           : [title]")
            print ("Abscissa        : [abscissa]")
            print ("LabelX          : [label of x axis]")
            print ("UnitX           : [unit of x axis]")
            print ("Anti-aliasing   : [anti aliasing]")
            print ("LinkXAll        : [link all x axis]")
            print
            print ("where :")
            print ("- [number of rows] is the number of rows")
            print ("- [number of columns] is the number of colums")
            print ("- [maximum time] is the maximum time of each curve")
            print ("- [title] is the title of the window")
            print ("- [abscissa] is the name of abscissa in cvs file")
            print ("- [label of x axis] is the label of x axis")
            print ("- [unit of x axis] is the unit of x axis")
            print ("- [anti aliasing] is True if you want anti aliasing to be")
            print ("  applied to the window, False else")
            print (
                "- [link all x axis] is True if you want to link all x axis,")
            print ("  False else")
            exit()

        except (ValueError, TypeError):
            print ("There is a no valid value on " +
                   GENERAL_SECTION + " section")
            print ("Please, respect the following format :")
            print ("- [number of rows] is an integer")
            print ("- [number of columns] is an integer")
            print ("- [maximum time] is an integer")
            print ("- [title] is a string")
            print ("- [abscissa] is a string")
            print ("- [label of x axis] is a string")
            print ("- [unit of x axis] is a string")
            print ("- [anti aliasing] is True if you want anti aliasing to be")
            print ("  applied to the window, False else")
            print ("- [UpdateServeur] is the time between two windows refresh")

            exit()

        # Figures parameters

        # Figures dictionnary is the configuration dictionnary without
        # [General] and [Curves] sections

        # Curves parameters
        def print_help():
            """Print help"""
            print ("Easy Plot configuration file MUST have a section named")
            print ("[Curves] like the one following :")
            print
            print ("[Curves]")
            print ("[CurveName] : [Row] [Column] [Legend] [Color]")
            print ("[CurveName] : [Row] [Column] [Legend] [Color]")
            print ("[CurveName] : [Row] [Column] [Legend] [Color]")
            print ("[CurveName] : [Row] [Column] [Legend] [Color]")
            print ("...")
            print
            print ("where :")
            print ("- [CurveName] is the name of the curve")
            print ("- [Row] is the row number of the curve")
            print ("- [Column] is the column number of the curve")
            print ("- [Legend] is the legend of the curve")
            print ("- [Color] is the color of the curve")

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
                print ("ERROR: A section name is not good")
                print ("       Please, check configuration file")
                exit()

            try:
                title = " ".join(dic_fig_caract["Title"])
            except (KeyError, IndexError):
                title = None

            try:
                label_y = " ".join(dic_fig_caract["LabelY"])
            except (KeyError, IndexError):
                label_y = None

            try:
                unit_y = " ".join(dic_fig_caract["UnitY"])
            except (KeyError, IndexError):
                unit_y = None

            try:
                min_y = float(dic_fig_caract["MinY"][0])
            except (KeyError, IndexError):
                min_y = DEFAULT_MIN
            except (ValueError, TypeError):
                print ("ERROR : an error occured on MinY in")
                print (
                    "   [" + str_num_row + "-" + str_num_column + "] section")
                print ("   -> MinY is set to default value")
                print
                min_y = DEFAULT_MIN

            try:
                max_y = float(dic_fig_caract["MaxY"][0])
            except (KeyError, IndexError):
                max_y = DEFAULT_MAX
            except (ValueError, TypeError):
                print ("ERROR : an error occured on MaxY in")
                print (
                    "   [" + str_num_row + "-" + str_num_column + "] section")
                print ("   -> MaxY is set to default value")
                print
                max_y = DEFAULT_MAX

            try:
                rep = "True" in dic_fig_caract["GridX"][0]
                grid_x = rep
            except (KeyError, IndexError):
                grid_x = False
            except (ValueError, TypeError):
                print ("ERROR : an error occured on GridX in")
                print (
                    "   [" + str_num_row + "-" + str_num_column + "] section")
                print ("   -> GridX is set to False")
                print
                grid_x = False

            try:
                rep = "True" in dic_fig_caract["GridY"][0]
                grid_y = rep
            except (KeyError, IndexError):
                grid_y = False
            except (ValueError, TypeError):
                print ("ERROR : an error occured on GridY in")
                print (
                    "   [" + str_num_row + "-" + str_num_column + "] section")
                print ("   -> GridY is set to False")
                print
                grid_y = False

            try:
                if self.link_x_all is False:
                    (link_row, link_col) = dic_fig_caract["LinkX"]
                    link = (int(link_row), int(link_col))
                else:
                    link = None
            except (KeyError, IndexError):
                link = None
            except (ValueError, TypeError):
                print ("ERROR : an error occured on LinkX in")
                print (
                    "   [" + str_num_row + "-" + str_num_column + "] section")
                print ("   -> LinkX is set to None")
                print
                link = None

            figure = Figure(title, label_y, unit_y, min_y,
                            max_y, grid_x, grid_y, link)

            self.figures[fig_coord] = figure

            dic_curves = conf_dic[CURVES_SECTION]

        save_random_color=[]
        for name, parameters in dic_curves.items():
            nb_parameter = len(parameters)
            if nb_parameter >= 4:
                try:

                    dic_color = {'red': 'r', 'green': 'g', 'blue': 'b',
                                 'cyan': 'c', 'magenta': 'm', 'yellow': 'y',
                                 'black': 'k', 'white': 'w'}

                    try:
                        test_param = parameters[-1]
                        test_param = int(test_param)
                        pos_color = -2
                    except (ValueError, TypeError):
                        pos_color = -1

                    str_row = parameters[0]
                    str_column = parameters[1]
                    legend = str(' '.join(parameters[2:pos_color]))
                    color = parameters[pos_color]

                    if pos_color == -2:
                        width = parameters[-1]
                    else:
                        width = 1

                    if color == 'random':

                        color = random_color(
                        0, MAX_COLOR_VALUE, MIN_COLOR_VALUE,save_random_color)

                        save_random_color.append(color)

                        color = (color['red'],
                                 color['green'],
                                 color['blue'])

                    elif len(color) > 1 and color[0] is not '#':
                        color = dic_color[color]

                    # to test if color has a correct format
                    color = pg.mkPen(color=color, width=int(width))

                    curve = Curve(int(str_row), int(str_column), legend, color)
                    self.curves[name] = curve

                except (ValueError, TypeError, KeyError):
                    print ("There is a no valid value on [Curves] section")
                    print ("Please, respect the following format :")
                    print
                    print (
                        "[CurveName]: [Row] [Column] [Legend] [Color] [Width]")
                    print
                    print ("where:")
                    print ("- [CurveName] is a string")
                    print ("- [Row] is an integer")
                    print ("- [Column] is an integer")
                    print ("- [Legend] is a string")
                    print ("- [Color] must be :")
                    print ("          r or red")
                    print ("          g or green")
                    print ("          b or blue")
                    print ("          c or cyan")
                    print ("          m or magenta")
                    print ("          y or yellow")
                    print ("          k or black")
                    print ("          w or white")
                    print ("          (R, G, B, [A]) tuple of integers 0-255")
                    print ("          hexadecimal strings; may begin with #")
                    print ("- [Width] is an integer")
                    exit()

            else:
                print_help()
                exit()
