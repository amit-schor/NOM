"""
Welcome to Input Manager
This module gets the input from the user and manages it. It defines classes for the users answers and validates the
answers.

algorithm: First, a script array and a CommandsList, MapCommandsList or GraphCommandsList object, commands_list, need
to be created. The purpose of the algorithm is to fill the commands_list and script array.
The main function calls the 'get info' functions to ask the user questions, with the use of the
'send query' functions. If needed, the user's answer can be validated with the 'validate answer' functions, while using
partial validate function inside the 'send query' function itself. If an answer is illegal, the question will be asked
again, until a legal answer is given.
In the 'send query' function, the raw answer will be added to the script array.
After getting an answer, the answer will be added to the commands_list object after some processing.
"""

import netCDF_file_handler as nfh
from functools import partial
import safer_prompt_toolkit
from typing import List, Optional, Callable
import extra_prompt_toolkit_utilities as eptu

# initialising to False. if True, then the program knows that it reads from a file and will not create user interface
is_reading_from_file = False


# a class that contains the basic commands
class CommandsList:
    info_list: Optional[List[str]]  # list of all the fields name
    netcdf_path: Optional[str]  # the path to the netCDF file
    plot_type: Optional[int]  # type of the plot (0 - map, 1 - graph)
    make_script_file: Optional[bool]  # if to make a script file with the raw answers
    script_file_print_address: Optional[str]  # where to create the script file (and name)
    name_of_fig: Optional[str]  # the name of the fig
    fig_format: Optional[str]  # the format of the fig
    fig_location: Optional[str]  # the address of the fig on the computer
    current_time_value: Optional[int]  # the time value of this current fig
    current_depth_value: Optional[int]  # the depth value of this current fig

    # TODO fill value function

    def __init__(self):
        self.info_list = None
        self.netcdf_path = None
        self.plot_type = None
        self.make_script_file = None
        self.script_file_print_address = None
        self.name_of_fig = None
        self.fig_format = None
        self.fig_location = None
        self.current_time_value = 0
        self.current_depth_value = 0


# a class that contains the commands to create a map
class MapCommandsList(CommandsList):
    lat: Optional[int]  # latitude
    lon: Optional[int]  # longitude
    time: Optional[int]
    depth: Optional[int]
    is_vector_field: Optional[bool]
    scalar_field_label: Optional[int]  # the name of the data field if its scalar
    is_polar: Optional[bool]
    lon_component: Optional[int]  # data field of the longitude component of the total field (cartesian)
    lat_component: Optional[int]  # data field of the latitude component of the total field (cartesian)
    rad_component: Optional[int]  # data field of the radial component of the total field (polar)
    ang_component: Optional[int]  # data field of the angular component of the total field (polar)
    is_depends_on_time: Optional[bool]  # is the data field depends on time
    is_depends_on_depth: Optional[bool]  # is the data field depends on depth

    # preferences
    quiver_color: Optional[str]  # color of arrows
    quiver_space: Optional[int]  # space between the arrow (quiver_space = 5 means to take data from every 5th element)
    width: Optional[int]
    height: Optional[int]
    lon_center: Optional[float]  # the mean of all lon values (center of map)
    lat_center: Optional[float]  # the mean of all lat values (center of map)
    lon_lower_left_corner: Optional[float]  # llcrnrlon
    lat_lower_left_corner: Optional[float]  # llcrnrlat
    lon_upper_right_corner: Optional[float]  # urcrnrlon
    lat_upper_right_corner: Optional[float]  # urcrnrlat
    resolution: Optional[str]
    projection: Optional[str]  # type of of projection of the map

    # TODO create defaults for lon_min and lat_min etc after finding lon and lat

    def __init__(self, *args):
        if len(args) == 1:
            self.info_list = args[0].info_list
            self.netcdf_path = args[0].netcdf_path
            self.plot_type = args[0].plot_type
            self.make_script_file = args[0].make_script_file
            self.script_file_print_address = args[0].script_file_print_address
            self.name_of_fig = args[0].name_of_fig
            self.fig_format = args[0].fig_format
            self.fig_location = args[0].fig_location
            self.current_time_value = args[0].current_time_value
            self.current_depth_value = args[0].current_depth_value

        elif len(args) == 0:
            super().__init__()
        else:
            raise Exception("too many arguments")
        self.lat = None
        self.lon = None
        self.time = None
        self.depth = None
        self.is_vector_field = None
        self.scalar_field_label = None
        self.is_polar = None
        self.lon_component = None
        self.lat_component = None
        self.rad_component = None
        self.ang_component = None
        self.is_depends_on_time = None
        self.is_depends_on_depth = None

        self.quiver_color = 'b'
        self.quiver_space = 15
        self.width = None
        self.height = None
        self.lon_center = None
        self.lat_center = None
        self.lon_lower_left_corner = None
        self.lat_lower_left_corner = None
        self.lon_upper_right_corner = None
        self.lat_upper_right_corner = None
        self.resolution = 'c'
        self.projection = 'gall'


