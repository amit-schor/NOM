"""
Welcome to netCDF File Handler.
This module contains functions that interacts with the netcdf_file. They can be used both for getting value from
the file, and to get better understanding of it.
"""

import netCDF4 as nc
import numpy as np
from enum import Enum
from typing import Optional


# a class that contains the three types of variables in the netCDF
class Labels(Enum):
    LABELS = 1
    DIMENSIONS = 2
    DATA = 3


# gets path as raw string
def open_netcdf(path_to_file):
    """
    :param path_to_file: the path for the netCDF file as a string
    :return: the netcdf file

    about: this function opens the netCDF file
    """
    netcdf_file = nc.Dataset(path_to_file)
    return netcdf_file


def get_time_vector_size(netcdf_file, commands_list):
    """
    :param netcdf_file: the netCDF file
    :param commands_list: an object that contains all the information we need to build the figure.
    :return: the size of the time vector

    about: finding the time vector size
    """
    netcdf_info = list(netcdf_file.variables.values())
    return netcdf_info[commands_list.time].size


def get_depth_vector_size(netcdf_file, commands_list):
    """
    :param netcdf_file: the netCDF file
    :param commands_list: an object that contains all the information we need to build the figure.
    :return: the size of the depth vector

    about: finding the time vector size
    """
    netcdf_info = list(netcdf_file.variables.values())
    return netcdf_info[commands_list.depth].size


def show_info(path_to_file, show_specific_label=False, show_var_object=False, show_name=False, show_shape=False,
              show_size=False, show_ndim=False, show_datatype=False, show_dimensions=False):
    """
    :param path_to_file: the path for the netCDF file as a string
    :param show_specific_label: gets the index of the wanted object
    :param show_var_object: show all the information fields about that object
    :param show_name: show the object's names
    :param show_shape: show the object's shape
    :param show_size: show the object's size
    :param show_ndim: show the number of dimensions the object is depends on
    :param show_datatype: show the object's data type (if it contains 32 bits ints, chars etc...)
    :param show_dimensions: show the object's dimensions

    about: printing the variables object of the netCDF file, or only one of them, or specific field of them or one of
    them.
    call_example: show_info(path_to_file, show_name=False, show_ndim = True)
    shows the number of dimensions every object depends on, and the objects names
    """

    netcdf_file = open_netcdf(path_to_file)

    # getting the variable.values objects in a list, so the program could access and print only one of them.
    netcdf_info = list(netcdf_file.variables.values())

    print("general information:\n")

    # separating to two cases: multiple objects or only one
    if not show_specific_label:
        # printing the wanted information of all the objects in the list
        for var_object in netcdf_info:
            print_var_object(var_object, show_var_object, show_name, show_shape,
                             show_size, show_ndim, show_datatype, show_dimensions)
            print("\n")
    else:
        # printing the wanted information on a specific object
        print_var_object(netcdf_info[show_specific_label], show_var_object, show_name, show_shape,
                         show_size, show_ndim, show_datatype, show_dimensions)
    netcdf_file.close()


def print_var_object(var_object, show_var_object=False, show_name=False, show_shape=False,
                     show_size=False, show_ndim=False, show_datatype=False, show_dimensions=False):
    """
    :param var_object: The variable object from the netCDF file
    :param show_var_object: show all the information fields about that object
    :param show_name: show the object's names
    :param show_shape: show the object's shape
    :param show_size: show the object's size
    :param show_ndim: show the number of dimensions the object is depends on
    :param show_datatype: show the object's data type (if it contains 32 bits ints, chars etc...)
    :param show_dimensions: show the object's dimensions

    about: this function prints the wanted info about var_object.
    """
    # split to cases and print accordingly
    if show_var_object or (not show_var_object and not show_name and not show_shape and not show_size and not show_ndim
                           and not show_datatype and not show_dimensions):
        print(var_object)
        print("\n")
    if show_name:
        print(var_object.name)
        print("\n")
    if show_shape:
        print(var_object.shape)
        print("\n")
    if show_size:
        print(var_object.size)
        print("\n")
    if show_ndim:
        print(var_object.ndim)
        print("\n")
    if show_datatype:
        print(var_object.datatype)
        print("\n")
    if show_dimensions:
        print(var_object.dimensions)
        print("\n")


def variable_name_list(netcdf_file, label: Labels):
    """
    :param netcdf_file: the netCDF file
    :param label: The variable type as a Labels object's field
    :return: a list with the variables labels of a specific variable type

    about: returns the labels of the variables of the type given in label.
    """

    info_list = []
    variable_list = []

    if label == Labels.LABELS or label == Labels.DATA:
        for var in netcdf_file.variables.values():
            variable_list.append(var.name)
        if label == Labels.LABELS:
            info_list = variable_list
    dimension_list = []
    if label == Labels.DIMENSIONS or label == Labels.DATA:
        for dim in netcdf_file.dimensions.values():
            dimension_list.append(dim.name)
        if label == Labels.DIMENSIONS:
            info_list = dimension_list
    data_variables_list = []
    if label == Labels.DATA:
        for var in variable_list:
            if var not in dimension_list:
                data_variables_list.append(var)
        info_list = data_variables_list
    return info_list


