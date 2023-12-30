import matplotlib.pyplot as plt
import omnom
import ognom
from InputManager import MapCommandsList, GraphCommandsList, CommandsList
import InputManager
import netCDF_file_handler as nfh
import sys
import OutputManager

# searching what parameters the program got.
if '-i' in sys.argv:
    InputManager.is_reading_from_file = True


def main():
    # creating a CommandsList object to store answers and values that can be obtained from them
    script = []
    commands_list = CommandsList()
    # asking whether to print a script file with the raw answers
    commands_list = InputManager.get_if_script_file(script, commands_list)
    # getting the name and location of the netCDF file
    commands_list = InputManager.get_name_and_location(script, commands_list)
    # opening the netCDF file
    netcdf_file = nfh.open_netcdf(commands_list.netcdf_path)
    # inserting to the commands_list object a list of all the names of the netCDF files variables
    InputManager.update_info_list_in_command_list(netcdf_file, commands_list)
    # asking for the plot type
    commands_list = InputManager.get_plot_type(script, commands_list)

    # opening the figure we want to create
    plt_figure = plt.figure()

    # splitting the cases for different types of plots
    if commands_list.plot_type == 0:
        # Converting the commands_list object from CommandsList type to MapCommandsList type
        commands_list = MapCommandsList(commands_list)
        # asking the user about the map's properties
        InputManager.get_map_choose_parameters(netcdf_file, script, commands_list)
        # making the map
        omnom.make_map(netcdf_file, commands_list)
    else:
        # Converting the commands_list object from CommandsList type to GraphCommandsList type
        commands_list = GraphCommandsList(commands_list)
        # asking the user about the graph's properties
        InputManager.get_graph_choose_parameters(netcdf_file, script, commands_list)
        # making the graph
        ognom.make_graph_2d(netcdf_file, commands_list)
    print("\n")
    # getting from the user the output's full name
    commands_list = InputManager.get_plot_name_location_and_format(script, commands_list)
    # printing the script file if asked
    OutputManager.print_script_to_file(script, commands_list)
    # saving the fig
    OutputManager.print_fig(plt_figure, commands_list)
    # closing the netCDF file
    netcdf_file.close()
    print("\nEND")
    plt.show()


if __name__ == "__main__":
    main()