class GraphCommandsList(CommandsList):
    x_axis: Optional[int]
    y_axis: Optional[int]
    time: Optional[int]
    depth: Optional[int]
    is_depends_on_time: Optional[bool]  # is the data field depends on time
    is_depends_on_depth: Optional[bool]  # is the data field depends on depth

    # preferences
    width: Optional[int]
    height: Optional[int]

    # TODO create defaults for lon_min and lat_min etc after finding lon and lat

    def __init__(self, *args):
        if len(args) == 1:
            self.info_list = args[0].info_list
            self.netcdf_path = args[0].netcdf_path
            self.plot_type = args[0].plot_type
            self.make_script_file = args[0].make_script_file
            self.script_file_print_address = args[0].script_file_print_address
            self.name_of_fig = args[0].name_of_fig
            self.fig_format = args[0].fig_format
            self.fig_location = args[0].fig_location
            self.current_time_value = args[0].current_time_value
            self.current_depth_value = args[0].current_depth_value

        elif len(args) == 0:
            super().__init__()
        else:
            raise Exception("too many arguments")
        self.x_axis = None
        self.y_axis = None
        self.time = None
        self.depth = None
        self.is_depends_on_time = None
        self.is_depends_on_depth = None

        # preferences
        self.width = None
        self.height = None


# TODO
#  a mode that get an existing text script and run on all the questions and enables interactive editing to create a new,
#  edited working script
def edit_mode():
    pass


# get info from the user functions


def get_if_script_file(script, commands_list: CommandsList):
    """
    :param script: a list with the user's raw answers, by order
    :param commands_list: an object that can be filled with somewhat processed answers to the questions
    :return: commands_list

    about: this function asks the user if they want to create a script from their answers, and if so asks for the new
    script's location.
    """
    question = 'To to create your output from the netCDF file, you will be asked questions. Your\n' \
               'answers will determine how this output is generated. To ease the building of a new\n' \
               'output, your raw answers will be saved in a list, that can be converted to a text\n' \
               'file. The text file can be used as an input to this program, and it will answer the\n' \
               'questions the program asks.\n' \
               'The script file can be used to run on multiple netCDF files, or multiple times on\n' \
               'the same netCDF file.\n\n' \
               'ATTENTION!\n' \
               'To avoid an excess of script files while automatically running the program\n' \
               'with scripts created in the questioning process, the answer to this\n' \
               'question will always be saved as "NO".\n\n' \
               'Do you want to save a script text file with your answers at ' \
               'the end of the run?\n    (0)NO   (1)YES\n'

    # printing the question and getting the user's input, and inserting it into the commands_list
    make_script_file = send_query_script_file(question, [0, 1], script)
    commands_list.make_script_file = (make_script_file == str(1))

    # if the user want to create a script, getting the script's full name and address
    if commands_list.make_script_file:
        commands_list.script_file_print_address = send_query_path_new_script('Enter where you'
                                                                             ' want the script'
                                                                             ' text file to be'
                                                                             ' created. for '
                                                                             'example: '
                                                                             'C:\\Home\\location'
                                                                             '\\script_name.txt'
                                                                             '): ')
    return commands_list


