# Flatten faces to average plane
Flatten selected faces to the best fit plane in Maya
![image](https://user-images.githubusercontent.com/88772846/211122741-a2dcbdc9-7e15-4dbe-acdb-9cb8f6873c43.png)
![image](https://user-images.githubusercontent.com/88772846/211122764-12fa2b55-f50e-4419-b16e-1ee4c36abb42.png)

# Why?
Well you can always use the scale tool to flatten the faces and works great. This was a fun maths exercise for me.

## How to use:
1. Run the preriquisite.bat file as admin for the **first time**, this will install numpy to Maya if its not already installed.
2. Then you can run the py script from the editor or save it to shelf.

## How this works?
1. First we get an expanded list of vertices and faces from the selection
2. Then we find the centroid of all the points, this will also act as the centroid of the best fit plane
3. Then we get the normal vector of all faces in selection and find the mean of it. This will be the mean of the plane as well.
4. (optional calculation) this finds the rotation and translation of the plane if you were to create one using polyPlane so that it represents the abtract best fit plane
5. Then we move the abstract plane to the origin, project the points to that and move it back relative to the plane thus moving it to the best fit planar.

## Note:
Needs numpy, either run the bat file if your maya installation is located in the default location else, go to maya\bin and run mayapy -m pip install numpy