def get_dimensions_values(netcdf_file):
    """
    :param netcdf_file: the netCDF file
    :return: an array of arrays with the values of all the dimension objects

    about: extracts the dimensions (axes) data from a netcdf file object
    """
    dimension_names_list, *_ = variable_name_list(netcdf_file, Labels.LABELS)
    dimension_values = []
    for i in range(len(dimension_names_list)):
        dimension_values.append(get_values(netcdf_file, dimension_names_list[i]))
    return dimension_values


def get_data_variables_values(netcdf_file):
    """
    :param netcdf_file: the netCDF file
    :return: an array of arrays with the values of all the data objects

    about: extracts the fields data (values) from a netcdf file object
    """

    data_variable_list, *_ = variable_name_list(netcdf_file, Labels.DATA)
    data_values = []
    for i in range(len(data_variable_list)):
        data_values.append(get_values(netcdf_file, data_variable_list[i]))
    return data_values


def get_all_values(netcdf_file):
    """
    :param netcdf_file: the netCDF file
    :return: an array of arrays with the values of all the objects

    about: extracts all data from a netcdf file object
    """

    dimensions_name_list, *_ = variable_name_list(netcdf_file, Labels.DIMENSIONS)
    data_variable_list, *_ = variable_name_list(netcdf_file, Labels.DATA)
    all_values_list = get_dimensions_values(netcdf_file) + get_data_variables_values(netcdf_file)
    return all_values_list


def get_values(netcdf_file, field_name):
    """
    :param netcdf_file: the netCDF file
    :param field_name: the name of the variables.values object in the netCDF
    :return: an array that contains all the fields numerical values

    about: getting from the netCDF variables.values object an array of the numerical values

    call_example:
    get_values(netcdf_file, 'wave_max_height')
    gets an array with the height of the waves depends on all wave_max_height's dimensions
    [[54, 34.4, 53 ...],
    [... ... ...],
        ...
    [... ... ...]]

    """
    values = np.ma.filled(netcdf_file[field_name][:].astype(float), np.nan)
    return values


def dimensions_of_variable_list(netcdf_file, field_name):
    """
    :param netcdf_file: the netCDF file
    :param field_name: the name of the variables.values object in the netCDF
    :return: a list of the dimensions the field object depends on, by the order they are located in the array

    about: getting a list of the dimensions field_name depends on, by the order they are located in the array.

    call_example:
    dimensions_of_variable_list(netcdf_file, 'wave_max_height')
    it returns: [time, lat, lon]
    """
    dimensions = []
    for dim in netcdf_file.variables[field_name].get_dims():
        dimensions.append(dim.name)
    return dimensions


# a class that saves to an object the dimention's indexes of a specific variable object in the netCDF
class FieldIndexes:
    time: Optional[int]
    depth: Optional[int]
    lat: Optional[int]
    lon: Optional[int]

    def __init__(self):
        self.time = None
        self.depth = None
        self.lat = None
        self.lon = None


def find_indexes_in_dimension_list(netcdf_file, field_name, commands_list):
    """
    :param netcdf_file: the netCDF file
    :param field_name: the name of the variables.values object in the netCDF
    :param commands_list: an object that contains all the information we need to build the figure.
    :return: an object that contains field_name's indexes for every dimension
    """
    field_indexes = FieldIndexes()
    dimensions = dimensions_of_variable_list(netcdf_file, field_name)
    if commands_list.time is not None:
        field_indexes.time = find_index(dimensions, commands_list.info_list[commands_list.time])
    if commands_list.depth is not None:
        field_indexes.depth = find_index(dimensions, commands_list.info_list[commands_list.depth])
    if commands_list.lat is not None:
        field_indexes.lat = find_index(dimensions, commands_list.info_list[commands_list.lat])
    if commands_list.lon is not None:
        field_indexes.lon = find_index(dimensions, commands_list.info_list[commands_list.lon])
    return field_indexes


def find_index(dimensions, target_dim: str):
    """
    :param dimensions: a list of dimensions
    :param target_dim: specific dimension's name
    :return:the index if target_dim in the dimensions list

    about: finding the index of a specific dimension in a list of a variable object's dimensions

    call_example:
    find_index([lat, time, lon], lon)
    -> 2
    """
    for i in range(len(dimensions)):
        if dimensions[i] == target_dim:
            return i
    else:
        raise Exception("target_dim not found in dimensions list")