def get_name_and_location(script, commands_list: CommandsList):
    """
    :param script: a list with the user's raw answers, by order
    :param commands_list: an object that can be filled with somewhat processed answers to the questions
    :return: commands_list

    about: gets from the user the netCDF's location and name
    """
    commands_list.netcdf_path = send_query_path('Enter the name and location of the netCDF file you want to'
                                                ' work on:', script)
    return commands_list


def get_plot_type(script, commands_list: CommandsList):
    """
    :param script: a list with the user's raw answers, by order
    :param commands_list: an object that can be filled with somewhat processed answers to the questions
    :return: commands_list

    about: gets from the user the type of the plot they want to create
    """
    plot_type = send_query('Select the type of the plot:\n0) map\n1) 2D graph\n', [0, 1], script,
                           commands_list)
    commands_list.plot_type = int(plot_type)
    return commands_list


def get_map_choose_parameters(netcdf_file, script, commands_list: MapCommandsList):
    """
    :param netcdf_file: the netCDF file
    :param script: a list with the user's raw answers, by order
    :param commands_list:  a MapCommandsList object  that can be filled with somewhat processed answers to the
    questions. contains fields specific to map building.
    :return: commands_list
    """

    # asking the user for the index in the netCDF of the latitude and longitude objects
    print_labels_list_and_explanation(commands_list)
    lat = send_query("what is the latitude?", range(len(commands_list.info_list)), script, commands_list)
    lon = send_query("what is the longitude?", range(len(commands_list.info_list)), script, commands_list)
    commands_list.lat = int(lat)
    commands_list.lon = int(lon)

    # asking the user if the data field is vector field or scalar field
    is_vector_field = send_query("is your field a scalar field (0) or a vector field (1)?", [0, 1], script,
                                 commands_list)
    commands_list.is_vector_field = (is_vector_field == str(1))

    # if the field is scalar, asking what is the index in the netCDF of the scalar field
    if is_vector_field == str(0):

        scalar_field_label = send_query("what is the scalar field?", range(len(commands_list.info_list)),
                                        script, commands_list)
        commands_list.scalar_field_label = int(scalar_field_label)

        # printing the dimensions the scalar field depends on, in order to ask the user about time and depth dependence
        print("the field", str(commands_list.info_list[int(scalar_field_label)]), "have the following dimensions:")
        print(nfh.dimensions_of_variable_list(netcdf_file, str(commands_list.info_list[int(scalar_field_label)])))

    # if the field is a vector field, asking if its in a polar or cartesian coordinates system,
    # then asking for the components accordingly
    else:

        is_polar = send_query("is the components already in polar coordinated?\n    (0)NO   (1)YES\n", [0, 1],
                              script, commands_list)
        commands_list.is_polar = (is_polar == str(1))

        if is_polar == str(0):  # the coordinates are cartesian

            lon_component = send_query("what component is parallel to the longitude?",
                                       range(len(commands_list.info_list)), script, commands_list)
            lat_component = send_query("what component is parallel to the latitude?",
                                       range(len(commands_list.info_list)), script, commands_list)
            commands_list.lon_component = int(lon_component)
            commands_list.lat_component = int(lat_component)

            # printing the dimensions the fields depends on, in order to ask the user about time and depth dependence
            print("the fields", str(commands_list.info_list[int(lon_component)]), ",",
                  str(commands_list.info_list[int(lat_component)]),
                  "have the following dimensions:")
            print(nfh.dimensions_of_variable_list(netcdf_file, str(commands_list.info_list[int(lon_component)])))
            print(nfh.dimensions_of_variable_list(netcdf_file, str(commands_list.info_list[int(lat_component)])))

        else:  # the coordinates are polar

            rad_component = send_query("what is the radial component?", range(len(commands_list.info_list)),
                                       script, commands_list)
            ang_component = send_query("what is the angular component?", range(len(commands_list.info_list)),
                                       script, commands_list)
            commands_list.rad_component = int(rad_component)
            commands_list.ang_component = int(ang_component)

            # printing the dimensions the fields depends on, in order to ask the user about time and depth dependence
            print("the fields", str(commands_list.info_list[int(rad_component)]), ",",
                  str(commands_list.info_list[int(ang_component)]),
                  "have the following dimensions:")
            print(nfh.dimensions_of_variable_list(netcdf_file, str(commands_list.info_list[int(rad_component)])))
            print(nfh.dimensions_of_variable_list(netcdf_file, str(commands_list.info_list[int(ang_component)])))

    # asking if the data field depends on time
    is_depends_on_time = send_query("is one of the above dimensions is time?\n    (0)NO   (1)YES\n", [0, 1],
                                    script, commands_list)
    commands_list.is_depends_on_time = (is_depends_on_time == str(1))

    # if there is time dependence, asking the user the index in the netCDF of the time field
    # and to choose the index of the time they want in the time array
    if is_depends_on_time == str(1):
        print("Select from the following list:")
        print_labels_list(commands_list)
        time = send_query("what is the time label?", range(len(commands_list.info_list)), script, commands_list)
        commands_list.time = int(time)

        # asking for the index of the time they want in the time array
        get_time(netcdf_file, script, commands_list)

    # asking if the data field depends on depth
    is_depends_on_depth = send_query("is one of the above dimensions is depth/height?\n    (0)NO   (1)YES\n",
                                     [0, 1], script, commands_list)
    commands_list.is_depends_on_depth = (is_depends_on_depth == str(1))

    # if there is time dependence, asking the user the index in the netCDF of the time field
    # and to choose the index of the time they want in the depth array
    if is_depends_on_depth == str(1):
        print("Select from the following list:")
        print_labels_list(commands_list)
        depth = send_query("what is the depth/height label?", range(len(commands_list.info_list)), script,
                           commands_list)
        commands_list.depth = int(depth)

        # asking for the index of the time they want in the depth array
        get_depth(netcdf_file, script, commands_list)
    return commands_list


