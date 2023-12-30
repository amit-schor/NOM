# NOM
##### `made by amit schor 2021`
     
## Introduction
Welcome to NOM. This program helps you create and save a map or a graph from a netCDF file. While using 
the program you will be questioned about your graph\map preferences and dimensions, and your answers 
would be saved for further use.  

For better understanding of your netCDF file's structure, its recommended to use the netCDF_file_handler's
functions on it before proceeding to use this program.

If you are here to edit or add to the program itself, please read all the documentations and requirements first.

## Incompleteness
the map drawing part of this project is complete. 
regarding the plotting of profile and accumilating graphs this part of the project is called ognom and is not complete.

## Requirements  
python 3.6 or later  
netCDF4 Version 1.5.7 or later  
prompt toolkit 3.0.20 or later  
Basemap from mpl_toolkits.basemap  
matplotlib.pyplot

## Documentation
To run the program on terminal, use:
```
python location\in\computer\NOM\main.py
```

### input script file
An input script file is a text file that every line in it contains a number 
or text in accordance to the questions asked by the program. It's purpose is to enable running
the program without manually answering every question in the netCDF file.  


To run it on an input script file, use the '-i' flag.
```
python location\in\computer\NOM\main.py -i < input.txt
```
If '-i' flag is not used, the program will wait for input and
 will not run on the script file.  

#### suggested uses for input script file
* running the program on a multiple netCDF files, 
by using a batch script on the input script file to edit the line contains the path to the netCDF.  
* running it multiple times on the same netCDF file, changing the time or depth for every run, 
or changing little details  in the map properties.

#### creation of script input file
You can easily create an input file by running the program manually in the Terminal or in PyCharm Console.
You will be asked if you want to create a script file with your answers, and by answering 'YES', 
you will get to choose its location and name, and it will be created at the end of the run.
  
In this method, the input file created by the program will contain text identical to your 
answers, except for the answer to the creating input file question. The input to this question will be automatically set to 'NO', 
so to not create identical input files every time the program run automatically on a script. It can be changed manually through 
editing the text in script itself.

## Image export types
- pdf - pdf file
- png, jpg, jpeg - image file
- pickle* - python object file containing a matplotlib.figure object
- eps, ps, svg - vector graphics file

*pickle, in order to open pickle file, load the figure from the file, and run it's show() field-function. as shown in the following example piece of code:
```python
import pickle
file_name = <ENTER FILE NAME HERE>
with open(file_name,'rb') as f:
    fig_object = pickle.load(f)
fig_object.show()
```

## Utility functions
netCDF_file_handler.show_info - a very usfull function that details all or some of the details for each or part of the variables, in a given netcdf file. see function description for more info.
