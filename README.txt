This folder contains the completed work for Assignment 3

This assignment was completed in Python, and therefore can be executed by typing -> python RayTracer.py "testcase.txt" when checking for marking. It also uses the numpy library to store vectors and matrices, and the sys library to take the .txt file argument from the command line. No further libraries are used.

Ray tracer:

For this Ray tracer, values for the variables of the scene are first parsed with the parse_info function. Each line of the .txt file is iterated through, and lines that are blank are skipped. After splitting the values of each line, the the values are placed into variables and classes depending on the first string of the line. The classes Sphere and Light are used to stores the values of the objects, and the objects are then stored in lists. The dimensions of the image plane are stored as global variables, and other variables such as the background color and ambient lighting are stored as np.array variables.

The main function iterates pixel by pixel through the image, writing each pixel color to a ppm file, this iterating process goes from the bottom left pixel to the top right. After calculating the location of each pixel, the camera origin and the pixel direction are stored in a Ray object which will be used for the raytracing process.

To find the t value to get P, the function find_closest_intersection is used. This function iterates through every object in the scene to find whether there is an intersection, and which object is the closest. This function uses the helper function getDistance to find the distance to the intersection point in order to find the closest one. In order to get the scaled positions of the spheres, the inverse of the scaling matrix is applied to the values S and c. getDistance also checks if one of the two intersections point is behind the near plane. The closest intersection point will be returned unless there is a point behind the near plane, in this case the farther of the two points (inside of the sphere) is returned.

The variable t_inside is used to denote whether a point is inside of the sphere or not with the values 1 - yes and 0 - no.

The current value of t is then put into the equation S + tc to get our intersection point, which is used to get the normal of the sphere. To then shift the normal from local to world coordinates, it is multiplied by the inverse transpose of the scaling matrix. The point P is then shifted by 0.00001 to avoid any self intersection. In the case that the farther intersection point was taken, the normal is then flipped (because this point would be on the inside of the sphere).

clocal is found using the color_from_lights function. This function iterates through all the lights in the scene and adds the diffuse and specular values as needed. The ambient lighting will always be added. This function uses find_closest_intersection to check for the closest object the light ray comes in contact with. If the object happens to be in front of the point P, the point is assumed to be in shadow and diffuse and specular are not added. In the case that P is a point inside of the sphere, lights behind the near plane will be assumed to be in shadow since the point is inside of the sphere.

Once clocal has been found, the raytrace function recurses using the reflected ray found using -2 * (N * L)N + L since our ray L faces towards away from the point it is reflecting from (this is different from color_from_lights where the ray was pointing towards the point). The final color of the pixel adds clocal with the reflected color multiplied by the reflected coefficient of the object P is on. In the case that a ray every hits nothing, it will return the background color. If the ray reaches a depth greater than 3, it will return the color black.

A few helper functions were created to help with normalizing vectors, multiplying vectors by the inverse of a scaling matrix, and multiplying vectors by the inverse transpose of a scaling matrix.

Again, sys and numpy are the two libraries used for this assignments, and since it is written in Python, -> python RayTracer.py "testcase.txt" will allow it to be run.