def get_graph_choose_parameters(netcdf_file, script, commands_list: GraphCommandsList):
    print_labels_list_and_explanation(commands_list)
    x_axis = send_query("What is the x axis?", range(len(commands_list.info_list)), script, commands_list)
    commands_list.x_axis = int(x_axis)
    y_axis = send_query("What is the y axis?", range(len(commands_list.info_list)), script, commands_list)
    commands_list.y_axis = int(y_axis)

    print("the fields", str(commands_list.info_list[int(x_axis)]), ",", str(commands_list.info_list[int(y_axis)]),
          "have the following dimensions:")
    print(nfh.dimensions_of_variable_list(netcdf_file, str(commands_list.info_list[int(x_axis)])))
    print(nfh.dimensions_of_variable_list(netcdf_file, str(commands_list.info_list[int(y_axis)])))
    is_depends_on_time = send_query("is one of the above dimensions is time?\n    (0)NO   (1)YES\n", [0, 1], script,
                                    commands_list)
    commands_list.is_depends_on_time = (is_depends_on_time == str(1))
    if is_depends_on_time == str(1):
        print("Select from the following list:")
        print_labels_list(commands_list)
        time = send_query("what is the time label?", range(len(commands_list.info_list)), script, commands_list)
        commands_list.time = int(time)
        get_time(netcdf_file, script, commands_list)
    is_depends_on_depth = send_query("is one of the above dimensions is depth?\n    (0)NO   (1)YES\n", [0, 1], script,
                                     commands_list)
    commands_list.is_depends_on_depth = (is_depends_on_depth == str(1))
    if is_depends_on_depth == str(1):
        print("Select from the following list:")
        print_labels_list(commands_list)
        depth = send_query("what is the depth/height label?", range(len(commands_list.info_list)), script,
                           commands_list)
        commands_list.depth = int(depth)
        get_depth(netcdf_file, script, commands_list)


def get_time(netcdf_file, script, commands_list):
    """

    :param netcdf_file: the netCDF file
    :param script: a list with the user's raw answers, by order
    :param commands_list:  an object  that can be filled with somewhat processed answers to the
    questions.
    :return: commands_list

    about: asking for the index of the time they want in the time array
    """

    # getting the size of the time vector
    time_vector_size = nfh.get_time_vector_size(netcdf_file, commands_list)
    if time_vector_size > 1:
        question = "The time object have the size of " + str(time_vector_size) + ". please select the index of the " \
                                                                                 "time value you want from 0 to " + \
                   str(time_vector_size - 1) + "."

        # asking the user
        current_time_value = send_query(question, range(time_vector_size), script, commands_list)
        commands_list.current_time_value = int(current_time_value)
        return commands_list


