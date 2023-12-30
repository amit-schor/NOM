## maps
- map resolutions - ask the user for input and you can put it under MapCommandsList.resolution in InputManager. It defaults to 'c'.
- add colormap
- add color to landmasses - optional
- make spaces between quivers on vector maps - ask the user for input and you can put it under MapCommandsList.quiver_space in InputManager. It defaults to 15.
- fill the rest of the unused preferences of the CommandsList, MapCommandList, GraphCommandList

## graphs
- add graph making (Under ognom.py)
- add graph questions
- some of the axis the user will choose will have more than one dimension. for example wind speed that depends on time, latitude and longitude. the program will have to figure out the two axis the user wants and how to extract them. 
you can take a look at arrange_fields() function under omnom.py that do it for maps. 

## both maps and graphs
- add names and titles to axes
- do dimensions for graph with different dimensions's matrixses
