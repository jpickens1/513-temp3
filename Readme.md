CS513 Assignment 3 Readme 

Team members:  Jiaxing Wu(A20398273) /  Jingwen Pickens(A20349887) / Sumukh Ballal(A20442681) / Hyesoo Noh(A20360464)

Please install the following libraries prior to the main program
```
pip install numpy
```


To run the main program, type the following command in the command line:
```
python aerial_imagery_retrieval.py
```
then follow the prompt to enter the coordinates.  This program take two pairs of lat/lon as input.  The first lat/lon pair should be the coordinates for the top left corner of the bounding box.  The second lat/lon pair should be the coordinates for the bottom right corner of the bounding box.  


Some sample coordinates used for testing the program which successfully returned a aerial image are as follows:
1. IIT Main Campus: 41.837909 -87.629252  41.833163 -87.623726   
2. Grant Park: 41.878181 -87.623866  41.869907 -87.617474
3. Navy Pier: 41.892591 -87.609226 41.889484 -87.599752
4. Planetarium: 41.867154 -87.607633  41.865820 -87.605703