def get_depth(netcdf_file, script, commands_list):
    """

    :param netcdf_file: the netCDF file
    :param script: a list with the user's raw answers, by order
    :param commands_list:  an object  that can be filled with somewhat processed answers to the
    questions.
    :return: commands_list

    about: asking for the index of the time they want in the depth array
    """
    # getting the size of the depth vector
    depth_vector_size = nfh.get_depth_vector_size(netcdf_file, commands_list)
    if depth_vector_size > 1:
        question = "The depth object have the size of " + str(depth_vector_size) + ". please select the index of the " \
                                                                                   "depth value you want from 0 to " + \
                   str(depth_vector_size - 1) + "."

        # asking the user
        current_depth_value = send_query(question, range(depth_vector_size), script, commands_list)
        commands_list.current_depth_value = int(current_depth_value)
        return commands_list


def get_plot_name_location_and_format(script, commands_list):
    """
    :param script: a list with the user's raw answers, by order
    :param commands_list:  an object that contains all the information we need to build the figure.
    :return: commands_list

    about: getting the plot's full address and name
    """

    # asking fot the figure's format, creating an interface for the Terminal that suggest answers for this question
    completer, validator = eptu.make_ConstantOptions_Completer_and_Validator(
        ["pdf", "png", "jpg", "jpeg", "pickle", "eps", "ps", "svg"])
    fig_format = safer_prompt_toolkit.prompt("Select the figures format:\n", completer=completer, validator=validator,
                                             force_fail_safe=is_reading_from_file)
    fig_format = str(fig_format)
    add_to_script(script, [fig_format])
    commands_list.fig_format = fig_format

    # asking fot the figure's address
    fig_location = send_query_path("Select the directory in which you want the plot to be created:\n", script)
    commands_list.fig_location = fig_location

    # asking fot the figure's name
    name_of_fig = input("Select the name of the figure:\n")
    add_to_script(script, [name_of_fig])
    commands_list.name_of_fig = name_of_fig

    return commands_list


# updating fields in command list


def update_info_list_in_command_list(netcdf_file, commands_list: CommandsList):
    """
    :param netcdf_file: the netCDF file
    :param commands_list: an object that can be filled with somewhat processed answers to the questions
    :return: commands_list

    about: updating the commands_list.info_list field to have a list of all the netCDF's variable objects
    """
    commands_list.info_list = nfh.variable_name_list(netcdf_file, nfh.Labels.LABELS)
    return commands_list


# printing functions


def print_labels_list_and_explanation(commands_list):
    """
    :param commands_list: an object that can contains all the information we need to build the figure.

    about: printing the list of all the names of the netCDF variables, with explanation on how to answer.
    """
    print("Here is the list of the available labels:\n")
    print_labels_list(commands_list)
    print("\nTo answers the following questions, type the corresponding number from the table above, or from the\n"
          "question's content, then press enter. Type 'll' (ll for label list) in any question about the labels to\n"
          "see this list again.\n")


def print_labels_list(commands_list):
    """
     :param commands_list: an object that can contains all the information we need to build the figure.

     about: printing the list of all the names of the netCDF variables.
     """
    for i in range(len(commands_list.info_list)):
        print(str(i) + ")    " + str(commands_list.info_list[i]))


def print_turtle():
    turtle = "                           _______                  \n" \
             "                    /^^^^^^      ^^^^^^^^\\          \n" \
             "     /^^^^^^-_    /\\ \\\\ \\-----------/  // /\\        \n" \
             "    |   __     \\/   | \\\\==============// |   \\     \n" \
             "    |  |^ |    ||  / //  ___________  \\\\ \\   ||__ =\n" \
             "    |__ ==_____||\\/_//__/___________\\__\\\\_\\__/||_ / \n" \
             "               \\==============================/     \n" \
             "              (___/____/              \\___\\____)    \n"
    print(turtle)


# scrip editing


