"""
Welcome to Output Manager.
This module prints and creates the output files and commands script.
"""

import matplotlib.pyplot as plt
import pickle


def print_script_to_file(script, commands_list):
    """
    :param script: a list with the user's raw answers, by order
    :param commands_list: an object that contains all the information we need to build the figure.

    about: printing the command script to a file, if asked
    """
    # verifying if creating script file is wanted
    if commands_list.make_script_file:

        # opening or creating the script file
        script_file = open(commands_list.script_file_print_address, "w")

        # printing the content of the script to the script file, with enters
        for command in script:
            script_file.write(command)
            script_file.write("\n")

        script_file.close()


def print_fig(plt_figure, commands_list):
    """
    :param plt_figure: the final figure
    :param commands_list: an object that contains all the information we need to build the figure.

    about: creating the figure output, in a few formats
    """

    # creating the full name of the file
    file_name = commands_list.fig_location + "\\" + commands_list.name_of_fig + "." + commands_list.fig_format

    # splitting to two cases: pickle format and the rest of the formats.
    if commands_list.fig_format == 'pickle':
        with open(file_name, 'wb') as f:
            pickle.dump(plt_figure, f)
    else:
        plt.savefig(file_name)
