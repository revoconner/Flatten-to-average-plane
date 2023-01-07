import pymel.core as pm
import numpy as np
import math

#testing purposes
print("\n\n########### RESULTS HERE ############\n\n")

# Get the current selection
sel = pm.ls(selection=True)
vertex = pm.polyListComponentConversion(sel, tv=True)
polys = pm.polyListComponentConversion(sel, tf=True)
selection = pm.filterExpand(vertex, ex=True, sm=31)
face_selection = pm.filterExpand(polys, ex=True, sm=34)


# Filter the selection to only include vertices and faces
vertices = [v for v in selection]
faces = [f for f in face_selection]
# Get the coordinates of the vertices
coords = []

for v in vertices:
    coord = pm.xform(v, query=True, worldSpace=True, translation=True)
    coords.append(coord)

    
#putting the points in Numpy array
points = np.array(coords)
#Getting the centroid
centroid = np.mean(points, axis=0)
print("The centroid is: "+str(centroid))
# Calculate the distance of the centroid from the origin
distance = math.sqrt((centroid[0] - 0)**2 + (centroid[1] - 0)**2 + (centroid[2] - 0)**2)
print("The distance is: "+str(distance)) 


normals = []
for f in faces:
    normal = pm.polyInfo(f, fn=1)
    #print(normal)
    normals.append(normal)
    
#removing dt.normals from the normals and converting to numpy array
vector_data = [(float(x), float(y), float(z)) for sublist in normals for normals in sublist for x, y, z in [normals[normals.index(':')+2:].split()]]
vector_data = np.array(vector_data)
mean_vector = np.mean(vector_data, axis=0)

print("The mean of the normals is: "+str(mean_vector))


########## GETTING THE BEST FIT PLANE ############

# Vector of the initial plane
plane_vector = [0, 1, 0]

# Target vector
target_vector = mean_vector

# Normalize the vectors
plane_vector = [x / math.sqrt(sum(x**2 for x in plane_vector)) for x in plane_vector]
target_vector = [x / math.sqrt(sum(x**2 for x in target_vector)) for x in target_vector]

# Calculate the rotation angle around the X  Y Z
angle_x = math.atan2(target_vector[1], target_vector[2])
rotated_vector = [plane_vector[0], plane_vector[1] * math.cos(angle_x) - plane_vector[2] * math.sin(angle_x), plane_vector[1] * math.sin(angle_x) + plane_vector[2] * math.cos(angle_x)]
angle_y = math.atan2(-rotated_vector[0], rotated_vector[2])
rotated_vector = [rotated_vector[0] * math.cos(angle_y) + rotated_vector[2] * math.sin(angle_y), rotated_vector[1],-rotated_vector[0] * math.sin(angle_y) + rotated_vector[2] * math.cos(angle_y)]
angle_z = math.atan2(rotated_vector[1], rotated_vector[0])

# Convert the angles to degrees
angle_x = angle_x * 180 / math.pi
angle_y = angle_y * 180 / math.pi
angle_z = angle_z * 180 / math.pi

print('Rotation of Abstract plane is: '+f'X: {angle_x:.2f},  '+ f'Y: {angle_y:.2f},  '+ f'Z: {angle_z:.2f},  '+ 'degrees')

############ MOVING THE POINTS ##################

centroid = np.array(centroid)
normal = np.array(mean_vector)
translated_points = points - centroid

# Project the points onto the plane
projected_points = translated_points - np.dot(translated_points, normal[:, None]) * normal / np.dot(normal, normal)

# Move the points back to their original position relative to the plane
moved_points = projected_points + centroid

#converting to tuple from NP array
moved_verts =tuple([moved_points[i].tolist() for i in range(len(moved_points))])

#moving the vertices
count=0
while count <  len(vertices):
    pm.xform(vertices[count], worldSpace=True, translation=(moved_verts[count][0], moved_verts[count][1], moved_verts[count][2]))
    count = count+1