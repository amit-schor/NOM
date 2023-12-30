"""
welcome to 'omnom Mapping with Netcdf for Oceanography & Meteorology' module.
This module contains functions about map buildings and fields arrangement

algorithm: Map making starts with make_map(). This function finds whether the map is vectorial or scalar and calls for
the corresponding function, make_map_vectorial() or make_map_scalar(). both of the functions start with making the map
base, same for both, with make_map_base(). Then they get the values of the vectors used to build the map, and arrange
them in a specific order: time, depth, lat, lon with the arrange_fields() function and the
nfh.find_indexes_in_dimension_list() function. While make_map_scalar() does the two latter actions by itself,
make_map_vectorial() calls for make_polar_components() or make_cartesian_components() function to do it, depending on
the coordinate system.
Afterwards, they use contourf and quiver from matplotlib.pyplot to draw the data on the map. At this stage the user
preferences can be used to customize the map, using the MapCommandsList object, commands_list, from InputManager.

"""
import netCDF_file_handler as nfh
from netCDF_file_handler import FieldIndexes
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from InputManager import MapCommandsList


def make_map(netcdf_file, commands_list: MapCommandsList):
    """
    :param netcdf_file: the netCDF file
    :param commands_list: an object from the MapCommandsList type that contains all the information we need to build the
    map.

    about: this function creates a vectorial or a scalar map, depends on the the value of commands_list.is_vector_field
    """
    if commands_list.is_vector_field:
        make_map_vectorial(netcdf_file, commands_list)
    else:
        make_map_scalar(netcdf_file, commands_list)


# Making a map, assuming scalar field
def make_map_scalar(netcdf_file, commands_list: MapCommandsList):
    """
    :param netcdf_file: the netCDF file
    :param commands_list: an object from the MapCommandsList type that contains all the information we need to build the
    map.

    about: this function creates a scalar map
    """
    # making the base of the map
    xx, yy = make_map_base(netcdf_file, commands_list)

    # getting the values of the scalar field.
    scalar_field_name = commands_list.info_list[commands_list.scalar_field_label]
    scalar_field = nfh.get_values(netcdf_file, scalar_field_name)

    # finding the order of the dimensions the fields depends on and arranging the field's dimensions order to:
    # time, depth, lat, lon
    field_indexes = nfh.find_indexes_in_dimension_list(netcdf_file, scalar_field_name, commands_list)
    scalar_field = arrange_fields(scalar_field, commands_list, field_indexes)

    # drawing the field on the map
    plt.contourf(xx, yy, scalar_field[commands_list.current_time_value][commands_list.current_depth_value])


def make_map_vectorial(netcdf_file, commands_list: MapCommandsList):
    """
    :param netcdf_file: the netCDF file
    :param commands_list: an object from the MapCommandsList type that contains all the information we need to build the
    map.

    about: this function creates a vectorial map
    """
    # making the base of the map
    xx, yy = make_map_base(netcdf_file, commands_list)

    # splitting the two cases of scalar and vectorial maps
    if commands_list.is_polar:
        lat_component, lon_component, vector_size = make_polar_components(netcdf_file, commands_list)
    else:
        lat_component, lon_component, vector_size = make_cartesian_components(netcdf_file, commands_list)

    # drawing the vectors and their total sizes
    plt.contourf(xx, yy, vector_size[commands_list.current_time_value][commands_list.current_depth_value])
    plt.quiver(xx[::commands_list.quiver_space, ::commands_list.quiver_space],
               yy[::commands_list.quiver_space, ::commands_list.quiver_space],
               lat_component[commands_list.current_time_value][commands_list.current_depth_value][
               ::commands_list.quiver_space, ::commands_list.quiver_space],
               lon_component[commands_list.current_time_value][commands_list.current_depth_value][
               ::commands_list.quiver_space, ::commands_list.quiver_space],
               color='r')


def make_polar_components(netcdf_file, commands_list: MapCommandsList):
    """
    :param netcdf_file: the netCDF file
    :param commands_list: an object from the MapCommandsList type that contains all the information we need to build the
    map.
    :return: a vector containing the field's latitude, longitude and size components

    about: extracts the polar data from a netcdf file , reorders them in a predefined order, and projects them to
    latitude,longitude, and size
    """
    # getting the names of the size and angular vector fields as they are written in the netCDF file, from the info list
    vector_size_field_name = commands_list.info_list[commands_list.rad_component]
    vector_ang_field_name = commands_list.info_list[commands_list.ang_component]

    # getting the values of the fields from the netCDF file
    vector_size = nfh.get_values(netcdf_file, vector_size_field_name)
    vector_ang = nfh.get_values(netcdf_file, vector_ang_field_name)

    # finding the order of the dimensions the fields depends on and arranging the fields's dimensions order to:
    # time, depth, lat, lon
    vector_size_field_indexes = nfh.find_indexes_in_dimension_list(netcdf_file, vector_size_field_name,
                                                                   commands_list)
    vector_ang_field_indexes = nfh.find_indexes_in_dimension_list(netcdf_file, vector_ang_field_name, commands_list)
    vector_size = arrange_fields(vector_size, commands_list, vector_size_field_indexes)
    vector_ang = arrange_fields(vector_ang, commands_list, vector_ang_field_indexes)

    lat_component = vector_size * np.cos(vector_ang * np.pi / 180 + np.pi / 2)
    lon_component = vector_size * np.sin(vector_ang * np.pi / 180 + np.pi / 2)
    return lat_component, lon_component, vector_size