def add_to_script(script, new_commands):
    """
    :param script: a list with the user's raw answers, by order
    :param new_commands: the raw answer to a question

    about: adding new answers to the script
    """
    script.extend(new_commands)


# Send query functions:

def send_query(question, possible_answers, script, commands_list):
    """
    :param question: a string, the question the program will print
    :param possible_answers: a list of possible answers to question
    :param script: a list with the user's raw answers, by order
    :param commands_list: an object that can contains all the information we need to build the figure.
    :return: the users answer

    about: asking the user for input and validating it
    """

    # creating the possible_answer_string and converting every element in it to a string
    possible_answer_string = [str(a) for a in possible_answers]
    possible_answer_string = possible_answer_string + ['ll', 'banana?', 'turtle']

    # making a partial function object the validator will call to
    partial_validate_answer: Callable[[str], bool] = partial(validate_answer, possible_answer_string)

    while True:
        # asking the question and validating the answer with partial_validate_answer, that
        # uses validate_answer function.
        answer = safer_prompt_toolkit.prompt(
            message=question + "\n",
            validator=safer_prompt_toolkit.validation.Validator.from_callable(partial_validate_answer,
                                                                              error_message="\nInput is not a valid "
                                                                                            "answer to the question."),
            force_fail_safe=is_reading_from_file)
        if answer not in ['ll', 'banana?', 'turtle'] and answer in possible_answer_string:
            break
        # printing the list of label again and asking the same question
        if answer == 'll':
            print_labels_list(commands_list)

        if answer == "banana?":  # banana!
            print("\nBANANA!!!")
        if answer == "turtle":  # turtle!
            print_turtle()

    # adding the raw final answer to the script
    add_to_script(script, [answer])
    return answer


def send_query_script_file(question, possible_answers, script):
    """
    :param question: a string, the question the program will print
    :param possible_answers: a list of possible answers to question
    :param script: a list with the user's raw answers, by order
    :return: the users answer

    about: asking the user for input and validating it
    """
    # creating the possible_answer_string and converting every element in it to a string
    possible_answer_string = [str(a) for a in possible_answers]

    # making a partial function object the validator will call to
    partial_validate_answer_script_file: Callable[[str], bool] = partial(validate_answer_script_file,
                                                                         possible_answer_string)
    # asking the question and validating the answer with partial_validate_answer_script_file, that
    # uses validate_answer_script_files function.
    answer = safer_prompt_toolkit.prompt(
        message=question + "\n",
        validator=safer_prompt_toolkit.validation.Validator.from_callable(partial_validate_answer_script_file,
                                                                          error_message="Input is not a valid answer to"
                                                                                        " the question."),
        force_fail_safe=is_reading_from_file)

    # always adding 0 to the script no matter what answer, to prevent script creation on multiple automatic runs
    add_to_script(script, [str(0)])
    return answer


def send_query_path(question, script):
    """
    :param question: a string, the question the program will print
    :param script: a list with the user's raw answers, by order
    :return: the users answer

    about: asking the user for an address and suggesting completions while typing
    """
    answer = safer_prompt_toolkit.prompt(message=question + "\n",
                                         completer=safer_prompt_toolkit.completion.PathCompleter(),
                                         force_fail_safe=is_reading_from_file)
    add_to_script(script, [answer])
    return answer


def send_query_path_new_script(question):
    """
    :param question: a string, the question the program will print
    :return: the users answer

    about: asking the user for an address and suggesting completions while typing
    """
    answer = safer_prompt_toolkit.prompt(message=question + "\n",
                                         completer=safer_prompt_toolkit.completion.PathCompleter(),
                                         force_fail_safe=is_reading_from_file)

    # no need to add script's address to the script
    return answer


# validate answer functions:


def validate_answer_script_file(possible_answer_string, answer):
    """
    :param possible_answer_string: list of possible answers
    :param answer: the users answer
    :return: True if answer is in possible_answer_string, False if not
    """
    return answer in possible_answer_string


def validate_answer(possible_answer_string, answer):
    """
    :param possible_answer_string: list of possible answers
    :param answer: the users answer
    :return: True if answer is in possible_answer_string, False if not
    """
    return answer in possible_answer_string