def make_cartesian_components(netcdf_file, commands_list: MapCommandsList):
    """
    :param netcdf_file: the netCDF file
    :param commands_list: an object from the MapCommandsList type that contains all the information we need to build the
    map.
    :return: a vector containing the field's latitude, longitude and size components

    about: extracts the cartesian data from a netcdf file , reorders them in a predefined order, and projects them to
    latitude,longitude, and size
    """
    # getting the names of the size and angular vector fields as they are written in the netCDF file, from the info list
    lat_component_field_name = commands_list.info_list[commands_list.lat_component]
    lon_component_field_name = commands_list.info_list[commands_list.lon_component]

    # getting the values of the fields from the netCDF file
    lat_component = nfh.get_values(netcdf_file, lat_component_field_name)
    lon_component = nfh.get_values(netcdf_file, lon_component_field_name)

    # finding the order of the dimensions the fields depends on and arranging the fields's dimensions order to:
    # time, depth, lat, lon
    lat_component_field_indexes = nfh.find_indexes_in_dimension_list(netcdf_file, lat_component_field_name,
                                                                     commands_list)
    lon_component_field_indexes = nfh.find_indexes_in_dimension_list(netcdf_file, lon_component_field_name,
                                                                     commands_list)
    lat_component = arrange_fields(lat_component, commands_list, lat_component_field_indexes)
    lon_component = arrange_fields(lon_component, commands_list, lon_component_field_indexes)
    lat_component = np.array(lat_component)
    lon_component = np.array(lon_component)

    vector_size = np.sqrt(np.power(lat_component, 2) + np.power(lon_component, 2))
    return lat_component, lon_component, vector_size


def arrange_fields(field, commands_list, field_indexes: FieldIndexes):
    """
    :param field: the field this function is going to arrange
    :param commands_list: an object from the MapCommandsList type that contains all the information we need to build
     the map.
    :param field_indexes: an object that contains every dimension's index. The indexes are obtained from the field
     object in the netCDF, and not from the netCDF dimension objects's indexes
    :return: the arranged field

    about: this function arranges the data fields to be in order: time, depth, lat, lon, and creating a 1 sized time or
    depth dimension if needed
    """

    field = np.array(field)

    # splitting into cases depends on time or depth dependence. Adding to the  field a dummy dimension if needed to
    # make them easier to use, and arranging the field with transpose from numpy.
    if commands_list.is_depends_on_time and commands_list.is_depends_on_depth:
        field = field.transpose(field_indexes.time, field_indexes.depth, field_indexes.lat,
                                field_indexes.lon)
    elif commands_list.is_depends_on_time and not commands_list.is_depends_on_depth:
        field = [field]
        field = np.array(field)
        field = field.transpose(int(field_indexes.time) + 1, 0, int(field_indexes.lat) + 1, int(field_indexes.lon) + 1)
    elif not commands_list.is_depends_on_time and commands_list.is_depends_on_depth:
        field = [field]
        field = np.array(field)
        field = field.transpose(0, int(field_indexes.depth) + 1, int(field_indexes.lat) + 1, int(field_indexes.lon) + 1)
    else:
        field = [[field]]
        field = np.array(field)
        field = field.transpose(0, 1, int(field_indexes.lat) + 2, int(field_indexes.lon) + 2)

    return field


def make_map_base(netcdf_file, commands_list: MapCommandsList):
    """
    :param netcdf_file: the netCDF file
    :param commands_list: an object from the MapCommandsList type that contains all the information we need to build
     the map.
    :return: and the x and y axis for the map

    about: this function makes the base of a map. It sets the size and edges, and creates coastlines
    """

    # getting the latitude and longitude vectors from the netCDF file
    lon = nfh.get_values(netcdf_file, commands_list.info_list[commands_list.lon])
    lat = nfh.get_values(netcdf_file, commands_list.info_list[commands_list.lat])

    # setting the temporary defaults to those values. they are already in the command list, just needs to get a value
    lat_0 = lat.mean()
    lon_0 = lon.mean()
    lon_min = lon.min()
    lon_max = lon.max()
    lat_min = lat.min()
    lat_max = lat.max()

    # creating the base of the map
    xx, yy = np.meshgrid(lon, lat)
    m = Basemap(width=2000, height=2000, resolution=commands_list.resolution, projection=commands_list.projection,
                lon_0=lon_0, lat_0=lat_0,
                llcrnrlon=lon_min, urcrnrlon=lon_max, llcrnrlat=lat_min, urcrnrlat=lat_max)
    xx, yy = m(xx, yy)
    m.drawcoastlines()

    return xx, yy
